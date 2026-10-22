#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Check every `Default Params` cell against STANDARDS.md §4.3.

§4.3 was written to govern the example tree's eight `Default Params` cells. A rule that
governs eight cells should be executed against those eight cells — this is that pass, so
it can be re-run by whoever next edits §4.3 rather than living on one machine.

Scope matches the rule: it reads the example tree under `skills/` and the §4.3 heading of
`STANDARDS.md`. It is **repo-internal tooling** for maintainers, like
`check_invariants.py` — a user's project has its own defaults to define.

This is the seed for #24 item 5. Whether it becomes a general invariant there is that
issue's decision; here it pins the rule against the tree that motivated it.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_GLOB = "skills/axb-gherkin-and-dsl/examples/**/dsl.md"

# A binding must say what establishes it. These are the phrasings §4.3's examples use;
# a cell naming none of them is a binding that points at nothing in particular.
ESTABLISHING_HINTS = (
    "established by",
    "created by",
    "preceding",
    "scenario text",
    "accumulated",
    "constant",
)


@dataclass
class Violation:
    path: Path
    section: str
    sentence: str
    entry: str
    problems: list[str]


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def iter_entries(root: Path):
    """Yield (path, section, sentence, gherkin_params, data_table, default) per DSL row."""
    for path in sorted(root.glob(EXAMPLE_GLOB)):
        section = None
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                section = line.split()[1]
                continue
            if not line.startswith("| `"):
                continue
            cells = split_row(line)
            if len(cells) < 5:
                continue
            yield path, section or "?", cells[0], cells[1], cells[2], cells[3]


def check_entry(sentence: str, params: str, data_table: str, default: str) -> list[str]:
    """§4.3's tests, applied to one cell."""
    if default.lower() in ("none", ""):
        return []

    problems: list[str] = []

    # "Write the value, not the word 'default'" — a constant is not a default.
    if re.search(r"\bdefault", default, re.IGNORECASE):
        problems.append("uses the word 'default'; state the value or the binding instead")

    # Names may be lower-case-and-hyphenated (`target-cart`) or title-cased with spaces
    # (`Product Code`), so the pattern must admit both.
    name_match = re.match(r"`([A-Za-z][A-Za-z -]*)`", default)
    name = name_match.group(1) if name_match else None

    # "The test is on the parameter, not the value." A name the sentence or table can
    # supply is a parameter, not a default.
    placeholders = set(re.findall(r"\{([^{}]+)\}", sentence))
    columns = set()
    if data_table.lower().startswith(("supported", "supported:")):
        columns = {c.lower() for c in re.findall(r"`([A-Za-z][A-Za-z ]*)`", data_table)}
    if name:
        if name in placeholders:
            problems.append(
                f"`{name}` is a Gherkin placeholder — it is a parameter, not a default"
            )
        if name.lower() in columns:
            problems.append(
                f"`{name}` is a DataTable column — it is a table parameter, not a default"
            )

    # A binding must say what establishes it.
    if not any(hint in default.lower() for hint in ESTABLISHING_HINTS):
        problems.append("names no establishing source")

    # The genuinely circular case: resolving from state this step itself produces.
    if "current cart owner" in default.lower():
        problems.append(
            "circular — resolves from state this step produces, not from state established earlier"
        )

    return problems


def run(root: Path) -> list[Violation]:
    violations: list[Violation] = []
    for path, section, sentence, params, data_table, default in iter_entries(root):
        problems = check_entry(sentence, params, data_table, default)
        if problems:
            violations.append(Violation(path, section, sentence, default, problems))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="repository root to check (default: this script's repository)",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    violations = run(root)
    checked = sum(
        1
        for _p, _s, _sent, _params, _dt, default in iter_entries(root)
        if default.lower() not in ("none", "")
    )

    print(f"Default Params conformance (STANDARDS.md §4.3): {root}")
    print(f"Entries checked: {checked}")

    if violations:
        print(f"\nViolations ({len(violations)}):")
        for v in violations:
            try:
                where = v.path.relative_to(root)
            except ValueError:
                where = v.path
            print(f"  {where}: {v.entry}")
            for problem in v.problems:
                print(f"    - {problem}")
        print(f"\nResult: FAILED ({len(violations)} cell(s))")
        return 1

    print("\nResult: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
