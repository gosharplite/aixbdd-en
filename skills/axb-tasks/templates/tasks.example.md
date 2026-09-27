# Tasks: Room Chat Spec Adjustment

**Plan Package**: `specs/plans/004-room-chat-adjustment`
**Core Inputs**: `spec.md`, `plan.md`, `research.md`, `truth-delta.md`, `specs/truth/techstack.md`, `specs/truth/contracts/**`, `specs/truth/data/**`, `specs/truth/features/backend/**`, `specs/truth/features/frontend/**`, `ui/**`

## Task Binding Contract

- Every **development task** must correspond to an ADD / MODIFY / DELETE / NOOP semantic in `truth-delta.md`.
- This round's `research.md` decided Decisions and `specs/truth/**` non-NOOP items must be fully covered in the tasks' `Read` or delivery targets, leaving no orphaned artifacts (Pre-Delivery Orphan Coverage Sweep).
- Unobservable atomic effect claims (Atomic Effect Claims) derived from every normative item (FR / NFR / SC / EC) must be scheduled for `[WITNESS]` task coverage, or recorded as `accepted-unwitnessed` on the project decision surface; anything unwitnessed must never be promoted to truth surfaces in prose guarantee form (Claim→Witness Obligation).
- When tasks have ordering dependencies, the ordering constraint must be explicitly declared with `Dependencies: T###`.
- Setup / Foundational build or verification tasks derived from `research.md` Decisions (e.g. build parameters, version, make targets) need not correspond to `truth-delta.md` rows.
- Phase 1 `Setup` does only this round's new-technology infrastructure, technical environment, and final smoke-test; writes no DSL semantics and no product behavior.
- Phase 2 `Foundational` only establishes the implementation code, test-shared components, entry points, fixtures, helpers, and touchpoint skeletons for later work.
- Phase 3 `Test Alignment & Implementation`'s purpose: before writing product code, align the automated tests of all affected DSL this round with the latest truth first.
- Truth references must use `specs/truth/**` paths; only plan references use relative paths within the current plan package.

## Phase 1: Setup

**Goal**: This round's chat adds websockets. The backend uses FastAPI's built-in `WebSocket` to mount an endpoint; the test side uses `websockets` to connect. Prepare the package and connection configuration first, then use a smoke-test to confirm one websocket can be reached. Write no chat DSL semantics and no message-sending product behavior.

- [ ] T001 Add the `websockets` package and test connection configuration
  - Read:
    - `specs/truth/techstack.md` -> Backend, Testing & Verification
  - Add `websockets` to backend test dependencies.
  - Write the websocket URL clearly in test configuration (e.g. `ws://127.0.0.1:{port}/ws`) for subsequent tests to read; write no message-sending semantics.

- [ ] T002 Align the backend FastAPI websocket technical environment
  - Read:
    - `specs/truth/techstack.md` -> Backend test entry
    - `backend/` -> FastAPI app and test server mount point
  - FastAPI mounts a `WebSocket` endpoint (e.g. `/ws`) so the test server can accept `websockets` connections.
  - Only open connections; do not implement message sending, clearing, or rejection rules.

- [ ] T003 Smoke-test confirming `websockets` can connect to FastAPI `/ws`
  - Read:
    - `specs/truth/techstack.md` -> Testing & Verification
  - Use `websockets.connect` to hit T001's URL; stop once connectivity is confirmed.
  - Do not run this round's Feature; write no stepdef semantics.

## Phase 2: Foundational

**Goal**: Only establish the implementation code, test-shared components, entry points, fixtures, helpers, and touchpoint skeletons for later work, so later Phase 3 does not each re-open files or invent connection methods on their own. Semantic alignment does not go here.

- [ ] T004 Establish the chat test shared helper entry and skeleton
  - Read:
    - `truth-delta.md` -> `/axb-dsl-refine`'s chat ADD / MODIFY / DELETE rows
    - `backend/features/steps/shared/chat_helpers.py`
  - Only do: fix the helper at `backend/features/steps/shared/chat_helpers.py`, leaving function shells that later stepdefs will call.
  - Do not: write any sentence's StepDef 實作語意, nor message sending, clearing, or rejection rules.

- [ ] T005 Establish the websocket connection helper
  - Read:
    - `specs/truth/techstack.md` -> Testing & Verification
    - `backend/features/steps/shared/chat_helpers.py`
  - Only do: wrap open/close connections with `websockets.connect`; the context records "player name → connection"; close connections at scenario end.
  - Do not: send chat contents, nor assert who sees what.

- [ ] T006 Reserve the room-chat stepdef independent touchpoint skeleton (Zero Shared Edits principle)
  - Read:
    - `backend/features/steps/modules/room-chat/`
  - Only do: under `backend/features/steps/modules/room-chat/` create the stepdef independent touchpoint skeleton files (`when_send_msg.py`, `then_both_see_chat.py`, `then_opponent_see_history.py`, `given_single_wait.py`, `when_empty_msg.py`, `then_reject_send.py`, `then_no_prior_history.py`), making later Phase 3 parallel task target files mutually exclusive.
  - Do not: write ALIGN / REMOVE / RED semantics, nor helper logic.

- [ ] T007 Establish the two-player room test fixture entry
  - Read:
    - `specs/truth/data/**` -> room / player related entities
    - `backend/features/steps/shared/chat_helpers.py`
  - Only do: be able to open two players' websocket connections and map them to the same room's test entry.
  - Do not: write the DSL for "single-player waiting", "send message", or empty rejection.

## Phase 3: Test Alignment & Implementation

**Goal**: Align the automated tests of the DSL used by this round's Feature with the latest truth; including the sentences changed in truth-delta, and the sentences used by this round's Feature that have no stepdef yet. Write no product behavior.

**DSL Reference**:
- Each sentence belongs to exactly one authoritative `dsl.md`: the same-module `specs/truth/features/{interface}/{module}/dsl.md`, or the interface root `specs/truth/features/{interface}/dsl.md`. Do not scan other modules.
- This round's sentences all live in the same module `specs/truth/features/backend/room-chat/dsl.md`. This round has no sentences from the interface root `specs/truth/features/backend/dsl.md`.
- How to read: match the task title's sentence to that row in the file, taking `StepDef 實作語意` as the test code semantics. For Given / When read `怎麼做`, `權威狀態落地`, `回寫`; for Then read `必查` (`呈現結果`, `權威狀態`, `再讀確認`).
- `truth-delta.md` only tells whether this sentence is ADD / MODIFY / DELETE. Semantics follow that `dsl.md` row; do not invent from feature wording or old stepdefs.

**Markers**:
- `[BDD-ALIGN]`: `MODIFY`. The existing stepdef is still there but its semantics are old truth. Change the tests per that `dsl.md` row so they express the latest `StepDef 實作語意`.
- `[BDD-REMOVE]`: `DELETE`. This sentence is no longer truth. Remove or rewrite the stepdef / assertion still bound to this sentence, leaving no tests protecting old behavior.
- `[BDD-RED]`: `ADD`, or sentences used by this round's Feature with no stepdef yet. Write the stepdef per that `dsl.md` row. When done, this sentence can be run, with failures only from assertions or product behavior — never undefined steps.
- All three markers touch only the test layer, writing no product code.

**Shared Must Read**:
- `specs/truth/features/backend/room-chat/dsl.md`
  -> `When: "{player}" sends message "{content}"`
  -> `Then: "{player}" and "{player}" can both see the following chat content:`
  -> `Then: the opponent still sees messages sent before leaving the room`
  -> `Given: "{player}" is alone waiting in the room`
  -> `When: "{player}" attempts to send an empty message`
  -> `Then: this chat send is rejected`
  -> `Then: "{player}" cannot see previous chat messages`
- `truth-delta.md` -> the sentences where `/axb-dsl-refine` has corresponding ADD / MODIFY / DELETE
- `backend/features/steps/modules/room-chat/` (each stepdef's independent touchpoint skeleton)

**Boundary**:
- One DSL sentence per task.
- Change only that sentence's stepdef / assertion / directly dependent helpers.
- Touchpoint files prefer independent files (Zero Shared Edits principle, SHOULD), giving parallel dispatch mutually exclusive write targets.
- Write no product code.
- Review launches a subagent; all of this round's Test Scopes must no longer have undefined steps, failures only from assertions or product behavior. Fix issues and review again until there are none. Phase 4 stays locked until it passes.

**Parallel Hint**:
- T008–T014 each get one independent subagent, dispatching the whole batch in parallel at once (target files independent, satisfying Zero Shared Edits); T015 starts its review subagent only after all return.

- [ ] T008 [P] [BDD-ALIGN] `When: "{player}" sends message "{content}"`
  - Read: `backend/features/steps/modules/room-chat/when_send_msg.py`

- [ ] T009 [P] [BDD-ALIGN] `Then: "{player}" and "{player}" can both see the following chat content:`
  - Read: `backend/features/steps/modules/room-chat/then_both_see_chat.py`

- [ ] T010 [P] [BDD-REMOVE] `Then: the opponent still sees messages sent before leaving the room`
  - Read: `backend/features/steps/modules/room-chat/then_opponent_see_history.py`

- [ ] T011 [P] [BDD-RED] `Given: "{player}" is alone waiting in the room`
  - Read: `backend/features/steps/modules/room-chat/given_single_wait.py`

- [ ] T012 [P] [BDD-RED] `When: "{player}" attempts to send an empty message`
  - Read: `backend/features/steps/modules/room-chat/when_empty_msg.py`

- [ ] T013 [P] [BDD-RED] `Then: this chat send is rejected`
  - Read: `backend/features/steps/modules/room-chat/then_reject_send.py`

- [ ] T014 [P] [BDD-RED] `Then: "{player}" cannot see previous chat messages`
  - Read: `backend/features/steps/modules/room-chat/then_no_prior_history.py`

- [ ] T015 subagent review (phase quality gate)

## Phase 4A: ADD Feature File - backend/room-chat/single-player-waiting-and-empty-message-rejection.feature

**Goal**: Make this feature file all green with minimal message-send rejection logic.

**Shared Must Read**:
- `specs/truth/features/backend/room-chat/single-player-waiting-and-empty-message-rejection.feature` -> `Feature: Single-player waiting and empty-message rejection`
- `specs/truth/features/backend/room-chat/dsl.md` -> `Given: "{player}" is alone waiting in the room`, `When: "{player}" attempts to send an empty message`, `Then: this chat send is rejected`
- `truth-delta.md` -> `/axb-dsl-refine` ADD single-player waiting and empty-message rejection

**Boundary**:
- Handle only single-player waiting and empty rejection, not match-continuation or leave-clearing.

**Test Scope**:
- `specs/truth/features/backend/room-chat/single-player-waiting-and-empty-message-rejection.feature`

- [ ] T016 [BDD-GREEN] Make the Test Scope all green
- [ ] T017 [BDD-REFACTOR] Tidy the rejection messages and test helpers under the green light

## Phase 4B: MODIFY Feature File - backend/room-chat/realtime-chat-while-both-present.feature

**Goal**: Adjust the message-send implementation and snapshot projection to make the updated tests all green.

**Shared Must Read**:
- `specs/truth/features/backend/room-chat/realtime-chat-while-both-present.feature` -> `Feature: Realtime chat while both present`
- `specs/truth/features/backend/room-chat/dsl.md` -> `When: "{player}" sends message "{content}"`, `Then: "{player}" and "{player}" can both see the following chat content:`
- `truth-delta.md` -> `/axb-dsl-refine` MODIFY `When: "{player}" sends message "{content}"`

**Boundary**:
- Do not add unrelated chat scenarios.

**Test Scope**:
- `specs/truth/features/backend/room-chat/realtime-chat-while-both-present.feature`

- [ ] T018 [BDD-GREEN] Make the Test Scope all green
- [ ] T019 [BDD-REFACTOR] Tidy the chat-write and `再讀確認` (re-read confirmation) shared logic under the green light

## Phase 4C: DELETE Feature / DSL Truth - old messages still visible after leaving the room

**Goal**: Remove the obsolete product code branch retaining leave-room messages, and confirm the new version of truth still holds.

**Shared Must Read**:
- `specs/truth/features/backend/room-chat/clear-after-leaving-and-room-isolation.feature` -> `Feature: Clear after leaving and room isolation`
- `specs/truth/features/backend/room-chat/dsl.md` -> `Then: "{player}" cannot see previous chat messages`
- `truth-delta.md` -> `/axb-dsl-refine` DELETE `Then: the opponent still sees messages sent before leaving the room`
- `backend/app/store.py` -> the product branch possibly still retaining leave-room messages

**Boundary**:
- Remove only the obsolete semantics of retaining old messages after leaving the room, not the chat history when both are present.

**Test Scope**:
- `specs/truth/features/backend/room-chat/clear-after-leaving-and-room-isolation.feature`

- [ ] T020 [CODE-REMOVE] Remove the obsolete product code branch retaining leave-room messages
- [ ] T021 [REGRESSION] Run the Test Scope, confirming the new version of truth holds

## Phase 4W: Witness Pins - websocket disconnection guarantees

**Goal**: Establish unit test witness pins for this round's websocket disconnection and abnormal-closure invariants.

**Shared Must Read**:
- `specs/truth/techstack.md` -> Backend test entry
- `spec.md` -> NFR-002
- `truth-delta.md` -> `/axb-technical-research`

**Boundary**:
- Only establish unit-level witnesses for automatically releasing room resources on abnormal websocket disconnection; chat message presentation is not involved.

- [ ] T022 [WITNESS] Connection resources are released immediately when the websocket is abnormally interrupted
  - Dependencies: T018
  - Read:
    - `spec.md` -> NFR-002
    - `specs/truth/techstack.md` -> Backend test entry
  - Test Scope: `backend/tests/unit/test_ws_lifecycle.py`
  - Falsifier: when mutated to ignore the close event, the test fails with the failure clearly attributed to the resource-leak assertion
  - Target: `backend/app/ws.py`

## Pre-Delivery Inventory & Coverage Cross-Reference

### 1. Pre-Delivery Orphan Coverage Sweep (Orphaned Artifact Inventory)
- `truth-delta.md` non-NOOP items: fully allocated to T008–T014, T016, T018, T020.
- `research.md` decided Decisions: fully referenced by task Reads or delivered by concrete tasks.
- `specs/truth/techstack.md` changed sections: taken over by T001–T003.
- Orphaned artifact count: 0. Scan passed.

### 2. Claim→Witness Ledger (Claim→Witness Inventory Cross-Reference)

| Claim ID | Source Spec / Truth Anchor | Claimed Effect (Atomic Effect Claim) | Witness Type (`[WITNESS]` / `[BDD-GREEN]` / `accepted-unwitnessed`) | Bound Task / Decision Record | Discriminating Falsifier | Status |
|---|---|---|---|---|---|---|
| CLM-001 | FR-001 | Both room parties can send messages and see them presented in chat history | [BDD-GREEN] | T018 | Disable history broadcast -> BDD test red | Verified |
| CLM-002 | FR-002 | Sending a message while alone waiting is rejected | [BDD-GREEN] | T016 | Allow solo sending -> BDD test red | Verified |
| CLM-003 | NFR-002 | Connection resources are released immediately on abnormal websocket interruption | [WITNESS] | T022 | Mutate to ignore close event -> unit test red | Verified |

