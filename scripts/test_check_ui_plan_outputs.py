"""Tests for scripts/check_ui_plan_outputs.py.

The fixtures are written from the **defect text** in #24 item 3 — "a reference to a frame
or page the plan does not declare" — not from this checker's code, because #24 records
that writing them from the code is how the first two attempts passed all three of their
motivating escapes.

Both historical instances (#14) were a plan body contradicting its own `Planned output
files:` line, so that is what the fixtures reproduce.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

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

CONFORMING_DECLARATION = "`ui/screens/entry.txt`, `ui/screens/10-suggestion.txt`, `ui/screens/20-running.txt`"


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


class KeybindingColumnTests(Fixture):
    """A `Target Frame` naming a frame the plan never declares."""

    def test_undeclared_keybinding_target_is_caught(self) -> None:
        self.terminal_plan("`40-history`", "`10-suggestion`", CONFORMING_DECLARATION)
        violations = self.run_check().violations
        self.assertEqual([v.reference for v in violations], ["40-history"], violations)

    def test_declared_keybinding_target_passes(self) -> None:
        self.terminal_plan("`10-suggestion`", "`10-suggestion`", CONFORMING_DECLARATION)
        self.assertEqual(self.run_check().violations, [])

    def test_ordered_prefix_is_not_identity(self) -> None:
        # `suggestion` and `10-suggestion.txt` name the same frame; the prefix is ordering.
        self.terminal_plan("`suggestion`", "`suggestion`", CONFORMING_DECLARATION)
        self.assertEqual(self.run_check().violations, [])

    def test_a_different_order_prefix_is_still_a_different_file(self) -> None:
        # Leniency on the prefix must not become leniency on the name.
        self.terminal_plan("`10-history`", "`10-suggestion`", CONFORMING_DECLARATION)
        self.assertEqual([v.reference for v in self.run_check().violations], ["10-history"])


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
        text = (
            "## State Transition List\n\n"
            "1. `entry` --`Esc`--> `10-suggestion` --`Tab`--> `entry`\n\n"
            "## Prototype Output Planning\n\n"
            f"- Planned output files: {CONFORMING_DECLARATION}\n"
        )
        report = self.run_check_with(text)
        self.assertEqual(report.violations, [])
        self.assertEqual(report.references, 3)

    def run_check_with(self, body: str):
        self.write("ui-plan.terminal.example.md", body)
        return self.run_check()


class LabelledScreenLineTests(Fixture):
    """A screen section pointing at a page the plan never declares."""

    def test_undeclared_prototype_file_is_caught(self) -> None:
        self.write(
            "ui-plan.example.md",
            HTML_PLAN.format(corresponding="`ui/account.html`"),
        )
        violations = self.run_check().violations
        self.assertEqual([v.reference for v in violations], ["ui/account.html"], violations)

    def test_declared_prototype_file_passes(self) -> None:
        self.write(
            "ui-plan.example.md",
            HTML_PLAN.format(corresponding="`ui/product-detail.html`"),
        )
        self.assertEqual(self.run_check().violations, [])

    def test_a_path_is_not_matched_by_its_stem(self) -> None:
        # A bare name resolves by stem (scene names are ordered files); a path must be
        # exact, or `ui/screens/entry.txt` would authorize `ui/entry.txt`.
        self.write(
            "ui-plan.example.md",
            HTML_PLAN.format(corresponding="`other/index.html`"),
        )
        self.assertEqual(
            [v.reference for v in self.run_check().violations], ["other/index.html"]
        )


class ScopeTests(Fixture):
    def test_a_template_with_a_placeholder_is_skipped_not_failed(self) -> None:
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
        self.assertEqual([p.name for p in report.skipped], ["ui-plan.terminal.md"])
        self.assertEqual(report.plans, [])

    def test_prose_target_is_counted_not_failed(self) -> None:
        # A modal overlay whose target is "the frame it was opened from" names a state,
        # not a file. Failing on it would delete the check; silence would hide the gap.
        text = (
            "## Keybinding Map\n\n"
            "| Key | Action | Target Frame | Expected Result |\n"
            "| --- | --- | --- | --- |\n"
            "| `Esc` | Dismiss the overlay | the frame the overlay was opened from | closes |\n"
            "\n## Prototype Output Planning\n\n"
            f"- Planned output files: {CONFORMING_DECLARATION}\n"
        )
        self.write("ui-plan.terminal.example.md", text)
        report = self.run_check()
        self.assertEqual(report.violations, [])
        self.assertEqual(report.prose, 1)
        self.assertEqual(report.references, 0)


class RealTreeTests(unittest.TestCase):
    """The shipped tree must pass, and must have been read for it to mean anything."""

    def test_the_shipped_examples_conform(self) -> None:
        report = plan_outputs.run(plan_outputs.DEFAULT_ROOT)
        self.assertEqual(
            [f"{v.path.name}:{v.line}: {v.reference}" for v in report.violations], []
        )

    def test_the_check_is_not_vacuous(self) -> None:
        # A check that reads nothing passes trivially. These numbers are the tree's, and
        # they are here so a glob that stops matching fails the suite instead of the gate.
        report = plan_outputs.run(plan_outputs.DEFAULT_ROOT)
        self.assertEqual(len(report.plans), 2, report.plans)
        self.assertEqual(len(report.skipped), 2, report.skipped)
        self.assertEqual(report.declared, 8)
        self.assertEqual(report.references, 29)


if __name__ == "__main__":
    unittest.main()
