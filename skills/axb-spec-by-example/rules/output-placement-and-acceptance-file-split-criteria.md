# Rule 1 - Acceptance feature files must stay in the plan package

- Level: `MUST`
- The output location of `/axb-spec-by-example` is fixed at `specs/plans/NNN-<slug>/features/acceptance/*.feature`.
- Acceptance Gherkin is this iteration's business acceptance journey, not interface truth.
- Acceptance feature files must not be written into `specs/truth/features/**`.

## Good Example

- This example is good because the acceptance stays in the current plan package.

```text
specs/plans/004-room-game-chat/features/acceptance/realtime-chat-while-both-present.feature
```

## Bad Example

- This example is bad because it writes the journey acceptance as a truth interface feature.

```text
specs/truth/features/backend/room-chat/realtime-chat-while-both-present.feature
```

# Rule 2 - Acceptance file splitting is based on business journeys

- Level: `SHOULD`
- Each acceptance feature should describe a complete business journey or explicit business rule that the PM can review.
- Do not split files by API endpoints, data tables, frontend components, or step definition technical boundaries.
- If the same journey has multiple important variants, use multiple Rules / Examples rather than over-splitting files.

## Good Example

- This example is good because the file name describes a business journey.

```text
features/acceptance/match-started-chat-continues-in-one-thread.feature
```

## Bad Example

- This example is bad because it splits acceptance by endpoint.

```text
features/acceptance/post-room-message-api.feature
```
