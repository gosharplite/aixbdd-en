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
  were updated accordingly. Cross-skill references use the agreed English names (e.g. axb-bdd
  references `axb-implement`'s `rules/definition-of-done-verification-and-writeback-criteria.md`).
- Code identifiers, file paths, and skill names (e.g., `/axb-clarify`, `CONSTITUTION.md`) are kept
  as-is.
- **Fixed DSL contract tokens stay in Chinese**, per `axb-gherkin-and-dsl/STANDARDS.md`'s "Project
  Language" section: the meta-schema field tokens (`DSL 句型`, `Gherkin 參數`, `Data Table 參數`,
  `預設參數`, `…實作語意`), the `不支援`/`支援：` cell literals, and the §5.1/§5.2 sub-labels
  (`怎麼做`, `權威狀態落地`, `回寫`, `不必查`/`必查`, `呈現結果`, `權威狀態`, `再讀確認`, `跨視角`,
  `不該發生`). The audit script requires the first table column header to be exactly `DSL 句型`;
  translating these tokens would break it silently. Everything else — including example Gherkin,
  parameter keys, and file names — follows the project-declared language and is translated.

## Attribution & license

This repository is distributed under the **Apache License, Version 2.0** — see [LICENSE](LICENSE).

The upstream attribution notice is reproduced verbatim in [NOTICE](NOTICE), as required by
Apache-2.0 §4(d), together with a note describing this repository's modifications (the English
translation).

Five of the inherited skills — `axb-specify`, `axb-clarify-over-specs`, `axb-tasks`,
`axb-implement`, and `axb-technical-research` — were in turn derived by AIxBDD from
[GitHub Spec Kit](https://github.com/github/spec-kit) (MIT). Their per-skill `LICENSE` files are
retained alongside those skills; the original notices are preserved verbatim, with an unofficial
English translation appended for convenience (the original text is authoritative).

## Translation progress

Translation is done step by step, one file at a time.

| Skill | Status |
|---|---|
| axb-constitution | ✅ Done |
| axb-bdd | ✅ Done |
| axb-clarify | ✅ Done |
| axb-clarify-over-specs | ✅ Done |
| axb-data-plan | ✅ Done |
| axb-dsl-refine | ✅ Done |
| axb-gherkin-and-dsl | ✅ Done |
| axb-implement | ✅ Done |
| axb-spec-by-example | ✅ Done |
| axb-specify | ✅ Done |
| axb-system-analysis | ⬜ Pending |
| axb-tasks | ⬜ Pending |
| axb-technical-research | ⬜ Pending |
| axb-truth-delta | ⬜ Pending |
| axb-ui-plan | ⬜ Pending |
| axb-api-plan | ⬜ Pending |
