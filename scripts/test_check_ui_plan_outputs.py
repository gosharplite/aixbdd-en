"""Tests for scripts/check_ui_plan_outputs.py.

Two layers, and the second is the one that matters most:

1. **Defect text first.** Fixtures are written from #24 item 3's sentence — "a reference to
   a frame or page the plan does not declare" — and from the review of #28, not from this
   checker's code. #24 records that writing them from the code is how the first two
   attempts passed all three of their motivating escapes.

2. **Structure second.** The rewrite's two claims are structural, so they get structural
   tests: *fenced content is never scanned* and *checked + prose == seen*. Those are
   asserted as properties over the shipped tree and over fixtures, so a future scanner that
   drops an item fails a test rather than passing the gate quietly.

Both historical instances (#14) were a plan body contradicting its own `Planned output
files:` line, so that is what the first group reproduces.
"""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_ui_plan_outputs as plan_outputs  # noqa: E402

TERMINAL_PLAN = """# Terminal / TUI & Frame Prototype Planning

## Screens & Flows

### 1. `Startup / Edit Frame`

- Corresponding frame file: `ui/screens/entry.txt`

### 2. `Live Suggestion Frame`

- Corresponding frame file: `ui/screens/10-suggestion.txt`

## Keybinding Map

| Key | Action | Target Frame | Expected Result |
| --- | --- | --- | --- |
| `Enter` | Submit current input | `entry` | history adds one |
| `Tab` | Accept current suggestion | {accept_target} | editor inserts suggestion text |

## State Transition List

1. `entry` --type text--> {first_target} (list recomputed)
2. `entry` --`Enter`--> `running` (show running status)

## Prototype Output Planning

- Planned output files: {declared}
"""

HTML_PLAN = """# Frontend / UI & Static Prototype Planning

## Screens & Flows

### 1. `Product Listing Entry Screen`

- Corresponding prototype file: {corresponding}

## Static Prototype Output Planning

- Multi-page entry: `fixedly use ui/index.html as the prototype entry page.`
- Planned output files: `ui/index.html`, `ui/product-detail.html`
"""

CONFORMING_DECLARATION = (
    "`ui/screens/entry.txt`, `ui/screens/10-suggestion.txt`, `ui/screens/20-running.txt`"
)


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.templates = self.root / "skills/axb-ui-plan/templates"
        self.templates.mkdir(parents=True)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, name: str, text: str) -> Path:
        path = self.templates / name
        path.write_text(text, encoding="utf-8")
        return path

    def terminal_plan(self, accept_target: str, first_target: str, declared: str) -> Path:
        return self.write(
            "ui-plan.terminal.example.md",
            TERMINAL_PLAN.format(
                accept_target=accept_target, first_target=first_target, declared=declared
            ),
        )

    def run_check(self):
        return plan_outputs.run(self.root.resolve())

    def run_main(self) -> tuple[int, str]:
        """Run `main()` end to end, because the vacuity guard lives there and not in run()."""
        buffer = io.StringIO()
        argv = ["check_ui_plan_outputs.py", "--root", str(self.root)]
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(buffer):
            code = plan_outputs.main()
        return code, buffer.getvalue()


class KeybindingColumnTests(Fixture):
    """A `Target Frame` naming a frame the plan never declares."""

    def test_undeclared_keybinding_target_is_caught(self) -> None:
        self.terminal_plan("`40-history`", "`10-suggestion`", CONFORMING_DECLARATION)
        violations = self.run_check().violations
        self.assertEqual([v.reference for v in violations], ["40-history"], violations)

    def test_declared_keybinding_target_passes(self) -> None:
        self.terminal_plan("`10-suggestion`", "`10-suggestion`", CONFORMING_DECLARATION)
        self.assertEqual(self.run_check().violations, [])

    def test_ordered_prefix_is_optional_in_a_reference(self) -> None:
        # `suggestion` and `10-suggestion.txt` name the same frame; the prefix is ordering.
        self.terminal_plan("`suggestion`", "`suggestion`", CONFORMING_DECLARATION)
        self.assertEqual(self.run_check().violations, [])

    def test_a_different_order_prefix_is_still_a_different_file(self) -> None:
        # Only the *omission* is optional. A reference that states a prefix must state the
        # right one: renumbering is the edit a ui plan actually undergoes, and
        # `20-suggestion` names a different file from `10-suggestion.txt`.
        self.terminal_plan("`20-suggestion`", "`10-suggestion`", CONFORMING_DECLARATION)
        self.assertEqual(
            [v.reference for v in self.run_check().violations], ["20-suggestion"]
        )

    def test_a_different_extension_is_still_a_different_file(self) -> None:
        # Same stem, `.html` vs the declared `.txt`: discarding extensions on both sides
        # (the first version of `is_declared`) made these one file.
        self.terminal_plan("`suggestion.html`", "`10-suggestion`", CONFORMING_DECLARATION)
        self.assertEqual(
            [v.reference for v in self.run_check().violations], ["suggestion.html"]
        )


class StateTransitionTests(Fixture):
    """A transition endpoint naming a frame the plan never declares."""

    def test_undeclared_transition_endpoint_is_caught(self) -> None:
        self.terminal_plan("`entry`", "`history`", CONFORMING_DECLARATION)
        violations = self.run_check().violations
        self.assertIn("history", [v.reference for v in violations], violations)

    def test_declared_transition_endpoints_pass(self) -> None:
        self.terminal_plan("`entry`", "`10-suggestion`", CONFORMING_DECLARATION)
        self.assertEqual(self.run_check().violations, [])

    def test_the_arrow_key_is_not_read_as_a_frame(self) -> None:
        # `--`Esc`-->` : the key sits in the arrow, between hyphens. Reading it as a frame
        # would make every conforming plan fail on `Esc`.
        self.write(
            "ui-plan.terminal.example.md",
            "## State Transition List\n\n"
            "1. `entry` --`Esc`--> `10-suggestion` --`Tab`--> `entry`\n\n"
            "## Prototype Output Planning\n\n"
            f"- Planned output files: {CONFORMING_DECLARATION}\n",
        )
        report = self.run_check()
        self.assertEqual(report.violations, [])
        self.assertEqual(report.checked, 3)


class LabelledScreenLineTests(Fixture):
    """A screen section pointing at a page the plan never declares."""

    def test_undeclared_prototype_file_is_caught(self) -> None:
        self.write("ui-plan.example.md", HTML_PLAN.format(corresponding="`ui/account.html`"))
        violations = self.run_check().violations
        self.assertEqual([v.reference for v in violations], ["ui/account.html"], violations)

    def test_declared_prototype_file_passes(self) -> None:
        self.write(
            "ui-plan.example.md", HTML_PLAN.format(corresponding="`ui/product-detail.html`")
        )
        self.assertEqual(self.run_check().violations, [])

    def test_a_path_is_not_matched_by_its_stem(self) -> None:
        # A bare name resolves by stem; a path must be exact, or `ui/screens/entry.txt`
        # would authorize `ui/entry.txt`.
        self.write("ui-plan.example.md", HTML_PLAN.format(corresponding="`other/index.html`"))
        self.assertEqual(
            [v.reference for v in self.run_check().violations], ["other/index.html"]
        )


class EntryLineTests(Fixture):
    """`Entry frame:` and `Multi-page entry:` — the highest-value single references.

    The first version of this check read neither, and the printed `Not checked:` statement
    did not say so: the author's own defense against silence-reads-as-coverage understated
    the gap.
    """

    def test_an_undeclared_entry_frame_is_caught(self) -> None:
        text = (
            "## Prototype Output Planning\n\n"
            "- Entry frame: `ui/screens/00-entry.txt`\n"
            f"- Planned output files: {CONFORMING_DECLARATION}\n"
        )
        self.write("ui-plan.terminal.example.md", text)
        violations = self.run_check().violations
        self.assertEqual([v.reference for v in violations], ["ui/screens/00-entry.txt"])

    def test_a_declared_entry_frame_passes(self) -> None:
        text = (
            "## Prototype Output Planning\n\n"
            "- Entry frame: `ui/screens/entry.txt`\n"
            f"- Planned output files: {CONFORMING_DECLARATION}\n"
        )
        self.write("ui-plan.terminal.example.md", text)
        self.assertEqual(self.run_check().violations, [])

    def test_a_path_inside_a_prose_value_is_audited(self) -> None:
        # `Multi-page entry:` is a sentence with a path in it, not a bare path.
        self.write("ui-plan.example.md", HTML_PLAN.format(corresponding="`ui/index.html`"))
        report = self.run_check()
        references = [o.text for o in report.observations]
        self.assertIn("ui/index.html", references)

    def test_an_undeclared_path_inside_a_prose_value_is_caught(self) -> None:
        text = (
            "## Static Prototype Output Planning\n\n"
            "- Multi-page entry: `fixedly use ui/nowhere.html as the prototype entry page.`\n"
            "- Planned output files: `ui/index.html`\n"
        )
        self.write("ui-plan.example.md", text)
        violations = self.run_check().violations
        self.assertEqual([v.reference for v in violations], ["ui/nowhere.html"])

    def test_an_entry_line_with_no_path_is_prose(self) -> None:
        text = (
            "## Prototype Output Planning\n\n"
            "- Entry frame: `whichever the clarify step settles on`\n"
            f"- Planned output files: {CONFORMING_DECLARATION}\n"
        )
        self.write("ui-plan.terminal.example.md", text)
        report = self.run_check()
        self.assertEqual(report.violations, [])
        self.assertEqual(report.prose, 1)
        self.assertEqual(report.checked, 0)


class FenceTests(Fixture):
    """Fenced content is documentation *about* the format, never the format.

    The first version masked fences in one scanner out of three; the two that did not were
    the declaration line and the labelled-screen scan, and both bit immediately.
    """

    def test_a_fenced_declaration_above_the_real_one_does_not_make_a_template(self) -> None:
        """#28 finding 1's first half: the whole-plan skip, reopened through a fence.

        A filled plan that documents how to fill the template must still be audited. The
        declaration line is the *first visible* one; a fenced quote of the template form
        above it is illustration.
        """
        text = (
            "## How to fill this template\n\n"
            "```md\n- Planned output files: `{{PLANNED_FRAME_OUTPUTS}}`\n```\n\n"
            "## Screens & Flows\n\n"
            "### 1. `Startup / Edit Frame`\n\n"
            "- Corresponding frame file: `ui/screens/99-undeclared.txt`\n\n"
            "## Prototype Output Planning\n\n"
            f"- Planned output files: {CONFORMING_DECLARATION}\n"
        )
        self.write("ui-plan.terminal.example.md", text)
        report = self.run_check()
        self.assertEqual([(p.name, r) for p, r in report.skipped], [])
        self.assertEqual(len(report.plans), 1)
        self.assertEqual(
            [v.reference for v in report.violations], ["ui/screens/99-undeclared.txt"]
        )

    def test_a_fenced_corresponding_line_is_not_a_reference(self) -> None:
        """#28 finding 1's second half: a fenced example was a *false failure*.

        Adding an illustrative snippet to a plan must not break the gate.
        """
        text = (
            "## Screens & Flows\n\n"
            "### 1. `Startup / Edit Frame`\n\n"
            "- Corresponding frame file: `ui/screens/entry.txt`\n\n"
            "## Authoring note\n\n"
            "```md\n- Corresponding frame file: `ui/screens/whatever.txt`\n```\n\n"
            "## Prototype Output Planning\n\n"
            f"- Planned output files: {CONFORMING_DECLARATION}\n"
        )
        self.write("ui-plan.terminal.example.md", text)
        report = self.run_check()
        self.assertEqual(report.violations, [])
        self.assertEqual(report.checked, 1)

    def test_a_fenced_keybinding_table_is_not_read(self) -> None:
        text = (
            "## Keybinding Map\n\n"
            "| Key | Action | Target Frame | Expected Result |\n"
            "| --- | --- | --- | --- |\n"
            "| `Enter` | Submit | `entry` | history adds one |\n\n"
            "## Example\n\n"
            "```md\n| `Ghost` | Illustrative | `ui/screens/ghost.txt` | nothing |\n```\n\n"
            "## Prototype Output Planning\n\n"
            f"- Planned output files: {CONFORMING_DECLARATION}\n"
        )
        self.write("ui-plan.terminal.example.md", text)
        report = self.run_check()
        self.assertEqual(report.violations, [])
        self.assertEqual(report.checked, 1)


class CoverageAccountingTests(Fixture):
    """Finding 2: an item must land in a ledger, never in neither.

    The first version had two hand-synchronised parsers. Anything `references_of` dropped,
    `prose_count` had to drop identically or the item vanished from the verdict *and* from
    the printed gap — and all three of these fixtures did exactly that.
    """

    def test_an_empty_key_continuation_row_is_audited(self) -> None:
        """`set("") <= set("-: ")` is True, so the separator heuristic ate these rows."""
        text = (
            "## Keybinding Map\n\n"
            "| Key | Action | Target Frame | Expected Result |\n"
            "| --- | --- | --- | --- |\n"
            "| `Ctrl+C` | Cancel input | `entry` | clears editor |\n"
            "|  | (same key, second effect) | `ui/screens/99-ghost.txt` | ghost |\n\n"
            "## Prototype Output Planning\n\n"
            f"- Planned output files: {CONFORMING_DECLARATION}\n"
        )
        self.write("ui-plan.terminal.example.md", text)
        report = self.run_check()
        self.assertEqual(
            [v.reference for v in report.violations], ["ui/screens/99-ghost.txt"]
        )
        self.assertEqual(report.checked + report.prose, len(report.observations))

    def test_a_backticked_target_with_a_space_lands_in_the_prose_ledger(self) -> None:
        text = (
            "## Keybinding Map\n\n"
            "| Key | Action | Target Frame | Expected Result |\n"
            "| --- | --- | --- | --- |\n"
            "| `Esc` | Dismiss | `ghost frame` | closes |\n\n"
            "## Prototype Output Planning\n\n"
            f"- Planned output files: {CONFORMING_DECLARATION}\n"
        )
        self.write("ui-plan.terminal.example.md", text)
        report = self.run_check()
        self.assertEqual(report.violations, [])
        self.assertEqual(report.prose, 1)
        self.assertEqual(report.checked, 0)
        self.assertEqual(len(report.observations), 1)

    def test_the_prose_tail_of_a_mixed_transition_line_is_counted(self) -> None:
        text = (
            "## State Transition List\n\n"
            "1. `entry` --`?`--> `ui/screens/entry.txt` --`Esc`--> somewhere else entirely\n\n"
            "## Prototype Output Planning\n\n"
            f"- Planned output files: {CONFORMING_DECLARATION}\n"
        )
        self.write("ui-plan.terminal.example.md", text)
        report = self.run_check()
        self.assertEqual(report.violations, [])
        # Two resolvable heads and one prose tail.
        self.assertEqual(report.checked, 2)
        self.assertEqual(report.prose, 1)

    def test_checked_plus_prose_equals_everything_seen(self) -> None:
        """The structural invariant, over a fixture mixing every reference kind.

        This is the assertion that makes a silent drop impossible: if a future scanner
        skips an item without classifying it, the sum no longer matches what was
        collected.
        """
        self.write("ui-plan.example.md", HTML_PLAN.format(corresponding="`ui/account.html`"))
        report = self.run_check()
        self.assertEqual(report.checked + report.prose, len(report.observations))
        self.assertGreater(len(report.observations), 0)


class ScopeTests(Fixture):
    def test_a_template_with_a_placeholder_is_skipped(self) -> None:
        self.write(
            "ui-plan.terminal.md",
            TERMINAL_PLAN.format(
                accept_target="{{SCREEN_1_FILE}}",
                first_target="{{SCREEN_1_FILE}}",
                declared="{{PLANNED_FRAME_OUTPUTS}}",
            ),
        )
        report = self.run_check()
        self.assertEqual(report.violations, [])
        self.assertEqual([p.name for p, _reason in report.skipped], ["ui-plan.terminal.md"])
        self.assertEqual(report.plans, [])

    def test_a_stray_placeholder_outside_the_declaration_does_not_exempt_the_plan(self) -> None:
        """The skip is scoped to the declaration line (#27's "an exemption that widens")."""
        text = (
            "## Screens & Flows\n\n"
            "### 1. `Startup / Edit Frame`\n\n"
            "- Corresponding frame file: `ui/screens/entry.txt`\n\n"
            "### 2. `Other Frame`\n\n"
            "- Corresponding frame file: `ui/screens/99-other.txt`\n"
            "- Main purpose: `{{MAIN_PURPOSE_SLOT_NOT_YET_FILLED}}`\n\n"
            "## Prototype Output Planning\n\n"
            "- Planned output files: `ui/screens/entry.txt`\n"
        )
        self.write("ui-plan.terminal.example.md", text)
        report = self.run_check()
        self.assertEqual(report.skipped, [])
        self.assertEqual([v.reference for v in report.violations], ["ui/screens/99-other.txt"])

    def test_a_plan_with_no_declaration_line_fails_rather_than_passes(self) -> None:
        # "Nothing declared" must not be grandfathered in as "nothing to check".
        text = (
            "## Screens & Flows\n\n"
            "### 1. `Startup / Edit Frame`\n\n"
            "- Corresponding frame file: `ui/screens/entry.txt`\n"
        )
        self.write("ui-plan.terminal.example.md", text)
        violations = self.run_check().violations
        self.assertEqual([v.reference for v in violations], ["ui/screens/entry.txt"])
        self.assertIn("none declared", violations[0].detail)

    def test_an_unreadable_plan_is_recorded_not_dropped(self) -> None:
        """Finding 6: an unreadable plan was silently dropped while a template skip was
        recorded and printed. An I/O gap should not be quieter than a deliberate skip."""
        (self.templates / "ui-plan.terminal.example.md").write_bytes(b"\xff\xfe not utf-8\n")
        report = self.run_check()
        self.assertEqual(len(report.skipped), 1, report.skipped)
        _path, reason = report.skipped[0]
        self.assertIn("unreadable", reason)


class MainGuardTests(Fixture):
    """Finding 3: the vacuity guard lived in the test suite, which the hook never runs.

    `make check` runs `main()`; `make test` does not. A commit-time gate that audits nothing
    therefore passed every commit, which is #25 finding 2's lesson (the gate must judge the
    thing it claims to judge) in its emptiness form.
    """

    def test_no_plans_audited_fails(self) -> None:
        code, output = self.run_main()
        self.assertEqual(code, 1, output)
        self.assertIn("no plans audited", output)

    def test_plans_audited_but_no_references_seen_fails(self) -> None:
        self.write(
            "ui-plan.terminal.example.md",
            "## Prototype Output Planning\n\n- Planned output files: `ui/screens/entry.txt`\n",
        )
        code, output = self.run_main()
        self.assertEqual(code, 1, output)
        self.assertIn("no reference sites seen", output)

    def test_a_conforming_tree_passes_with_zero(self) -> None:
        # The negative fixture: without it the guard could fail everything and still pass
        # both tests above.
        self.terminal_plan("`entry`", "`10-suggestion`", CONFORMING_DECLARATION)
        code, output = self.run_main()
        self.assertEqual(code, 0, output)
        self.assertIn("Result: PASSED", output)

    def test_the_output_prints_both_ledgers_and_their_sum(self) -> None:
        """The accounting is only a defence if it is printed; a silent ledger is the bug."""
        self.terminal_plan("`entry`", "`10-suggestion`", CONFORMING_DECLARATION)
        _code, output = self.run_main()
        self.assertIn("Reference sites seen:", output)
        self.assertIn("checked against the declaration:", output)
        self.assertIn("prose (names a state, not a file):", output)

    def test_the_output_states_the_not_checked_dimension(self) -> None:
        self.terminal_plan("`entry`", "`10-suggestion`", CONFORMING_DECLARATION)
        _code, output = self.run_main()
        self.assertIn("Not checked: prototype link targets", output)


class RealTreeTests(unittest.TestCase):
    """The shipped tree must pass, and must have been read for it to mean anything.

    The counts are this tree's, deliberately: a glob that stops matching, a skip that
    widens, or a parser that stops reading a section should fail the suite rather than let
    the gate pass over nothing. Updating the example tree means updating them — that is the
    notice working, not an inconvenience.
    """

    def setUp(self) -> None:
        self.report = plan_outputs.run(plan_outputs.DEFAULT_ROOT)

    def test_the_shipped_examples_conform(self) -> None:
        self.assertEqual(
            [f"{v.path.name}:{v.line}: {v.reference}" for v in self.report.violations], []
        )

    def test_the_check_is_not_vacuous(self) -> None:
        self.assertEqual(len(self.report.plans), 2, self.report.plans)
        self.assertEqual(self.report.declared, 8)
        self.assertEqual(self.report.checked, 31)

    def test_the_skipped_set_cannot_widen_unnoticed(self) -> None:
        self.assertEqual(
            [(p.name, r) for p, r in self.report.skipped],
            [
                ("ui-plan.md", "template — the declaration line is a placeholder"),
                ("ui-plan.terminal.md", "template — the declaration line is a placeholder"),
            ],
        )

    def test_the_prose_count_is_measured_not_assumed(self) -> None:
        # Three: the modal overlay's "the frame the overlay was opened from", plus the two
        # unresolvable segments of the terminal plan's "no transition" line. Pinned because
        # a count that silently read 0 would report a gap of *none*, which is worse than a
        # failure — a failure gets read.
        self.assertEqual(self.report.prose, 3)

    def test_every_item_lands_in_a_ledger_on_the_real_tree(self) -> None:
        self.assertEqual(
            self.report.checked + self.report.prose, len(self.report.observations)
        )
        self.assertEqual(len(self.report.observations), 34)

    def test_the_entry_lines_are_audited(self) -> None:
        # Both example plans declare where a reviewer starts; those two references were
        # previously read by nothing.
        texts = [o.text for o in self.report.observations]
        self.assertIn("ui/screens/entry.txt", texts)
        self.assertIn("ui/index.html", texts)


if __name__ == "__main__":
    unittest.main()
