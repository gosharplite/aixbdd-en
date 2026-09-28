# Rule 1 - The root constitution only carries governance boundaries, not artifact details

- Level: `MUST`
- `CONSTITUTION.md` is only responsible for defining governance principles, reading order, directory conventions, and rule format boundaries.
- If a requirement describes what fields, semantics, prohibitions, or examples an artifact of a certain skill should have,
  it must not be written into `CONSTITUTION.md`.
- Writing artifact details into the root constitution bloats the root file quickly and breaks the modular design.

## Good Example

- This example is good because the root constitution only keeps governance-level information.

````md
### V. The directory only keeps rules that are actually read

1. `CONSTITUTION.md`
2. `shared.md`
3. `skills/<current-skill>/<artifact>.md`
````

## Bad Example

- This example is bad because it stuffs API response details directly into the root constitution.

````md
### VI. API Response Rules

- All `200` responses must contain `roomId`
- All `409` responses must contain `errorCode`
````

# Rule 2 - Only rules that are genuinely cross-skill go into shared.md

- Level: `MUST`
- `shared.md` may only contain rules that are reused across multiple skills and multiple artifacts.
- If a rule actually serves only a single skill or a single artifact, it should go into `skills/<skill>/<artifact>.md`.
- Judge by "who directly consumes this rule", not by whether the rule's topic looks generic.

## Good Example

- This example is good because language consistency is used by multiple artifacts together.

````md
## Rule 1 - Descriptive text must be written in English
````

## Bad Example

- This example is bad because API responses are actually only used by the contract artifact of `/axb-api-plan`.

````md
## Rule 2 - Success and failure responses must be expressed separately
````

# Rule 3 - Skill rule files take the artifact as the smallest placement unit

- Level: `MUST`
- Each `.md` file under `skills/<skill>/` handles exactly one artifact.
- If the same skill produces both `spec.md` and `requirements-checklist.md`, they should be split into two files rather than mixed together.
- Two rules belong in the same file only when both constrain the same artifact.

## Good Example

- This example is good because each file under the skill directory maps to exactly one artifact.

````text
skills/axb-specify/spec.md
skills/axb-specify/requirements-checklist.md
````

## Bad Example

- This example is bad because rules for different artifacts are mixed into a single file.

````text
skills/axb-specify/constitution.md
# Contains all rules for both spec and requirements-checklist
````

# Rule 4 - The shared constitution must carry the Claim→Witness obligation and declare the project decision surface

- Level: `MUST`
- "A normative claim without a witness must never be promoted to truth (Claim→Witness Obligation)" is the highest governance principle spanning all skills, all phases, and all artifacts, and must be placed in the project's shared constitution `.agents/constitution/shared.md`.
- The project's `.agents/constitution/shared.md` must explicitly declare the project's **decision surface placement** (e.g., the project ADR directory `decisions/NNNN-*.md`). A normative claim for which no automated witness is established is an architecture decision and must be recorded on that declared decision surface (including rationale, anti-washing ladder review, and sign-off by the human decision maker) — it must never be kept as prose on any truth surface.
- If the project has not declared a decision surface placement, the Claim→Witness Obligation should block conditionally when encountering `accepted-unwitnessed`, until the project completes the declaration.

## Good Example

- This example is good because the shared constitution clearly defines the cross-skill Claim→Witness governance principle and the project decision surface placement.

````md
## Rule X - A normative claim without a witness must not be promoted to Truth (Claim→Witness Obligation)

- Any normative item (FR / NFR / SC / EC) or system behavior guarantee must have an executable falsification witness (observable ones are carried by Gherkin BDD, non-observable ones by [WITNESS] unit/fault-injection pins), otherwise it must not exist as truth in prose form.
- If ladder review confirms it is a decision that cannot be witnessed automatically, it must be recorded on this project's decision surface: `decisions/NNNN-*.md`, and approved by the human decision maker.
- Claims that are neither witnessed nor recorded on the decision surface are strictly forbidden from appearing on any specs/truth/** surface.
````

## Bad Example

- This example is bad because it treats a globally applicable witness obligation as a local detail of a single skill (e.g., axb-tasks), leaving other truth owners with unprotected prose truths.

````md
### Only axb-tasks checks witnesses; other skills are free to write unwitnessed guarantees into techstack.md or dsl.md.
````

