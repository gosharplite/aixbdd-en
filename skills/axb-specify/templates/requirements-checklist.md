# Spec Quality Checklist: {{FEATURE_TITLE}}

**Created Date**: {{CREATED_DATE}}

**Feature Directory**: `{{FEATURE_DIRECTORY}}`

**Spec Path**: `{{SPEC_FILE}}`

## How to Use

- Check each item against the current `spec.md` content.
- If an item fails, add the concrete gap and fix direction in "Issues & Fix Log".
- If `NEEDS CLARIFICATION` remains, explicitly state whether it blocks downstream planning.

## Content Completeness

- [ ] All required sections are complete
- [ ] The feature topic, scope, and main flows are clearly expressed
- [ ] No implementation technologies, frameworks, or code details are written as requirements
- [ ] Edge cases cover the main high-risk scenarios
- [ ] Key entities and success criteria are filled in, or explicitly explained as not applicable

## User Stories & Requirement Attribution

- [ ] User stories are ordered by business value and delivery order
- [ ] Every user story can be independently verified
- [ ] Every user story includes acceptance scenarios
- [ ] FR / NFR attributable to a single story hang directly under that story
- [ ] Global requirements keep only cross-story or un-attributable entries
- [ ] Formal requirements are not duplicated between the story area and the global requirements area

## Gaps & Clarify Strategy

- [ ] Only high-impact gaps escalate to `/axb-clarify`
- [ ] This round's clarify question count is kept to 1 to 3 questions
- [ ] Low-risk undecided details are disclosed via `NEEDS CLARIFICATION` or assumptions
- [ ] Remaining `NEEDS CLARIFICATION` items are marked whether they block downstream planning

## Verifiability & Success Criteria

- [ ] Acceptance scenarios suffice to verify the main success paths
- [ ] Success criteria are measurable, verifiable, and technology-neutral
- [ ] All normative items (FR / NFR / SC / EC) are annotated with a Verification Intent
- [ ] Assumptions express only premises and boundaries, without smuggling in new requirements
- [ ] Requirements, edge cases, key entities, and success criteria are consistent with each other

## Issues & Fix Log

- {{ISSUE_NOTE_1}}
- {{ISSUE_NOTE_2}}
- {{ISSUE_NOTE_3}}

## Ready Judgment

- [ ] Ready to proceed to downstream planning
- [ ] High-impact requirement gaps still need filling first

**Note**: {{FINAL_NOTE}}
