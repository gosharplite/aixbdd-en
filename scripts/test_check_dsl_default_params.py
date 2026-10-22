"""Tests for scripts/check_dsl_default_params.py.

The fixtures are the PRE-FIX cells from the tree as it stood before #23 — the eight
entries that said "defaults to …" — because a check that only passes on a clean tree has
not been shown to catch anything.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_dsl_default_params as params  # noqa: E402

HEADER = (
    "| DSL Sentence | Gherkin Params | Data Table Params | Default Params | Semantics |\n"
    "| --- | --- | --- | --- | --- |\n"
)

PRE_FIX_CELLS = [
    # (sentence, params, data table, default)  — as they were on `main` before #23
    (
        '`the platform has a usable discount code "{discount-code}"`',
        "`discount-code`: string",
        "Not supported",
        "`discount-amount`: integer; defaults to 100.",
    ),
    (
        "`the cart already contains the following items:`",
        "none",
        "Supported:`Product Code` (required, string)",
        "`player`: defaults to the current cart owner.",
    ),
    (
        '`"{player}" applies discount code "{discount-code}"`',
        "`player`: string",
        "Not supported",
        "`target-cart`: defaults to that player's current cart.",
    ),
]

POST_FIX_CELLS = [
    ("`the platform has a usable discount code \"{discount-code}\"`", "`discount-code`: string", "Not supported", "none"),
    (
        "`the cart already contains the following items:`",
        "none",
        "Supported:`Product Code` (required, string)",
        "`player`: the scenario's only player, resolved from the scenario text per §4.3; the cart belongs to them.",
    ),
    (
        '`"{player}" applies discount code "{discount-code}"`',
        "`player`: string",
        "Not supported",
        "`target-cart`: the cart `{player}` owns, created by the preceding cart Given.",
    ),
    (
        '`"{player}" enters discount code "{discount-code}" on the checkout page and applies it`',
        "`player`: string",
        "Not supported",
        "`initial-screen`: the checkout page, constant — the When always opens it directly.",
    ),
]


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write_tree(self, cells) -> None:
        path = self.root / "skills/axb-gherkin-and-dsl/examples/demo/features/backend/mod/dsl.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        body = "".join(
            f"| {sent} | {par} | {dt} | {default} | `Must-check`: nothing to see |\n"
            for sent, par, dt, default in cells
        )
        path.write_text("# Demo DSL\n\n## Then Sentences\n\n" + HEADER + body)

    def run_check(self):
        return params.run(self.root.resolve())


class PreFixTests(Fixture):
    """Every one of the historical cells must be caught."""

    def test_all_pre_fix_cells_are_caught(self) -> None:
        self.write_tree(PRE_FIX_CELLS)
        violations = self.run_check()
        self.assertEqual(len(violations), len(PRE_FIX_CELLS), violations)

    def test_word_default_is_caught(self) -> None:
        problems = params.check_entry("`x`", "none", "Not supported", "`a`: defaults to 100.")
        self.assertTrue(any("word 'default'" in p for p in problems), problems)

    def test_circular_binding_is_caught(self) -> None:
        problems = params.check_entry(
            "`the cart contains items:`", "none", "Not supported",
            "`player`: defaults to the current cart owner.",
        )
        self.assertTrue(any("circular" in p for p in problems), problems)

    def test_missing_establishing_source_is_caught(self) -> None:
        # A binding written without saying what establishes it — the two cells #23's
        # review flagged as non-conforming.
        problems = params.check_entry(
            "`x`", "none", "Not supported", "`target-cart`: the current cart of `{player}`."
        )
        self.assertTrue(any("establishing source" in p for p in problems), problems)


class PostFixTests(Fixture):
    def test_create_new_cells_pass(self) -> None:
        self.write_tree(POST_FIX_CELLS)
        self.assertEqual(self.run_check(), [])

    def test_none_is_conforming(self) -> None:
        problems = params.check_entry("`x`", "", "", "none")
        self.assertEqual(problems, [])


class OperandTests(Fixture):
    """The test is on the PARAMETER, not the value — the #23 review's finding 3.

    The pre-fix `target-cart: defaults to that player's current cart` mentions
    `{player}`, so a value-scoped test would pass it. It must fail.
    """

    def test_value_mentioning_a_placeholder_still_fails(self) -> None:
        problems = params.check_entry(
            '`"{player}" applies code`', "`player`: string", "Not supported",
            "`target-cart`: defaults to that player's current cart.",
        )
        self.assertTrue(problems, "a value that mentions a placeholder must not satisfy the test")

    def test_name_that_is_a_placeholder_is_caught(self) -> None:
        problems = params.check_entry(
            '`"{owner}" does a thing`', "`owner`: string", "Not supported",
            "`owner`: the scenario's only player.",
        )
        self.assertTrue(any("placeholder" in p for p in problems), problems)

    def test_name_that_is_a_datatable_column_is_caught(self) -> None:
        problems = params.check_entry(
            "`the cart contains:`", "none", "Supported:`Product Code` (required, string)",
            "`Product Code`: a constant.",
        )
        self.assertTrue(any("DataTable column" in p for p in problems), problems)


class RealTreeTests(unittest.TestCase):
    def test_the_shipped_example_tree_conforms(self) -> None:
        violations = params.run(params.DEFAULT_ROOT)
        self.assertEqual([v.entry for v in violations], [])


if __name__ == "__main__":
    unittest.main()
