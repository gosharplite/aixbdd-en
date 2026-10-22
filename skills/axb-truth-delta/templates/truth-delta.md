# Truth Delta: {{PLAN_ID}}

**Plan Package**: `specs/plans/{{PLAN_PACKAGE}}`
**Truth Root**: `specs/truth`

<!--
  Every section needs at least one row; no row may be left as its placeholder at delivery.
  A `NOOP` row's `Reason` must say which situation applies: "inspected, nothing needed" (the owner
  read its scope and found it sufficient) or "not applicable, by analysis decision" (no planner or
  owner applied this round, e.g. a plain CLI has no API surface, so axb-system-analysis skipped
  axb-api-plan and records that here on the owner's behalf).
-->

## /axb-technical-research

| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| {{TECHNICAL_RESEARCH_ACTION}} | `{{TECHNICAL_RESEARCH_TRUTH_SPEC}}` | {{TECHNICAL_RESEARCH_SUMMARY}} | {{TECHNICAL_RESEARCH_REASON}} |

## /axb-api-plan

| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| {{API_PLAN_ACTION}} | `{{API_PLAN_TRUTH_SPEC}}` | {{API_PLAN_SUMMARY}} | {{API_PLAN_REASON}} |

## /axb-data-plan

| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| {{DATA_PLAN_ACTION}} | `{{DATA_PLAN_TRUTH_SPEC}}` | {{DATA_PLAN_SUMMARY}} | {{DATA_PLAN_REASON}} |

## /axb-dsl-refine

| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| {{DSL_REFINE_ACTION}} | `{{DSL_REFINE_TRUTH_SPEC}}` | {{DSL_REFINE_SUMMARY}} | {{DSL_REFINE_REASON}} |
