# Truth Delta: 004-room-game-chat

**Plan Package**: `specs/plans/004-room-game-chat`
**Truth Root**: `specs/truth`

## /axb-technical-research

| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| MODIFY | `specs/truth/techstack.md` -> `Testing & Verification` | Add that frontend BDD verifies the chat blocks. | This round adds chat acceptance for the ready page and battle page. |

## /axb-api-plan

| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| ADD | `specs/truth/contracts/openapi.yaml` -> `POST /rooms/{roomId}/messages` | Add the room message send API. | Chat needs an independent command entry. |
| MODIFY | `specs/truth/contracts/openapi.yaml` -> `RoomSnapshot.messages` | Add a `messages` field to the room snapshot. | The frontend obtains messages through the same polling entry. |

## /axb-data-plan

| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| ADD | `specs/truth/data/data-model.dbml` -> `Table chat_messages` | Add the in-room message model. | The message life cycle must bind to the room and presence state. |

## /axb-dsl-refine

| Action | Truth Spec | Change Summary | Reason |
| --- | --- | --- | --- |
| ADD | `specs/truth/features/backend/room-chat/realtime-chat-while-both-present.feature` | Add the backend interface feature for both-present mutual messaging. | Carries the acceptance journey's backend responsibility. |
| MODIFY | `specs/truth/features/backend/room-chat/dsl.md` -> `When: "{player}" sends message "{content}"` | Specify that sending must land in the store and write back the chat list. | Later BDD steps need consistent verification semantics. |
