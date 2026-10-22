# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Mechanically audit the module topology of features and DSL and the unique matching of sentences."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


INTERFACE_KINDS = ("backend", "frontend", "cli")

# Latin step keywords are conventionally separated from the sentence by
# whitespace; CJK step keywords are conventionally written with no separator
# (e.g. `當使用者登入`). Requiring whitespace after CJK keywords made every
# Chinese step a non-step, so unmapped Chinese sentences passed the audit.
STEP_RE = re.compile(
    r"^\s*(?:(?:Given|When|Then|And|But|\*)\s+|"
    r"(?:假如|假設|假定|當|那麼|而且|並且|同時|但是))(.+?)\s*$"
)
# NOTE: the Chinese keywords above are functional Gherkin keywords (Chinese
# locale) and must not be removed or translated; see STANDARDS.md "Project
# Language" (STEP_RE accepts both English and Chinese keywords).
# NOTE: whitespace after a CJK keyword is optional. Do not "simplify" this back
# to `\s+` for both groups; that reintroduces the silent zh-TW false PASS.

# Feature/Rule headings open a free-text description block. Gherkin allows no
# steps in that region, so a keyword-initial line there is description prose.
FEATURE_DESCRIPTION_HEADING_RE = re.compile(r"^\s*(?:Feature|Rule)\s*:")
# These headings end the description block and open a step-bearing section.
STEP_SECTION_HEADING_RE = re.compile(
    r"^\s*(?:Background|Scenario Outline|Scenario|Example)\s*:"
)
DOCSTRING_DELIMITER = '"""'
PLACEHOLDER_RE = re.compile(r"\{[^{}]+\}")
SEPARATOR_CELL_RE = re.compile(r"^:?-{3,}:?$")


@dataclass(frozen=True)
class DslRow:
    phrase: str
    path: Path
    line: int
    scope: str


@dataclass(frozen=True)
class GherkinStep:
    text: str
    path: Path
    line: int


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the module topology under the features interface root, "
            "DSL row uniqueness, and the DSL match count of every Gherkin step."
        )
    )
    parser.add_argument(
        "--root",
        required=True,
        type=Path,
        metavar="<features-root>",
        help=(
            "either one interface features root, e.g. specs/truth/features/backend, "
            "or the shared parent specs/truth/features (every interface "
            "subdirectory is then audited in turn)"
        ),
    )
    return parser


def relative_display(path: Path, root: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def split_markdown_row(line: str) -> list[str]:
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|") and not text.endswith(r"\|"):
        text = text[:-1]
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", text)]


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(
        SEPARATOR_CELL_RE.fullmatch(cell.replace(" ", "")) for cell in cells
    )


def fenced_line_mask(lines: list[str]) -> list[bool]:
    """Mark lines that sit inside (or delimit) a fenced code block.

    Fenced blocks are documentation, never live DSL rows; ingesting them creates
    phantom rows that corrupt uniqueness and matching.
    """
    mask: list[bool] = []
    in_fence = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            mask.append(True)
            in_fence = not in_fence
            continue
        mask.append(in_fence)
    return mask


def read_text(path: Path, errors: list[str]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"cannot read {path}: {exc}")
        return None


def parse_dsl(path: Path, scope: str, errors: list[str]) -> list[DslRow]:
    text = read_text(path, errors)
    if text is None:
        return []

    lines = text.splitlines()
    fenced = fenced_line_mask(lines)
    rows: list[DslRow] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if fenced[index] or not line.lstrip().startswith("|"):
            index += 1
            continue

        header = split_markdown_row(line)
        # The first column header must be exactly "DSL Sentence" (the legacy
        # upstream Chinese header "DSL 句型" is also accepted). This literal is a
        # fixed contract token and must not be translated (see STANDARDS.md).
        if not header or header[0].strip() not in {"DSL Sentence", "DSL 句型"}:
            index += 1
            continue

        index += 1
        if (
            index < len(lines)
            and not fenced[index]
            and lines[index].lstrip().startswith("|")
        ):
            separator = split_markdown_row(lines[index])
            if is_separator_row(separator):
                index += 1

        while (
            index < len(lines)
            and not fenced[index]
            and lines[index].lstrip().startswith("|")
        ):
            cells = split_markdown_row(lines[index])
            line_number = index + 1
            index += 1
            if is_separator_row(cells) or not cells:
                continue

            match = re.fullmatch(r"`(.+)`", cells[0].strip())
            if match is None:
                errors.append(
                    f"{path}:{line_number} the DSL Sentence cell must be a single backticked sentence"
                )
                continue
            phrase = match.group(1).replace(r"\|", "|").strip()
            if not phrase:
                errors.append(f"{path}:{line_number} the DSL Sentence must not be empty")
                continue
            rows.append(DslRow(phrase=phrase, path=path, line=line_number, scope=scope))

    return rows


def parse_feature(path: Path, errors: list[str]) -> list[GherkinStep]:
    text = read_text(path, errors)
    if text is None:
        return []

    steps: list[GherkinStep] = []
    in_docstring = False
    in_description = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()

        if in_docstring:
            if stripped.endswith(DOCSTRING_DELIMITER):
                in_docstring = False
            continue
        if stripped.startswith(DOCSTRING_DELIMITER):
            in_docstring = True
            continue

        if FEATURE_DESCRIPTION_HEADING_RE.match(line):
            in_description = True
            continue
        if STEP_SECTION_HEADING_RE.match(line):
            in_description = False
            continue
        if in_description:
            continue

        match = STEP_RE.match(line)
        if match:
            steps.append(
                GherkinStep(
                    text=" ".join(match.group(1).split()),
                    path=path,
                    line=line_number,
                )
            )
    return steps


def escape_static(text: str) -> str:
    chunks = re.split(r"(\s+)", text)
    return "".join(r"\s+" if chunk.isspace() else re.escape(chunk) for chunk in chunks)


def compile_phrase(phrase: str) -> re.Pattern[str]:
    normalized = " ".join(phrase.split())
    parts: list[str] = []
    cursor = 0
    for placeholder in PLACEHOLDER_RE.finditer(normalized):
        parts.append(escape_static(normalized[cursor : placeholder.start()]))
        quoted = (
            placeholder.start() > 0
            and placeholder.end() < len(normalized)
            and normalized[placeholder.start() - 1] == '"'
            and normalized[placeholder.end()] == '"'
        )
        parts.append(r'[^"]+' if quoted else r".+?")
        cursor = placeholder.end()
    parts.append(escape_static(normalized[cursor:]))
    return re.compile("^" + "".join(parts) + "$")


def format_locations(rows: Iterable[DslRow], root: Path) -> str:
    return ", ".join(
        f"{relative_display(row.path, root)}:{row.line}" for row in rows
    )


def audit(root: Path) -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []
    stats = {
        "features": 0,
        "modules": 0,
        "root_rows": 0,
        "module_rows": 0,
        "steps": 0,
    }

    if not root.exists():
        return [f"the specified features root does not exist: {root}"], warnings, stats
    if not root.is_dir():
        return [f"the specified features root is not a directory: {root}"], warnings, stats

    feature_paths = sorted(root.rglob("*.feature"))
    stats["features"] = len(feature_paths)
    features_by_module: dict[str, list[Path]] = defaultdict(list)

    for feature_path in feature_paths:
        relative = feature_path.relative_to(root)
        if len(relative.parts) == 1:
            errors.append(
                f"features must not be placed directly in the interface root: {relative_display(feature_path, root)}"
            )
            continue
        module = relative.parts[0]
        features_by_module[module].append(feature_path)
        if len(relative.parts) != 2:
            errors.append(
                "a feature must sit exactly one functional-module level deep: "
                f"{relative_display(feature_path, root)}"
            )

    stats["modules"] = len(features_by_module)
    root_dsl = root / "dsl.md"
    root_rows = parse_dsl(root_dsl, "root", errors) if root_dsl.is_file() else []
    stats["root_rows"] = len(root_rows)

    all_rows = list(root_rows)
    dsl_modules = {
        path.parent.name for path in root.glob("*/dsl.md") if path.is_file()
    }
    for module in sorted(set(features_by_module) | dsl_modules):
        dsl_path = root / module / "dsl.md"
        if not dsl_path.is_file():
            errors.append(f"a module with features is missing dsl.md: {module}/dsl.md")
            continue
        rows = parse_dsl(dsl_path, module, errors)
        all_rows.extend(rows)
        stats["module_rows"] += len(rows)

    rows_by_phrase: dict[str, list[DslRow]] = defaultdict(list)
    for row in all_rows:
        rows_by_phrase[row.phrase].append(row)
    for phrase, rows in sorted(rows_by_phrase.items()):
        if len(rows) < 2:
            continue
        scopes = [row.scope for row in rows]
        root_scoped = [row for row in rows if row.scope == "root"]
        repeated_in_one_scope = len(set(scopes)) != len(scopes)
        if root_scoped or repeated_in_one_scope:
            # Either a root row is shadowed by a module row (a lookup in that
            # module merges root with same-module and hits twice), or one DSL file
            # declares the same sentence twice. Both are genuinely ambiguous.
            errors.append(
                f"DSL Sentence `{phrase}` has multiple authoritative locations: "
                f"{format_locations(rows, root)}"
            )
        else:
            # Sibling modules may each legitimately need the sentence: a lookup
            # merges root with same-module only, so every module still resolves to
            # exactly one row. Recommend promotion instead of failing the audit.
            warnings.append(
                f"the DSL Sentence `{phrase}` is defined in {len(rows)} sibling modules "
                f"({format_locations(rows, root)}); each module still resolves to exactly one row, "
                "but consider promoting it to the interface-root dsl.md"
            )

    compiled_rows = [(row, compile_phrase(row.phrase)) for row in all_rows]
    root_usage: dict[DslRow, set[str]] = defaultdict(set)
    all_steps: list[GherkinStep] = []

    for module, paths in sorted(features_by_module.items()):
        allowed_rows = [
            item
            for item in compiled_rows
            if item[0].scope in {"root", module}
        ]
        for feature_path in paths:
            steps = parse_feature(feature_path, errors)
            all_steps.extend(steps)
            for step in steps:
                matches = [
                    row for row, pattern in allowed_rows if pattern.fullmatch(step.text)
                ]
                for row in matches:
                    if row.scope == "root":
                        root_usage[row].add(module)
                if not matches:
                    errors.append(
                        f"{relative_display(step.path, root)}:{step.line} "
                        f"no DSL row found: `{step.text}`"
                    )
                elif len(matches) > 1:
                    errors.append(
                        f"{relative_display(step.path, root)}:{step.line} "
                        f"matched {len(matches)} DSL rows: `{step.text}`; "
                        f"{format_locations(matches, root)}"
                    )

    stats["steps"] = len(all_steps)
    for row in root_rows:
        modules = root_usage.get(row, set())
        if len(modules) == 1:
            only_module = next(iter(modules))
            warnings.append(
                f"the interface-root DSL row `{row.phrase}` is used only by module '{only_module}' "
                f"({relative_display(row.path, root)}:{row.line}); "
                "please have the agent judge whether it should be demoted"
            )
        elif not modules:
            # Asymmetric with the demotion warning above: an orphaned contract
            # sentence is the more severe case, so it must be visible rather than
            # silently discarded.
            warnings.append(
                f"the interface-root DSL row `{row.phrase}` is used by no module "
                f"({relative_display(row.path, root)}:{row.line}); "
                "please remove it or give it a consumer"
            )

    return errors, warnings, stats


def interface_roots(root: Path) -> list[Path]:
    """Resolve the given root into the interface roots that should be audited.

    The audit contract is per interface (`backend`, `frontend`, `cli`), because a
    top-level directory under an interface root is a functional module while a
    top-level directory under the shared parent is an interface. Running a
    per-interface audit on the parent reported every correctly placed feature as
    "not exactly one functional-module level deep", so the parent is accepted and
    expanded here instead of being rejected.
    """
    if not root.is_dir():
        return [root]
    candidates = [root / kind for kind in INTERFACE_KINDS if (root / kind).is_dir()]
    if not candidates:
        return [root]
    # If the root already has features at functional-module depth it is itself an
    # interface root whose module happens to share an interface name; audit it
    # directly instead of expanding.
    for feature_path in root.rglob("*.feature"):
        if len(feature_path.relative_to(root).parts) == 2:
            return [root]
    return candidates


def audit_target(root: Path) -> tuple[list[Path], list[str], list[str], dict[str, int]]:
    roots = interface_roots(root)
    if len(roots) == 1 and roots[0] == root:
        errors, warnings, stats = audit(root)
        return roots, errors, warnings, stats

    errors: list[str] = []
    warnings: list[str] = []
    stats = {
        "features": 0,
        "modules": 0,
        "root_rows": 0,
        "module_rows": 0,
        "steps": 0,
    }
    for interface_root in roots:
        interface_errors, interface_warnings, interface_stats = audit(interface_root)
        label = interface_root.name
        errors.extend(f"[{label}] {message}" for message in interface_errors)
        warnings.extend(f"[{label}] {message}" for message in interface_warnings)
        for key, value in interface_stats.items():
            stats[key] += value
    return roots, errors, warnings, stats


def print_report(
    root: Path,
    roots: list[Path],
    errors: list[str],
    warnings: list[str],
    stats: dict[str, int],
) -> None:
    print(f"Feature / DSL topology audit: {root}")
    if len(roots) > 1:
        print(
            "Interface roots audited: "
            + ", ".join(interface_root.name for interface_root in roots)
        )
    print(
        "Summary: "
        f"{stats['features']} features, "
        f"{stats['modules']} modules with features, "
        f"{stats['root_rows']} root DSL rows, "
        f"{stats['module_rows']} module DSL rows, "
        f"{stats['steps']} Gherkin steps"
    )

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for message in errors:
            print(f"  [ERROR] {message}")
    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for message in warnings:
            print(f"  [WARNING] {message}")

    if errors:
        print("\nResult: FAILED (errors fail the audit; warnings are for semantic judgment only)")
    else:
        print("\nResult: PASSED (warnings do not affect the exit code)")


def main() -> int:
    args = build_parser().parse_args()
    root = args.root.expanduser().resolve()
    roots, errors, warnings, stats = audit_target(root)
    print_report(root, roots, errors, warnings, stats)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
