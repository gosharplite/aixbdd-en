# Rule 1 - Before delivering tasks.md, run the full coverage scan (Pre-Delivery Orphan Coverage Sweep)

- Level: `MUST`
- After writing `tasks.md` and before formal delivery, all of this round's input artifacts and decided decisions must be inventoried to ensure no decision or truth state becomes an un-consumed Orphaned Artifact.
- Downstream `/axb-implement` is limited by the minimal-context principle (`skills/axb-implement/rules/technical-reference-loading-and-minimal-context-criteria.md`): implementation subagents read only the task's `Read` and the phase `Shared Must Read`, and must not pre-read `research.md` or other truth in full on their own. Therefore items not referenced by a task `Read` or directly delivered effectively vanish at the implementation layer.
- Concrete scan and assertion items include:
  1. **`truth-delta.md` non-NOOP items**: all truth rows marked `ADD`, `MODIFY`, `DELETE` this round (including API contracts, data models, techstack, interface features/dsl) must be 100% assigned to tasks in the corresponding phase (Phase 1 Setup, Phase 2 Foundational, Phase 3 Test Alignment, or Phase 4 Feature).
  2. **`research.md` decided Decisions**: all normative, algorithmic, architectural, or selection decisions must be referenced by at least one task's `Read` (e.g. `Read: research.md -> Decision 3`), or directly delivered by a concrete task; negative decisions (e.g. excluding a package), if they constitute implementation constraints, should be explicitly stated in the relevant task's `Boundary` or `Read`.
  3. **`specs/truth/techstack.md` added or changed sections**: those involving compile parameters, version injection (e.g. `VERSION` ldflags), test helper targets (e.g. `make verify-no-test-sleep`), test runner commands, etc., must be referenced by and concretely landed in Setup or Foundational build/verification tasks' `Read`.
- **NOOP item exemption**: `NOOP` items in `truth-delta.md` are audit records checked with no changes needed; implementation tasks must not be created for them.
- **Empty-set exemption**: if this round has no `research.md`, or that file has no decided Decisions, that item is an empty set and the scan passes directly; do not fabricate decisions or create tasks out of thin air.
- If any non-NOOP truth row or decided Decision is uncovered, `tasks.md` is judged failed and must not be delivered.

## Good Example

- This example is good because before delivery it asserts one by one that every decision and truth has task coverage or a reference.

```md
Pre-Delivery Orphan Coverage Sweep cross-reference:
- research.md Decision 3 (6-step resolver algorithm) -> referenced in T018 [BDD-GREEN]'s Read
- research.md Decision 6 & techstack.md VERSION declaration -> referenced in T001 Setup's Read and bound to compile parameters
- research.md Decision 7 & techstack.md verify target -> concretely landed by T002 Makefile task
- truth-delta.md 5 non-NOOP rows -> correspond to T008–T012 (Phase 3) and T016 (Phase 4) respectively
- Orphaned artifact count: 0. Scan passed; delivery approved.
```

## Bad Example

- This example is bad because it checks only format, missing the core algorithm and build parameters decided in research.md.

```md
Checked that tasks are all `- [ ] T###` and Feature phases have Test Scope, then delivered directly.
Result:
- research.md Decision 3's parsing algorithm is read by no task; subagents can only guess during implementation.
- techstack.md's VERSION and make verify-no-test-sleep are missing; no task establishes the corresponding configuration.
```

# Rule 2 - Orphaned artifacts must be eliminated by adding tasks or supplementing Read references

- Level: `MUST`
- When the Pre-Delivery scan finds orphaned decisions or specs:
  - If the item is infrastructure, configuration, scripts, or make targets to be built (e.g. missing build parameters or verification commands), a corresponding task must be added in Phase 1 (`Setup`) or Phase 2 (`Foundational`).
  - If the item is concrete business logic, data rules, or algorithm details, that section must be added to the corresponding Feature phase's `Shared Must Read` or a concrete task's `Read`.
  - Do not eliminate orphan warnings by deleting `research.md` decisions, force-changing non-NOOP to NOOP, or ignoring the scan results.

## Good Example

- This example is good because upon finding an omission it immediately adds the task and Read in the correct Phase.

```md
Scan found: `research.md` Decision 7's adopted `verify-no-test-sleep` is not referenced.
Fix: add that Decision to T002's (Foundational Makefile task) Read, and explicitly require adding that make target in the task description.
Re-scan: orphaned artifact count is 0.
```

## Bad Example

- This example is bad because upon finding an orphaned decision it chooses to ignore it or delete the decision privately.

```md
Scan found Decision 6 (VERSION parameter) is read by no one; the agent thinks it unimportant, declares verification passed and delivers without adding a task.
```

# Rule 3 - Before delivering tasks.md, run the Claim→Witness Coverage Sweep

- Level: `MUST`
- After writing `tasks.md` and before formal delivery, a Claim→Witness Coverage Sweep must be run against all of this round's normative items and truth-surface claims, and a `Claim→Witness Ledger` must be output in `tasks.md`.
- **Promotion Gate principle**: no normative item (FR / NFR / SC / EC) or truth-surface prose guarantee may ever be promoted to truth without a witness. Existing truth is audited triggered-on-contact.
- Concrete inventory and classification requirements:
  1. **The distillation unit is the "Atomic Effect Claim"**:
     - Perform a surface-anchored text walk from `spec.md`'s coarse-grained verification intent hints and the truth surfaces modified this round (`specs/truth/**`, including `techstack.md`, `dsl.md` preambles, DBML notes, etc.).
     - Each claim must be distilled into a single atomic effect (e.g. "on rollback failure the old history file's bytes are unchanged", "a crash leaves no stray temp files").
     - Mechanism details (e.g. using temp file rename) must not masquerade as effect claims unless the means IS the contract (e.g. "no external network requests"); and **effect-strength calibration** must be performed — in-process crash-safety must not be over-claimed as power-loss durability.
  2. **Observable claims routing**:
     - Those directly observable through external interfaces or Gherkin acceptance flows must correspond to Features / DSL under `specs/truth/features/**` and be bound to Phase 4's `[BDD-GREEN]` implementation tasks.
  3. **Unobservable claims routing**:
     - Internal invariants, durability, atomicity, or failure handling not externally observable via Gherkin must have dedicated `[WITNESS]` tasks.
     - `[WITNESS]` tasks must explicitly state `Dependencies: T###`, `Test Scope` (unit tests or fault-injection seams), and `Falsifier` (the discriminating mutation that can break the guarantee).
  4. **Witness-exempt approval and anti-laundering clause**:
     - Those evaluated as genuinely unable to have automated witnesses must go through the exhaustive ladder check (`effect/fault-injection` → `mechanism-seam` → only when both fail may `accepted-unwitnessed` be evaluated).
     - `accepted-unwitnessed` must have a clear rationale and an explanation of "why no input can invalidate it", and must be decided and recorded by the **human decision maker** on the project's declared decision surface (e.g. the project ADR); AI agents are strictly forbidden from declaring it themselves.
     - If a claim is Demoted, the prose must be thoroughly deleted from all of this round's truth surfaces (techstack, dsl prologue, dbml, etc.), leaving no half-baked unwitnessed text.
- If any normative claim is carried by neither `[BDD-GREEN]` nor `[WITNESS]` and is not legitimately recorded as `accepted-unwitnessed` on the project decision surface, `tasks.md` is judged failed and delivery is strictly forbidden.

## Good Example

- This example is good because before delivery it inventories unobservable claims one by one, distills them into atomic effects, and binds discriminating witness tasks.

```md
Claim→Witness Ledger:
- NFR-001's prototype claim "the rollback operation is atomic and durable" is distilled into two atomic effects:
  1. CLM-001 (a crash during rollback leaves the old file uncorrupted) -> [WITNESS] T015 (Test Scope: internal/store/rollback_test.go, Falsifier: test turns red when mutated to in-place write)
  2. CLM-002 (rollback flush-to-disk durability) -> [WITNESS] T016 (Test Scope: internal/store/fsync_test.go, Falsifier: test turns red when f.Sync() is commented out)
- CLM-003 (cross-datacenter power-loss consistency) -> ladder evaluation deems automated testing infeasible; the human decision maker approved accepted-unwitnessed in project ADR-0053, and the truth surface prose guarantee has been removed.
- Unwitnessed and unapproved claim count: 0. Scan passed; delivery approved.
```

## Bad Example

- This example is bad because it lets a normative MUST item pass as background knowledge, leaving it in truth prose with no witness task at all.

```md
Checked that truth-delta's table has corresponding tasks, then declared done.
Result:
- spec.md NFR-001's "the rollback operation must have atomicity: write temp file + fsync + atomic rename" has no [WITNESS] task.
- techstack.md and dsl.md preambles record that atomicity guarantee, but removing fsync from the whole test suite still leaves it all green.
```

