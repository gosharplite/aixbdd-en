# aixbdd-en

**English translation of [aixbdd-tmg](https://github.com/gosharplite/aixbdd-tmg)** — a set of AI
agent skills implementing a BDD (Behavior-Driven Development) workflow with clearly separated PM
and RD (developer) responsibilities.

> *PM defines acceptance criteria in Gherkin, RD turns them into automated tests, developing
> correct systems in one continuous flow.*

## About this repository

This repository is a **translation of a derivative work**, maintained as a faithful English
rendering of the original Traditional Chinese sources:

1. **[AIxBDD](https://github.com/Waterball-Software-Academy/aixbdd)** by Waterball Agent Limited
   (水球球特務有限公司) — the original BDD workflow, licensed under the **Apache License, Version 2.0**.
2. **[aixbdd-tmg](https://github.com/gosharplite/aixbdd-tmg)** — a derivative of AIxBDD adding a
   domain model, decision records, PM/RD role configs, and CLI-application guidance (Apache-2.0).
3. **aixbdd-en** (this repository) — the English translation of aixbdd-tmg.

All files are translated from the original Traditional Chinese; structure, semantics, and content
are preserved. Translation decisions:

- Skill definition filenames (`SKILL.md`) and folder names are kept identical to the source.
- Rule filenames under `skills/*/rules/` have been renamed into English; internal cross-references
  were updated accordingly. Cross-skill references use the planned English names (e.g. axb-bdd
  references `axb-implement`'s `rules/definition-of-done-verification-and-writeback-criteria.md`,
  which will be created under that name when axb-implement is translated).
- Code identifiers, file paths, and skill names (e.g., `/axb-clarify`, `CONSTITUTION.md`) are kept
  as-is.

## Attribution & license

This repository is distributed under the **Apache License, Version 2.0** — see [LICENSE](LICENSE).

The upstream attribution notice is reproduced verbatim in [NOTICE](NOTICE), as required by
Apache-2.0 §4(d), together with a note describing this repository's modifications (the English
translation).

Five of the inherited skills — `axb-specify`, `axb-clarify-over-specs`, `axb-tasks`,
`axb-implement`, and `axb-technical-research` — were in turn derived by AIxBDD from
[GitHub Spec Kit](https://github.com/github/spec-kit) (MIT). Their per-skill `LICENSE` files are
retained alongside those skills.

## Translation progress

Translation is done step by step, one file at a time.

| Skill | Status |
|---|---|
| axb-constitution | ✅ Done |
| axb-bdd | ✅ Done |
| axb-clarify | ✅ Done |
| axb-clarify-over-specs | ⬜ Pending |
| axb-data-plan | ⬜ Pending |
| axb-dsl-refine | ⬜ Pending |
| axb-gherkin-and-dsl | ⬜ Pending |
| axb-implement | ⬜ Pending |
| axb-spec-by-example | ⬜ Pending |
| axb-specify | ⬜ Pending |
| axb-system-analysis | ⬜ Pending |
| axb-tasks | ⬜ Pending |
| axb-technical-research | ⬜ Pending |
| axb-truth-delta | ⬜ Pending |
| axb-ui-plan | ⬜ Pending |
| axb-api-plan | ⬜ Pending |
