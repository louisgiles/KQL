#!/usr/bin/env python3
"""Lint runtime-sensitive literal arguments in active KQL sources."""

from __future__ import annotations

from pathlib import Path
import sys


ACTIVE_ROOTS = ("investigation", "threat-work")
FORMAT_FUNCTION = "format_datetime"
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


def find_call_arguments(text: str, open_parenthesis: int) -> tuple[list[tuple[int, int]], int]:
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
            after_ok = after_index == len(text) or not is_identifier_character(text[after_index])
            if before_ok and after_ok:
                cursor = after_index
                while cursor < len(text) and text[cursor].isspace():
                    cursor += 1
                if cursor < len(text) and text[cursor] == "(":
                    arguments, end = find_call_arguments(text, cursor)
                    if len(arguments) >= 2:
                        start, stop = arguments[1]
                        while start < stop and text[start].isspace():
                            start += 1
                        while stop > start and text[stop - 1].isspace():
                            stop -= 1
                        literal = text[start:stop]
                        if len(literal) >= 2 and literal[0] in ("'", '"') and literal[-1] == literal[0]:
                            yield start, literal[1:-1]
                    index = end
                    continue
        index += 1


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


def main() -> int:
    run_self_test()
    repo_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    files = sorted(
        file
        for root_name in ACTIVE_ROOTS
        for file in (repo_root / root_name).rglob("*.kql")
        if (repo_root / root_name).is_dir()
    )

    if not files:
        print(f"No active .kql files found under {repo_root}", file=sys.stderr)
        return 2

    failures = 0
    for file in files:
        text = file.read_text(encoding="utf-8")
        for offset, format_string in iter_literal_formats(text):
            error = validate_datetime_format(format_string)
            if error is None:
                continue
            line, column = line_and_column(text, offset)
            relative = file.relative_to(repo_root).as_posix()
            print(
                f"KQLFMT001 {relative}:{line}:{column}: {error} in "
                f"format_datetime argument #2: {format_string!r}",
                file=sys.stderr,
            )
            failures += 1

    if failures:
        print(f"Runtime-literal lint failed with {failures} error(s).", file=sys.stderr)
        return 1

    print(f"Runtime-literal lint passed for {len(files)} active KQL file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
