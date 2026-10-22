#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Check that every frame or page a `ui-plan` refers to is one that plan declares.

This is #24 item 3, the last surviving candidate from #12's deferred list:

> No reference to a frame or page the plan does not declare.

The defect text is quoted rather than paraphrased because #24's lesson is that a check
written from its own code passes tests written from the code too. The two historical
instances were found by review in #14, and both lived in the example tree this script
reads — which is why the real-tree test asserts the references it checked, not just the
violations it did not report.

**Scope: one direction.** A *reference* must resolve to a *declaration*. The reverse (a
declared page no screen section ever specifies) is a different question with a different
defect behind it, and mixing the two would let a failure name either end.

## What is read

- **Declarations**: the backticked paths on a plan's `Planned output files:` line.
- **References**: the two labelled screen lines (`Corresponding prototype file:` /
  `Corresponding frame file:`), the `Target Frame` column of a `Keybinding Map`, and the
  endpoints of every transition in a `State Transition List`.

A plan whose `Planned output files:` line still carries a `{{PLACEHOLDER}}` (i.e. a
template, not a filled plan) cannot be audited and is skipped — see "Exemptions" below.

## What is deliberately not read

- **Prototype link targets.** The defect would be a clickable target the plan does not
  declare, but this repository's example prototypes are named `prototype-*.example.html`
  while the plan declares `ui/*.html`, so no filename mapping exists to resolve a target
  *against*. A check would have to invent one, and an invented mapping fails open: it
  would report zero violations whether or not a target was declared. The half that can be
  decided from the tree — a plan contradicting its own declaration — is the half built
  here; the link-target half becomes buildable when a fixture exists whose prototype
  filenames are the declared ones.
- **Prose endpoints.** `Target Frame` may legitimately name a *state* rather than a file
  ("the frame the overlay was opened from" is a modal overlay's correct description), and
  a `State Transition List` line may state that no transition happens. Neither is
  machine-resolvable, and failing on them would delete the check. They are counted and
  printed instead, so the coverage gap is visible rather than silent.

## Exemptions

This module's review on #27 established the rule this file is held to: **every exemption
is staleness-guarded, and none is expressible as a byte radius.** There are two, and
neither is a window:

1. **A template whose declared line carries a placeholder.** The condition is read from
   the declaration line *itself*, not from the file: earlier this check searched the whole
   document, which silently skipped any filled plan that kept one leftover `{{…}}` in
   unrelated scaffolding — the exemption quietly widening, which is the failure it was
   supposed to prevent. It is not an `invariant_allowlist.json` entry because a hard-coded
   path list would go stale in the *noisy* direction (a renamed or newly added template
   reports false failures). Content-derived plus test-pinned is the stronger guard, and
   `RealTreeTests` asserts the exact skipped set so a skip cannot widen unnoticed.
2. **Prose endpoints** (`the frame the overlay was opened from`) are not exempted from the
   audit so much as excluded from what is auditable; they name a state, not a file. They
   are counted and printed, and the count is pinned in the tests, so the gap is measured
   rather than assumed.

Scope is repo-internal tooling for maintainers, like `check_invariants.py` and
`check_dsl_default_params.py` — a user's project has its own plan to declare its own
files.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent
PLAN_GLOB = "skills/axb-ui-plan/templates/ui-plan*.md"

DECLARED_RE = re.compile(r"^\s*-\s*Planned output files:\s*(.*)$")
CORRESPONDING_RE = re.compile(
    r"^\s*-\s*Corresponding (?:prototype|frame) file:\s*`([^`]+)`\s*$"
)
HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
# `10-suggestion.txt` is ordered by its prefix; `entry.txt` is not. The prefix is
# rendering order, not identity, so it is stripped on both sides of a comparison.
ORDER_PREFIX_RE = re.compile(r"^\d+-")
PLACEHOLDER_RE = re.compile(r"\{\{[^}]*\}\}")
# A transition endpoint sits at the head of a segment: `entry` --key--> `suggestion`.
TRANSITION_HEAD_RE = re.compile(r"^\s*(?:\d+\.)?\s*`([^`]+)`")


@dataclass
class Violation:
    path: Path
    line: int
    reference: str
    detail: str


@dataclass
class Report:
    plans: list[Path] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)
    declared: int = 0
    references: int = 0
    prose: int = 0
    violations: list[Violation] = field(default_factory=list)


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def section_body(lines: list[str], heading_prefix: str) -> list[tuple[int, str]]:
    """The (1-based line number, text) pairs of the section headed by `heading_prefix`.

    Fenced blocks are skipped for heading detection, so a defining section that gains a
    fenced example containing a `## ...` line cannot be truncated by it.
    """
    fenced: list[bool] = []
    inside = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            fenced.append(True)
            inside = not inside
            continue
        fenced.append(inside)

    start = None
    start_level = None
    for index, line in enumerate(lines):
        if fenced[index]:
            continue
        match = HEADING_RE.match(line)
        if not match:
            continue
        if start is None:
            if match.group(2).startswith(heading_prefix):
                start = index + 1
                start_level = len(match.group(1))
            continue
        if len(match.group(1)) <= start_level:
            return [(n, lines[n - 1]) for n in range(start + 1, index + 1)]
    if start is None:
        return []
    return [(n, lines[n - 1]) for n in range(start + 1, len(lines) + 1)]


def stem_of(token: str) -> str:
    """`ui/screens/10-suggestion.txt` -> `suggestion`; `ui/index.html` -> `index`."""
    name = token.strip().rsplit("/", 1)[-1]
    if "." in name:
        name = name.rsplit(".", 1)[0]
    return ORDER_PREFIX_RE.sub("", name)


def is_declared(reference: str, declared: list[str]) -> bool:
    """A path reference must match exactly; a bare frame name matches by ordered stem."""
    if "/" in reference:
        return reference in declared
    wanted = stem_of(reference)
    return any(stem_of(entry) == wanted for entry in declared)


def declared_line(lines: list[str]) -> str | None:
    """The raw text after `Planned output files:`, or None when the line is absent."""
    for line in lines:
        match = DECLARED_RE.match(line)
        if match:
            return match.group(1)
    return None


def declared_outputs(raw: str | None) -> list[str]:
    if raw is None:
        return []
    return [token.strip() for token in BACKTICK_RE.findall(raw)]


def references_of(lines: list[str]) -> list[tuple[int, str]]:
    """Every machine-resolvable frame/page reference, as (line number, reference)."""
    found: list[tuple[int, str]] = []

    for number, line in enumerate(lines, start=1):
        match = CORRESPONDING_RE.match(line)
        if match:
            found.append((number, match.group(1).strip()))

    for number, line in section_body(lines, "Keybinding Map"):
        if not line.strip().startswith("|"):
            continue
        cells = split_row(line)
        if len(cells) < 3:
            continue
        key_cell, target = cells[0], cells[2]
        if key_cell == "Key" or set(key_cell) <= set("-: "):
            continue
        for span in BACKTICK_RE.findall(target):
            span = span.strip()
            if " " in span:
                continue
            found.append((number, span))

    for number, line in section_body(lines, "State Transition List"):
        if "-->" not in line:
            continue
        for segment in line.split("-->"):
            match = TRANSITION_HEAD_RE.match(segment)
            if match:
                found.append((number, match.group(1).strip()))

    return found


def prose_count(lines: list[str]) -> int:
    """References that name a state in prose — real, but not machine-resolvable."""
    count = 0
    for _number, line in section_body(lines, "Keybinding Map"):
        if not line.strip().startswith("|"):
            continue
        cells = split_row(line)
        if len(cells) < 3 or cells[0] == "Key" or set(cells[0]) <= set("-: "):
            continue
        if cells[2] and not BACKTICK_RE.search(cells[2]):
            count += 1
    for _number, line in section_body(lines, "State Transition List"):
        if "-->" in line and not any(
            TRANSITION_HEAD_RE.match(segment) for segment in line.split("-->")
        ):
            count += 1
    return count


def audit(plan: Path, lines: list[str], declared: list[str], report: Report) -> None:
    report.plans.append(plan)
    report.declared += len(declared)

    for number, reference in references_of(lines):
        report.references += 1
        if is_declared(reference, declared):
            continue
        report.violations.append(
            Violation(
                path=plan,
                line=number,
                reference=reference,
                detail=(
                    f"`{reference}` is not on this plan's `Planned output files:` line "
                    f"({', '.join(f'`{d}`' for d in declared) or 'none declared'})"
                ),
            )
        )

    report.prose += prose_count(lines)


def run(root: Path) -> Report:
    report = Report()
    for plan in sorted(root.glob(PLAN_GLOB)):
        try:
            lines = plan.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            continue
        raw = declared_line(lines)
        # A template's *declaration line* is a placeholder: there is nothing to resolve
        # against. The test is on that line alone — searching the whole document would
        # skip any real plan that kept a leftover `{{…}}` elsewhere, which is an exemption
        # silently widening rather than a template being recognized.
        if raw is not None and PLACEHOLDER_RE.search(raw):
            report.skipped.append(plan)
            continue
        audit(plan, lines, declared_outputs(raw), report)
    return report


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

    report = run(root)

    print(f"UI plan declared-output conformance (#24 item 3): {root}")
    print(f"Plans audited: {len(report.plans)}")
    for skipped in report.skipped:
        try:
            where = skipped.relative_to(root)
        except ValueError:
            where = skipped
        print(f"  skipped (declaration line is a placeholder, so a template): {where}")
    print(f"Declared output files: {report.declared}")
    print(f"References checked: {report.references}")
    if report.prose:
        print(
            f"Prose references, not machine-resolvable and therefore not counted: {report.prose}"
        )
    # Silence about an unchecked dimension reads as coverage. State it here, where the
    # PASS/FAIL verdict is printed, not only in the docstring nobody re-reads.
    print("Not checked: prototype link targets — no filename mapping exists between the")
    print("  example prototypes and the declared `ui/*.html` names (see this module's docstring).")

    if report.violations:
        print(f"\nViolations ({len(report.violations)}):")
        for violation in report.violations:
            try:
                where = violation.path.relative_to(root)
            except ValueError:
                where = violation.path
            print(f"  {where}:{violation.line}: {violation.detail}")
        print(f"\nResult: FAILED ({len(report.violations)} reference(s))")
        return 1

    print("\nResult: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
