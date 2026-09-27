# Rule 1 - Multi-screen prototypes fixedly use the entry screen as the entrance

- Level: `MUST`
- This criteria covers both web and terminal media.
- If the feature's real product flow needs to cross screens, `axb-ui-plan` must fixedly use the entry screen as the prototype entrance:
  - web: `ui/index.html`.
  - terminal: `ui/screens/entry.txt`.
- The entry screen itself must also be part of the product — not a sitemap, help page, or pure link directory.
- If the feature does not need to cross screens, there must still be at least one operable product screen.

## Good Example

- This example is good because the entry is itself the product entrance, not an extra navigation document.

```md
# web
ui/index.html           -> product listing entry screen
ui/product-detail.html  -> product detail screen
ui/checkout.html        -> cart and checkout screen

# terminal
ui/screens/entry.txt         -> startup / input frame
ui/screens/10-suggestion.txt -> live suggestion frame
ui/screens/20-running.txt    -> running status frame
```

## Bad Example

- This example is bad because the entry is just a file list, not really serving as the product flow entrance.

```md
ui/index.html
- Link: product-detail.html
- Link: checkout.html
- Link: order-success.html
```

# Rule 2 - Prototypes must cover the complete user flow from entry to main result

- Level: `MUST`
- The prototypes `axb-ui-plan` produces must cover at least this feature's main flow entry, key intermediate states, and main result (screens or frames).
- Do not build only one pretty screen while missing the waiting, error, result, or round states in the flow.
- If the number of screens must be trimmed, prioritize keeping the complete flow over keeping only the most visually striking fragments.

## Good Example

- This example is good because it lets the reviewer walk from startup all the way to completion or error results.

```md
Flow coverage (terminal):
1. Startup / input
2. Live suggestions (key intermediate state)
3. Running status
4. Completion summary or error bar (main result)
```

## Bad Example

- This example is bad because it presents only one middle screen; the real product flow cannot be reviewed.

```md
Flow coverage:
1. Build only one completion screen
2. No entry
3. No input, suggestion, or running flow
```

# Rule 3 - Prototypes must remain operable, simulating real interactions with fake data

- Level: `SHOULD`
- web: although the prototype connects to no real backend, it should still provide clickable buttons, navigable page switching, form inputs, and fake-data-driven state switching so users can feel the real product rhythm.
- terminal: the terminal cannot "click"; instead express operability via `ui/ui-plan.md`'s `Keybinding Map` (key → action → target frame → expected result) and `State Transition List`, rendering each state frame with fake data.
- Neither medium should deliver only static screenshot-like content that leaves the reviewer unable to operate or feel the interaction.

## Good Example

- This example is good because although there is no real backend, it still simulates basic interactions and lets the reviewer track key by key.

```md
# terminal operability (written in ui/ui-plan.md)
Keybinding Map:
| Key   | Action              | Target Frame | Expected Result              |
| Enter | Submit input        | entry        | history adds one, list recomputed |
| Tab   | Accept current hint | entry        | editor inserts suggestion text |
| Esc   | Abort execution     | entry        | show abort summary           |
```

## Bad Example

- This example is bad because it has only static screens with no followable operation path.

```text
┌─ Done ─────────────────────────────┐
│ Roughly what it will look like.    │
└────────────────────────────────────┘
```
