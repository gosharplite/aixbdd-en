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
- **References**: the labelled screen lines (`Corresponding prototype file:` /
  `Corresponding frame file:` / `Entry frame:` / `Multi-page entry:`), the `Target Frame`
  column of a `Keybinding Map`, and every endpoint of a `State Transition List`.

## Two structural rules this file is built on

Review of #28 found that all of its escapes began in one of two places, so both are
structural here rather than fixed case by case.

**One fence mask, applied before any line scan.** Fenced content is documentation *about*
the format, not the format: a plan quoting the template's `Planned output files:` line in a
code block is illustrating, and a fenced `Corresponding frame file:` line is not a
reference. The first version masked fences in one scanner out of three, so a fenced quote
above the real declaration classified a filled plan as a template and skipped it whole,
while a fenced example below it became a false failure. `visible()` is the only way any
scanner sees a line, so a new scanner cannot forget.

**One pass, two ledgers that sum to it.** `observations()` classifies every reference site
exactly once as either *resolvable* (checked against the declaration) or *prose* (names a
state, not a file). The first version had two hand-synchronised parsers, and anything one
dropped the other did not count — an empty-key continuation row, a backticked target
containing a space, and the prose tail of a half-resolvable transition line all vanished
from the verdict *and* from the printed gap. Now `checked + prose == seen` holds by
construction, and the gate prints all three numbers, so a drop shows up in the output
rather than only in its absence.

The rule behind both: **every item a scanner drops must land in a ledger the output
prints.** Dropped-but-unprinted is how every escape in #28's review began.

## What is deliberately not read

- **Prototype link targets.** The defect would be a clickable target the plan does not
  declare, but this repository's example prototypes are named `prototype-*.example.html`
  while the plan declares `ui/*.html`, so no filename mapping exists to resolve a target
  *against*. A check would have to invent one, and an invented mapping fails open: it
  would report zero violations whether or not a target was declared. The half that can be
  decided from the tree — a plan contradicting its own declaration — is the half built
  here; the link-target half becomes buildable when a fixture exists whose prototype
  filenames are the declared ones. Printed with the verdict, not only recorded here.

Nothing else is silently out of scope: an unreadable plan is recorded as skipped with its
error, and a plan skipped as a template says so.

## Exemptions

This module is held to the rule #27 established: **every exemption is staleness-guarded,
and none is expressible as a byte radius.** Two, neither a window:

1. **A template whose declaration line carries a placeholder**, tested on that line alone
   (and on its fenced-visible version). It is not an `invariant_allowlist.json` entry
   because a hard-coded path list goes stale in the *noisy* direction (a renamed or added
   template reports false failures); content-derived plus a test-pinned skipped set is the
   stronger guard.
2. **Prose reference sites** are not exempted so much as classified: they name a state, not
   a file. They are counted, printed, and pinned in the tests.

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
# `Entry frame:` names one frame outright; `Multi-page entry:` wraps it in a sentence
# ("fixedly use ui/index.html as the prototype entry page"), so its value is scanned for a
# path rather than taken whole. These are the highest-value single references in a plan —
# they say where a reviewer starts — and the first version of this check read neither.
ENTRY_LINE_RE = re.compile(r"^\s*-\s*(?:Entry frame|Multi-page entry):\s*(.*)$")
HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
# A path-shaped token: at least one `/` and a file extension. Used only inside a labelled
# value, so it cannot run wild over the document.
PATH_TOKEN_RE = re.compile(r"[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)+\.[A-Za-z0-9]{1,5}\b")
# `10-suggestion.txt` is ordered by its prefix; `entry.txt` is not. The prefix is
# rendering order *and* identity — two files can share a stem — so it is compared, not
# discarded.
ORDER_PREFIX_RE = re.compile(r"^(\d+)-(.*)$")
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
class Observation:
    """One reference site, classified. Exactly one of the two ledgers takes it."""

    line: int
    text: str
    resolvable: bool


@dataclass
class Report:
    plans: list[Path] = field(default_factory=list)
    skipped: list[tuple[Path, str]] = field(default_factory=list)
    declared: int = 0
    observations: list[Observation] = field(default_factory=list)
    violations: list[Violation] = field(default_factory=list)

    @property
    def checked(self) -> int:
        return sum(1 for o in self.observations if o.resolvable)

    @property
    def prose(self) -> int:
        return sum(1 for o in self.observations if not o.resolvable)


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def fenced_line_mask(lines: list[str]) -> list[bool]:
    """Mark lines inside (or delimiting) a fenced code block.

    This repository writes markdown about markdown, so a plan may quote the format it is
    written in. Fenced content is illustration, not content — see the module docstring.
    """
    mask: list[bool] = []
    inside = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            mask.append(True)
            inside = not inside
            continue
        mask.append(inside)
    return mask


def visible(lines: list[str]) -> list[tuple[int, str]]:
    """Every (1-based line number, text) pair outside a fence.

    The single entry point for line scanning. A scanner that iterates `lines` directly is
    the bug this function exists to make unwritable.
    """
    mask = fenced_line_mask(lines)
    return [
        (number, line)
        for number, (line, fenced) in enumerate(zip(lines, mask), start=1)
        if not fenced
    ]


def declared_line(lines: list[str]) -> str | None:
    """The raw text after the first *visible* `Planned output files:`, if any."""
    for _number, line in visible(lines):
        match = DECLARED_RE.match(line)
        if match:
            return match.group(1)
    return None


def declared_outputs(raw: str | None) -> list[str]:
    if raw is None:
        return []
    return [token.strip() for token in BACKTICK_RE.findall(raw)]


def section_body(lines: list[str], heading_prefix: str) -> list[tuple[int, str]]:
    """The visible (line number, text) pairs of the section headed by `heading_prefix`."""
    rows = visible(lines)
    start = None
    start_level = None
    for index, (_number, line) in enumerate(rows):
        match = HEADING_RE.match(line)
        if not match:
            continue
        if start is None:
            if match.group(2).startswith(heading_prefix):
                start = index + 1
                start_level = len(match.group(1))
            continue
        if len(match.group(1)) <= start_level:
            return rows[start:index]
    if start is None:
        return []
    return rows[start:]


def name_parts(token: str) -> tuple[str | None, str, str]:
    """Split a frame reference into (order prefix, stem, extension).

    `ui/screens/10-suggestion.txt` -> ("10", "suggestion", ".txt")
    `suggestion`                   -> (None, "suggestion", "")
    """
    name = token.strip().rsplit("/", 1)[-1]
    stem, dot, extension = name.partition(".")
    match = ORDER_PREFIX_RE.match(stem)
    if match:
        return match.group(1), match.group(2), (dot + extension)
    return None, stem, (dot + extension)


def is_declared(reference: str, declared: list[str]) -> bool:
    """Does `reference` name one of `declared`?

    A path reference must match a declared entry exactly. A bare name is matched by stem,
    because plans refer to `10-suggestion.txt` as `suggestion` — but only the *prefix* is
    optional: a reference that states a prefix, or an extension, must state the same one
    the declaration does. Discarding both sides' prefixes and extensions (the first
    version of this function) let `20-suggestion` match `10-suggestion.txt` and
    `suggestion.html` match `suggestion.txt` — same stem, different file, and renumbering
    is exactly the edit a ui plan undergoes.
    """
    if "/" in reference:
        return reference in declared
    ref_prefix, ref_stem, ref_extension = name_parts(reference)
    for entry in declared:
        entry_prefix, entry_stem, entry_extension = name_parts(entry)
        if ref_stem != entry_stem:
            continue
        if ref_prefix is not None and ref_prefix != entry_prefix:
            continue
        if ref_extension and entry_extension and ref_extension != entry_extension:
            continue
        return True
    return False


def labelled_values(
    rows: list[tuple[int, str]], pattern: re.Pattern[str]
) -> list[tuple[int, str]]:
    found = []
    for number, line in rows:
        match = pattern.match(line)
        if match:
            found.append((number, match.group(1).strip()))
    return found


def observations(lines: list[str]) -> list[Observation]:
    """Classify every reference site exactly once.

    One pass, two ledgers. `resolvable` sites are checked against the declaration; the rest
    are prose. Nothing is dropped: a site is either in the checked ledger or in the prose
    ledger, so the printed totals cannot disagree with what was seen.
    """
    found: list[Observation] = []
    rows = visible(lines)

    for number, value in labelled_values(rows, CORRESPONDING_RE):
        found.append(Observation(number, value, True))

    for number, value in labelled_values(rows, ENTRY_LINE_RE):
        spans = BACKTICK_RE.findall(value) or [value]
        paths = [path for span in spans for path in PATH_TOKEN_RE.findall(span)]
        if paths:
            found.extend(Observation(number, path, True) for path in paths)
        elif value:
            found.append(Observation(number, value, False))

    for number, line in section_body(lines, "Keybinding Map"):
        if not line.strip().startswith("|"):
            continue
        cells = split_row(line)
        if len(cells) < 3:
            continue
        key_cell, target = cells[0], cells[2]
        # Skip the header row and the `--- | ---` separator. An *empty* key cell is a
        # continuation row ("same key, second effect") and carries a real target: the first
        # version tested `set(key_cell) <= set("-: ")`, and the empty set is a subset of
        # every set, so those rows vanished from both ledgers.
        if key_cell == "Key" or (key_cell and set(key_cell) <= set("-: ")):
            continue
        spans = [span.strip() for span in BACKTICK_RE.findall(target)]
        resolvable = [span for span in spans if span and not any(c.isspace() for c in span)]
        if resolvable:
            found.extend(Observation(number, span, True) for span in resolvable)
            continue
        if target:
            found.append(Observation(number, target, False))

    for number, line in section_body(lines, "State Transition List"):
        if "-->" not in line:
            continue
        for segment in line.split("-->"):
            match = TRANSITION_HEAD_RE.match(segment)
            if match:
                found.append(Observation(number, match.group(1).strip(), True))
            elif segment.strip():
                found.append(Observation(number, segment.strip(), False))

    return found


def audit(plan: Path, lines: list[str], declared: list[str], report: Report) -> None:
    report.plans.append(plan)
    report.declared += len(declared)

    for observation in observations(lines):
        report.observations.append(observation)
        if not observation.resolvable or is_declared(observation.text, declared):
            continue
        report.violations.append(
            Violation(
                path=plan,
                line=observation.line,
                reference=observation.text,
                detail=(
                    f"`{observation.text}` is not on this plan's `Planned output files:` line "
                    f"({', '.join(f'`{d}`' for d in declared) or 'none declared'})"
                ),
            )
        )


def run(root: Path) -> Report:
    report = Report()
    for plan in sorted(root.glob(PLAN_GLOB)):
        try:
            lines = plan.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as error:
            # A plan that cannot be read is a gap in the audit, so it is recorded. The first
            # version dropped it silently while the template skip two lines below was
            # recorded and printed — an unreadable plan should not be quieter than a
            # deliberately skipped one.
            report.skipped.append((plan, f"unreadable ({error.__class__.__name__})"))
            continue
        raw = declared_line(lines)
        if raw is not None and PLACEHOLDER_RE.search(raw):
            report.skipped.append((plan, "template — the declaration line is a placeholder"))
            continue
        audit(plan, lines, declared_outputs(raw), report)
    return report


def relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


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
    for path, reason in report.skipped:
        print(f"  skipped ({reason}): {relative(path, root)}")
    print(f"Declared output files: {report.declared}")
    print(f"Reference sites seen: {len(report.observations)}")
    print(f"  checked against the declaration: {report.checked}")
    print(f"  prose (names a state, not a file): {report.prose}")
    # Silence about an unchecked dimension reads as coverage. State it here, where the
    # PASS/FAIL verdict is printed, not only in the docstring nobody re-reads.
    print("Not checked: prototype link targets — no filename mapping exists between the")
    print("  example prototypes and the declared `ui/*.html` names (see this module's docstring).")

    if report.violations:
        print(f"\nViolations ({len(report.violations)}):")
        for violation in report.violations:
            print(f"  {relative(violation.path, root)}:{violation.line}: {violation.detail}")
        print(f"\nResult: FAILED ({len(report.violations)} reference(s))")
        return 1

    # The vacuity guard belongs here, not only in the test suite: `make check` runs this
    # script, `make test` does not, so a commit-time gate that audits nothing would pass
    # every commit. Renaming the templates directory, or a whole-plan skip, is enough to
    # reach this — the suite's own comment argued "fail rather than pass over nothing", and
    # this is the layer where that has to be true.
    if not report.plans:
        print("\nResult: FAILED (no plans audited — the gate judged nothing)")
        return 1
    if not report.observations:
        print(
            "\nResult: FAILED (plans audited but no reference sites seen — "
            "the parser is not reading them)"
        )
        return 1

    print("\nResult: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
