---
name: axb-gherkin-and-dsl
description: Evaluate and refactor Gherkin feature files and DSL vocabularies so they can be implemented as test code with minimal inference. Use when converting test plans into Gherkin, reviewing or tightening Given/When/Then sentences, deciding Rule/Background/Scenario Outline/DataTable structure, or checking whether Gherkin and DSL fully cover the intended test cases.
disable-model-invocation: true
---

# Gherkin And DSL

Converge Gherkin and DSL so that two things hold at the same time:

- PMs / requirement owners can read and understand the Gherkin
- The AI / test author can directly implement Gherkin + DSL as step definitions and test code

## Quick Start

1. First read the target feature files, the same module's `dsl.md`, the relevant interface root shared `dsl.md`, and the upstream testplan / spec.
2. Decide first whether this round is "create", "check", or "refactor".
3. Change structure and vocabulary together — **do not change Gherkin without changing the DSL**.
4. If any Gherkin sentence has no DSL counterpart, supplement the DSL first, then backfill the feature.
5. The final result must satisfy both "business-readable" and "directly test-implementable".

## SOP

## Phase 1 -- Converge the input and output scope

1. READ Read the user requirements, the target feature files, the same module's `dsl.md`, the interface root shared `dsl.md` related to the target sentences, and the upstream testplan / spec; confirm this round's interface and processing scope.
2. THINK Determine whether this round is new creation, coverage verification, sentence convergence, structure reorganization, or strictness reinforcement; inventory the feature and DSL files to modify.
3. WRITE Report the modification scope and the high-impact ambiguities that would affect file splitting or sentence boundaries; if there are ambiguities, stop and confirm first.

## Phase 2 -- Inventory test cases and coverage gaps

1. READ Read the "Coverage & Implementability Checks" and "Gherkin Sentence Standards" sections in [STANDARDS.md](STANDARDS.md).
2. THINK Compare each test case's Arrange / Act / expected output / must-remain-invariant / not-verified-by-this-case one by one, judging whether the current Gherkin and DSL fully cover them; if steps exist but semantics have been diluted, that also counts as a gap.
3. WRITE List the gaps: missing sentences, over-fat sentences, misplaced DataTable / Background / Rule boundaries, insufficient Then strictness, or technical jargon leaking into Gherkin.

## Phase 3 -- Converge Gherkin sentences

1. READ Read the "Gherkin Language Boundaries & Sentence Convergence" and "In-Sentence Parameters & DataTable Format" sections in [STANDARDS.md](STANDARDS.md).
2. THINK Converge the shared sentences of `Given` / `When` / `Then`: sentences with identical semantics must be shared; if a sentence is too fat, split it into more core, reusable steps; prefer DataTables only for multi-row data or single sentences that actually summarize more than 3 fields.
3. WRITE Modify the Gherkin: add missing Given / When / Then, add business-relevant default-value comments, adjust DataTables, and remove obsolete carry-over comments and technical details.

## Phase 4 -- Converge the DSL vocabulary

1. READ Read the "DSL Required Fields", "Backend Implementation Semantics", and "Frontend Implementation Semantics" sections in [STANDARDS.md](STANDARDS.md).
2. READ If you need to create or move DSL rows, or determine whether a sentence should be carried by the module or the interface root, read `rules/interface-module-and-dsl-unique-ownership-criteria.md` on demand to confirm the complete contract and unique-ownership criteria.
3. THINK For each Gherkin sentence, judge whether the existing row, DataTable fields, default parameters, and implementation semantics are sufficient, and decide the unique authoritative location per the loaded criteria.
4. WRITE Create or update rows in the unique authoritative DSL file, ensuring the sentence, parameters, DataTable fields, defaults, and implementation semantics can directly support step definitions.

## Phase 5 -- Perform structure optimization

1. READ Read the "Feature / Rule / Example Structure" and "Background / Scenario Outline / DataTable Decisions" sections in [STANDARDS.md](STANDARDS.md).
2. THINK Split feature files by functional aspect, deciding whether to extract `Rule`, `Background`, `Scenario Outline`; `Rule` must be atomic, `Example` should describe data scenarios rather than repeating the rule's name.
3. WRITE Refactor the feature files: split files, extract Rules, extract Backgrounds, introduce Scenario Outline where needed, and remove the obsolete single all-in-one master file.

## Phase 6 -- Check implementability

1. READ Re-read the modified feature files, the same-module DSL, and the relevant interface root shared DSL.
2. DELEGATE Run `uv run skills/axb-gherkin-and-dsl/scripts/audit_feature_dsl_topology.py --root <features-root>` to mechanically check the topology, DSL row duplicates, and unique matching of every step; keep the output for later judgment.
3. THINK Combine the audit results with the loaded standards to judge whether shared contracts are truly semantically consistent, whether every test case is fully covered, whether the Gherkin remains in business language, whether the DSL is sufficient for direct implementation, and whether Then goes beyond surface output.
4. WRITE Report the mechanical audit results, semantic and structure decisions, the sentences still needing convergence, and the scope that can be handed directly to step definition / test implementation.

## Additional Resources

- Detailed standards and decision criteria: [STANDARDS.md](STANDARDS.md)
- Complete e-commerce demonstration: [examples.md](examples.md)
