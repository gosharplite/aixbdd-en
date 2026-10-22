#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Check this repository's own mechanical invariants.

**Scope: the maintainers of this repository, not the users of its skills.** Every check
below audits `skills/`, `domain-model/` and `README.md` — files only a maintainer edits.
A user's project is *supposed* to contain `specs/truth/**`, so these invariants would be
meaningless there. The user-facing skill invocations (e.g. the DSL topology audit that
`axb-gherkin-and-dsl/SKILL.md` Phase 6 tells an agent to run inside a user's project)
are authoritative in their own skill and are deliberately not restated here.

Invariants 1-4 fail; 5-6 report candidates and exit 0 unless an unambiguous violation is
found. A check that fails on candidates it cannot triage gets deleted, so the triage
criterion is written into each candidate's output instead.

See issue #12 for why each invariant exists and which PR's defect it would have caught.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent


def registry_path(root: Path) -> Path:
    """The registry lives inside the repository it describes, so a fixture carries its own."""
    return root / "scripts" / "token_registry.json"


def allowlist_path(root: Path) -> Path:
    return root / "scripts" / "invariant_allowlist.json"

CHECKED_EXTENSIONS = (".md", ".py", ".yaml", ".html", ".txt")
CHECKED_ROOTS = ("skills", "domain-model")
EXTRA_FILES = ("README.md",)


@dataclass
class Finding:
    invariant: str
    message: str
    path: Path | None = None
    line: int | None = None
    root: Path | None = None

    def format(self) -> str:
        where = ""
        if self.path is not None:
            base = self.root if self.root is not None else self.path.parent
            try:
                rel = self.path.relative_to(base)
            except ValueError:
                rel = self.path
            where = str(rel)
            if self.line is not None:
                where += f":{self.line}"
            where += ": "
        return f"  [{self.invariant}] {where}{self.message}"


@dataclass
class Result:
    findings: list[Finding] = field(default_factory=list)
    candidates: list[Finding] = field(default_factory=list)

    root: Path | None = None

    def fail(self, invariant: str, message: str, path: Path | None = None, line: int | None = None) -> None:
        self.findings.append(Finding(invariant, message, path, line, self.root))

    def report(self, invariant: str, message: str, path: Path | None = None, line: int | None = None) -> None:
        self.candidates.append(Finding(invariant, message, path, line, self.root))


def iter_text_files(root: Path) -> list[Path]:
    """The same file set the historical verification greps used (#11, #14, #15)."""
    paths: list[Path] = []
    for root_name in CHECKED_ROOTS:
        base = root / root_name
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file() and path.suffix in CHECKED_EXTENSIONS:
                paths.append(path)
    for extra in EXTRA_FILES:
        path = root / extra
        if path.is_file():
            paths.append(path)
    return paths


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_allowlist(root: Path) -> dict:
    path = allowlist_path(root)
    if not path.is_file():
        return {}
    return load_json(path)


def allowlisted(allowlist: dict, invariant: str, path: Path, line_text: str, root: Path) -> bool:
    """An allowlist entry is executable, not prose: {invariant: [{path, contains}]}."""
    try:
        key = str(path.relative_to(root))
    except ValueError:
        key = str(path)
    for entry in allowlist.get(invariant, []):
        if entry.get("path") != key:
            continue
        needle = entry.get("contains")
        if needle is None or needle in line_text:
            return True
    return False


# --------------------------------------------------------------------------------------
# Invariants 1-3: spec path roots
# --------------------------------------------------------------------------------------

SPECS_REF_RE = re.compile(r"specs/(\{\{|[0-9]{3}-|[a-zA-Z])")
ALLOWED_SPECS_ROOT_RE = re.compile(r"specs/(plans|truth)(?![A-Za-z0-9_-])")


def check_specs_roots(result: Result, allowlist: dict, root: Path) -> None:
    """Invariant 1: every `specs/<segment>` reference resolves to plans/ or truth/."""
    for path in iter_text_files(root):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            continue
        for number, line in enumerate(lines, start=1):
            for match in SPECS_REF_RE.finditer(line):
                tail = line[match.start():]
                if ALLOWED_SPECS_ROOT_RE.match(tail):
                    continue
                if allowlisted(allowlist, "specs-roots", path, line, root):
                    continue
                result.fail(
                    "specs-roots",
                    f"`{tail.split()[0].rstrip('`')}` — a `specs/` root other than `plans` or `truth`; "
                    "write `specs/plans/...` or `specs/truth/...`",
                    path,
                    number,
                )


TRUTH_ARTIFACT_RE = re.compile(r"(?<![A-Za-z])contracts/|(?<![A-Za-z])data-model(?![a-z-])")

# Shapes that are *not* a reference to a truth artifact living outside specs/truth/.
TRUTH_ARTIFACT_EXEMPT_SUBSTRINGS = (
    "specs/truth/",
    "constitution",
    "templates/data-model",
    "skills/axb-data-plan",
)


def check_truth_paths(result: Result, allowlist: dict, root: Path) -> None:
    """Invariant 2: no contracts/ or data-model reference outside specs/truth/."""
    for path in iter_text_files(root):
        if path in (registry_path(root), allowlist_path(root)):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            continue
        for number, line in enumerate(lines, start=1):
            for match in TRUTH_ARTIFACT_RE.finditer(line):
                start = max(0, match.start() - 40)
                window = line[start: match.end() + 40]
                if any(needle in window for needle in TRUTH_ARTIFACT_EXEMPT_SUBSTRINGS):
                    continue
                if allowlisted(allowlist, "truth-paths", path, line, root):
                    continue
                result.fail(
                    "truth-paths",
                    f"`{match.group(0)}…` reads as a package-local truth artifact; truth lives under "
                    "`specs/truth/contracts/**` and `specs/truth/data/**`",
                    path,
                    number,
                )


PLAN_PACKAGE_RE = re.compile(r"\{\{PLAN_PACKAGE\}\}")


def check_plan_package_prefix(result: Result, allowlist: dict, root: Path) -> None:
    """Invariant 3: every {{PLAN_PACKAGE}} is preceded by a literal specs/plans/."""
    for path in iter_text_files(root):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            continue
        for number, line in enumerate(lines, start=1):
            for match in PLAN_PACKAGE_RE.finditer(line):
                prefix = line[: match.start()]
                if prefix.rstrip().endswith("specs/plans/"):
                    continue
                if allowlisted(allowlist, "plan-package-prefix", path, line, root):
                    continue
                result.fail(
                    "plan-package-prefix",
                    "`{{PLAN_PACKAGE}}` must be preceded by a literal `specs/plans/` "
                    "(the placeholder's value is a bare `NNN-<slug>`)",
                    path,
                    number,
                )


# --------------------------------------------------------------------------------------
# Invariant 4: the fixed-token registry
# --------------------------------------------------------------------------------------

HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$")


def section_text(document: str, heading_prefix: str) -> str | None:
    """Return the body of the section whose heading starts with `heading_prefix`."""
    lines = document.splitlines()
    start = None
    start_level = None
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match:
            continue
        if start is None:
            if match.group(2).startswith(heading_prefix):
                start = index + 1
                start_level = len(match.group(1))
            continue
        if len(match.group(1)) <= start_level:
            return "\n".join(lines[start:index])
    if start is None:
        return None
    return "\n".join(lines[start:])


VARIANT_PROBE_EXTENSIONS = (".md",)
VARIANT_SKIP_TOKENS = {
    # Single ordinary words whose lowercase form is legitimate prose elsewhere
    # ("stdout", "landing", "how", "invocation"). Spelling drift on these is not
    # distinguishable from normal English, so they are checked for presence only.
    "Stdout",
    "Stderr",
    "How",
    "Landing",
    "Invocation",
}


def token_variants(token: str) -> set[str]:
    """Spellings of `token` that would be drift: case, hyphen and spacing changes."""
    words = re.split(r"[-\s]+", token)
    if len(words) < 2:
        return set()
    variants: set[str] = set()
    for joiner in (" ", "-", ""):
        for transform in (str.lower, str.upper, str.title):
            candidates = transform(joiner.join(words))
            if transform is str.title:
                candidates = joiner.join(word.capitalize() for word in words)
            if candidates != token:
                variants.add(candidates)
    return variants


def check_token_registry(result: Result, allowlist: dict, root: Path) -> None:
    """Invariant 4: registry matches the definitions, and naming surfaces use it exactly."""
    registry_file = registry_path(root)
    if not registry_file.is_file():
        result.fail("token-registry", f"missing registry: {registry_file.name}")
        return

    registry = load_json(registry_file)
    defining_file = root / registry["definingFile"]
    if not defining_file.is_file():
        result.fail("token-registry", f"registry names a defining file that does not exist: {registry['definingFile']}")
        return

    document = defining_file.read_text(encoding="utf-8")
    tokens = [entry["token"] for entry in registry["tokens"]]

    # Direction 1 — completeness: every registered token is defined where the registry says.
    for entry in registry["tokens"]:
        body = section_text(document, entry["section"])
        if body is None:
            result.fail(
                "token-registry",
                f"`{entry['token']}` names section `{entry['section']}`, which does not exist in "
                f"{registry['definingFile']}",
                defining_file,
            )
            continue
        if f"`{entry['token']}`" not in body:
            result.fail(
                "token-registry",
                f"`{entry['token']}` is registered to `{entry['section']}` but is not written there — "
                "the registry and the definition have drifted apart",
                defining_file,
            )

    # Direction 2 — consistency: tokens named elsewhere use the canonical spelling.
    variant_map: dict[str, str] = {}
    for token in tokens:
        if token in VARIANT_SKIP_TOKENS:
            continue
        for variant in token_variants(token):
            variant_map.setdefault(variant, token)

    # Only *backticked* spans are candidates: this repo writes contract tokens in backticks,
    # so an unbracketed "authoritative state" is ordinary English, not a token reference.
    # Backticked file paths are excluded too — `…verification-and-writeback-criteria.md`
    # contains a token substring without naming a token.
    if variant_map:
        backticked = re.compile(r"`([^`\n]+)`")
        for path in iter_text_files(root):
            if path.suffix not in VARIANT_PROBE_EXTENSIONS:
                continue
            if path == registry_path(root):
                continue
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeError):
                continue
            for number, line in enumerate(lines, start=1):
                for span in backticked.finditer(line):
                    inner = span.group(1).strip()
                    if "/" in inner or "." in inner or "_" in inner:
                        continue
                    canonical = variant_map.get(inner)
                    if canonical is None:
                        continue
                    if allowlisted(allowlist, "token-registry", path, line, root):
                        continue
                    result.fail(
                        "token-registry",
                        f"`{inner}` should be spelled `{canonical}` — a fixed contract token "
                        "is not translatable or reformattable",
                        path,
                        number,
                    )


# --------------------------------------------------------------------------------------
# Invariants 5-6: candidate reports (non-failing)
# --------------------------------------------------------------------------------------

NORMATIVE_ROOTS = ("skills",)
NORMATIVE_FILENAME_ALLOW = ("SKILL.md", "STANDARDS.md")

ISSUE_REF_RE = re.compile(r"#[0-9]+")


def check_normative_refs(result: Result, root: Path) -> None:
    """Invariant 5: no normative document depends on an artifact that does not exist yet.

    Reports every issue reference inside normative prose as a CANDIDATE. Triage:
    a reference that *records provenance* is fine ("known gap tracked as #5");
    a reference a reader must *follow to comply* is the defect ("register it in the
    registry per #12"). Only the second is a violation.
    """
    for path in iter_text_files(root):
        if path.suffix != ".md":
            continue
        if not path.name.endswith(NORMATIVE_FILENAME_ALLOW):
            if "rules" not in path.parts:
                continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            continue
        for number, line in enumerate(lines, start=1):
            if not ISSUE_REF_RE.search(line):
                continue
            result.report(
                "refs",
                "cites an issue — provenance is fine; a reader who must follow it to comply is not",
                path,
                number,
            )


ENFORCEMENT_CLAIM_RE = re.compile(
    r"fails delivery|must not be delivered|cannot reach delivery|blocks delivery|judged failed",
    re.IGNORECASE,
)


def check_asserted_enforcement(result: Result, root: Path) -> None:
    """Invariant 6: every MUST asserting a delivery gate names the check that enforces it.

    Reports every such claim as a CANDIDATE. Triage: does the named check exist? If the
    text names no check and no tracker, the claim is intent stated as fact.
    """
    for path in iter_text_files(root):
        if path.suffix != ".md":
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            continue
        for number, line in enumerate(lines, start=1):
            if not ENFORCEMENT_CLAIM_RE.search(line):
                continue
            result.report(
                "enforcement",
                "asserts a delivery gate — confirm the check that fails it exists, or state it as intent",
                path,
                number,
            )


# --------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------


def run(root: Path, selected: set[str] | None = None) -> Result:
    allowlist = load_allowlist(root)
    result = Result(root=root)
    checks = {
        "paths": lambda: (
            check_specs_roots(result, allowlist, root),
            check_truth_paths(result, allowlist, root),
            check_plan_package_prefix(result, allowlist, root),
        ),
        "tokens": lambda: check_token_registry(result, allowlist, root),
        "refs": lambda: (check_normative_refs(result, root), check_asserted_enforcement(result, root)),
    }
    for name, check in checks.items():
        if selected and name not in selected:
            continue
        check()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--only",
        choices=("paths", "tokens", "refs"),
        action="append",
        help="run only this group (repeatable); default runs all",
    )
    parser.add_argument(
        "--quiet-candidates",
        action="store_true",
        help="suppress the non-failing candidate reports (invariants 5-6)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="repository root to check (default: this script's repository)",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    selected = set(args.only) if args.only else None
    result = run(root, selected)

    print(f"Repository invariant checks: {root}")

    if result.findings:
        print(f"\nFailures ({len(result.findings)}):")
        for finding in result.findings:
            print(finding.format())
    else:
        print("\nFailures: none")

    if result.candidates and not args.quiet_candidates:
        print(f"\nCandidates for human triage ({len(result.candidates)}, non-failing):")
        for finding in result.candidates:
            print(finding.format())

    if result.findings:
        print(f"\nResult: FAILED ({len(result.findings)} violation(s))")
        return 1
    print("\nResult: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
