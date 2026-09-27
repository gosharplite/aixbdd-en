# Rule 1 - `ui/ui-plan.md` is the control plane; prototypes are the reviewable product surface

- Level: `MUST`
- This criteria covers both media: web／`frontend` HTML prototypes (`ui/*.html`), and interactive CLI terminal prototypes (`ui/screens/*.txt`).
- `axb-ui-plan`'s output order must be: finalize `ui/ui-plan.md` first, then produce the corresponding medium's prototype from that plan.
- `ui/ui-plan.md`'s responsibility is organizing the interface scope, medium, screens & flows, states, verification, and prototype output planning.
- The web prototype (`ui/*.html`) is responsible for landing the above plan as a high-fidelity static prototype that is clickable, navigable, and lets you feel the product rhythm.
- The terminal prototype (`ui/screens/*.txt`) is responsible for landing the above plan as frames consistent with the actual terminal rendering; its operability is carried by `ui/ui-plan.md`'s `Keybinding Map` and `State Transition List`, letting the reviewer track key → state → outcome.
- Do not mix the control plane and the prototype into one artifact, nor let the prototype take shape first and then back-derive key flow decisions.

## Good Example

- This example is good because it converges screens and flows with `ui-plan.md` first, then truly presents the product with multiple prototypes.

```md
1. Complete `ui/ui-plan.md` first
   - web: define `ui/index.html`, `ui/product-detail.html`, `ui/checkout.html`
   - terminal: define `ui/screens/entry.txt`, `ui/screens/10-suggestion.txt`, `ui/screens/20-running.txt`
   - Define each screen's main purpose and transition relations

2. Then produce the corresponding medium's prototypes per the plan
   - web: `ui/index.html`, `ui/product-detail.html`, `ui/checkout.html`
   - terminal: `ui/screens/entry.txt`, `ui/screens/10-suggestion.txt`, `ui/screens/20-running.txt`
```

## Bad Example

- This example is bad because it draws prototypes first and back-fills the plan afterward, breaking single-source-of-truth.

```md
1. Casually make three HTML pages, or three terminal frames
2. Later decide whether to add `ui/ui-plan.md`
3. When flow conflicts are found, go back and change all files
```

# Rule 2 - Prototypes must look like the product, not documentation

- Level: `MUST`
- The web prototype (`ui/*.html`) may contain only content the product would really display to users, e.g. titles, fields, states, CTAs, error messages, result summaries, and fake data.
- The terminal prototype (`ui/screens/*.txt`) may contain only frame content the terminal would really render for users, e.g. title bars, panels, fields, cursors, status bars, error bars, and fake data.
- Neither medium may write analysis notes, component trees, implementation TODOs, field explanations, review instructions, `Keybinding Map`, or `State Transition List` directly into prototype screens.
- If some information is for developers or reviewers, keep it in `ui/ui-plan.md`, not on the product surface.

## Good Example

- This example is good because the terminal frame shows only product content users really see; the keybinding map stays in the plan.

```text
┌─ tell-me-go · interactive prompt ───────────────────────────┐
│ Type your question; ↑/↓ browse suggestions, Tab accept      │
│                                                             │
│  Input                            [editing]                 │
│  deploy to staging                                          │
│  ▏                                                          │
│                                                             │
│  Enter send · Tab accept · ? help · Ctrl+C cancel           │
└─────────────────────────────────────────────────────────────┘
```

## Bad Example

- This example is bad because it stuffs documentation content (keybinding map, implementation TODOs) directly into the product frame.

```text
┌─ Frame 1: interactive prompt ───────────────────────────────┐
│ This screen lets users type commands.                       │
│ Keybindings: Enter=send, Tab=accept, ?=help                 │
│ TODO: this may later become a real TUI.                     │
└─────────────────────────────────────────────────────────────┘
```
