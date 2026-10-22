"""Lifecycle tests for the pre-commit hook.

These exist because #25's defect shipped past a hand-written transcript: the transcript
walked the happy path, and the defect was a branch switch. #26's review then found three
more defects on paths a transcript does not walk — a moved clone, a missing stub, a
pre-hook branch. So the scenarios are encoded here rather than narrated in a PR body.

Each test builds a throwaway repository, so nothing depends on the developer's checkout.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# What a scratch repo needs for `make check` to run meaningfully.
COPY = ("Makefile", "README.md", "scripts", "skills")


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


class HookLifecycle(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        # resolve() matters: on macOS /tmp is a symlink to /private/tmp, and one of the
        # findings is precisely that logical-vs-physical paths break a path-based identity
        # test. Tests must exercise the physical form to be representative.
        self.root = Path(self._tmp.name).resolve() / "repo"
        self.root.mkdir()
        for name in COPY:
            src = REPO / name
            dst = self.root / name
            if src.is_dir():
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
            else:
                shutil.copy2(src, dst)
        shutil.rmtree(self.root / "scripts" / "__pycache__", ignore_errors=True)

        self.git("init", "-q")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "T")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base", "--no-verify")

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)
        self._tmp.cleanup()

    # -- helpers -------------------------------------------------------------------
    def git(self, *args: str) -> subprocess.CompletedProcess:
        return run(["git", *args], self.root)

    def make(self, *args: str) -> subprocess.CompletedProcess:
        return run(["make", "-s", *args], self.root)

    @property
    def hook(self) -> Path:
        return self.root / ".git" / "hooks" / "pre-commit"

    def plant_violation(self) -> None:
        readme = self.root / "README.md"
        readme.write_text(readme.read_text() + "\nSee `specs/{{BAD}}/`.\n")

    def commit(self, message: str, *extra: str) -> subprocess.CompletedProcess:
        self.git("add", "-A")
        return self.git("commit", "-q", "-m", message, *extra)

    # -- scenarios -----------------------------------------------------------------
    def test_install_creates_a_managed_file_not_a_symlink(self) -> None:
        result = self.make("install-hooks")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.hook.is_symlink(), "the installed hook must not be a symlink")
        self.assertIn("# aixbdd-en-managed-hook", self.hook.read_text())

    def test_clean_commit_is_allowed(self) -> None:
        self.make("install-hooks")
        readme = self.root / "README.md"
        readme.write_text(readme.read_text() + "\nA harmless line.\n")
        result = self.commit("clean change")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_staged_violation_is_blocked_and_named(self) -> None:
        self.make("install-hooks")
        self.plant_violation()
        result = self.commit("violation")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("specs-roots", result.stderr)

    def test_partial_stage_is_blocked_on_the_index_not_the_worktree(self) -> None:
        self.make("install-hooks")
        readme = self.root / "README.md"
        readme.write_text(readme.read_text() + "\nAlso `specs/{{BAD2}}/`.\n")
        self.git("add", "README.md")
        # Fix it on disk only; the index still carries the violation.
        readme.write_text(readme.read_text().replace("specs/{{BAD2}}/", "specs/plans/BAD2/"))
        result = self.git("commit", "-q", "-m", "partial stage")
        self.assertNotEqual(result.returncode, 0, "the gate must judge the staged index")
        self.assertIn("specs-roots", result.stderr)

    def test_branch_without_the_gate_script_fails_closed(self) -> None:
        self.make("install-hooks")
        # A branch predating the gate script: the tracked file is removed and committed.
        self.git("checkout", "-q", "-b", "pre-hook")
        shutil.rmtree(self.root / "scripts" / "hooks")
        result = self.commit("strip hooks")
        # The gate cannot run, so the commit must be refused rather than silently allowed.
        self.assertNotEqual(result.returncode, 0, "a missing gate script must fail closed")
        self.assertIn("GATE DID NOT RUN", result.stderr)

    def test_fail_closed_message_names_a_remedy_that_can_help(self) -> None:
        # Finding 2: the message used to say "rerun make install-hooks", which cannot help
        # because the stub is already installed and branch-independent.
        self.make("install-hooks")
        self.git("checkout", "-q", "-b", "pre-hook")
        shutil.rmtree(self.root / "scripts" / "hooks")
        result = self.commit("strip hooks")
        self.assertNotIn("Rerun `make install-hooks`", result.stderr)
        self.assertTrue(
            "--no-verify" in result.stderr or "rebase" in result.stderr.lower(),
            result.stderr,
        )

    def test_upgrade_from_legacy_symlink_survives_a_moved_clone(self) -> None:
        # Finding 1: the legacy-symlink upgrade compared absolute paths, so a moved or
        # renamed clone misclassified its OWN symlink as foreign and refused to upgrade.
        hooks = self.root / ".git" / "hooks"
        hooks.mkdir(parents=True, exist_ok=True)
        stale = "/somewhere/else/entirely/scripts/hooks/pre-commit"
        self.hook.symlink_to(stale)
        result = self.make("install-hooks")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.hook.is_symlink(), "the legacy symlink should have been replaced")

    def test_upgrade_failure_leaves_the_old_hook_intact(self) -> None:
        # Finding 3: rm-then-cp could leave NO hook when the copy failed. The realistic
        # version of that failure is a branch carrying the new Makefile but not the new
        # stub file, so simulate exactly that.
        self.make("install-hooks")
        before = self.hook.read_text()
        stub = self.root / "scripts" / "hooks" / "pre-commit-stub"
        saved = stub.read_text()
        stub.unlink()
        try:
            result = self.make("install-hooks")
        finally:
            stub.write_text(saved)
            stub.chmod(0o755)
        self.assertNotEqual(result.returncode, 0, "install must fail when the stub is missing")
        self.assertTrue(self.hook.exists(), "a failed install must not remove the working hook")
        self.assertEqual(self.hook.read_text(), before)

    def test_stale_installed_stub_is_reported(self) -> None:
        # Finding 6: the installed stub is a frozen copy, so an older one would silently
        # stay behind. The gate script compares versions and says so.
        self.make("install-hooks")
        self.hook.write_text(self.hook.read_text().replace("v2", "v1"))
        readme = self.root / "README.md"
        readme.write_text(readme.read_text() + "\nHarmless.\n")
        result = self.commit("after stale stub")
        self.assertIn("installed hook stub is version 1", result.stderr)

    def test_uninstall_removes_only_its_own_hook(self) -> None:
        self.make("install-hooks")
        result = self.make("uninstall-hooks")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.hook.exists())

    def test_foreign_hook_is_refused_then_preserved(self) -> None:
        hooks = self.root / ".git" / "hooks"
        hooks.mkdir(parents=True, exist_ok=True)
        self.hook.write_text("#!/bin/sh\nexit 0\n")
        self.hook.chmod(0o755)
        install = self.make("install-hooks")
        self.assertNotEqual(install.returncode, 0, "install must refuse a foreign hook")
        self.assertIn("refusing", install.stderr)
        uninstall = self.make("uninstall-hooks")
        self.assertEqual(uninstall.returncode, 0, uninstall.stderr)
        self.assertTrue(self.hook.exists(), "uninstall must leave a foreign hook alone")

    def test_install_is_idempotent(self) -> None:
        self.assertEqual(self.make("install-hooks").returncode, 0)
        second = self.make("install-hooks")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertTrue(self.hook.exists())

    def test_no_verify_bypasses_deliberately(self) -> None:
        self.make("install-hooks")
        self.plant_violation()
        result = self.commit("bypassed", "--no-verify")
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
