# Terminal / TUI & Frame Prototype Planning

## Interface Scope

- Target system interface: `tell-me-go -i interactive TUI prompt interface`
- medium: `terminal`
- Requirement source: `User Stories 1 to 3, FR-004, FR-007, and NFR-002`
- Upstream basis: `spec.md, features/acceptance/interactive-prompt.feature`
- Output sequence: `Finalize ui/ui-plan.md first, then produce the ui/screens/*.txt frames per this plan.`

## Terminal Visual Direction

- Style source: `Follow the existing CLI layout vocabulary; when the requirements carry no visual spec, first converge panel hierarchy and color accessibility via clarify.`
- Style conclusion this time: `A single terminal screen with high information density but scannable: live suggestion list on top, multi-line editor in the middle, status bar and keybinding hints at the bottom.`
- Visual focus: `The suggestion list's selection cursor, the editor cursor, the visual separation of the focused panel, and grayscale hints for unavailable states.`
- Aesthetic principles: `Frames must look like what the terminal really renders; the keybinding map, state transition list, or analysis notes are not written into frame files.`

## Screens & Flows

### 1. `Startup / Edit Frame`

- Corresponding frame file: `ui/screens/entry.txt`
- Main purpose: `Let users type questions while browsing live suggestions as they type, serving as the entrance to the whole interactive flow.`
- Entry condition: `The user runs tell-me-go -i to enter interactive mode.`
- Primary operation keys: `Type text, ↑/↓ move suggestions, Tab accept suggestion, Enter send, ? help, Ctrl+C cancel.`
- Success transitions: `After sending, enter the running frame; on completion, return to this frame with an output summary.`
- Error feedback: `On empty input or unparseable input, show an error bar in place without clearing typed content.`

### 2. `Live Suggestion Frame`

- Corresponding frame file: `ui/screens/10-suggestion.txt`
- Main purpose: `Provide a live suggestion list from history / FS / tools while typing.`
- Entry condition: `The user types at least one character in the edit frame.`
- Primary operation keys: `↑/↓ move selection, Tab accept, Esc dismiss suggestions.`
- Success transitions: `After accepting a suggestion, return to the edit frame with the suggestion text inserted at the cursor.`
- Error feedback: `When there are no suggestions, show a "No suggestions" placeholder row without changing the input.`

### 3. `Running Status Frame`

- Corresponding frame file: `ui/screens/20-running.txt`
- Main purpose: `Show the steps and recent output while the command runs, so users can track progress.`
- Entry condition: `The user submits executable input in the edit frame.`
- Primary operation keys: `Esc abort execution, ? help.`
- Success transitions: `After completion, return to the edit frame with an output summary.`
- Error feedback: `On execution failure, show an error summary and suggested next step, then return to the edit frame.`

## Keybinding Map

| Key | Action | Target Frame | Expected Result |
| --- | --- | --- | --- |
| `Enter` | Submit current input | `entry` | history adds one, suggestion list recomputed |
| `Tab` | Accept current suggestion | `entry` | editor inserts suggestion text, cursor at end of line |
| `↑` / `↓` | Move suggestion selection | `entry` | suggestion list selection cursor moves |
| `Esc` | Abort execution | `entry` | show abort summary |
| `?` | Show keybinding help | `30-help` | open the overlay help frame |
| `Ctrl+C` | Cancel current input | `entry` | clear editor and return to startup frame |

## State Transition List

1. `entry` --type text--> `suggestion` (list recomputed from history / FS / tools)
2. `suggestion` --`Tab` accept--> `entry` (editor inserts suggestion text)
3. `entry` --`Enter` send--> `running` (show running status)
4. `running` --complete--> `entry` (output summary, then back to editing)
5. `entry` --`?`--> `help` --`Esc`--> `entry`
6. Any frame --invalid input--> show error bar in place (no transition)

## Interaction & Fake Data Principles

- Fake data strategy: `With fake history, fake file paths, and fake tool output, let the reviewer directly feel the suggestion engine and status bar.`
- Interaction principles: `Every frame maps back to operable keys; render list, editor, and status bar state switches with fake data.`
- Content principles: `Frames contain only what the terminal really renders; the keybinding map and state transition list stay in this plan.`

## States & Information Disclosure

- User-visible information: `Input content, suggestion list, focused panel, running status bar, and error messages.`
- Information that must be hidden: `Internal tool parameters, the full filesystem index, and any server-internal info that should not be exposed.`
- Main UI states: `Startup, editing, suggestions visible, running, completion summary, error hints.`
- Role or permission differences: `Single user; no multi-role differences.`

## Validation & Error Feedback

- Input validation: `Check non-empty before submitting; empty input shows an error bar in the frame in place.`
- State conflict handling: `While running, the submitted content stays visible, but new submissions are not accepted until back in the editing state.`
- User-understandable error messages: `The error bar explains cause and next step, e.g. "Input cannot be empty; please type again".`

## Prototype Output Planning

- Entry frame: `ui/screens/entry.txt`
- Planned output files: `ui/screens/entry.txt`, `ui/screens/10-suggestion.txt`, `ui/screens/20-running.txt`, `ui/screens/30-help.txt`
- Frame transition principles: `Only swap frames when the terminal really switches the whole screen; otherwise prefer switching state sections within the same frame.`
- Review goal: `Let the reviewer track key → state → outcome key by key without reading Markdown.`

## Terminal Implementation Split Suggestions

- Pane / component split: `Suggestion list pane, multi-line editor pane, status bar, and help pane.`
- Shared components or blocks: `Selection cursor, status bar, error bar, and pane borders.`
- Dependencies on backend contracts: `Suggestion engine input/output, history writes, and tool output summaries.`
- Acceptance focus: `The flow from startup, typing, accepting suggestions, to sending and completion summary must be continuous and understandable, and must not expose internal tool and index details.`
