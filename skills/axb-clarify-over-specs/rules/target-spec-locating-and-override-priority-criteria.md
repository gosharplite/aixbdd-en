# Rule 1 - Explicit override takes priority over any automatic inference

- Level: `MUST`
- If the user, the caller skill, or the current context has explicitly specified a `spec.md` path, a feature directory, or an equivalent target artifact, that explicit specification must be adopted first and must not be overridden by automatic inference.
- Once an explicit override holds, the corresponding `CHECKLIST_FILE` should default to `checklists/requirements.md` under the same feature directory; if that file does not exist, write back only to the spec and explicitly note the checklist's absence in the completion report.
- Do not ignore an explicitly stated override target just because the IDE focus, recent files, or existing conventions look more commonly used.

## Good Example

- This example is good because it adopts the explicitly stated target first, then derives the corresponding checklist.

```md
User specified:
- Target spec: `specs/003-billing/spec.md`

Decision:
- `SPEC_FILE` = `specs/003-billing/spec.md`
- `CHECKLIST_FILE` = `specs/003-billing/checklists/requirements.md` (if present)
```

## Bad Example

- This example is bad because it ignores the explicitly stated path and instead guesses the spec that currently looks like the "latest".

```md
User specified:
- Target spec: `specs/003-billing/spec.md`

Decision:
- Use the recently opened `specs/004-search/spec.md` instead
```

# Rule 2 - Without explicit specification, locate the target spec automatically in a fixed order

- Level: `MUST`
- If there is no explicit override, the target `SPEC_FILE` must be located in a fixed order, not freely guessed on the spot:
  1. The `SPEC_FILE` just produced by this round's upstream `/axb-specify`
  2. The `spec.md` corresponding to the feature directory uniquely identifiable in the current context
  3. The `spec.md` currently in IDE focus
- If none of these sources exists, or multiple candidates appear and no unique determination is possible, work must stop and the user must be asked to specify the target; do not pick one spec among many on your own.
- After successful automatic location, `checklists/requirements.md` in the same directory should serve as the default `CHECKLIST_FILE`; if it does not exist, treat it only as a checklist absence, not as a spec location failure.

## Good Example

- This example is good because it converges on the unique target with a fixed order, without skipping steps and guessing.

```md
Conditions:
- `/axb-specify` was just run this round
- `/axb-specify` reported `SPEC_FILE = specs/001-online-pvp-1a2b/spec.md`

Decision:
- Directly reuse `specs/001-online-pvp-1a2b/spec.md`
- Do not look at IDE focus or recent files again
```

## Bad Example

- This example is bad because it has no fixed priority order, so different executors might select different specs.

```md
Conditions:
- No explicit specification
- Two different `spec.md` files among recent files

Decision:
- Use whichever content looks more like a new feature first
```

# Rule 3 - The writeback scope is limited to the target spec and its paired checklist

- Level: `SHOULD`
- Once `SPEC_FILE` and `CHECKLIST_FILE` are converged, this round's writeback scope should be limited to this pair of artifacts, not extended to modifying other feature directories, other checklists, or parallel specs.
- If a high-impact gap actually involves a cross-spec product scope conflict, explicitly note the risk in the completion report and, when necessary, ask the user to designate other artifacts separately — do not secretly synchronize changes across multiple documents.
- The completion report should explicitly state which files were actually written back this round, so the user knows the skill's boundary of effect.

## Good Example

- This example is good because it limits the writeback to this round's target without secretly spreading cross-feature problems.

```md
This round's target:
- `specs/001-online-pvp-1a2b/spec.md`
- `specs/001-online-pvp-1a2b/checklists/requirements.md`

Processing:
- Update only these two files
- Note in the completion report that other features may also be affected, without modifying them directly
```

## Bad Example

- This example is bad because it synchronously modifies multiple features' specs without the user's designation.

```md
This round's target:
- `specs/001-online-pvp-1a2b/spec.md`

Processing:
- Also casually modify `specs/002-ranking/spec.md`
- Also adjust another checklist in sync
```
