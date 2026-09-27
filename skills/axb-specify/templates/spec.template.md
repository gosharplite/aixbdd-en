# Functional Spec: {{FEATURE_TITLE}}

**Feature Branch**: `{{FEATURE_BRANCH}}`

**Created Date**: {{CREATED_DATE}}

**Status**: Draft

**Input**: User description: "{{USER_INPUT}}"

## User Scenarios & Testing *(required)*

<!--
  Important: user stories must be ordered by business value and delivery priority.
  Every user story must be independently testable — i.e., implementing only a single story
  must still form a demonstrable, verifiable, deliverable minimal viable increment.

  Each story should directly hold:
  1. Acceptance scenarios (Acceptance Criteria)
  2. Story-specific Functional Requirements (FR)
  3. Story-specific Non-Functional Requirements (NFR, if any)

  Claim→Witness Obligation (Verification Intent annotation):
  Every normative item (FR / NFR / SC / EC) must be annotated with a Verification Intent:
  - observable → <corresponding acceptance scenario or Rule>: externally observable and verifiable via acceptance Gherkin.
  - unobservable → <expected witness level>: not observable by external Gherkin; requires unit pins or fault-injection seams at the implementation layer (e.g. unit pin, fault-injection seam).
  - accepted-unwitnessed: approved via the project decision surface as witness-exempt (must comply with the anti-washing clause and must not be abused).
  Leaving any normative item without a Verification Intent annotation is strictly forbidden.

  Only requirements that genuinely cannot reasonably belong to a single user story,
  or that explicitly span multiple stories, should go into the "Global Requirements" section below.
-->

### User Story 1 - {{USER_STORY_1_TITLE}} (Priority: P1)

{{USER_STORY_1_NARRATIVE}}

**Why this priority**: {{USER_STORY_1_PRIORITY_RATIONALE}}

**Independent verification method**: {{USER_STORY_1_TEST_APPROACH}}

**Acceptance scenarios**:

1. **Given** {{USER_STORY_1_SCENARIO_1_GIVEN}}, **When** {{USER_STORY_1_SCENARIO_1_WHEN}}, **Then** {{USER_STORY_1_SCENARIO_1_THEN}}
2. **Given** {{USER_STORY_1_SCENARIO_2_GIVEN}}, **When** {{USER_STORY_1_SCENARIO_2_WHEN}}, **Then** {{USER_STORY_1_SCENARIO_2_THEN}}

**Functional Requirements (FR)**:

- **FR-001**: The system MUST {{USER_STORY_1_FR_001}} [Verification Intent: observable → acceptance scenario 1]
- **FR-002**: The system MUST {{USER_STORY_1_FR_002}} [Verification Intent: observable → acceptance scenario 1]
- **FR-003**: The user MUST be able to {{USER_STORY_1_FR_003}} [Verification Intent: observable → acceptance scenario 2]

<!--
  If this story currently has no dedicated NFR, delete this subsection;
  if the requirement actually spans multiple stories, move it to "Global Requirements".
-->
**Non-Functional Requirements (NFR)**:

- **NFR-001**: {{USER_STORY_1_NFR_001}} [Verification Intent: unobservable → {{USER_STORY_1_NFR_001_WITNESS_TIER}}]

---

### User Story 2 - {{USER_STORY_2_TITLE}} (Priority: P2)

{{USER_STORY_2_NARRATIVE}}

**Why this priority**: {{USER_STORY_2_PRIORITY_RATIONALE}}

**Independent verification method**: {{USER_STORY_2_TEST_APPROACH}}

**Acceptance scenarios**:

1. **Given** {{USER_STORY_2_SCENARIO_1_GIVEN}}, **When** {{USER_STORY_2_SCENARIO_1_WHEN}}, **Then** {{USER_STORY_2_SCENARIO_1_THEN}}

**Functional Requirements (FR)**:

- **FR-004**: The system MUST {{USER_STORY_2_FR_004}} [Verification Intent: observable → acceptance scenario 1]
- **FR-005**: The system MUST {{USER_STORY_2_FR_005}} [Verification Intent: observable → acceptance scenario 1]

**Non-Functional Requirements (NFR)**:

- **NFR-002**: {{USER_STORY_2_NFR_002}} [Verification Intent: unobservable → {{USER_STORY_2_NFR_002_WITNESS_TIER}}]

---

### User Story 3 - {{USER_STORY_3_TITLE}} (Priority: P3)

{{USER_STORY_3_NARRATIVE}}

**Why this priority**: {{USER_STORY_3_PRIORITY_RATIONALE}}

**Independent verification method**: {{USER_STORY_3_TEST_APPROACH}}

**Acceptance scenarios**:

1. **Given** {{USER_STORY_3_SCENARIO_1_GIVEN}}, **When** {{USER_STORY_3_SCENARIO_1_WHEN}}, **Then** {{USER_STORY_3_SCENARIO_1_THEN}}

**Functional Requirements (FR)**:

- **FR-006**: The system MUST {{USER_STORY_3_FR_006}} [Verification Intent: observable → acceptance scenario 1]

**Non-Functional Requirements (NFR)**:

- **NFR-003**: {{USER_STORY_3_NFR_003}} [Verification Intent: unobservable → {{USER_STORY_3_NFR_003_WITNESS_TIER}}]

---

<!--
  Add more user stories as needed, continuing the same skeleton:
  title, narrative, priority rationale, independent verification method, acceptance scenarios, story-specific FR, story-specific NFR.
-->

### Edge Cases

- **EC-001**: When {{EDGE_CASE_1_CONDITION}} occurs, the system MUST {{EDGE_CASE_1_EXPECTED_BEHAVIOR}} [Verification Intent: observable → {{EDGE_CASE_1_VERIFICATION_TARGET}}]
- **EC-002**: When {{EDGE_CASE_2_CONDITION}} occurs, the system MUST {{EDGE_CASE_2_EXPECTED_BEHAVIOR}} [Verification Intent: observable → {{EDGE_CASE_2_VERIFICATION_TARGET}}]
- **EC-003**: When {{EDGE_CASE_3_CONDITION}} occurs, the system MUST {{EDGE_CASE_3_EXPECTED_BEHAVIOR}} [Verification Intent: observable → {{EDGE_CASE_3_VERIFICATION_TARGET}}]

## Requirements *(required)*

> Each user story's dedicated FR / NFR should be listed directly under the story; this section keeps only global requirements that cannot reasonably belong to a single user story, or that explicitly span multiple user stories.

### Global Requirements

#### Functional Requirements

- **FR-007**: The system MUST {{GLOBAL_FR_007}} [Verification Intent: observable → {{GLOBAL_FR_007_VERIFICATION_TARGET}}]

<!--
  If there are currently no cross-story global functional requirements, delete this subsection.
-->

#### Non-Functional Requirements

- **NFR-004**: {{GLOBAL_NFR_004}} [Verification Intent: unobservable → {{GLOBAL_NFR_004_WITNESS_TIER}}]

<!--
  If a requirement is still unclear, use the following format to mark it:

  - **FR-XXX**: The system MUST {{REQUIREMENT_TEXT}} [NEEDS CLARIFICATION: {{CLARIFICATION_GAP}}]
  - **NFR-XXX**: {{NON_FUNCTIONAL_REQUIREMENT_TEXT}} [NEEDS CLARIFICATION: {{CLARIFICATION_GAP}}]
-->

### Key Entities *(required if the feature involves data)*

- **{{ENTITY_1_NAME}}**: {{ENTITY_1_DESCRIPTION}}
- **{{ENTITY_2_NAME}}**: {{ENTITY_2_DESCRIPTION}}

## Success Criteria *(required)*

<!--
  Define measurable, technology-neutral, and verifiable success criteria.
-->

### Measurable Outcomes

- **SC-001**: {{SUCCESS_CRITERION_001}} [Verification Intent: observable → {{SUCCESS_CRITERION_001_VERIFICATION_TARGET}}]
- **SC-002**: {{SUCCESS_CRITERION_002}} [Verification Intent: unobservable → {{SUCCESS_CRITERION_002_WITNESS_TIER}}]
- **SC-003**: {{SUCCESS_CRITERION_003}} [Verification Intent: observable → {{SUCCESS_CRITERION_003_VERIFICATION_TARGET}}]

## Assumptions

- {{ASSUMPTION_1}}
- {{ASSUMPTION_2}}
- {{ASSUMPTION_3}}
