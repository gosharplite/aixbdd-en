# System Analysis Plan

## Project Structure

### Document Structure (this feature)

```text
specs/plans/{{PLAN_PACKAGE}}/
├── spec.md                      # /axb-specify
├── checklists/
│   └── requirements.md          # /axb-specify
├── truth-delta.md               # initialized and maintained by /axb-truth-delta
├── features/
│   └── acceptance/
│       └── *.feature            # /axb-spec-by-example
├── ui/                          # /axb-ui-plan; absent for a plain line-oriented CLI
│   ├── ui-plan.md
│   ├── *.html                   # HTML mode (web / frontend)
│   └── screens/                 # terminal mode (CLI with a TUI), instead of *.html
│       ├── entry.txt
│       └── NN-<name>.txt
├── research.md                  # /axb-technical-research
├── plan.md                      # /axb-system-analysis (this file)
└── tasks.md                     # /axb-tasks
```

**Truth this feature maintains**: {{TRUTH_ARTIFACTS_PARAGRAPH}}

<!--
  Fill {{TRUTH_ARTIFACTS_PARAGRAPH}} with the concrete `specs/truth/**` artifacts this feature adds
  or changes, grouped by owner (contracts, data, techstack, features/DSL). This is the mapping
  `/axb-tasks` consumes when it builds the truth-impact inventory, so it must name paths, not
  categories.

  The package holds only plan-side artifacts. Truth is not package-local: API contracts live in
  `specs/truth/contracts/**`, data models in `specs/truth/data/**`, the stack in
  `specs/truth/techstack.md`, and executable interface features + DSL in `specs/truth/features/**`.
  Do not create a package-local `contracts/` or `data-model.md`; those layouts predate this design.
-->

### Source Structure (repository root)

```text
{{SOURCE_ROOT_1}}/
├── {{SOURCE_ROOT_1_DIR_1}}/
│   ├── {{SOURCE_ROOT_1_FILE_1}}
│   ├── {{SOURCE_ROOT_1_DIR_2}}/
│   ├── {{SOURCE_ROOT_1_DIR_3}}/
│   └── {{SOURCE_ROOT_1_DIR_4}}/
├── {{SOURCE_ROOT_1_DIR_5}}/
│   ├── {{SOURCE_ROOT_1_FILE_2}}
│   └── {{SOURCE_ROOT_1_DIR_6}}/
└── {{SOURCE_ROOT_1_DIR_7}}/

{{SOURCE_ROOT_2}}/
├── {{SOURCE_ROOT_2_FILE_1}}
├── {{SOURCE_ROOT_2_DIR_1}}/
│   ├── {{SOURCE_ROOT_2_FILE_2}}
│   ├── {{SOURCE_ROOT_2_DIR_2}}/
│   ├── {{SOURCE_ROOT_2_DIR_3}}/
│   └── {{SOURCE_ROOT_2_DIR_4}}/
└── {{SOURCE_ROOT_2_DIR_5}}/
```

**Structure Decision**: {{STRUCTURE_DECISION}}

## Analysis Process Planning

### System Interface Inventory

This requirement's inventory finds `{{SYSTEM_INTERFACE_COUNT}}` system interfaces.

1. `{{SYSTEM_INTERFACE_1_NAME}}`
   - Endpoint type: `{{SYSTEM_INTERFACE_1_ENDPOINT_TYPE}}`
   - Main interfaces: `{{SYSTEM_INTERFACE_1_PRIMARY_INTERFACE}}`
   - Requirement basis: `{{SYSTEM_INTERFACE_1_REQUIREMENT_EVIDENCE}}`
   - Delegation: `{{SYSTEM_INTERFACE_1_DELEGATION}}`

2. `{{SYSTEM_INTERFACE_2_NAME}}`
   - Endpoint type: `{{SYSTEM_INTERFACE_2_ENDPOINT_TYPE}}`
   - Main interfaces: `{{SYSTEM_INTERFACE_2_PRIMARY_INTERFACE}}`
   - Requirement basis: `{{SYSTEM_INTERFACE_2_REQUIREMENT_EVIDENCE}}`
   - Delegation: `{{SYSTEM_INTERFACE_2_DELEGATION}}`

3. `{{SYSTEM_INTERFACE_3_NAME}}`
   - Endpoint type: `{{SYSTEM_INTERFACE_3_ENDPOINT_TYPE}}`
   - Main interfaces: `{{SYSTEM_INTERFACE_3_PRIMARY_INTERFACE}}`
   - Requirement basis: `{{SYSTEM_INTERFACE_3_REQUIREMENT_EVIDENCE}}`
   - Delegation: `{{SYSTEM_INTERFACE_3_DELEGATION}}`

<!--
  Add or remove entries per the technical endpoints actually involved in the requirement.
  Every entry must map back to the requirement text; do not invent system interfaces not touched by the requirement.
  If one system interface carries multiple user-perceivable responsibilities at once, account for them together in the "Main interfaces" field.
-->

### Analysis Process Arrangement

#### Wave 1

- Parallel analysis interfaces:
  - `{{WAVE_1_INTERFACE_1}}`
  - `{{WAVE_1_INTERFACE_2}}`
- Analysis focus:
  - `{{WAVE_1_ANALYSIS_FOCUS_1}}`
  - `{{WAVE_1_ANALYSIS_FOCUS_2}}`
- Arrangement rationale: `{{WAVE_1_PLANNING_RATIONALE}}`
- Delegation order:
  - `{{WAVE_1_DELEGATION_ORDER_1}}`
  - `{{WAVE_1_DELEGATION_ORDER_2}}`   <!-- repeat per delegation; delete unused rows -->

#### Wave 2

- Parallel analysis interfaces:
  - `{{WAVE_2_INTERFACE_1}}`
  - `{{WAVE_2_INTERFACE_2}}`
- Analysis focus:
  - `{{WAVE_2_ANALYSIS_FOCUS_1}}`
  - `{{WAVE_2_ANALYSIS_FOCUS_2}}`
- Arrangement rationale: `{{WAVE_2_PLANNING_RATIONALE}}`
- Delegation order:
  - `{{WAVE_2_DELEGATION_ORDER_1}}`
  - `{{WAVE_2_DELEGATION_ORDER_2}}`   <!-- repeat per delegation; delete unused rows -->

<!--
  Planning must observe:
  1. Every inventoried system interface must appear at least once in some Wave.
  2. Within the same Wave, only place one or more interfaces that can be analyzed in parallel.
  3. Every Wave must account for what that wave really analyzes — not just list interface names.
  4. Wave ordering must reflect requirement dependencies; later Waves mean greater dependence on earlier waves' analysis results — do not group arbitrarily.
  5. This section only plans the analysis order, wave splits, and per-wave focus; do not expand each interface's actual analysis output here.
  6. If the requirement involves more endpoint interfaces or longer dependency chains, continue the `#### Wave N` skeleton downward.
  7. Every inventoried interface must carry exactly one `Delegation` value, using that exact
     spelling (the same field name every rule and example in
     `rules/analysis-interface-delegation-and-planner-mapping-criteria.md` uses): a planner skill
     (`/axb-api-plan`, `/axb-data-plan`), or an explicit taker (`Taken over by: ...`) when no
     planner applies — the PM's existing `ui/**` reviewed read-only, or `/axb-dsl-refine` for a
     CLI contract. Rule 2 decides which; do not leave it blank.
  8. `Delegation order` lists this Wave's delegations in **launch order**, including merged
     handoffs (Rule 3). Launch order and parallel analysis are not in conflict: entries listed
     consecutively in the same Wave may be started in parallel, and the order decides only what is
     launched first when that matters (a merged handoff must launch before the entries it absorbs,
     and a Wave whose analysis is genuinely sequential must say so in its `Arrangement rationale`).
     Rule 1 delegates by this list, so an omitted entry is an unimplementable plan rather than a
     formatting slip. Continue the list downward per delegation; a Wave with one delegation keeps
     one row.
-->
