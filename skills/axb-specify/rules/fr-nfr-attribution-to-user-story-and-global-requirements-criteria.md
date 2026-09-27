# Rule 1 - FR / NFR reasonably attributable to a single story must hang directly under that story

- Level: `MUST`
- If an FR or NFR mainly serves a single user story's establishment, acceptance, or experience, it must be listed directly under that story — not scattered into a master list outside the stories.
- When attributing, first judge which piece of user value the requirement supports, rather than grouping all FRs together and all NFRs together by requirement type first.
- If a story currently has no dedicated NFR, do not force one in; but do not leave an NFR that clearly belongs to that story in the global section just for tidying convenience.

## Good Example

- This example is good because the browsing-related FR / NFR all hang directly under "Browse date albums on the homepage".

````md
### User Story 2 - Browse date albums on the homepage (Priority: P2)

**Functional Requirements (FR)**:
- **FR-005**: The system MUST display all date albums on the homepage sorted from newest to oldest by date.
- **FR-006**: The system MUST present photos as a tiled preview within each date album.

**Non-Functional Requirements (NFR)**:
- **NFR-001**: When the homepage load includes up to 200 visible photos, a browsable screen presentation MUST complete within 2 seconds in 95% of cases.
````

## Bad Example

- This example is bad because it leaves a requirement clearly belonging to a single story outside the story, weakening the story-requirement hierarchy.

````md
### User Story 2 - Browse date albums on the homepage (Priority: P2)

**Acceptance scenarios**:
1. **Given** ...

## Requirements

### Functional Requirements
- **FR-005**: The system MUST display all date albums on the homepage sorted from newest to oldest by date.

### Non-Functional Requirements
- **NFR-001**: When the homepage load includes up to 200 visible photos, a browsable screen presentation MUST complete within 2 seconds in 95% of cases.
````

# Rule 2 - Global requirements keep only what spans multiple stories or cannot reasonably belong to one story

- Level: `MUST`
- `Global Requirements` should keep only FR / NFR that simultaneously constrain multiple user stories, or that inherently cannot reasonably be assigned to a single story.
- If a requirement is only indirectly used by multiple stories but mainly still serves one of them, attribute it to that story first; do not over-expand global requirements.
- The global requirements section exists for exceptions, not as a default collection point.

## Good Example

- This example is good because "albums must not be nested" affects organization, browsing, and sorting at the same time, so it stays in global requirements.

````md
## Requirements *(required)*

### Global Requirements

#### Functional Requirements
- **FR-003**: The system MUST keep all albums as single-level top-level albums, with no nested album structure.
````

## Bad Example

- This example is bad because it puts a requirement clearly related only to drag-and-drop sorting into global requirements, distorting attribution.

````md
### Global Requirements

#### Functional Requirements
- **FR-009**: The system MUST prevent drag-and-drop sorting from changing the date album a photo belongs to.
````

# Rule 3 - After attribution, a requirement must not be listed in multiple places

- Level: `SHOULD`
- After attribution, the same FR or NFR should appear in only one most-appropriate location, not copied into both the story area and the global requirements area.
- If the same concept genuinely needs to be mentioned in multiple places, the story area keeps the formal requirement statement; other locations keep only narrative explanation, without duplicating numbered entries.
- Requirement numbering should remain unique, avoiding one requirement appearing in multiple places with different narrative versions.

## Good Example

- This example is good because the formal requirement appears in only one place; other mentions are merely explanatory context.

````md
### User Story 3 - Adjust photo order via drag-and-drop (Priority: P3)

**Functional Requirements (FR)**:
- **FR-009**: The system MUST prevent drag-and-drop sorting from changing the date album a photo belongs to.

### Edge Cases
- When the user attempts to drag a photo into another date album, the system must still preserve the original date grouping.
````

## Bad Example

- This example is bad because the same requirement is formally listed in both the story area and the global requirements area.

````md
### User Story 3 - Adjust photo order via drag-and-drop (Priority: P3)

**Functional Requirements (FR)**:
- **FR-009**: The system MUST prevent drag-and-drop sorting from changing the date album a photo belongs to.

### Global Requirements

#### Functional Requirements
- **FR-009**: The system MUST prevent drag-and-drop sorting from changing the date album a photo belongs to.
````

# Rule 4 - A local gap that does not block the whole spec should be marked NEEDS CLARIFICATION, not filled in out of thin air

- Level: `SHOULD`
- If a requirement's existence is already confirmed, but its concrete approach, quantitative threshold, or applicable scope is not yet decided, and the gap is insufficient to block the whole spec, use the `NEEDS CLARIFICATION` marker to preserve the gap.
- Only when the gap would directly change story splitting, requirement attribution, main flows, or acceptance criteria should you return to `/axb-clarify` first.
- Do not invent unconfirmed requirement details on the user's behalf just to make the document look complete.

## Good Example

- This example is good because it keeps the unconfirmed details without disguising them as settled requirements.

````md
- **NFR-004**: The system MUST provide understandable progress feedback on homepage load [NEEDS CLARIFICATION: not yet specified whether skeleton screen, progress bar, or another presentation]
````

## Bad Example

- This example is bad because it decides unconfirmed details on the user's behalf directly.

````md
- **NFR-004**: The system MUST display homepage loading progress with a blue linear progress bar.
````
