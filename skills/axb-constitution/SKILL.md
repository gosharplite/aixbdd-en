---
name: axb-constitution
description: Based on user requirements, create or modify the modular constitution in minimal, incremental steps. First locate the constitution file to change, then interview, converge, and write only the necessary root constitution, shared rules, or specific skill artifact rules. Use when the user asks to create, split, refine, or extend the modular constitution under `.agents/constitution/`.
disable-model-invocation: true
---

# Constitution

Turn the user's requirements for artifact governance into the minimal constitution changes under `.agents/constitution/`. Prefer reusing
the existing `CONSTITUTION.md`, `shared.md`, and `skills/<skill>/<artifact>.md`; create new files only when the requirement truly
adds a governance boundary or a new artifact. If a gap would change where a rule lands, its applicable scope, or rule strength,
interview the user first — do not fill in the blanks yourself.

# SOP

## Phase 1 -- Locate the constitution file to change in this round

1. READ Read the user requirements and the current state of `.agents/constitution/`, determine whether this round adds, modifies, or splits rules, and converge the candidate target files to `CONSTITUTION.md`, `shared.md`, or `skills/<skill>/<artifact>.md`.
2. READ If you need to determine whether a rule should live in shared, the root constitution, or a specific skill artifact, read `rules/rule-placement-criteria.md`, then converge the minimal change surface for this round based on the loaded rules.
3. THINK List the files that genuinely need to be added or modified in this round; if a requirement does not affect the existing constitution structure, avoid expanding into other files.

## Phase 2 -- Converge high-impact gaps and interview the user

1. THINK First judge from the requirements whether there are high-impact gaps that would change where rules land, the applicable skill, the applicable artifact, rule strength, or whether a new file is needed.
2. READ If you need to determine which gaps must be asked first, read `rules/minimal-interview-criteria.md`, then converge 1 to 3 questions for this round as it requires.
3. DELEGATE If high-impact gaps remain, call `/axb-clarify` and specify that the questioning dimensions are rule placement, applicable artifact, enforceability level, and whether the change is incremental; stop before convergence and do not assume answers on your own.

## Phase 3 -- Write the minimal constitution increment

1. THINK Based on confirmed requirements, decide whether this round should modify `CONSTITUTION.md`, `shared.md`, or a single `skills/<skill>/<artifact>.md`; if adding a new skill artifact rule file, follow the existing file naming conventions and RuleFile structure.
2. READ If you need to control the scope of changes and avoid over-writing, read `rules/minimal-increment-criteria.md`, then keep only the minimal rule set that supports this round's requirements as it requires.
3. WRITE Update the target constitution file; if adding or modifying artifact rules, follow the existing format of `Applies To`, `## Rule N - ...`, `- Level:`, `### Good Example`, `### Bad Example`.
4. READ Review whether only the necessary files were touched, whether process responsibilities were kept out of the artifact constitution, and whether the shared / skill placement is consistent; fix any deviations immediately.

## Phase 4 -- Deliver and hand off follow-ups

1. WRITE Report to the user the constitution files added or modified in this round, the rules added or adjusted in each file, whether `/axb-clarify` was conducted, and which requirements were deliberately deferred to future skills or artifacts.
2. WRITE If a skill still needs to be wired into the constitution reading flow afterwards, state explicitly that follow-up should continue via `/skill-engineering` or the corresponding skill's edit process — do not automatically expand implementation within this skill.

## Additional Resources

- Rule placement criteria: `rules/rule-placement-criteria.md`
- Minimal interview criteria: `rules/minimal-interview-criteria.md`
- Minimal increment criteria: `rules/minimal-increment-criteria.md`
