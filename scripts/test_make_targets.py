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

Every test scrubs the variables that steer `make`: `ROOT` (which `ROOT ?= .` yields to),
`MODELITH` (the override this suite itself relies on), and `MAKEFLAGS`/`MFLAGS` (which
`make -i test` exports, turning every non-zero exit into a zero and defeating the drift
assertions). The suite should construct its world, not inherit the caller's.

The scrub list is **derived** from one table, `INTERFACE_VARS`, that also builds the
command line, and a test asserts that every `run_make` knob appears in it. That is not
tidiness: the first version kept the two lists apart and shipped without `MODELITH` in the
scrub, so an exported `MODELITH=` broke four tests and a stale `MODELITH=/path` silently
redirected them. A variable the design invites you to export in a shell profile is the
likelier leak, not the unlikelier one — so ambient-leak coverage is a property of the
mechanism here, rather than a per-variable memory.
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

# **Every variable `run_make` treats as an interface must be in the scrub list.** One table
# drives both the command line and the scrub, so a new knob cannot be added without being
# scrubbed — the previous version kept the two in separate places and shipped with
# `MODELITH` missing, which meant an exported `MODELITH=` broke four detection-dependent
# tests and a stale path silently redirected them.
INTERFACE_VARS = {"root": "ROOT", "modelith": "MODELITH"}
# Not make variables: `extra_env` is how a test injects variables, so it is the injection
# channel rather than a knob, and it is exactly what the scrub filters.
NOT_KNOBS = frozenset({"extra_env"})
# Not ours: make itself reads these. `MAKEFLAGS=i` (from `make -i`) makes the sub-make
# ignore its own non-zero exit, defeating every drift assertion.
MAKE_VARS = ("MAKEFLAGS", "MFLAGS")
SCRUB = frozenset(INTERFACE_VARS.values()) | frozenset(MAKE_VARS)


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
    knobs = {"root": root, "modelith": modelith}
    command = ["make", *args]
    # Driven by INTERFACE_VARS, so the command line and the scrub cannot disagree about
    # which knobs exist. `None` means "not set", and an empty string is meaningful
    # (`MODELITH=` is how a test constructs absence), which is why the test is `is not None`.
    for kwarg, value in knobs.items():
        if value is not None:
            command.append(f"{INTERFACE_VARS[kwarg]}={value}")
    return subprocess.run(
        command,
        cwd=DEFAULT_ROOT,
        capture_output=True,
        text=True,
        env=scrubbed_env(extra_env),
    )


def run_make_with_environment(args: list[str], environment: dict[str, str]):
    """Run make with an environment supplied verbatim — the scrub deliberately lifted.

    The suite scrubs `MODELITH`, so **no test going through `run_make` can observe make's
    own handling of an exported `MODELITH`**. One property still needs exactly that: an
    *environment* value must be honoured, which `:=` would overwrite and `?=` keeps. This
    helper is the single named place the scrub is lifted, and it is deliberately not a
    `run_make` knob — an escape hatch there would have made the knob guard carry an
    exception, and an exception in the guard is where the next leak lives.
    """
    return subprocess.run(
        ["make", *args],
        cwd=DEFAULT_ROOT,
        capture_output=True,
        text=True,
        env=environment,
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
        cannot tell the two apart — the first version of this suite could not.) Because the
        suite scrubs `MODELITH`, this is the one test that supplies its environment
        verbatim, via the named helper above.
        """
        stripped = "/usr/bin:/bin"
        if shutil.which("modelith", path=stripped) is not None:
            self.skipTest("modelith is installed on the stripped PATH; cannot split the lookups")

        environment = {k: v for k, v in os.environ.items() if k not in MAKE_VARS}
        environment["PATH"] = stripped
        environment["MODELITH"] = str(MODELITH)

        result = run_make_with_environment(["check-model"], environment)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("up to date", result.stdout)

class AmbientEnvironmentTests(unittest.TestCase):
    """The scrub list is a property of the mechanism, not per-variable memory.

    Added after the review of #29 exported `MODELITH=` and broke four tests: the fix for
    the absent-tool suite *minted* an override variable and did not add it to the scrub.
    `MODELITH` is the likelier leak, not the unlikelier one — the target's own design
    invites `export MODELITH=/path/to/tool` in a shell profile, and then a stale or empty
    value silently redirects (a path) or breaks (an empty string) every
    detection-dependent test, which are exactly the two directions ambient `ROOT` already
    had.
    """

    def test_every_run_make_knob_is_scrubbed(self) -> None:
        """The structural guard: a new knob cannot be added without being scrubbed.

        `run_make`'s keyword parameters *are* the knobs. Each must appear in
        `INTERFACE_VARS`, which is the single table feeding both the command line and the
        scrub, so this fails the moment someone adds a parameter and forgets the list.
        """
        import inspect

        knobs = {
            name
            for name, parameter in inspect.signature(run_make).parameters.items()
            if parameter.kind is inspect.Parameter.KEYWORD_ONLY
            and name not in NOT_KNOBS
        }
        self.assertEqual(
            knobs,
            set(INTERFACE_VARS),
            "run_make grew or lost a knob; add it to INTERFACE_VARS so it is scrubbed too",
        )
        for variable in INTERFACE_VARS.values():
            self.assertIn(variable, SCRUB, f"{variable} is an interface but is not scrubbed")
        for variable in MAKE_VARS:
            self.assertIn(variable, SCRUB)

    def test_an_exported_modelith_is_scrubbed(self) -> None:
        """The probe that found the residual, as a test.

        Both directions matter: an empty export breaks detection-dependent tests, and a
        stale *path* silently redirects them — so the assertion is on the scrub, not on one
        symptom.
        """
        self.assertNotIn("MODELITH", scrubbed_env({"MODELITH": ""}))
        self.assertNotIn("MODELITH", scrubbed_env({"MODELITH": "/nonexistent/modelith"}))

    def test_an_exported_modelith_does_not_reach_the_clean_tree_run(self) -> None:
        """End to end: the export must not change what the clean-tree run reports.

        A pure scrub assertion could pass while `run_make` bypassed the helper, so this
        checks the observable outcome too. It needs the tool, hence the skip.
        """
        if MODELITH is None:
            self.skipTest("modelith not installed")
        result = run_make(
            "check-model",
            extra_env={"MODELITH": "/nonexistent/modelith"},
        )
        self.assertIn("up to date", result.stdout)
        self.assertNotIn("No such file", result.stdout + result.stderr)


class AmbientSteeringTests(unittest.TestCase):
    """The behavioural half of the scrub: dirty environments a caller can really create.

    These need `modelith`, because each asserts that the *real* check ran despite the
    environment. The pure scrub assertions live in `AmbientEnvironmentTests`, which needs
    nothing — so the mechanism is still covered on a host without the tool.
    """

    def setUp(self) -> None:
        if MODELITH is None:
            self.skipTest("modelith not installed")

    def test_an_ambient_ROOT_does_not_redirect_the_clean_tree(self) -> None:
        """An exported `ROOT` must not reach the sub-make.

        `ROOT ?= .` yields to the environment, so a caller's export silently retargets
        every assertion in this file. The round trip through `scrubbed_env` is asserted
        here because a test that builds a dirty dict and never passes it proves nothing.
        """
        self.assertNotIn("ROOT", scrubbed_env({"ROOT": "/nowhere"}))
        result = run_make("check-model", extra_env={"ROOT": "/nonexistent-root"})
        self.assertIn("up to date", result.stdout)
        self.assertNotIn("nonexistent-root", result.stdout)

    def test_makeflags_cannot_make_drift_pass(self) -> None:
        """`make -i test` exports MAKEFLAGS=i; the sub-make must not inherit it.

        Without the scrub, `make check-model` ignores its own non-zero exit, so a drift
        assertion reads a real failure as a pass — a test reporting success while the thing
        under test failed.
        """
        self.assertNotIn("MAKEFLAGS", scrubbed_env())
        self.assertNotIn("MFLAGS", scrubbed_env())
        with tempfile.TemporaryDirectory() as tmp:
            snapshot = Path(tmp)
            models = copy_model(snapshot)
            generated = models / "aixbdd.modelith.md"
            generated.write_text(generated.read_text() + "\n<!-- hand edit -->\n")

            result = run_make("check-model", root=snapshot, extra_env={"MAKEFLAGS": "-i"})
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
