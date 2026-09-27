# Rule 1 - Each truth owner must maintain its own table

- Level: `MUST`
- `truth-delta.md` must keep an independent section for each truth owner: `/axb-technical-research`, `/axb-api-plan`, `/axb-data-plan`, `/axb-dsl-refine`.
- Each section records only the truth specs that owner is responsible for; do not mix API, data, techstack, and interface feature changes into one table.
- Each table fixedly uses the four columns `Action`, `Truth Spec`, `Change Summary`, `Reason`.

## Good Example

- This example is good because the API change appears only in the `/axb-api-plan` section.

```md
## /axb-api-plan

| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| ADD | `specs/truth/contracts/openapi.yaml` -> `POST /rooms/{roomId}/messages` | Add the room message send API. | Chat needs an independent command entry. |
```

## Bad Example

- This example is bad because it mixes different owners' truth changes together.

```md
## Truth Updates

| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| ADD | `specs/truth/contracts/openapi.yaml` -> `POST /messages` | Add API. | Chat needs it. |
| ADD | `specs/truth/data/data-model.dbml` -> `Table chat_messages` | Add table. | Chat needs it. |
```

# Rule 2 - Action classification must use ADD, MODIFY, DELETE, or NOOP

- Level: `MUST`
- `ADD` means adding a semantic unit that does not exist in current truth.
- `MODIFY` means changing an existing truth semantic unit's fields, behavior, life cycle, verification conditions, output content, or test contract.
- `DELETE` means removing an existing semantic unit from current truth, or explicitly declaring that an existing behavior no longer holds.
- `NOOP` means the truth owner has inspected its responsible truth scope but no modification is needed this round.
- Undefined actions such as `UPDATE`, `CHANGE`, `NEW`, `REMOVE` must not be used.

## Good Example

- This example is good because the action values can be stably interpreted downstream.

```md
| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| MODIFY | `specs/truth/contracts/openapi.yaml` -> `RoomSnapshot.messages` | Add `messages` to the room snapshot's required fields. | The frontend polls chat messages with the same snapshot. |
| NOOP | `specs/truth/contracts/openapi.yaml` -> `GET /rooms/{roomId}` | Inspected the read entry; no new endpoint needed. | The existing snapshot entry suffices. |
```

## Bad Example

- This example is bad because the action value is ambiguous.

```md
| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| UPDATE | `openapi.yaml` | Changed some stuff. | Requirements changed. |
```

# Rule 3 - Truth Spec must be recorded down to the semantic-unit level

- Level: `MUST`
- `Truth Spec` should not write only the file path; use `->` to point to a semantic unit downstream can locate.
- API truth semantic units can be operations, schemas, fields, error codes, or response shapes.
- Data truth semantic units can be tables, enums, refs, fields, indexes, or lifecycle notes.
- Feature truth semantic units can be feature files, Rules, Examples, or DSL sentences.
- Techstack truth semantic units can be categories, adopted technologies, excluded technologies, or the test verification strategy.

## Good Example

- This example is good because downstream directly knows which truth part to read.

```md
| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| ADD | `specs/truth/data/data-model.dbml` -> `Table chat_messages` | Add the in-room message model. | Messages must bind to the room life cycle. |
| MODIFY | `specs/truth/features/backend/room-chat/dsl.md` -> `When: "{player}" sends message "{content}"` | Add verification semantics that the send must land in the store. | Then must not trust only the API response. |
```

## Bad Example

- This example is bad because it writes only a file with no semantic location.

```md
| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| MODIFY | `specs/truth/data/data-model.dbml` | Update data model. | Chat feature. |
```

# Rule 4 - High-impact MODIFY or DELETE must already have a clarify basis

- Level: `MUST`
- If a change would remove an API, change existing request/response semantics, delete data fields, rewrite existing feature behavior, or weaken the DSL verification contract, the truth owner must first complete `/axb-clarify` or provide an explicit user decision in the handoff.
- `/axb-truth-delta` does not make product decisions for the truth owner; if the confirmation basis is missing, stop writing and require returning to the owner skill's clarify gate.
- Low-risk additions, supplementary descriptions, or detail tidying that does not change external semantics may be recorded directly.

## Good Example

- This example is good because the DELETE has an explicit decision basis.

```md
| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| DELETE | `specs/truth/contracts/openapi.yaml` -> `POST /rooms/{roomId}/messages` | Remove the independent message send endpoint. | The user decided in clarify to use the existing command channel instead. |
```

## Bad Example

- This example is bad because it deletes an existing contract directly with no confirmation basis.

```md
| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| DELETE | `specs/truth/contracts/openapi.yaml` -> `POST /rooms/{roomId}/messages` | Remove endpoint. | I think it's unused. |
```

# Rule 5 - A DSL move of the authoritative location only must be recorded as MODIFY

- Level: `MUST`
- If a DSL row's sentence, parameters, DataTable, defaults, and implementation contract are all unchanged — merely promoted from module DSL to the interface root shared DSL, or demoted from root DSL to module DSL — it must be recorded as one `MODIFY`.
- `Truth Spec` must list both the old location and new location plus the DSL sentence, and the summary must explicitly state "authoritative location moved, semantics unchanged".
- Do not split it into `DELETE + ADD`; that would make downstream misjudge it as removing old behavior and adding another behavior.
- If the move also changes the contract, still use `MODIFY`, but the summary must separately list the actual semantic changes and must not claim semantics are unchanged.

## Good Example

- This example is good because the same sentence merely goes from single-module to cross-module shared, not triggering wrong remove-and-add tasks.

```md
| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| MODIFY | `specs/truth/features/backend/room-chat/dsl.md` → `specs/truth/features/backend/dsl.md` -> `Then: this operation was rejected` | Authoritative location moved, semantics unchanged. | A second module starts using the exact same contract. |
```

## Bad Example

- This example is bad because a pure move is split into two behavior changes, making downstream produce wrong BDD-REMOVE and BDD-RED.

```md
| DELETE | `specs/truth/features/backend/room-chat/dsl.md` -> `Then: this operation was rejected` | Delete old sentence. | Moving. |
| ADD | `specs/truth/features/backend/dsl.md` -> `Then: this operation was rejected` | Add shared sentence. | Moving. |
```
