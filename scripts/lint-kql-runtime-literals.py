#!/usr/bin/env python3
"""Lint changed KQL for runtime-sensitive literals and surface hazards."""

from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
import subprocess
import sys


ACTIVE_ROOTS = ("investigation", "threat-work")
FORMAT_FUNCTION = "format_datetime"
REQUIRED_HEADERS = (
    "name",
    "purpose",
    "starting_entities",
    "required_tables",
    "optional_tables",
    "variables",
    "time_window",
    "done_criteria",
    "artifact_type",
    "output_type",
    "execution_surface",
)
ALLOWED_SURFACES = {
    "sentinel-log-analytics",
    "defender-advanced-hunting",
    "azure-data-explorer",
}
SUPPORTED_DELIMITERS = set(" /-:,. _[]")
SUPPORTED_RUNS = {
    "d": {1, 2},
    "f": set(range(1, 8)),
    "F": set(range(1, 8)),
    "h": {1, 2},
    "H": {1, 2},
    "m": {1, 2},
    "M": {1, 2},
    "s": {1, 2},
    "y": {1, 2, 4},
    "t": {2},
}


def is_identifier_character(char: str) -> bool:
    return char.isalnum() or char == "_"


def is_active_kql(path: str) -> bool:
    return path.endswith(".kql") and any(
        path.startswith(f"{root}/") for root in ACTIVE_ROOTS
    )


def normalize_repo_path(value: str) -> str:
    path = PurePosixPath(value.replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe repository path {value!r}")
    return path.as_posix()


def skip_string(text: str, start: int) -> int:
    quote = text[start]
    index = start + 1
    while index < len(text):
        if text[index] == "\\":
            index += 2
            continue
        if text[index] == quote:
            if index + 1 < len(text) and text[index + 1] == quote:
                index += 2
                continue
            return index + 1
        index += 1
    return len(text)


def skip_space(text: str, start: int) -> int:
    index = start
    while index < len(text) and text[index].isspace():
        index += 1
    return index


def find_call_arguments(
    text: str, open_parenthesis: int
) -> tuple[list[tuple[int, int]], int]:
    matching = {")": "(", "]": "[", "}": "{"}
    stack = ["("]
    argument_start = open_parenthesis + 1
    arguments: list[tuple[int, int]] = []
    index = argument_start

    while index < len(text):
        if text.startswith("//", index):
            newline = text.find("\n", index + 2)
            index = len(text) if newline == -1 else newline + 1
            continue
        if text.startswith("/*", index):
            close = text.find("*/", index + 2)
            index = len(text) if close == -1 else close + 2
            continue

        char = text[index]
        if char in ("'", '"'):
            index = skip_string(text, index)
            continue
        if char in "([{":
            stack.append(char)
            index += 1
            continue
        if char in matching:
            if not stack or stack[-1] != matching[char]:
                return [], index + 1
            stack.pop()
            if not stack:
                arguments.append((argument_start, index))
                return arguments, index + 1
            index += 1
            continue
        if char == "," and len(stack) == 1:
            arguments.append((argument_start, index))
            argument_start = index + 1
        index += 1

    return [], len(text)


def iter_literal_formats(text: str):
    lowered = text.lower()
    index = 0

    while index < len(text):
        if text.startswith("//", index):
            newline = text.find("\n", index + 2)
            index = len(text) if newline == -1 else newline + 1
            continue
        if text.startswith("/*", index):
            close = text.find("*/", index + 2)
            index = len(text) if close == -1 else close + 2
            continue
        if text[index] in ("'", '"'):
            index = skip_string(text, index)
            continue

        if lowered.startswith(FORMAT_FUNCTION, index):
            before_ok = index == 0 or not is_identifier_character(text[index - 1])
            after_index = index + len(FORMAT_FUNCTION)
            after_ok = after_index == len(text) or not is_identifier_character(
                text[after_index]
            )
            if before_ok and after_ok:
                cursor = skip_space(text, after_index)
                if cursor < len(text) and text[cursor] == "(":
                    arguments, end = find_call_arguments(text, cursor)
                    if len(arguments) >= 2:
                        start, stop = arguments[1]
                        while start < stop and text[start].isspace():
                            start += 1
                        while stop > start and text[stop - 1].isspace():
                            stop -= 1
                        literal = text[start:stop]
                        if (
                            len(literal) >= 2
                            and literal[0] in ("'", '"')
                            and literal[-1] == literal[0]
                        ):
                            yield start, literal[1:-1]
                    index = end
                    continue
        index += 1


def iter_code_identifiers(text: str):
    index = 0
    while index < len(text):
        if text.startswith("//", index):
            newline = text.find("\n", index + 2)
            index = len(text) if newline == -1 else newline + 1
            continue
        if text.startswith("/*", index):
            close = text.find("*/", index + 2)
            index = len(text) if close == -1 else close + 2
            continue
        if text[index] in ("'", '"'):
            index = skip_string(text, index)
            continue
        if text[index].isalpha() or text[index] == "_":
            start = index
            index += 1
            while index < len(text) and is_identifier_character(text[index]):
                index += 1
            yield start, index, text[start:index]
            continue
        index += 1


def iter_multikey_top(text: str):
    matching = {")": "(", "]": "[", "}": "{"}
    for start, stop, identifier in iter_code_identifiers(text):
        if identifier.lower() != "top":
            continue

        cursor = skip_space(text, stop)
        number_start = cursor
        while cursor < len(text) and text[cursor].isdigit():
            cursor += 1
        if cursor == number_start:
            continue

        cursor = skip_space(text, cursor)
        if text[cursor : cursor + 2].lower() != "by":
            continue
        after_by = cursor + 2
        if after_by < len(text) and is_identifier_character(text[after_by]):
            continue

        cursor = after_by
        stack: list[str] = []
        while cursor < len(text):
            if text.startswith("//", cursor):
                newline = text.find("\n", cursor + 2)
                cursor = len(text) if newline == -1 else newline + 1
                continue
            if text.startswith("/*", cursor):
                close = text.find("*/", cursor + 2)
                cursor = len(text) if close == -1 else close + 2
                continue
            if text[cursor] in ("'", '"'):
                cursor = skip_string(text, cursor)
                continue

            char = text[cursor]
            if char in "([{":
                stack.append(char)
            elif char in matching:
                if stack and stack[-1] == matching[char]:
                    stack.pop()
            elif not stack and char in "|;":
                break
            elif not stack and char == ",":
                yield start
                break
            cursor += 1


def clause_end(text: str, start: int) -> int:
    matching = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    cursor = start
    while cursor < len(text):
        if text.startswith("//", cursor):
            newline = text.find("\n", cursor + 2)
            cursor = len(text) if newline == -1 else newline + 1
            continue
        if text.startswith("/*", cursor):
            close = text.find("*/", cursor + 2)
            cursor = len(text) if close == -1 else close + 2
            continue
        if text[cursor] in ("'", '"'):
            cursor = skip_string(text, cursor)
            continue

        char = text[cursor]
        if char in "([{":
            stack.append(char)
        elif char in matching:
            if stack and stack[-1] == matching[char]:
                stack.pop()
        elif not stack and char in "|;":
            return cursor
        cursor += 1
    return len(text)


def top_level_segments(text: str, start: int, end: int) -> list[tuple[int, int]]:
    matching = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    segments: list[tuple[int, int]] = []
    segment_start = start
    cursor = start
    while cursor < end:
        if text.startswith("//", cursor):
            newline = text.find("\n", cursor + 2, end)
            cursor = end if newline == -1 else newline + 1
            continue
        if text.startswith("/*", cursor):
            close = text.find("*/", cursor + 2, end)
            cursor = end if close == -1 else close + 2
            continue
        if text[cursor] in ("'", '"'):
            cursor = min(skip_string(text, cursor), end)
            continue

        char = text[cursor]
        if char in "([{":
            stack.append(char)
        elif char in matching:
            if stack and stack[-1] == matching[char]:
                stack.pop()
        elif not stack and char == ",":
            segments.append((segment_start, cursor))
            segment_start = cursor + 1
        cursor += 1
    segments.append((segment_start, end))
    return segments


def top_level_equals(text: str, start: int, end: int) -> int | None:
    matching = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    cursor = start
    while cursor < end:
        if text.startswith("//", cursor):
            newline = text.find("\n", cursor + 2, end)
            cursor = end if newline == -1 else newline + 1
            continue
        if text.startswith("/*", cursor):
            close = text.find("*/", cursor + 2, end)
            cursor = end if close == -1 else close + 2
            continue
        if text[cursor] in ("'", '"'):
            cursor = min(skip_string(text, cursor), end)
            continue

        char = text[cursor]
        if char in "([{":
            stack.append(char)
        elif char in matching:
            if stack and stack[-1] == matching[char]:
                stack.pop()
        elif not stack and char == "=":
            return cursor
        cursor += 1
    return None


def iter_extend_alias_dependencies(text: str):
    for start, stop, identifier in iter_code_identifiers(text):
        if identifier.lower() != "extend":
            continue
        previous = start - 1
        while previous >= 0 and text[previous].isspace():
            previous -= 1
        if previous < 0 or text[previous] != "|":
            continue

        end = clause_end(text, stop)
        earlier_aliases: set[str] = set()
        for segment_start, segment_end in top_level_segments(text, stop, end):
            equals = top_level_equals(text, segment_start, segment_end)
            if equals is None:
                continue
            left_identifiers = list(
                iter_code_identifiers(text[segment_start:equals])
            )
            if len(left_identifiers) != 1:
                continue
            alias = left_identifiers[0][2]
            for ref_start, _, reference in iter_code_identifiers(
                text[equals + 1 : segment_end]
            ):
                if reference in earlier_aliases:
                    yield equals + 1 + ref_start, reference
            earlier_aliases.add(alias)


def validate_datetime_format(format_string: str) -> str | None:
    if not format_string:
        return "format string is empty"

    index = 0
    while index < len(format_string):
        char = format_string[index]
        if char in SUPPORTED_DELIMITERS:
            index += 1
            continue
        if char not in SUPPORTED_RUNS:
            return f"unsupported token or delimiter {char!r}"

        end = index + 1
        while end < len(format_string) and format_string[end] == char:
            end += 1
        run_length = end - index
        if run_length not in SUPPORTED_RUNS[char]:
            return f"unsupported token run {char * run_length!r}"
        index = end

    return None


def line_and_column(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    last_newline = text.rfind("\n", 0, offset)
    column = offset + 1 if last_newline == -1 else offset - last_newline
    return line, column


def header_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines()[:80]:
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.startswith("//"):
            break
        content = stripped[2:].strip()
        if ":" not in content:
            continue
        key, value = content.split(":", 1)
        normalized = key.strip().lower()
        if normalized in REQUIRED_HEADERS:
            fields[normalized] = value.strip()
    return fields


def has_int_annotation(text: str, identifier_end: int) -> bool:
    cursor = skip_space(text, identifier_end)
    if cursor >= len(text) or text[cursor] != ":":
        return False
    cursor = skip_space(text, cursor + 1)
    end = cursor
    while end < len(text) and is_identifier_character(text[end]):
        end += 1
    return text[cursor:end].lower() == "int"


def all_active_files(repo_root: Path) -> list[Path]:
    return sorted(
        path
        for root_name in ACTIVE_ROOTS
        for path in (repo_root / root_name).rglob("*.kql")
        if (repo_root / root_name).is_dir()
    )


def changed_active_files(repo_root: Path, base: str) -> list[Path]:
    command = [
        "git",
        "-C",
        str(repo_root),
        "diff",
        "--name-only",
        "--diff-filter=ACMR",
        f"{base}...HEAD",
        "--",
        *ACTIVE_ROOTS,
    ]
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git diff failed")

    files: list[Path] = []
    for value in result.stdout.splitlines():
        path = normalize_repo_path(value.strip())
        if not is_active_kql(path):
            continue
        absolute = repo_root / path
        if absolute.is_file():
            files.append(absolute)
    return sorted(set(files))


def run_self_test() -> None:
    invalid = (
        "yyyy-MM-ddTHH:mm:ss.fffZ",
        "yyyy-MM-dd'T'HH:mm:ss'Z'",
        "yyyy-MM-dd HH:mm:ss.ffffffff",
    )
    valid = (
        "yyyy-MM-dd HH:mm:ss.fff",
        "yyyy-MM-dd HH:mm:ss.fffffff",
        "yyyy-MM-dd",
        "HH:mm:ss.fff",
    )
    assert all(validate_datetime_format(value) is not None for value in invalid)
    assert all(validate_datetime_format(value) is None for value in valid)

    identifiers = list(
        iter_code_identifiers(
            '// Timestamp\nprint A = "Timestamp", B = Timestamp, SortOrder:int\n'
        )
    )
    assert [value for _, _, value in identifiers].count("Timestamp") == 1
    assert any(value == "SortOrder" for _, _, value in identifiers)

    assert list(iter_multikey_top("T | top 1 by Rank desc, Time asc | take 1"))
    assert not list(iter_multikey_top("T | top 1 by iff(A, B, C) desc | take 1"))
    assert any(
        value.lower() == "dcountif"
        for _, _, value in iter_code_identifiers(
            "T | summarize Matches = dcountif(Key, Predicate)"
        )
    )
    assert has_int_annotation("print SortOrder : INT = 1", 15)
    assert header_fields("// name: test\n// purpose: value\nprint x = 1")["name"] == "test"
    dependencies = list(
        iter_extend_alias_dependencies(
            "T | extend A = tostring(X), B = strcat(A, 'x'), C = strcat(B, 'y') "
            "| project C"
        )
    )
    assert [name for _, name in dependencies] == ["A", "B"]
    assert not list(
        iter_extend_alias_dependencies(
            "T | extend A = tostring(X) | extend B = strcat(A, 'x')"
        )
    )


def main() -> int:
    run_self_test()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repo_root", nargs="?", default=Path(__file__).resolve().parents[1]
    )
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument(
        "--all", action="store_true", help="Lint every active KQL file"
    )
    selection.add_argument(
        "--base", help="Lint active KQL changed since this git base"
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    try:
        files = (
            changed_active_files(repo_root, args.base)
            if args.base
            else all_active_files(repo_root)
        )
    except (RuntimeError, ValueError) as error:
        print(f"KQLSTATIC001 cannot resolve lint scope: {error}", file=sys.stderr)
        return 2

    failures = 0
    for file in files:
        text = file.read_text(encoding="utf-8")
        relative = file.relative_to(repo_root).as_posix()
        headers = header_fields(text)

        for field in REQUIRED_HEADERS:
            if not headers.get(field):
                print(
                    f"KQLHDR001 {relative}: missing nonempty // {field}: header",
                    file=sys.stderr,
                )
                failures += 1

        surface = headers.get("execution_surface", "").lower()
        effective_surface = (
            "sentinel-log-analytics"
            if relative.startswith("investigation/")
            else surface
        )
        if surface and surface not in ALLOWED_SURFACES:
            print(
                f"KQLHDR002 {relative}: unsupported execution_surface {surface!r}",
                file=sys.stderr,
            )
            failures += 1
        if relative.startswith("investigation/") and surface != "sentinel-log-analytics":
            print(
                f"KQLHDR003 {relative}: investigation KQL must declare "
                "execution_surface: sentinel-log-analytics",
                file=sys.stderr,
            )
            failures += 1

        for offset, format_string in iter_literal_formats(text):
            error = validate_datetime_format(format_string)
            if error is None:
                continue
            line, column = line_and_column(text, offset)
            print(
                f"KQLFMT001 {relative}:{line}:{column}: {error} in "
                f"format_datetime argument #2: {format_string!r}",
                file=sys.stderr,
            )
            failures += 1

        for offset in iter_multikey_top(text):
            line, column = line_and_column(text, offset)
            print(
                f"KQLTOP001 {relative}:{line}:{column}: top accepts one ordering "
                "expression; use order by with all keys, then take",
                file=sys.stderr,
            )
            failures += 1

        for offset, alias in iter_extend_alias_dependencies(text):
            line, column = line_and_column(text, offset)
            print(
                f"KQLALIAS001 {relative}:{line}:{column}: {alias} is created "
                "earlier in the same extend and is not available to sibling "
                "expressions; split the dependent calculation into another extend",
                file=sys.stderr,
            )
            failures += 1

        for start, stop, identifier in iter_code_identifiers(text):
            if relative.startswith("investigation/"):
                if identifier.lower() == "dcountif":
                    line, column = line_and_column(text, start)
                    print(
                        f"KQLAGG001 {relative}:{line}:{column}: dcountif can fail "
                        "when all or no rows satisfy the predicate; deduplicate the "
                        "key first, then use countif",
                        file=sys.stderr,
                    )
                    failures += 1
                if identifier == "SortOrder":
                    if has_int_annotation(text, stop):
                        line, column = line_and_column(text, start)
                        print(
                            f"KQLTYPE001 {relative}:{line}:{column}: declare SortOrder:long "
                            "so union output keeps one sortable column",
                            file=sys.stderr,
                        )
                        failures += 1
            if identifier == "Timestamp" and effective_surface == "sentinel-log-analytics":
                line, column = line_and_column(text, start)
                print(
                    f"KQLSURF001 {relative}:{line}:{column}: Sentinel Log Analytics "
                    "KQL must use TimeGenerated, not Defender Advanced Hunting "
                    "Timestamp",
                    file=sys.stderr,
                )
                failures += 1

    if failures:
        print(f"KQL static runtime gate failed with {failures} error(s).", file=sys.stderr)
        return 1

    print(f"KQL static runtime gate passed for {len(files)} active KQL file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
