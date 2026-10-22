"""Tests for scripts/check_invariants.py.

Each invariant is proven against **its own historical escape** — the defect from the PR
that motivated it — not merely against a clean tree. A check that only passes on a clean
tree has not been shown to catch anything (issue #12, acceptance criteria).

Constructed trees live in a temporary root; the checker takes `--root`, so a fixture is a
small repository carrying its own registry and allowlist.
"""

from __future__ import annotations

import json
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


class TokenRegistryTests(Fixture):
    """Invariant 4 — #15's registration failures and #16's variant drift."""

    def test_token_missing_from_its_section_is_caught(self) -> None:
        data = json.loads(json.dumps(MINIMAL_REGISTRY))
        data["tokens"].append({"token": "Stdout", "section": "5.2 Then Granularity", "kind": "then-channel"})
        self._write_registry(data)
        result = self.run_check({"tokens"})
        self.assertEqual(len(result.findings), 1, result.findings)
        self.assertIn("Stdout", result.findings[0].message)

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

    def test_ordinary_prose_is_not_a_token_reference(self) -> None:
        # Unbackticked prose is English, not a token naming.
        self.write("skills/x/SKILL.md", "The authoritative state must land in the store.\n")
        result = self.run_check({"tokens"})
        self.assertEqual(result.findings, [])

    def test_backticked_path_containing_a_token_substring_passes(self) -> None:
        self.write("skills/x/SKILL.md", "Read `rules/definition-of-done-and-writeback-criteria.md`.\n")
        result = self.run_check({"tokens"})
        self.assertEqual(result.findings, [])

    def test_canonical_spelling_passes(self) -> None:
        self.write("skills/x/SKILL.md", "Open the cell with `Must-check`.\n")
        result = self.run_check({"tokens"})
        self.assertEqual(result.findings, [])


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


class RepoAllowlistStillNeededTests(unittest.TestCase):
    """Every entry in the real allowlist must still match something.

    An entry that stops matching is a stale exemption — and a stale exemption silently
    widens what the check tolerates. This is the executable-baseline criterion from #12.
    """

    def test_every_allowlist_entry_matches_live_text(self) -> None:
        root = checker.DEFAULT_ROOT
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
                needle = entry.get("contains")
                if needle is not None and needle not in path.read_text(encoding="utf-8"):
                    stale.append(f"{invariant}: {entry['path']} no longer contains {needle!r}")
        self.assertEqual(stale, [], "stale allowlist entries")


if __name__ == "__main__":
    unittest.main()
