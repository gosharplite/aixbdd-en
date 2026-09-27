# Rule 1 - User stories must be split by independently verifiable user value

- Level: `MUST`
- Every user story must represent a piece of user value that can be understood, verified, and demonstrated independently — not merely cutting a feature list or technical work into pieces.
- If a requirement fragment has only internal implementation steps, data processing details, or UI component names without a corresponding clear user outcome, it should not be used directly as a user story title.
- Split stories should be able to answer "as who, wanting to accomplish what, therefore getting what value".

## Good Example

- This example is good because all three stories correspond to independent user outcomes, rather than force-splitting the requirements by sentence order.

````md
### User Story 1 - Automatically organize photos by date (Priority: P1)

As a user who wants to quickly organize life photos, I hope that after importing photos, the system can automatically distribute photos into different albums by date, so I don't have to manually create and classify each batch of photos.

### User Story 2 - Browse date albums on the homepage (Priority: P2)

As a user who wants to quickly review the organization results, I hope to see all date albums at once on the homepage, making it easy to quickly judge the contents and choose an album to organize.
````

## Bad Example

- This example is bad because it treats feature sentences or implementation fragments directly as stories, forming no complete user-value slices.

````md
### User Story 1 - Import photos
### User Story 2 - Date field parsing
### User Story 3 - Drag-and-drop component
````

# Rule 2 - User stories should be prioritized by business value and delivery order

- Level: `MUST`
- User story Priority must reflect user value and delivery order, with P1 representing the core value that needs proving first.
- If a later story's value builds on a previous story's established outcome, its priority should be ordered later; do not decide priority merely by prompt appearance order.
- Each story should include `why this priority`, clearly explaining the ranking rationale instead of just marking P1 / P2 / P3.

## Good Example

- This example is good because it delivers the core organization capability first, then the follow-up value of browsing and sorting.

````md
### User Story 1 - Automatically organize photos by date (Priority: P1)
**Why this priority**: This is the core value of the entire product; if date grouping cannot be done automatically, the subsequent browsing and sorting flows cannot stand.

### User Story 2 - Browse date albums on the homepage (Priority: P2)
**Why this priority**: After the user completes the automatic organization, the next high-value behavior is reviewing the results.
````

## Bad Example

- This example is bad because it marks priorities only by narrative order or personal preference, without aligning delivery dependencies and business value.

````md
### User Story 1 - Drag-and-drop to adjust photo order (Priority: P1)
**Why this priority**: Because drag-and-drop looks the coolest.

### User Story 2 - Automatically organize photos by date (Priority: P2)
**Why this priority**: Automatic grouping can be added later.
````

# Rule 3 - Every user story should keep the minimal necessary verification information

- Level: `SHOULD`
- Every user story should have at least a story narrative, a priority rationale, an independent verification method, and 1 or more acceptance scenarios — avoiding being just a title with a requirements list.
- The `independent verification method` should describe how to verify the story holds even when only that story is implemented.
- Acceptance scenarios should first cover the story's main success path, then add high-risk exception scenarios as needed.

## Good Example

- This example is good because it fills in the minimal necessary verification information, making the story more than a requirements container.

````md
### User Story 1 - Automatically organize photos by date (Priority: P1)

As a user who wants to quickly organize life photos, I hope that after importing photos, the system can automatically distribute photos into different albums by date.

**Independent verification method**: Import a set of photos containing multiple dates; confirm the system creates the corresponding albums and places the photos into the correct groups.

**Acceptance scenarios**:
1. **Given** the user imports multiple photos from different dates, **When** the import completes, **Then** the system creates the corresponding date albums and correctly distributes the photos.
````

## Bad Example

- This example is bad because it has only a story title, lacking information on how to verify the story holds.

````md
### User Story 1 - Automatically organize photos by date (Priority: P1)

Photos should be able to be organized automatically.
````
