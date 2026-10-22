"""Regression tests for the feature / DSL topology audit.

Run with:

    python3 -m unittest discover -s skills/axb-gherkin-and-dsl/scripts -p 'test_*.py'

Every test below pins one behaviour that the audit used to get wrong: either a
false PASS (a real defect reported as healthy) or a false FAILED (a correct tree
reported as broken). See issues #1 and #6.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import audit_feature_dsl_topology as audit_mod  # noqa: E402


BACKEND_DSL_HEADER = "| DSL Sentence | StepDef Implementation Semantics |\n| --- | --- |\n"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def dsl(*rows: str) -> str:
    return BACKEND_DSL_HEADER + "".join(f"| `{row}` | how: x |\n" for row in rows)


def feature(*steps: str, name: str = "F") -> str:
    """Build a feature whose `steps` are complete Gherkin step lines."""
    body = "".join(f"      {step}\n" for step in steps)
    return f"Feature: {name}\n  Rule: r1\n    Example: e1\n{body}"


class AuditTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def audit(self, root: Path):
        return audit_mod.audit_target(root.resolve())


class ParentRootTests(AuditTestCase):
    """Finding #1.1 / #6.1: the parent features root must not be rejected."""

    def _build_two_interfaces(self) -> None:
        write(
            self.root / "backend" / "orders" / "o.feature",
            feature("Given a mapped step"),
        )
        write(self.root / "backend" / "orders" / "dsl.md", dsl("a mapped step"))
        write(
            self.root / "frontend" / "checkout" / "c.feature",
            feature("Given a mapped step"),
        )
        write(self.root / "frontend" / "checkout" / "dsl.md", dsl("a mapped step"))

    def test_parent_root_audits_each_interface(self) -> None:
        self._build_two_interfaces()
        roots, errors, _warnings, stats = self.audit(self.root)
        self.assertEqual([r.name for r in roots], ["backend", "frontend"])
        self.assertEqual(errors, [])
        self.assertEqual(stats["features"], 2)
        self.assertEqual(stats["steps"], 2)

    def test_interface_root_still_audited_directly(self) -> None:
        self._build_two_interfaces()
        roots, errors, _warnings, stats = self.audit(self.root / "backend")
        self.assertEqual([r.name for r in roots], ["backend"])
        self.assertEqual(errors, [])
        self.assertEqual(stats["features"], 1)

    def test_module_named_like_an_interface_is_not_expanded(self) -> None:
        # A module that happens to be named "cli" must not be mistaken for an
        # interface directory when the root is already an interface root.
        write(self.root / "cli" / "a.feature", feature("Given a mapped step"))
        write(self.root / "cli" / "dsl.md", dsl("a mapped step"))
        roots, errors, _warnings, _stats = self.audit(self.root)
        self.assertEqual(roots, [self.root.resolve()])
        self.assertEqual(errors, [])

    def test_real_depth_error_still_reported(self) -> None:
        # Expansion must not mask a genuinely mis-nested feature.
        write(
            self.root / "backend" / "orders" / "nested" / "o.feature",
            feature("Given a mapped step"),
        )
        write(self.root / "backend" / "orders" / "dsl.md", dsl("a mapped step"))
        _roots, errors, _warnings, _stats = self.audit(self.root / "backend")
        self.assertTrue(
            any("exactly one functional-module level deep" in e for e in errors),
            errors,
        )


class ChineseKeywordTests(AuditTestCase):
    """Finding #1.2: zh-TW steps are written without a space after the keyword."""

    def test_unmapped_chinese_step_is_reported(self) -> None:
        write(
            self.root / "m1" / "a.feature",
            "# language: zh-TW\n"
            "Feature: 中文功能\n"
            "  Rule: 中文規則\n"
            "    Example: 中文例子\n"
            "      當使用者登入\n"
            "      那麼應顯示首頁\n",
        )
        write(self.root / "m1" / "dsl.md", dsl("使用者登入"))
        _roots, errors, _warnings, stats = self.audit(self.root)
        self.assertEqual(stats["steps"], 2, "Chinese steps must be parsed as steps")
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("應顯示首頁", errors[0])

    def test_chinese_step_with_space_still_works(self) -> None:
        write(
            self.root / "m1" / "a.feature",
            "Feature: 中文功能\n  Rule: r\n    Example: e\n      當 使用者登入\n",
        )
        write(self.root / "m1" / "dsl.md", dsl("使用者登入"))
        _roots, errors, _warnings, stats = self.audit(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(stats["steps"], 1)


class DocstringAndDescriptionTests(AuditTestCase):
    """Finding #1.3: docstrings and Feature/Rule descriptions are not steps."""

    def test_docstring_content_is_not_a_step(self) -> None:
        write(
            self.root / "m1" / "a.feature",
            'Feature: F\n'
            '  Rule: r1\n'
            '    Example: e1\n'
            '      Given a mapped step\n'
            '      Then verify output:\n'
            '        """json\n'
            '        Given this is just data inside a docstring\n'
            '        """\n',
        )
        write(self.root / "m1" / "dsl.md", dsl("a mapped step", "verify output:"))
        _roots, errors, _warnings, stats = self.audit(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(stats["steps"], 2)

    def test_feature_description_keyword_line_is_not_a_step(self) -> None:
        write(
            self.root / "m1" / "a.feature",
            "Feature: F\n"
            "  Given this is a description line, not a step\n"
            "\n"
            "  Rule: r1\n"
            "    Example: e1\n"
            "      Given a mapped step\n",
        )
        write(self.root / "m1" / "dsl.md", dsl("a mapped step"))
        _roots, errors, _warnings, stats = self.audit(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(stats["steps"], 1)


class FencedBlockTests(AuditTestCase):
    """Finding #1.4: fenced example tables must not become live DSL rows."""

    def test_fenced_table_is_ignored(self) -> None:
        write(self.root / "m1" / "a.feature", feature("Given a mapped step"))
        write(
            self.root / "m1" / "dsl.md",
            dsl("a mapped step")
            + "\n```markdown\n"
            + BACKEND_DSL_HEADER
            + "| `phantom fenced row` | example only |\n"
            + "```\n",
        )
        _roots, errors, _warnings, stats = self.audit(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(stats["module_rows"], 1)


class DeadRootRowTests(AuditTestCase):
    """Finding #1.5: an orphaned root row must not pass silently."""

    def test_dead_root_row_warns(self) -> None:
        write(self.root / "m1" / "a.feature", feature("Given a mapped step"))
        write(self.root / "m1" / "dsl.md", dsl("a mapped step"))
        write(self.root / "dsl.md", dsl("a mapped step", "never used root row"))
        _roots, errors, warnings, _stats = self.audit(self.root)
        # root + module duplicate of "a mapped step" is a genuine ambiguity.
        self.assertTrue(any("never used root row" in w for w in warnings), warnings)
        self.assertTrue(any("used by no module" in w for w in warnings), warnings)
        self.assertTrue(errors, "root/module shadowing must still be an error")


class DuplicateScopeTests(AuditTestCase):
    """Finding #1.6: sibling-module duplication is not ambiguous."""

    def test_sibling_module_duplicate_warns_but_passes(self) -> None:
        write(self.root / "m1" / "a.feature", feature("Given a mapped step", name="F1"))
        write(self.root / "m2" / "b.feature", feature("Given a mapped step", name="F2"))
        write(self.root / "m1" / "dsl.md", dsl("a mapped step"))
        write(self.root / "m2" / "dsl.md", dsl("a mapped step"))
        _roots, errors, warnings, _stats = self.audit(self.root)
        self.assertEqual(errors, [])
        self.assertTrue(any("sibling modules" in w for w in warnings), warnings)

    def test_same_module_duplicate_is_an_error(self) -> None:
        write(self.root / "m1" / "a.feature", feature("Given a mapped step"))
        write(self.root / "m1" / "dsl.md", dsl("a mapped step", "a mapped step"))
        _roots, errors, _warnings, _stats = self.audit(self.root)
        self.assertTrue(any("multiple authoritative locations" in e for e in errors), errors)

    def test_root_and_module_duplicate_is_an_error(self) -> None:
        write(self.root / "m1" / "a.feature", feature("Given a mapped step"))
        write(self.root / "m1" / "dsl.md", dsl("a mapped step"))
        write(self.root / "dsl.md", dsl("a mapped step"))
        _roots, errors, _warnings, _stats = self.audit(self.root)
        self.assertTrue(any("multiple authoritative locations" in e for e in errors), errors)
        self.assertTrue(any("matched 2 DSL rows" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
