"""Tests for the Makefile's `check-model` target (#22 shape 14).

Shape 14 is "a generated artifact edited by hand rather than via its source", and the
artifact is `domain-model/aixbdd.modelith.md`, rendered from the sibling `.yaml`. The
target is deliberately OPTIONAL — `modelith` is an external Go binary this repository
declined to depend on — so the interesting cases are not only "does drift fail" but "does
the *absence* of the tool get said out loud".

Two defects in the first version are recorded as tests rather than notes, because both
were invisible to the exit code:

1. **A passing skip.** `MODEL_SOURCE` was defined above `ROOT ?= .` with `:=`, so `ROOT`
   was undefined when it expanded, the path became `/domain-model/…`, and the target
   reported the source as not found and exited 0 — on a tree where the check was possible.
   Hence `test_the_clean_tree_reports_up_to_date` asserts the **positive statement**, not
   the absence of a failure.

2. **Absence simulated by PATH.** The first absent-tool test stripped PATH, which fails on
   a machine with a system-wide install and cannot reproduce absence at all once the
   lookup has run at parse time. `MODELITH` is now `?=` so a caller sets it, and the suite
   constructs absence directly with `MODELITH=`.

Every test scrubs `ROOT`, `MAKEFLAGS` and `MFLAGS` from the environment it passes to
`make`: the suite should construct its world, not inherit the caller's. An exported `ROOT`
redirects a test at an arbitrary directory, and `make -i test` exports `MAKEFLAGS=i` into
the sub-make, which turns every non-zero exit into a zero and defeats the drift assertions.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent
MODELITH = shutil.which("modelith")

# A binary that exists and is executable, so the guard sees "installed" while the fixture
# supplies its own (absent) source tree. Using a real path keeps the test about the source
# branch rather than about the tool.
STAND_IN = "/usr/bin/true"
SCRUB = ("ROOT", "MAKEFLAGS", "MFLAGS")


def scrubbed_env(extra: dict[str, str] | None = None) -> dict[str, str]:
    """The environment `make` is given: the caller's plus `extra`, minus the steering vars.

    The scrub runs **last**, after `extra` is merged, because the point is that these keys
    never reach `make` no matter who set them. An earlier version filtered first and then
    applied `extra`, so the test helper could re-introduce the very variable it exists to
    remove — and the two tests below passed while proving nothing.
    """
    env = dict(os.environ)
    if extra:
        env.update(extra)
    return {k: v for k, v in env.items() if k not in SCRUB}


def run_make(
    *args: str,
    root: Path | None = None,
    modelith: str | None = None,
    extra_env: dict[str, str] | None = None,
):
    command = ["make", *args]
    if root is not None:
        command.append(f"ROOT={root}")
    if modelith is not None:
        command.append(f"MODELITH={modelith}")
    return subprocess.run(
        command,
        cwd=DEFAULT_ROOT,
        capture_output=True,
        text=True,
        env=scrubbed_env(extra_env),
    )


def copy_model(target: Path, suffixes: tuple[str, ...] = (".md", ".yaml")) -> Path:
    models = target / "domain-model"
    models.mkdir(parents=True)
    for suffix in suffixes:
        shutil.copy(DEFAULT_ROOT / f"domain-model/aixbdd.modelith{suffix}", models)
    return models


class AbsentToolTests(unittest.TestCase):
    """Optional must mean loud, not silent — and absence must be constructible."""

    def test_missing_modelith_is_reported_and_does_not_fail(self) -> None:
        result = run_make("check-model", modelith="")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("NOT CHECKED", result.stdout)
        self.assertIn("modelith is not installed", result.stdout)
        # And it must not pretend to have verified anything.
        self.assertNotIn("up to date", result.stdout)

    def test_missing_source_with_no_orphan_is_reported(self) -> None:
        """Nothing exists to check: a skip, not a failure — and said out loud.

        This test is the one that used to fail on a modelith-less machine: it did not
        strip PATH, so the *first* branch fired and it asserted text only the *second*
        prints. Setting MODELITH explicitly makes the branch under test independent of
        the machine.
        """
        with tempfile.TemporaryDirectory() as tmp:
            result = run_make("check-model", root=Path(tmp), modelith=STAND_IN)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("NOT CHECKED", result.stdout)
        self.assertIn("nothing to render-check", result.stdout)

    def test_an_orphaned_generated_file_fails(self) -> None:
        """The generated `.md` with no source is shape 14 in its worse direction.

        Losing the source is more alarming than drifting from it: the artifact is now
        maintained only by hand, which is exactly what this gate exists to prevent. The
        first version printed NOT CHECKED and exited 0 here.
        """
        with tempfile.TemporaryDirectory() as tmp:
            copy_model(Path(tmp), suffixes=(".md",))
            result = run_make("check-model", root=Path(tmp), modelith=STAND_IN)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("exists but its source", result.stdout + result.stderr)


@unittest.skipUnless(MODELITH is not None, "modelith not installed")
class DriftDetectionTests(unittest.TestCase):
    """With the tool present, the check must actually check."""

    def test_the_clean_tree_reports_up_to_date(self) -> None:
        """The regression test for the empty-ROOT bug.

        With `ROOT` unassigned the target printed `NOT CHECKED … not found` and exited 0
        — indistinguishable from success to any caller reading only the exit code. So this
        asserts the positive statement, not merely the absence of a failure.
        """
        result = run_make("check-model")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("up to date", result.stdout)
        self.assertNotIn("NOT CHECKED", result.stdout)

    def test_a_hand_edited_generated_file_fails(self) -> None:
        """Shape 14 itself, in a snapshot so the working tree is never touched.

        This also proves the target honours `ROOT` rather than reading the worktree path,
        which matters because the pre-commit hook points `ROOT` at a snapshot of the
        *index*: a target that read the worktree would pass a stale staged `.md` while the
        working copy was clean — the defect #25/#26 fixed for the other checks. The real
        worktree is clean here, so a worktree read would pass and this test would fail.

        (An earlier version asserted that property in its own test; it was the same
        fixture with one assertion removed, so it is folded in here instead of duplicated.)
        """
        with tempfile.TemporaryDirectory() as tmp:
            snapshot = Path(tmp)
            models = copy_model(snapshot)
            self.assertEqual(run_make("check-model", root=snapshot).returncode, 0)

            generated = models / "aixbdd.modelith.md"
            generated.write_text(generated.read_text() + "\n<!-- hand edit -->\n")

            result = run_make("check-model", root=snapshot)
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("out of date", result.stdout + result.stderr)

    def test_a_modelith_outside_PATH_is_used_by_its_resolved_path(self) -> None:
        """The guard resolves a path; the recipe must *use* that path.

        Invoking bare `modelith` looks the name up a second time. When the two lookups can
        disagree — an environment-supplied `MODELITH`, or a PATH that differs between make's
        parse and the recipe's shell — the guard reports "installed" and the recipe exits
        127 with no `NOT CHECKED` line. One identity decision, used everywhere (#26's
        classifier lesson).

        This also pins `MODELITH ?=`: an *environment* value is honoured, which `:=` would
        overwrite. (A command-line value would win either way, so a command-line-only test
        cannot tell the two apart — the first version of this suite could not.)
        """
        stripped = "/usr/bin:/bin"
        if shutil.which("modelith", path=stripped) is not None:
            self.skipTest("modelith is installed on the stripped PATH; cannot split the lookups")

        result = run_make(
            "check-model",
            extra_env={"MODELITH": str(MODELITH), "PATH": stripped},
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("up to date", result.stdout)

    def test_an_ambient_ROOT_does_not_redirect_the_clean_tree(self) -> None:
        """An exported `ROOT` must not reach the sub-make.

        `ROOT ?= .` yields to the environment, so a caller's export silently retargets
        every assertion in this file. The scrub is what prevents it, and the round trip
        through `scrubbed_env` is asserted here because a test that builds a dirty dict
        and never passes it proves nothing — which is what this test replaced.
        """
        self.assertNotIn("ROOT", scrubbed_env({"ROOT": "/nowhere"}))
        result = run_make("check-model", extra_env={"ROOT": "/nonexistent-root"})
        self.assertIn("up to date", result.stdout)
        self.assertNotIn("nonexistent-root", result.stdout)

    def test_makeflags_cannot_make_drift_pass(self) -> None:
        """`make -i test` exports MAKEFLAGS=i; the sub-make must not inherit it.

        Without the scrub, `make check-model` ignores its own non-zero exit, so the drift
        assertion below would read a real failure as a pass — a test reporting success
        while the thing under test failed.
        """
        self.assertNotIn("MAKEFLAGS", scrubbed_env())
        self.assertNotIn("MFLAGS", scrubbed_env())
        with tempfile.TemporaryDirectory() as tmp:
            snapshot = Path(tmp)
            models = copy_model(snapshot)
            generated = models / "aixbdd.modelith.md"
            generated.write_text(generated.read_text() + "\n<!-- hand edit -->\n")

            result = run_make(
                "check-model", root=snapshot, extra_env={"MAKEFLAGS": "-i"}
            )
        # Scrubbed, so the drift still fails as it must.
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)


class GateCompositionTests(unittest.TestCase):
    """`check-model` earns its place only if `make check` runs it."""

    def test_check_target_includes_the_model_check(self) -> None:
        # `make -n` prints each recipe expanded, so the assertion is on the command that
        # proves the check ran — not the target's name, which a dry run never prints.
        result = run_make("-n", "check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("render --check", result.stdout)

    def test_the_target_is_documented_in_help(self) -> None:
        result = run_make("help")
        self.assertIn("check-model", result.stdout)

    def test_help_does_not_hand_maintain_a_suite_inventory(self) -> None:
        """`make help` described `test` by listing suites, and the list went stale.

        The fix is to stop enumerating rather than to update the list: a hand-maintained
        inventory of the files `make test` discovers is a second place to drift, which is
        the failure the README already records for the plan-package placeholder.
        """
        result = run_make("help")
        self.assertIn("test", result.stdout)
        for stale in ("hook lifecycle", "invariants, params"):
            self.assertNotIn(stale, result.stdout)


if __name__ == "__main__":
    unittest.main()
