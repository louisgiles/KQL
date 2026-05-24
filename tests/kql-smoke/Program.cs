// KQL smoke-test harness.
//
// Parses every .kql file in the repo (excluding scratchpad/) and reports any
// syntax-level diagnostics emitted by Microsoft.Azure.Kusto.Language. Does NOT
// run semantic analysis — unknown tables / columns / unbound variables are
// expected because these queries are runtime-templated with analyst-supplied
// values, and there is no live schema available.

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Kusto.Language;
using Kusto.Language.Editor;

namespace KqlSmoke;

internal static class Program
{
    private static readonly string[] ExcludedDirSegments =
    {
        "/scratchpad/",
        "/bin/",
        "/obj/",
        "/.git/",
        "/node_modules/"
    };

    private static int Main(string[] args)
    {
        string repoRoot = args.Length > 0
            ? Path.GetFullPath(args[0])
            : FindRepoRoot();

        if (!Directory.Exists(repoRoot))
        {
            Console.Error.WriteLine($"Repo root does not exist: {repoRoot}");
            return 2;
        }

        var files = Directory
            .EnumerateFiles(repoRoot, "*.kql", SearchOption.AllDirectories)
            .Where(IsIncluded)
            .OrderBy(f => f, StringComparer.Ordinal)
            .ToList();

        if (files.Count == 0)
        {
            Console.Error.WriteLine($"No .kql files found under {repoRoot}");
            return 2;
        }

        Console.WriteLine($"KQL smoke test — root: {repoRoot}");
        Console.WriteLine($"Files: {files.Count} (scratchpad/ excluded)");
        Console.WriteLine(new string('-', 72));

        int passCount = 0;
        int failCount = 0;

        foreach (var file in files)
        {
            string relPath = Path.GetRelativePath(repoRoot, file).Replace('\\', '/');
            string text;
            try
            {
                text = File.ReadAllText(file);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"FAIL  {relPath}");
                Console.WriteLine($"      read error: {ex.Message}");
                failCount++;
                continue;
            }

            var errors = GetSyntaxErrors(text);
            if (errors.Count == 0)
            {
                Console.WriteLine($"PASS  {relPath}");
                passCount++;
            }
            else
            {
                Console.WriteLine($"FAIL  {relPath}");
                foreach (var d in errors)
                {
                    var (line, col) = LineColumnFromOffset(text, d.Start);
                    Console.WriteLine($"      line {line}, col {col}: {d.Message}");
                }
                failCount++;
            }
        }

        Console.WriteLine(new string('-', 72));
        Console.WriteLine($"Total: {files.Count}   Pass: {passCount}   Fail: {failCount}");
        return failCount == 0 ? 0 : 1;
    }

    // Parse syntax-only and return diagnostics that look like real parse errors.
    // We deliberately drop "unknown name / table / column / function" style
    // diagnostics because the analyst-templated `let`-blocks at the top of every
    // file and the absence of a live schema would generate noise that is not a
    // grammar issue.
    private static List<Diagnostic> GetSyntaxErrors(string text)
    {
        var code = KustoCode.Parse(text);
        var diags = code.GetSyntaxDiagnostics();

        return diags
            .Where(d => d.Severity == DiagnosticSeverity.Error)
            .Where(d => !IsSemanticNoise(d.Message))
            .ToList();
    }

    private static bool IsSemanticNoise(string message)
    {
        if (string.IsNullOrEmpty(message)) return false;
        string m = message.ToLowerInvariant();

        // Defensive filter: KustoCode.Parse should not emit semantic diagnostics,
        // but if a future library version starts to, drop the common shapes so
        // they cannot be misread as grammar failures.
        return m.Contains("could not be resolved")
            || m.Contains("not declared")
            || m.Contains("does not exist")
            || (m.Contains("unknown") && (m.Contains("name") || m.Contains("table") || m.Contains("column") || m.Contains("function")))
            || m.StartsWith("the name ")
            || m.Contains("not found in scope");
    }

    private static (int line, int col) LineColumnFromOffset(string text, int offset)
    {
        if (offset < 0) offset = 0;
        if (offset > text.Length) offset = text.Length;
        int line = 1, col = 1;
        for (int i = 0; i < offset; i++)
        {
            if (text[i] == '\n')
            {
                line++;
                col = 1;
            }
            else if (text[i] != '\r')
            {
                col++;
            }
        }
        return (line, col);
    }

    private static bool IsIncluded(string path)
    {
        string normalised = "/" + path.Replace('\\', '/').TrimStart('/');
        foreach (var seg in ExcludedDirSegments)
        {
            if (normalised.Contains(seg)) return false;
        }
        return true;
    }

    private static string FindRepoRoot()
    {
        // Walk up from the executable looking for repo-contract.md so the tool
        // can be run from anywhere inside the repo.
        var dir = new DirectoryInfo(AppContext.BaseDirectory);
        while (dir != null)
        {
            if (File.Exists(Path.Combine(dir.FullName, "repo-contract.md")))
                return dir.FullName;
            dir = dir.Parent;
        }
        return Directory.GetCurrentDirectory();
    }
}
