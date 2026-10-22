"""Tests for the Makefile's `check-model` target (#22 shape 14).

Shape 14 is "a generated artifact edited by hand rather than via its source", and the
artifact is `domain-model/aixbdd.modelith.md`, rendered from the sibling `.yaml`. The
target is deliberately OPTIONAL — `modelith` is an external Go binary this repository
declined to depend on — so the interesting cases are not only "does drift fail" but
"does the *absence* of the tool get said out loud".

That second case is why this file exists at all. The first version of the target used a
`:=` assignment for the model source, so `ROOT` had not been assigned yet, the path
expanded to `/domain-model/aixbdd.modelith.yaml`, and the target reported the source as
not found — a passing `NOT CHECKED` on a tree where the check was perfectly possible.
Read as a verdict it said "fine"; read as output it said "nothing was verified". That is
the exact failure the target's own design is meant to prevent, which is why it is now a
test rather than a note.

These tests shell out to `make` because the thing under test is a Makefile target. They
skip — visibly — when `modelith` is not installed, rather than asserting a behaviour the
machine cannot exhibit.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent
MODELITH = shutil.which("modelith")

# A PATH that keeps `make` and `sh` but cannot see `modelith`. Used to prove the optional
# check is loud rather than silent when the tool is missing.
STRIPPED_PATH = "/usr/bin:/bin"


def run_make(*args: str, env_path: str | None = None, root: Path | None = None):
    command = ["make", *args]
    if root is not None:
        command.append(f"ROOT={root}")
    env = dict(os.environ)
    if env_path is not None:
        env["PATH"] = env_path
    return subprocess.run(
        command, cwd=DEFAULT_ROOT, capture_output=True, text=True, env=env
    )


class AbsentToolTests(unittest.TestCase):
    """Optional must mean loud, not silent."""

    def test_missing_modelith_is_reported_and_does_not_fail(self) -> None:
        if not Path("/usr/bin/make").exists():
            self.skipTest("no /usr/bin/make to run under the stripped PATH")
        result = run_make("check-model", env_path=STRIPPED_PATH)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("NOT CHECKED", result.stdout)
        self.assertIn("modelith is not installed", result.stdout)
        # And it must not pretend to have verified anything.
        self.assertNotIn("up to date", result.stdout)

    def test_a_missing_source_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_make("check-model", root=Path(tmp))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("NOT CHECKED", result.stdout)
        self.assertIn("not found", result.stdout)


@unittest.skipUnless(MODELITH is not None, "modelith not installed")
class DriftDetectionTests(unittest.TestCase):
    """With the tool present, the check must actually check."""

    def test_the_clean_tree_reports_up_to_date(self) -> None:
        """The regression test for the empty-ROOT bug.

        With `ROOT` unassigned the target printed `NOT CHECKED ... not found` and exited
        0 — indistinguishable from success to any caller reading only the exit code. So
        this asserts the positive statement, not merely the absence of a failure.
        """
        result = run_make("check-model")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("up to date", result.stdout)
        self.assertNotIn("NOT CHECKED", result.stdout)

    def test_a_hand_edited_generated_file_fails(self) -> None:
        """Shape 14 itself, in a snapshot so the working tree is never touched."""
        with tempfile.TemporaryDirectory() as tmp:
            snapshot = Path(tmp)
            models = snapshot / "domain-model"
            models.mkdir()
            for suffix in (".md", ".yaml"):
                shutil.copy(DEFAULT_ROOT / f"domain-model/aixbdd.modelith{suffix}", models)
            self.assertEqual(run_make("check-model", root=snapshot).returncode, 0)

            generated = models / "aixbdd.modelith.md"
            generated.write_text(generated.read_text() + "\n<!-- hand edit -->\n")

            result = run_make("check-model", root=snapshot)
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("out of date", result.stdout + result.stderr)

    def test_the_check_follows_root_not_the_worktree(self) -> None:
        """The pre-commit hook points ROOT at an index snapshot.

        If the target read the worktree path instead, a stale staged `.md` would pass
        while the working copy was clean — the defect #25/#26 fixed for the other checks.
        """
        with tempfile.TemporaryDirectory() as tmp:
            snapshot = Path(tmp)
            models = snapshot / "domain-model"
            models.mkdir()
            for suffix in (".md", ".yaml"):
                shutil.copy(DEFAULT_ROOT / f"domain-model/aixbdd.modelith{suffix}", models)
            generated = models / "aixbdd.modelith.md"
            generated.write_text(generated.read_text() + "\n<!-- staged-only edit -->\n")

            result = run_make("check-model", root=snapshot)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)


class GateCompositionTests(unittest.TestCase):
    """`check-model` earns its place only if `make check` runs it."""

    def test_check_target_includes_the_model_check(self) -> None:
        # `make -n` prints each recipe expanded, so the assertion is on the *command* that
        # proves the check ran — not on the target's name, which a dry run never prints.
        # Asserting the name was the first version of this test and it failed for that
        # reason alone, which is its own small lesson: assert the property, not the label.
        result = run_make("-n", "check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("modelith render --check", result.stdout)

    def test_the_target_is_documented_in_help(self) -> None:
        result = run_make("help")
        self.assertIn("check-model", result.stdout)


if __name__ == "__main__":
    unittest.main()
