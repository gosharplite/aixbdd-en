# Rule 1 - Every user story must form a complete minimal verification slice

- Level: `MUST`
- Every user story must contain at least a story narrative, Priority, priority rationale, independent verification method, and 1 or more acceptance scenarios, so readers can understand how the story is verified independently.
- Each story should have its own `Functional Requirements (FR)` section; `Non-Functional Requirements (NFR)` may be omitted or deleted if genuinely absent, but empty shell sections must not be left behind.
- If a story lacks the necessary verification information and has only a title with a requirements list, it should be treated as an incomplete story, not a format-passing one.

## Good Example

- This example is good because it retains the minimal verification information and requirement attribution needed for the story to stand.

````md
### User Story 1 - Automatically organize photos by date (Priority: P1)

As a user who wants to quickly organize life photos, I hope that after importing photos, the system can automatically distribute photos into different albums by date.

**Why this priority**: This is the core value of the entire product.

**Independent verification method**: Import a set of photos containing multiple dates; confirm the system creates the corresponding albums and places the photos into the correct groups.

**Acceptance scenarios**:
1. **Given** the user imports multiple photos from different dates, **When** the import completes, **Then** the system creates the corresponding date albums and correctly distributes the photos.

**Functional Requirements (FR)**:
- **FR-001**: The system MUST allow the user to import one or more photos.
````

## Bad Example

- This example is bad because the story lacks verification and requirement attribution information, insufficient to be a complete slice.

````md
### User Story 1 - Automatically organize photos by date (Priority: P1)

Photos should be able to be organized by date.
````

# Rule 2 - Global requirements must truly contain only "outside-stories but still necessary" content

- Level: `MUST`
- The `Global Requirements` section may keep only cross-story requirements or entries that cannot reasonably belong to a single story; if global requirements are empty, the blank content in that subsection may be deleted, but the overall structural intent of the requirements section should be preserved.
- During self-check, confirm again whether story-specific requirements are mistakenly left in global requirements, or whether global-requirement entries can already be reasonably attributed to a story.
- Do not let global requirements regress into the old-style FR / NFR master list.

## Good Example

- This example is good because global requirements keep only cross-story constraints, without reverting to a master requirements pool.

````md
## Requirements *(required)*

### Global Requirements

#### Functional Requirements
- **FR-003**: The system MUST keep all albums as single-level top-level albums, with no nested album structure.
````

## Bad Example

- This example is bad because it re-gathers all stories' requirements into the global area, breaking the new hierarchical design.

````md
## Requirements *(required)*

### Global Requirements

#### Functional Requirements
- **FR-001**: The system MUST allow the user to import photos.
- **FR-005**: The system MUST display date albums on the homepage.
- **FR-007**: The user MUST be able to rearrange photos via drag-and-drop.
````

# Rule 3 - Success criteria must be measurable; assumptions must not smuggle in new requirements

- Level: `MUST`
- `Success Criteria` must be measurable and verifiable; avoid writing only abstract feelings or vague visions.
- `Assumptions` may record only the reasonable premises, scope boundaries, or existing conditions the current reasoning relies on; do not sneak in new must-do features.
- If some content, once removed, would change the product's must-have behavior, it is more likely a requirement than an assumption.

## Good Example

- This example is good because the success criteria are verifiable and the assumptions explicitly express premises and boundaries.

````md
### Measurable Outcomes
- **SC-001**: In the acceptance dataset, 100% of photos with valid date information automatically appear in the corresponding date albums.

## Assumptions
- Drag-and-drop sorting only adjusts the display order within the same date album and does not include cross-album moves.
````

## Bad Example

- This example is bad because the success criteria are not measurable and the assumptions smuggle in new product requirements.

````md
### Measurable Outcomes
- **SC-001**: Users will find organizing photos very convenient.

## Assumptions
- The system must support AI auto-generating album names and covers.
````

# Rule 4 - When encountering low-risk undecided details, preserve the gap instead of force-filling

- Level: `SHOULD`
- If the whole spec's main stories, requirement attribution, and acceptance logic all hold, but a few details remain undecided, prefer `NEEDS CLARIFICATION` markers or explicitly stating premises in assumptions — rather than pretending the requirements are confirmed.
- If a gap already affects core flows, story splitting, or formal requirement logic, it is not a low-risk detail; return to `/axb-clarify`.
- During self-check, especially inspect the document for seemingly complete but actually unsourced numeric thresholds, interaction rules, or scope limits.

## Good Example

- This example is good because it preserves the gap and explicitly discloses what is not yet confirmed.

````md
- **NFR-004**: The system MUST provide understandable recovery guidance when sorting fails [NEEDS CLARIFICATION: not yet specified whether a one-step undo or retry mechanism is needed]
````

## Bad Example

- This example is bad because it writes details with no source as established requirements.

````md
- **NFR-004**: The system MUST guide the user through recovery with a three-step wizard when sorting fails.
````

# Rule 5 - Every normative item (FR/NFR/SC/EC) must be annotated with a Verification Intent

- Level: `MUST`
- Every normative item (including story-specific and global FR, NFR, success criteria SC, and edge cases EC) must be annotated with its Verification Intent, conveying the verification path to the downstream RD planning stage:
  1. `observable → <corresponding acceptance scenario or Rule/Scenario identifier>`: verifiable externally through acceptance Gherkin by observing user behavior or black-box interfaces.
  2. `unobservable → <expected witness level>`: not directly observable by external Gherkin acceptance flows; requires unit test pins, fault-injection seams, or benchmarks at the implementation layer (e.g. `unit pin`, `fault-injection seam`).
  3. `accepted-unwitnessed`: approved via the project decision surface as witness-exempt (must comply with the anti-washing clause and must not be abused).
- Leaving any normative item unclassified or without a Verification Intent annotation is strictly forbidden.
- **PM hint responsibility and boundary**: What the PM side annotates at this stage is a coarse-grained intent hint. Based on the `spec-pm-authored` invariant, the RD side must not alter `spec.md` items on its own; instead, downstream `/axb-tasks` expands the requirements into concrete, atomic Atomic Effect Claims based on that hint and the truth-surface text, incorporating them into the Claim→Witness inventory cross-reference table.

## Good Example

- This example is good because every FR/NFR/EC is clearly marked with its verification intent and path.

````md
- **FR-001**: The system MUST allow the user to import one or more photos. [Verification Intent: observable → acceptance scenario 1]
- **NFR-001**: The rollback operation MUST keep the database file intact when handling failures. [Verification Intent: unobservable → fault-injection seam]
- **EC-001**: When disk space is insufficient, the system MUST throw a write failure error and leave no stray temp files. [Verification Intent: unobservable → unit pin]
````

## Bad Example

- This example is bad because the items carry strong normative requirements (MUST) with no explanation of how they are expected to be verified, causing non-observable requirements to be lost in later flows.

````md
- **NFR-001**: The rollback operation MUST have durability and atomicity: write temp file + fsync + atomic rename.
- When the system crashes, it MUST guarantee old data is not corrupted.
````

