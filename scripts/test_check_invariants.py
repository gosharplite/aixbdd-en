"""Tests for scripts/check_invariants.py.

Each invariant is proven against **its own historical escape** — the defect from the PR
that motivated it — not merely against a clean tree. A check that only passes on a clean
tree has not been shown to catch anything (issue #12, acceptance criteria).

Constructed trees live in a temporary root; the checker takes `--root`, so a fixture is a
small repository carrying its own registry and allowlist.
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_invariants as checker  # noqa: E402

MINIMAL_STANDARDS = """# Standards

## 4. DSL Required Fields

- `DSL Sentence`
- `Gherkin Params`
- `Data Table Params`
- `Default Params`

## 5. Backend DSL Implementation Semantics

### 5.1 Given / When Granularity

- `How` (how to do it)
- `State landing` (authoritative state landing)
- `Write-back` (write-back)
- `No-check` (the boundary of what this step does not assert)

### 5.2 Then Granularity

- `Must-check` opens the cell.
- `Presented Result`: this response
- `Authoritative State`: store truth
- `Re-read Confirmation`: still holds
- `Cross-Perspective`: another player sees the same
- `Should Not Happen`: must not be created

## 7. CLI DSL Implementation Semantics

### 7.2 Then Granularity

- `Stdout`: this command's standard output
- `Stderr`: this command's diagnostics
- `Exit Code`: the numeric exit status
- `Filesystem State`: files written or left untouched
"""

MINIMAL_REGISTRY = {
    "definingFile": "skills/axb-gherkin-and-dsl/STANDARDS.md",
    "tokens": [
        {"token": "DSL Sentence", "section": "4. DSL Required Fields", "kind": "meta-schema"},
        {"token": "Gherkin Params", "section": "4. DSL Required Fields", "kind": "meta-schema"},
        {"token": "Data Table Params", "section": "4. DSL Required Fields", "kind": "meta-schema"},
        {"token": "Default Params", "section": "4. DSL Required Fields", "kind": "meta-schema"},
        {"token": "How", "section": "5.1 Given / When Granularity", "kind": "given-when-label"},
        {"token": "State landing", "section": "5.1 Given / When Granularity", "kind": "given-when-label"},
        {"token": "Write-back", "section": "5.1 Given / When Granularity", "kind": "given-when-label"},
        {"token": "No-check", "section": "5.1 Given / When Granularity", "kind": "given-when-label"},
        {"token": "Must-check", "section": "5.2 Then Granularity", "kind": "then-marker"},
        {"token": "Presented Result", "section": "5.2 Then Granularity", "kind": "then-channel"},
        {"token": "Authoritative State", "section": "5.2 Then Granularity", "kind": "then-channel"},
        {"token": "Re-read Confirmation", "section": "5.2 Then Granularity", "kind": "then-channel"},
        {"token": "Cross-Perspective", "section": "5.2 Then Granularity", "kind": "then-channel"},
        {"token": "Should Not Happen", "section": "5.2 Then Granularity", "kind": "then-channel"},
        {"token": "Stdout", "section": "7.2 Then Granularity", "kind": "then-channel"},
        {"token": "Stderr", "section": "7.2 Then Granularity", "kind": "then-channel"},
        {"token": "Exit Code", "section": "7.2 Then Granularity", "kind": "then-channel"},
        {"token": "Filesystem State", "section": "7.2 Then Granularity", "kind": "then-channel"},
    ],
}


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "scripts").mkdir()
        (self.root / "skills" / "axb-gherkin-and-dsl").mkdir(parents=True)
        (self.root / "skills" / "axb-gherkin-and-dsl" / "STANDARDS.md").write_text(MINIMAL_STANDARDS)
        self._write_registry(MINIMAL_REGISTRY)
        self._write_allowlist({})

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _write_registry(self, data: dict) -> None:
        (self.root / "scripts" / "token_registry.json").write_text(json.dumps(data, indent=2))

    def _write_allowlist(self, data: dict) -> None:
        (self.root / "scripts" / "invariant_allowlist.json").write_text(json.dumps(data, indent=2))

    def write(self, relpath: str, text: str) -> Path:
        path = self.root / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def run_check(self, selected=None) -> checker.Result:
        return checker.run(self.root.resolve(), selected)


class CleanTreeTests(Fixture):
    def test_clean_tree_passes(self) -> None:
        self.write("README.md", "Nothing to see here.\n")
        result = self.run_check()
        self.assertEqual([f.format() for f in result.findings], [])


class SpecsRootTests(Fixture):
    """Invariant 1 — the #8 escape was the *placeholder* form, invisible to a numeric grep."""

    def test_placeholder_root_is_caught(self) -> None:
        self.write("skills/x/templates/plan.md", "specs/{{FEATURE_BRANCH}}/\n")
        result = self.run_check({"paths"})
        self.assertEqual(len(result.findings), 1, result.findings)
        self.assertIn("specs/{{FEATURE_BRANCH}}/", result.findings[0].message)

    def test_numeric_root_is_caught(self) -> None:
        self.write("skills/x/templates/plan.md", "- see `specs/001-foo/spec.md`\n")
        result = self.run_check({"paths"})
        self.assertEqual(len(result.findings), 1, result.findings)

    def test_named_root_is_caught(self) -> None:
        self.write("skills/x/templates/plan.md", "- see specs/billing/spec.md\n")
        result = self.run_check({"paths"})
        self.assertEqual(len(result.findings), 1, result.findings)

    def test_allowed_roots_pass(self) -> None:
        self.write(
            "skills/x/templates/plan.md",
            "specs/plans/004-x/spec.md\n**Truth Root**: `specs/truth`\nspecs/truth/contracts/openapi.yaml\n",
        )
        result = self.run_check({"paths"})
        self.assertEqual(result.findings, [])


class TruthPathTests(Fixture):
    """Invariant 2 — the #11 escape: a truth artifact reading as package-local."""

    def test_package_local_contract_is_caught(self) -> None:
        self.write("skills/x/rules/r.md", "It supplements with `contracts/openapi.yaml`.\n")
        result = self.run_check({"paths"})
        self.assertEqual(len(result.findings), 1, result.findings)
        self.assertIn("contracts/", result.findings[0].message)

    def test_package_local_data_model_is_caught(self) -> None:
        self.write("skills/x/rules/r.md", "Reads `data-model.dbml` too.\n")
        result = self.run_check({"paths"})
        self.assertEqual(len(result.findings), 1, result.findings)

    def test_truth_tree_paths_pass(self) -> None:
        self.write("skills/x/rules/r.md", "Reads `specs/truth/contracts/openapi.yaml`.\n")
        result = self.run_check({"paths"})
        self.assertEqual(result.findings, [])

    def test_deeply_nested_conforming_truth_path_passes(self) -> None:
        # Regression: the exemption used to be a +/-40-character window, so a conforming
        # path nested deeper than that was flagged. A checker that fails on correct content
        # gets allowlisted into silence (review of #21, finding 2).
        self.write(
            "skills/x/rules/r.md",
            "Reads `specs/truth/some/deeply/nested/subdirectory/tree/contracts/openapi.yaml`.\n",
        )
        result = self.run_check({"paths"})
        self.assertEqual(result.findings, [], result.findings)

    def test_skill_own_template_file_is_not_a_truth_artifact(self) -> None:
        self.write("skills/x/rules/r.md", "Place in `skills/axb-data-plan/data-model.md`.\n")
        result = self.run_check({"paths"})
        self.assertEqual(result.findings, [])

    def test_abbreviation_contextualised_by_truth_on_the_same_line_passes(self) -> None:
        self.write("skills/x/rules/r.md", "Read the relevant contracts/data, and `specs/truth/techstack.md`.\n")
        result = self.run_check({"paths"})
        self.assertEqual(result.findings, [])

    def test_package_local_artifact_beside_a_conforming_path_is_still_caught(self) -> None:
        # The line-scoped exemption must not swallow a real violation on the same line.
        self.write(
            "skills/x/rules/r.md",
            "Reads `specs/truth/contracts/a.yaml` and also a package-local `contracts/b.yaml`.\n",
        )
        result = self.run_check({"paths"})
        self.assertEqual(len(result.findings), 1, result.findings)
        self.assertIn("contracts/b.yaml", result.findings[0].message)

    def test_invariant_id_is_not_an_artifact(self) -> None:
        # `data-model-covers-all-state` is an invariant id, not a reference to data-model.md
        self.write("skills/x/rules/r.md", "- **data-model-covers-all-state** — everything.\n")
        result = self.run_check({"paths"})
        self.assertEqual(result.findings, [])


class PlanPackagePrefixTests(Fixture):
    """Invariant 3 — #11 finding 1: the placeholder's value convention forking."""

    def test_bare_placeholder_is_caught(self) -> None:
        self.write("skills/x/templates/t.md", "**Plan Package**: `{{PLAN_PACKAGE}}`\n")
        result = self.run_check({"paths"})
        self.assertEqual(len(result.findings), 1, result.findings)

    def test_prefixed_placeholder_passes(self) -> None:
        self.write("skills/x/templates/t.md", "**Plan Package**: `specs/plans/{{PLAN_PACKAGE}}`\n")
        result = self.run_check({"paths"})
        self.assertEqual(result.findings, [])

    def test_whitespace_gap_before_placeholder_is_caught(self) -> None:
        # Regression: `rstrip()` erased the gap, so a form that renders no valid path
        # passed (review of #21, finding 4).
        #
        # The prefix starts the line, so the boundary check is skipped (`before == 0`) and
        # only the adjacency check can fire. Otherwise the two checks overlap and mask each
        # other, making this test unable to distinguish them.
        self.write("skills/x/templates/t.md", "specs/plans/ {{PLAN_PACKAGE}}\n")
        result = self.run_check({"paths"})
        self.assertEqual(len(result.findings), 1, result.findings)
        self.assertIn("directly", result.findings[0].message)

    def test_prefix_following_other_path_characters_is_caught(self) -> None:
        # `foo-specs/plans/` merely *ends* with the string; it does not start a path.
        self.write("skills/x/templates/t.md", "`foo-specs/plans/{{PLAN_PACKAGE}}`\n")
        result = self.run_check({"paths"})
        self.assertEqual(len(result.findings), 1, result.findings)


class TokenRegistryTests(Fixture):
    """Invariant 4 — #15's registration failures and #16's variant drift."""

    def test_token_missing_from_its_section_is_caught(self) -> None:
        data = json.loads(json.dumps(MINIMAL_REGISTRY))
        data["tokens"].append({"token": "Landing", "section": "5.2 Then Granularity", "kind": "then-channel"})
        self._write_registry(data)
        result = self.run_check({"tokens"})
        self.assertEqual(len(result.findings), 1, result.findings)
        self.assertIn("Landing", result.findings[0].message)

    def test_registry_naming_a_missing_section_is_caught(self) -> None:
        data = json.loads(json.dumps(MINIMAL_REGISTRY))
        data["tokens"].append({"token": "Ghost", "section": "9. Nowhere", "kind": "x"})
        self._write_registry(data)
        result = self.run_check({"tokens"})
        self.assertTrue(any("does not exist" in f.message for f in result.findings), result.findings)

    def test_wrong_spelling_of_a_token_is_caught(self) -> None:
        self.write("skills/x/SKILL.md", "Open the cell with `must-check`.\n")
        result = self.run_check({"tokens"})
        self.assertEqual(len(result.findings), 1, result.findings)
        self.assertIn("Must-check", result.findings[0].message)

    def test_hyphen_variant_is_caught(self) -> None:
        self.write("skills/x/SKILL.md", "The `should-not-happen` channel.\n")
        result = self.run_check({"tokens"})
        self.assertEqual(len(result.findings), 1, result.findings)

    def test_sentence_case_drift_is_caught(self) -> None:
        # Regression: only lower/UPPER/Title were generated, so the likeliest drift in a
        # repo whose vocabulary mixes `Must-check` with `Exit Code` escaped (review of #21,
        # finding 3).
        self.write("skills/x/SKILL.md", "The `Exit code` channel.\n")
        result = self.run_check({"tokens"})
        self.assertEqual(len(result.findings), 1, result.findings)
        self.assertIn("Exit Code", result.findings[0].message)

    def test_drifted_token_with_trailing_cell_content_is_caught(self) -> None:
        # Regression: the span had to *equal* a variant, so the natural quoted form of a
        # cell carrying content after the colon escaped (review of #21, finding 5).
        self.write("skills/x/SKILL.md", "| row | `Must-Check: foo` |\n")
        result = self.run_check({"tokens"})
        self.assertEqual(len(result.findings), 1, result.findings)
        self.assertIn("Must-check", result.findings[0].message)

    def test_ordinary_prose_is_not_a_token_reference(self) -> None:
        # Unbackticked prose is English, not a token naming.
        self.write("skills/x/SKILL.md", "The authoritative state must land in the store.\n")
        result = self.run_check({"tokens"})
        self.assertEqual(result.findings, [])

    def test_different_phrase_sharing_a_token_prefix_passes(self) -> None:
        # `write-back data` is a distinct phrase (a §6.2 guidance label), not a drift of
        # `Write-back`; prefix matching must require a colon delimiter.
        self.write("skills/x/SKILL.md", "| `write-back data`: the latest summary |\n")
        result = self.run_check({"tokens"})
        self.assertEqual(result.findings, [], result.findings)

    def test_backticked_path_containing_a_token_substring_passes(self) -> None:
        self.write("skills/x/SKILL.md", "Read `rules/definition-of-done-and-writeback-criteria.md`.\n")
        result = self.run_check({"tokens"})
        self.assertEqual(result.findings, [])

    def test_canonical_spelling_passes(self) -> None:
        self.write("skills/x/SKILL.md", "Open the cell with `Must-check`.\n")
        result = self.run_check({"tokens"})
        self.assertEqual(result.findings, [])


class SectionParserTests(Fixture):
    """A fenced example inside a defining section must not truncate it.

    Markdown-about-markdown is this repo's normal mode, so a section that gains a fenced
    example containing a `## ...` line would otherwise make every token below it read as
    missing (review of #21, finding 10).
    """

    def test_fenced_heading_does_not_truncate_the_defining_section(self) -> None:
        standards = self.root / "skills" / "axb-gherkin-and-dsl" / "STANDARDS.md"
        text = standards.read_text()
        text = text.replace(
            "### 5.2 Then Granularity\n",
            "### 5.2 Then Granularity\n\nA fenced example:\n\n```md\n## 9. Not a real heading\n```\n",
            1,
        )
        standards.write_text(text)
        result = self.run_check({"tokens"})
        self.assertEqual(result.findings, [], result.findings)


class SkillReferenceTests(Fixture):
    """Invariant 7 — the #2 escapes: `/plan`, `/plan-with-class-diagram`, `/skill-engineering`."""

    def test_nonexistent_skill_is_caught(self) -> None:
        (self.root / "skills" / "axb-real").mkdir(parents=True)
        self.write("skills/x/SKILL.md", "Proceed to `/plan` when ready.\n")
        result = self.run_check({"names"})
        self.assertEqual(len(result.findings), 1, result.findings)
        self.assertIn("/plan", result.findings[0].message)

    def test_all_three_historically_shipped_escapes_are_caught(self) -> None:
        # #2's actual defect text. None carries the `axb-` prefix, which is exactly why an
        # `axb-`-only pattern passed all three and the check missed its own motivating cases.
        (self.root / "skills" / "axb-real").mkdir(parents=True)
        for name in ("/plan", "/plan-with-class-diagram", "/skill-engineering"):
            self.write("skills/x/SKILL.md", f"Follow up via `{name}`.\n")
            result = self.run_check({"names"})
            self.assertEqual(len(result.findings), 1, (name, result.findings))
            self.assertIn(name, result.findings[0].message)

    def test_http_route_is_not_a_command_reference_when_allowlisted(self) -> None:
        # `FastAPI /ws` is an endpoint, not a skill. The exemption is a line-scoped
        # allowlist entry, not a set in the checker: only the allowlist gets the staleness
        # test, so an in-code exemption would be one nothing keeps honest.
        (self.root / "skills" / "axb-real").mkdir(parents=True)
        self.write("skills/x/SKILL.md", "The client connects to the FastAPI `/ws` endpoint.\n")
        self._write_allowlist(
            {"skill-references": [{"path": "skills/x/SKILL.md", "contains": "`/ws`"}]}
        )
        result = self.run_check({"names"})
        self.assertEqual(result.findings, [], result.findings)

    def test_http_route_without_an_allowlist_entry_is_caught(self) -> None:
        # The same line, unexempted: the guard above must not be a global tolerance for
        # every non-skill token, or the exemption has become a rule.
        (self.root / "skills" / "axb-real").mkdir(parents=True)
        self.write("skills/x/SKILL.md", "The client connects to the FastAPI `/ws` endpoint.\n")
        result = self.run_check({"names"})
        self.assertEqual(len(result.findings), 1, result.findings)
        self.assertIn("/ws", result.findings[0].message)

    def test_real_skill_passes(self) -> None:
        (self.root / "skills" / "axb-real").mkdir(parents=True)
        self.write("skills/x/SKILL.md", "Proceed to `/axb-real` when ready.\n")
        result = self.run_check({"names"})
        self.assertEqual(result.findings, [])

    def test_unbackticked_prose_is_not_a_reference(self) -> None:
        (self.root / "skills" / "axb-real").mkdir(parents=True)
        self.write("skills/x/SKILL.md", "Then run plan as described.\n")
        result = self.run_check({"names"})
        self.assertEqual(result.findings, [])


class SectionReferenceTests(Fixture):
    """Invariant 8 — the #6 finding 2 escape: a section name that does not exist."""

    def test_nonexistent_section_is_caught(self) -> None:
        self.write("skills/x/SKILL.md", "Read the §9.9 section.\n")
        result = self.run_check({"names"})
        self.assertEqual(len(result.findings), 1, result.findings)
        self.assertIn("§9.9", result.findings[0].message)

    def test_real_section_passes(self) -> None:
        self.write("skills/x/SKILL.md", "Read §5.2 for the channels.\n")
        result = self.run_check({"names"})
        self.assertEqual(result.findings, [])

    def test_parent_section_number_passes(self) -> None:
        self.write("skills/x/SKILL.md", "See §4 and §7.\n")
        result = self.run_check({"names"})
        self.assertEqual(result.findings, [])

    def test_licence_section_reference_is_not_a_standards_reference(self) -> None:
        # `Apache-2.0 §4(d)` refers to the licence, not to STANDARDS.md §4.
        self.write("README.md", "Required by Apache-2.0 §4(d), verbatim.\n")
        result = self.run_check({"names"})
        self.assertEqual(result.findings, [], result.findings)


class NormativeRefTests(Fixture):
    """Invariant 5 — #16's normative forward reference. Reports, never fails."""

    def test_issue_reference_is_reported_not_failed(self) -> None:
        self.write("skills/x/rules/r.md", "- Register it in the registry per #12.\n")
        result = self.run_check({"refs"})
        self.assertEqual(result.findings, [], "a candidate must not fail the check")
        self.assertEqual(len(result.candidates), 1, result.candidates)
        self.assertEqual(result.candidates[0].line, 1)
        self.assertEqual(result.candidates[0].path.name, "r.md")

    def test_provenance_reference_is_also_only_a_candidate(self) -> None:
        # The check cannot tell provenance from a load-bearing citation — that is the triage.
        self.write("skills/x/rules/r.md", "- Known gap tracked as #5.\n")
        result = self.run_check({"refs"})
        self.assertEqual(result.findings, [])
        self.assertEqual(len(result.candidates), 1)


class AssertedEnforcementTests(Fixture):
    """Invariant 6 — #20's delivery gate asserted with no check behind it."""

    def test_delivery_claim_is_reported_not_failed(self) -> None:
        self.write("skills/x/rules/r.md", "- An unfilled section cannot reach delivery.\n")
        result = self.run_check({"refs"})
        self.assertEqual(result.findings, [], "the triage is human; the check must not fail")
        self.assertEqual(len(result.candidates), 1, result.candidates)

    def test_ordinary_prose_is_not_a_candidate(self) -> None:
        self.write("skills/x/rules/r.md", "- The plan is delivered to the next phase.\n")
        result = self.run_check({"refs"})
        self.assertEqual(result.candidates, [])


class AllowlistTests(Fixture):
    """The allowlist is data the script reads, and every entry must still be needed."""

    def test_allowlisted_line_is_suppressed(self) -> None:
        self.write("skills/x/rules/r.md", "Never write specs/{{X}}/ anywhere.\n")
        self._write_allowlist({"specs-roots": [{"path": "skills/x/rules/r.md", "contains": "Never write"}]})
        result = self.run_check({"paths"})
        self.assertEqual(result.findings, [])

    def test_allowlist_entry_requires_its_substring(self) -> None:
        self.write("skills/x/rules/r.md", "Actually do write specs/{{X}}/ here.\n")
        self._write_allowlist({"specs-roots": [{"path": "skills/x/rules/r.md", "contains": "Never write"}]})
        result = self.run_check({"paths"})
        self.assertEqual(len(result.findings), 1, result.findings)


def stale_allowlist_entries(root: Path) -> list[str]:
    """Every allowlist entry that no longer matches live text, in every shape it can take.

    Extracted rather than inlined so the scan itself can be tested: an untestable guard is
    how #27 finding 1 happened — the comment claimed this discipline while nothing enforced
    it. `AreTheGuardsThemselvesGuarded` below drives this helper over fixtures that are
    stale on purpose.
    """
    allowlist = checker.load_allowlist(root)
    stale: list[str] = []
    for invariant, entries in allowlist.items():
        if invariant.startswith("$"):
            continue
        for entry in entries:
            path = root / entry["path"]
            if not path.is_file():
                stale.append(f"{invariant}: missing file {entry['path']}")
                continue
            text = path.read_text(encoding="utf-8")
            needle = entry.get("contains")
            if needle is not None and needle not in text:
                stale.append(f"{invariant}: {entry['path']} no longer contains {needle!r}")
            pattern = entry.get("line_matches")
            if pattern is not None and not any(
                re.search(pattern, line) for line in text.splitlines()
            ):
                stale.append(f"{invariant}: {entry['path']} has no line matching {pattern!r}")
    return stale


class RepoAllowlistStillNeededTests(unittest.TestCase):
    """Every entry in the real allowlist must still match something.

    An entry that stops matching is a stale exemption — and a stale exemption silently
    widens what the check tolerates. This is the executable-baseline criterion from #12,
    and since #27 finding 3 it is the *only* exemption mechanism, so it now covers the
    slash-token and licence exemptions too.
    """

    def test_every_allowlist_entry_matches_live_text(self) -> None:
        self.assertEqual(
            stale_allowlist_entries(checker.DEFAULT_ROOT), [], "stale allowlist entries"
        )


class AreTheGuardsThemselvesGuarded(Fixture):
    """The staleness scan must be able to fail, in both entry shapes.

    #27 finding 2 is the general lesson: an exclusion pinned by a test that passes with the
    exclusion deleted is pinned by nothing. The same question applies to this scan, so each
    shape gets a fixture that is stale on purpose and must be named.
    """

    def test_stale_contains_entry_is_reported(self) -> None:
        self.write("skills/x/SKILL.md", "no route mentioned here\n")
        self._write_allowlist(
            {"skill-references": [{"path": "skills/x/SKILL.md", "contains": "`/ws`"}]}
        )
        stale = stale_allowlist_entries(self.root.resolve())
        self.assertEqual(len(stale), 1, stale)
        self.assertIn("/ws", stale[0])

    def test_stale_line_matches_entry_is_reported(self) -> None:
        self.write("skills/x/SKILL.md", "nothing licence-shaped on this line\n")
        self._write_allowlist(
            {"section-references": [{"path": "skills/x/SKILL.md", "line_matches": "Apache-\\d"}]}
        )
        stale = stale_allowlist_entries(self.root.resolve())
        self.assertEqual(len(stale), 1, stale)
        self.assertIn("Apache", stale[0])

    def test_entry_pointing_at_a_missing_file_is_reported(self) -> None:
        self._write_allowlist(
            {"skill-references": [{"path": "skills/gone/SKILL.md", "contains": "`/ws`"}]}
        )
        stale = stale_allowlist_entries(self.root.resolve())
        self.assertEqual(len(stale), 1, stale)
        self.assertIn("missing file", stale[0])

    def test_a_live_entry_is_not_reported(self) -> None:
        # The negative fixture: without it the scan could report everything and pass all
        # three tests above while being useless.
        self.write("skills/x/SKILL.md", "The client connects to the FastAPI `/ws` endpoint.\n")
        self._write_allowlist(
            {"skill-references": [{"path": "skills/x/SKILL.md", "contains": "`/ws`"}]}
        )
        self.assertEqual(stale_allowlist_entries(self.root.resolve()), [])


if __name__ == "__main__":
    unittest.main()
