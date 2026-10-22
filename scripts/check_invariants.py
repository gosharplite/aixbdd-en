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

Invariants 1-4 and 7-8 **fail** on violation. Invariants 5-6 **report candidates only** and never
fail: both need human triage (a citation may record provenance or be load-bearing; a
delivery claim may name a real check or none), and a check that fails on candidates it
cannot triage gets deleted. The triage criterion is printed with each candidate instead.

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

CHECKED_EXTENSIONS = (".md", ".py", ".yaml", ".html", ".txt")
CHECKED_ROOTS = ("skills", "domain-model")
EXTRA_FILES = ("README.md",)


def registry_path(root: Path) -> Path:
    """The registry lives inside the repository it describes, so a fixture carries its own."""
    return root / "scripts" / "token_registry.json"


def allowlist_path(root: Path) -> Path:
    return root / "scripts" / "invariant_allowlist.json"


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
    root: Path | None = None
    findings: list[Finding] = field(default_factory=list)
    candidates: list[Finding] = field(default_factory=list)

    def fail(self, invariant: str, message: str, path: Path | None = None, line: int | None = None) -> None:
        self.findings.append(Finding(invariant, message, path, line, self.root))

    def report(self, invariant: str, message: str, path: Path | None = None, line: int | None = None) -> None:
        self.candidates.append(Finding(invariant, message, path, line, self.root))


Source = tuple[Path, list[str]]


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


def load_sources(root: Path) -> list[Source]:
    """Read every checked file once; every check reuses this."""
    sources: list[Source] = []
    skip = {registry_path(root).resolve(), allowlist_path(root).resolve()}
    for path in iter_text_files(root):
        if path.resolve() in skip:
            continue
        try:
            sources.append((path, path.read_text(encoding="utf-8").splitlines()))
        except (OSError, UnicodeError):
            continue
    return sources


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


def fenced_line_mask(lines: list[str]) -> list[bool]:
    """Mark lines inside (or delimiting) a fenced code block.

    Markdown-about-markdown is this repository's normal mode, so a defining section that
    gains a fenced example containing a `## ...` line must not be truncated by it.
    """
    mask: list[bool] = []
    inside = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            mask.append(True)
            inside = not inside
            continue
        mask.append(inside)
    return mask


# --------------------------------------------------------------------------------------
# Invariants 1-3: spec path roots
# --------------------------------------------------------------------------------------

SPECS_REF_RE = re.compile(r"specs/(\{\{|[0-9]{3}-|[a-zA-Z])")
ALLOWED_SPECS_ROOT_RE = re.compile(r"specs/(plans|truth)(?![A-Za-z0-9_-])")

# Characters that may bound a path token.
PATH_BOUNDARY = set("`'\"()[]<>,;:| \t")


def path_token_at(text: str, index: int) -> str:
    """The contiguous whitespace/punctuation-delimited token containing `index`."""
    start = index
    while start > 0 and text[start - 1] not in PATH_BOUNDARY:
        start -= 1
    end = index
    while end < len(text) and text[end] not in PATH_BOUNDARY:
        end += 1
    return text[start:end]


def check_specs_roots(result: Result, allowlist: dict, root: Path, sources: list[Source]) -> None:
    """Invariant 1: every `specs/<segment>` reference resolves to plans/ or truth/."""
    for path, lines in sources:
        for number, line in enumerate(lines, start=1):
            for match in SPECS_REF_RE.finditer(line):
                tail = line[match.start():]
                if ALLOWED_SPECS_ROOT_RE.match(tail):
                    continue
                if allowlisted(allowlist, "specs-roots", path, line, root):
                    continue
                result.fail(
                    "specs-roots",
                    f"`{path_token_at(line, match.start())}` — a `specs/` root other than `plans` or "
                    "`truth`; write `specs/plans/...` or `specs/truth/...`",
                    path,
                    number,
                )


TRUTH_ARTIFACT_RE = re.compile(r"(?<![A-Za-z])contracts/|(?<![A-Za-z])data-model(?![a-z-])")


def check_truth_paths(result: Result, allowlist: dict, root: Path, sources: list[Source]) -> None:
    """Invariant 2: no contracts/ or data-model reference outside specs/truth/.

    The exemption is a property of the *path token*, not of a character radius: a
    conforming `specs/truth/<anything>/contracts/openapi.yaml` must pass however deeply
    nested it is.
    """
    for path, lines in sources:
        for number, line in enumerate(lines, start=1):
            for match in TRUTH_ARTIFACT_RE.finditer(line):
                token = path_token_at(line, match.start())
                # A conforming truth path passes however deeply nested it is: the exemption
                # is a property of the token, not of a character radius.
                if token.startswith(("specs/truth/", "truth/")):
                    continue
                # A skill's own files (`skills/axb-data-plan/data-model.md`, a skill's
                # `templates/` dir) are not truth artifacts.
                if token.startswith("skills/") or token.startswith("templates/") or "/templates/" in token:
                    continue
                if "constitution" in token:
                    continue
                # An *abbreviation* with no file extension ("contracts/data",
                # "data-model truth") is contextualised when the truth root appears on the
                # same line. A token naming an actual artifact — one with an extension —
                # is always flagged, so this exemption cannot swallow a real violation that
                # happens to share a line with a conforming path.
                looks_like_artifact = bool(re.search(r"\.[A-Za-z][A-Za-z0-9]{1,9}$", token))
                if not looks_like_artifact and "specs/truth" in line:
                    continue
                if allowlisted(allowlist, "truth-paths", path, line, root):
                    continue
                result.fail(
                    "truth-paths",
                    f"`{token}` reads as a package-local truth artifact; truth lives under "
                    "`specs/truth/contracts/**` and `specs/truth/data/**`",
                    path,
                    number,
                )


PLAN_PACKAGE_RE = re.compile(r"\{\{PLAN_PACKAGE\}\}")


def check_plan_package_prefix(result: Result, allowlist: dict, root: Path, sources: list[Source]) -> None:
    """Invariant 3: every {{PLAN_PACKAGE}} is directly preceded by specs/plans/.

    Adjacency is required — `specs/plans/ {{PLAN_PACKAGE}}` renders no valid path — and
    the prefix must be bounded like a path, so `foo-specs/plans/` does not qualify.
    """
    for path, lines in sources:
        for number, line in enumerate(lines, start=1):
            for match in PLAN_PACKAGE_RE.finditer(line):
                start = match.start()
                prefix = "specs/plans/"
                if not line[:start].endswith(prefix):
                    if allowlisted(allowlist, "plan-package-prefix", path, line, root):
                        continue
                    result.fail(
                        "plan-package-prefix",
                        "the plan-package placeholder must be *directly* preceded by `specs/plans/` "
                        "(the placeholder's value is a bare `NNN-<slug>`)",
                        path,
                        number,
                    )
                    continue
                before = start - len(prefix)
                if before > 0 and line[before - 1] not in PATH_BOUNDARY:
                    if allowlisted(allowlist, "plan-package-prefix", path, line, root):
                        continue
                    result.fail(
                        "plan-package-prefix",
                        "`specs/plans/` before the plan-package placeholder must start a path, not "
                        "follow other path characters",
                        path,
                        number,
                    )


# --------------------------------------------------------------------------------------
# Invariant 4: the fixed-token registry
# --------------------------------------------------------------------------------------

HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$")


def section_text(document: str, heading_prefix: str) -> str | None:
    """Return the body of the section whose heading starts with `heading_prefix`.

    Fenced blocks are skipped for heading detection, so an example containing a `## ...`
    line cannot truncate the section that defines the tokens.
    """
    lines = document.splitlines()
    fenced = fenced_line_mask(lines)
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
            return "\n".join(lines[start:index])
    if start is None:
        return None
    return "\n".join(lines[start:])


def token_variants(token: str) -> set[str]:
    """Spellings of `token` that would be drift: case, hyphen and spacing changes.

    Sentence case is included because it is the *likeliest* drift in this repo — the
    canonical vocabulary itself mixes conventions (`Must-check`, `State landing` beside
    `Exit Code`, `Should Not Happen`), so a writer applying house sentence-case style to a
    title-case token reproduces exactly the spelling drift this invariant exists to catch.
    """
    words = re.split(r"[-\s]+", token)
    if len(words) < 2:
        return set()
    variants: set[str] = set()
    for joiner in (" ", "-", ""):
        variants.add(joiner.join(word.lower() for word in words))
        variants.add(joiner.join(word.upper() for word in words))
        variants.add(joiner.join(word.capitalize() for word in words))
        # Sentence case: first word capitalized, the rest lowered.
        variants.add(joiner.join([words[0].capitalize()] + [word.lower() for word in words[1:]]))
    variants.discard(token)
    return variants


def check_token_registry(result: Result, allowlist: dict, root: Path, sources: list[Source]) -> None:
    """Invariant 4: registry matches the definitions, and naming surfaces use it exactly."""
    registry_file = registry_path(root)
    if not registry_file.is_file():
        result.fail("token-registry", f"missing registry: {registry_file.name}")
        return

    registry = load_json(registry_file)
    defining_file = root / registry["definingFile"]
    if not defining_file.is_file():
        result.fail(
            "token-registry",
            f"registry names a defining file that does not exist: {registry['definingFile']}",
        )
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
    #
    # Only *backticked* spans are candidates: this repo writes contract tokens in backticks,
    # so unbracketed "authoritative state" is ordinary English. Backticked paths are
    # excluded too — `…verification-and-writeback-criteria.md` contains a token substring
    # without naming a token.
    #
    # A span may *begin* with a drifted token followed by a delimiter (`:` or whitespace),
    # because the natural quoted form of a DSL cell always carries content after the colon.
    variant_map: dict[str, str] = {}
    for token in tokens:
        for variant in token_variants(token):
            variant_map.setdefault(variant, token)

    if variant_map:
        ordered = sorted(variant_map, key=len, reverse=True)
        variant_pattern = re.compile(r"(" + "|".join(re.escape(v) for v in ordered) + r")(?=$|:)")
        backticked = re.compile(r"`([^`\n]+)`")
        for path, lines in sources:
            if path.suffix != ".md":
                continue
            for number, line in enumerate(lines, start=1):
                for span in backticked.finditer(line):
                    inner = span.group(1).strip()
                    if "/" in inner or inner.endswith((".md", ".py", ".yaml", ".json", ".html", ".txt")):
                        continue
                    match = variant_pattern.match(inner)
                    if match is None:
                        continue
                    canonical = variant_map[match.group(1)]
                    if allowlisted(allowlist, "token-registry", path, line, root):
                        continue
                    result.fail(
                        "token-registry",
                        f"`{inner}` should be spelled `{canonical}` — a fixed contract token is not "
                        "translatable or reformattable",
                        path,
                        number,
                    )


# --------------------------------------------------------------------------------------
# Invariants 7-8: references that must resolve (fail)
# --------------------------------------------------------------------------------------

SKILL_REF_RE = re.compile(r"`/([a-z][a-z0-9-]*)`")

# Backticked slash tokens that are NOT command references. Deliberately a small, reviewed
# set rather than a pattern: the whole point of this invariant is that a stale skill name
# looks exactly like a live one, so the exemption must be explicit per token.
#
#   ws — an HTTP route (`FastAPI /ws`), not a command.
#
# The test suite asserts every entry here is still referenced somewhere, so a stale
# exemption fails rather than silently widening the check.
NON_SKILL_SLASH_TOKENS = {"ws"}


def check_skill_references(result: Result, root: Path, sources: list[Source]) -> None:
    """Invariant 7: every backticked `/command` names a skill that exists.

    Deliberately **not** restricted to `axb-` names. The defects this exists to catch were
    `/plan`, `/plan-with-class-diagram` and `/skill-engineering` (#2) — none of which carry
    the prefix — so an `axb-`-only pattern would pass every one of them. That is how the
    first version of this check missed its own motivating cases.
    """
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        result.fail("skill-references", "no `skills/` directory to resolve references against")
        return
    known = {p.name for p in skills_dir.iterdir() if p.is_dir()}

    for path, lines in sources:
        for number, line in enumerate(lines, start=1):
            for match in SKILL_REF_RE.finditer(line):
                name = match.group(1)
                if name in known or name in NON_SKILL_SLASH_TOKENS:
                    continue
                result.fail(
                    "skill-references",
                    f"`/{name}` is not a skill under `skills/` — a command reference must name a "
                    "real skill; if this is not a command, add it to NON_SKILL_SLASH_TOKENS with a reason",
                    path,
                    number,
                )


SECTION_REF_RE = re.compile(r"§(\d+(?:\.\d+)?)")


def check_section_references(result: Result, root: Path, sources: list[Source]) -> None:
    """Invariant 8: every `§N` naming a STANDARDS.md section resolves to a real heading.

    Would have caught #6 finding 2. One narrow exclusion, stated rather than hidden: a `§`
    preceded by a licence identifier (`Apache-2.0 §4(d)`) refers to that licence, not to the
    standard. `STANDARDS.md` is skipped because it cites its own section numbers in prose.
    """
    defining = root / "skills" / "axb-gherkin-and-dsl" / "STANDARDS.md"
    if not defining.is_file():
        return
    document = defining.read_text(encoding="utf-8")
    known = set(re.findall(r"^##+ (\d+)[\. ]", document, re.M))
    known |= set(re.findall(r"^### (\d+\.\d+)", document, re.M))

    for path, lines in sources:
        if path == defining:
            continue
        for number, line in enumerate(lines, start=1):
            for match in SECTION_REF_RE.finditer(line):
                before = line[max(0, match.start() - 16) : match.start()]
                if re.search(r"Apache-[\d.]+\s*$", before):
                    continue
                section = match.group(1)
                if section in known:
                    continue
                result.fail(
                    "section-references",
                    f"`§{section}` does not name a section of `skills/axb-gherkin-and-dsl/STANDARDS.md`",
                    path,
                    number,
                )


# --------------------------------------------------------------------------------------
# Invariants 5-6: candidate reports (never fail)
# --------------------------------------------------------------------------------------

ISSUE_REF_RE = re.compile(r"#[0-9]+")


def check_normative_refs(result: Result, sources: list[Source]) -> None:
    """Invariant 5: no normative document depends on an artifact that does not exist yet.

    Reports every issue reference inside normative prose as a CANDIDATE. Triage:
    a reference that *records provenance* is fine ("known gap tracked as #5");
    a reference a reader must *follow to comply* is the defect ("register it in the
    registry per #12"). Only the second is a violation.
    """
    for path, lines in sources:
        if path.suffix != ".md":
            continue
        if not (path.name == "SKILL.md" or path.name == "STANDARDS.md" or "rules" in path.parts):
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


def check_asserted_enforcement(result: Result, sources: list[Source]) -> None:
    """Invariant 6: every MUST asserting a delivery gate names the check that enforces it.

    Reports every such claim as a CANDIDATE. Triage: does the named check exist? If the
    text names no check and no tracker, the claim is intent stated as fact.
    """
    for path, lines in sources:
        if path.suffix != ".md":
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
    sources = load_sources(root)
    result = Result(root=root)
    checks = {
        "paths": lambda: (
            check_specs_roots(result, allowlist, root, sources),
            check_truth_paths(result, allowlist, root, sources),
            check_plan_package_prefix(result, allowlist, root, sources),
        ),
        "tokens": lambda: check_token_registry(result, allowlist, root, sources),
        "refs": lambda: (check_normative_refs(result, sources), check_asserted_enforcement(result, sources)),
        "names": lambda: (
            check_skill_references(result, root, sources),
            check_section_references(result, root, sources),
        ),
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
        choices=("paths", "tokens", "refs", "names"),
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
