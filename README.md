# aixbdd-en

**English translation of [aixbdd-tmg](https://github.com/gosharplite/aixbdd-tmg)** — a set of AI
agent skills implementing a BDD (Behavior-Driven Development) workflow with clearly separated PM
and RD (developer) responsibilities.

> *PM defines acceptance criteria in Gherkin, RD turns them into automated tests, developing
> correct systems in one continuous flow.*

## What it is

A collection of **16 skill definitions** (each a `SKILL.md` plus supporting `rules/` and `templates/`
directories) that guide an AI through the full software development lifecycle — from requirements to
working code — using Gherkin as the shared contract language. The tagline: *"PM defines acceptance
criteria in Gherkin, RD turns them into automated tests, developing correct systems in one
continuous flow."*

## Core idea

Most AI dev workflows blur PM/RD responsibilities (e.g., developers end up "mind-reading" unclear
requirements). AIxBDD splits it:

- **PM side**: writes specs, acceptance Gherkin, and UI prototypes
- **RD side**: does technical research, API/data design, test planning, and implementation
- **Shared "truth"** (`specs/truth/**`): OpenAPI contracts, DBML data models, techstack, and
  interface feature/DSL files act as the single source of truth, tracked via `truth-delta.md` per
  plan package

## The workflow (skills in order)

1. `/axb-constitution` (PM/RD) — set artifact governance rules
2. `/axb-specify` (PM) — create a numbered plan package with spec.md + checklist
3. `/axb-clarify-over-specs` (PM) — (optional) interactive requirement clarification
4. `/axb-spec-by-example` (PM) — acceptance Gherkin
5. `/axb-ui-plan` (PM) — HTML prototypes for a web interface; rendered terminal frames for a CLI TUI
6. `/axb-technical-research` (RD) — technical research & update techstack truth
7. `/axb-system-analysis` (RD) — orchestrates `/axb-api-plan` (RD), `/axb-data-plan` (RD) via dependency waves
8. `/axb-dsl-refine` (RD) — split acceptance criteria into executable front/back-end Gherkin + DSL
9. `/axb-tasks` (RD) — generate BDD task list tasks.md
10. `/axb-implement` (RD) — One-Shot TDD execution, red → green → refactor via `/axb-bdd` (RD)

Supporting skills:
- `/axb-clarify` (PM/RD) — user interviews
- `/axb-truth-delta` (RD) — truth change tracking
- `/axb-gherkin-and-dsl` (PM/RD) — Gherkin/DSL standards + a Python topology audit script

### Developing CLI Applications

When developing a CLI application (no web frontend or HTTP/REST API), the workflow is streamlined:

1. **Skip `/axb-ui-plan` for a plain CLI**: For a line-oriented CLI (commands, flags, arguments,
   exit codes, stdin/stdout/stderr) no web UI or HTML mockups are created; terminal interactions are
   defined directly as Gherkin acceptance scenarios in `/axb-spec-by-example`. **Exception:** a CLI
   that ships a rich terminal UI (TUI) runs `/axb-ui-plan` in **terminal mode** — textual
   screens/keybindings under `ui/screens/*.txt`, still no HTML.
2. **Lean `/axb-system-analysis`**:
   - **`/axb-api-plan`** is skipped — a standalone CLI has no OpenAPI endpoints. Because
     `/axb-system-analysis` is what decides to skip it, that skill records the skip: it delegates a
     `NOOP` row to `/axb-truth-delta` for the `/axb-api-plan` owner section, with the `Reason` stating
     that the planner was skipped by analysis decision. `NOOP` therefore covers both "inspected,
     nothing needed" and "not applicable, by analysis decision"; the row's `Reason` distinguishes them,
     and `axb-tasks`' coverage sweep skips both.
   - **`/axb-data-plan`** is conditional — invoked only if the CLI manages persistent configuration
     (e.g. `~/.config/...`), local storage (SQLite, JSON), or complex domain state. For stateless CLI
     tools it is skipped, and that skip is recorded the same way as the one above: a `NOOP` row in the
     `/axb-data-plan` section, reason "not applicable, by analysis decision".
3. **CLI Contract via `/axb-dsl-refine`**: The CLI end is a first-class truth-tree interface — a
   third `InterfaceKind`, `cli`, alongside `backend`/`frontend`. The executable Gherkin feature files
   (`specs/truth/features/cli/**`) and their step definitions (`dsl.md`) serve as the formal CLI
   contract and acceptance test runner. Since no API/data planner applies, `/axb-system-analysis`
   records those two skips as `NOOP` rows and carries the CLI end forward to its contract owner
   `/axb-dsl-refine`. (`/axb-ui-plan` applies to a TUI only, and is not a truth owner — it has no
   section in `truth-delta.md` and is never recorded there.)

### Resolving PR and Review Findings

When resolving architect or peer review findings on a pull request, modifying files under both implementation code and `specs/` is expected and required to prevent specification drift:

1. **Keep `specs/truth/**` synchronized with code**:
   - **Contracts**: Update `specs/truth/contracts/**` if endpoints, payloads, schemas, or status codes change.
   - **Data Models**: Update `specs/truth/data/**` if tables, relationships, fields, or indexes change.
   - **Techstack**: Update `specs/truth/techstack.md` if architectural choices or library selections change.
   - **Features & DSL**: Update `specs/truth/features/**` and `dsl.md` if business rules, step definitions, or acceptance assertions change.
2. **Log changes in `truth-delta.md`**: Record any changes made to `specs/truth/**` in the plan's `specs/plans/NNN-<slug>/truth-delta.md` (updating the corresponding truth owner's section with `MODIFY`, `ADD`, or `DELETE` and citing the review finding as the reason).
3. **Audit DSL changes**: If any feature or `dsl.md` files were modified, run the topology audit script to verify syntax and cross-references:
   ```bash
   uv run skills/axb-gherkin-and-dsl/scripts/audit_feature_dsl_topology.py --root specs/truth/features
   ```
   Pass either the shared features root or a single interface root (e.g. `specs/truth/features/backend`); with the shared root every interface subdirectory is audited in turn. Use `uv run` so the script's declared Python version is honoured.
4. **Code-only refactorings**: Internal refactorings, optimizations, or renames that do not alter external behavior or contracts do not touch `specs/` — update the production code and tests directly.

## Notes

- **Roles**: `roles/pm.yaml` and `roles/rd.yaml` role configs live in the upstream
  [aixbdd-tmg](https://github.com/gosharplite/aixbdd-tmg) repository (not translated here).
- **Decisions**: the workflow's own governed-artifact changes are recorded as short ADRs under
  `decisions/` in the upstream aixbdd-tmg repository.

## About this repository

This repository (**aixbdd-en**) originated as a faithful English translation of **[aixbdd-tmg](https://github.com/gosharplite/aixbdd-tmg)**, which is itself an adapted derivative work of the original **[AIxBDD](https://github.com/Waterball-Software-Academy/aixbdd)**.

### Repository Lineage

```
[AIxBDD] (Upstream original by Waterball Agent Limited)
   │
   └──► [aixbdd-tmg] (Derivative: adds domain model, CLI guidance, role configs, axb- prefix)
          │
          └──► [aixbdd-en] (English edition: ongoing independent evolution)
```

1. **[AIxBDD](https://github.com/Waterball-Software-Academy/aixbdd)**: The upstream original BDD workflow created by Waterball Agent Limited (水球球特務有限公司), licensed under the **Apache License, Version 2.0**.
2. **[aixbdd-tmg](https://github.com/gosharplite/aixbdd-tmg)**: A derivative work adapted from AIxBDD. **It is not identical to upstream AIxBDD** — it introduces several key architectural and workflow extensions:
   - **Prefix standard**: Skills are consistently renamed with an `axb-` prefix (e.g., `specify` → `axb-specify`, `bdd` → `axb-bdd`).
   - **Canonical Domain Model**: Introduces a formal domain model under `domain-model/` (`aixbdd.modelith.md` / `.yaml`).
   - **CLI Application Guidance**: Extends the workflow for command-line applications (the `cli` interface kind, terminal-mode UI plans, and streamlined analysis).
   - **Role configurations**: Adds PM and RD role definitions (`roles/pm.yaml`, `roles/rd.yaml`).
   - **Architecture Decision Records**: Tracks governance decisions under `decisions/`.
3. **[aixbdd-en](https://github.com/gosharplite/aixbdd-en)** (this repository): Began as the English translation of **aixbdd-tmg** (translated from aixbdd-tmg rather than original AIxBDD). Going forward, `aixbdd-en` maintains an **independent evolution path** — additional changes, English-native tooling, and workflow refinements are actively introduced here, so it is expected to deviate from upstream `aixbdd-tmg` over time.

### Baseline translation decisions

All initial files were translated from aixbdd-tmg's original Traditional Chinese; structure, semantics, and content are preserved as the baseline:

- Skill definition filenames (`SKILL.md`) and folder names are kept identical to the source.
- Rule filenames under `skills/*/rules/` have been renamed into English; internal cross-references
  were updated accordingly. Cross-skill references use the agreed English names (e.g. axb-bdd
  references `axb-implement`'s `rules/definition-of-done-verification-and-writeback-criteria.md`).
- Code identifiers, file paths, and skill names (e.g., `/axb-clarify`, `CONSTITUTION.md`) are kept
  as-is.
- The **default project language is flipped to English** (STANDARDS.md "Project Language" section and
  the §2/§3 defaults); it remains project-declarable, so projects may still declare any language.
- **Fixed DSL contract tokens are English**: `DSL Sentence`, `Gherkin Params`, `Data Table Params`,
  `Default Params`, `…Implementation Semantics`, `Not supported`/`Supported:`, the §5.1 Given / When
  sub-labels (`How`, `State landing`, `Write-back`, `No-check`), the §5.2 Then channels
  (`Presented Result`, `Authoritative State`, `Re-read Confirmation`, `Cross-Perspective`,
  `Should Not Happen`), and the `Must-check` marker that opens every Then cell in every interface kind
  (§5.2 defines it once; §6.2 and §7.2 use it).
- **The CLI interface kind has its own fixed vocabulary**, defined in `STANDARDS.md` §7.1 and §7.2.
  Those two subsections are the **single enumeration** — this README deliberately does not restate the
  labels, because three partial lists of one vocabulary is how `{{PLAN_PACKAGE}}` drifted before #11
  settled it. Read §7 for the set; do not maintain a copy here.
- The §4/§5 tokens above **were Chinese in upstream AIxBDD and are renamed in this repo**; the audit
  script accepts both the English header `DSL Sentence` and the legacy Chinese header `DSL 句型`, so
  upstream-era DSL files still audit cleanly. The §7 CLI vocabulary is **not** a translation — it is
  new in this repository and has no upstream counterpart.
- These tokens remain fixed — do not translate them per project language. The Chinese Gherkin
  keywords in the audit script's `STEP_RE` are kept as parser locale support (Gherkin sentence language
  is project-declarable).

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

## Repository-level artifacts

- `domain-model/` — the canonical domain model (`aixbdd.modelith.md` + `.yaml`, generated by
  `modelith render`). The source is already English and is included verbatim, so downstream
  projects can use a single skill+model source of truth here.

## Developing this repository

> **This section is for maintainers of `aixbdd-en` itself, not for users of its skills.** Every
> check below audits *this repo's* files. A user's project is supposed to contain `specs/truth/**`,
> so these invariants would be meaningless there — and the user-facing skill invocations (such as
> the DSL topology audit that `axb-gherkin-and-dsl/SKILL.md` Phase 6 tells an agent to run) stay
> authoritative in their own skill. This README does not restate them.

```bash
make install-hooks   # once per clone: run the gate before every commit
make check           # everything: invariant checks + the DSL topology audit of the example tree
make test            # the checkers' own test suites
make help            # list targets
```

**`make install-hooks` is the part that matters**, because a gate nobody runs cannot tell a
clean tree from an unexamined one. It installs a small **stub** into `.git/hooks/pre-commit`
that execs the tracked `scripts/hooks/pre-commit` from the current branch, so the gate runs
before every commit (~0.4s) and blocks the commit if any check fails. `git commit
--no-verify` skips it, as git intends — a reminder, not a lock.

Three design points worth knowing:

- **The gate checks the staged index, not the working tree.** A commit is built from the
  index, so with `git add -p` the two differ: a violation fixed on disk but still staged
  would pass a worktree check and land anyway. The hook snapshots the index
  (`git checkout-index -a --prefix=…`) and runs the checks against that snapshot.
- **The installed file is a stub, not a symlink into the worktree.** The hook script only
  exists on branches that carry it, and a symlink dangles elsewhere — which makes git treat
  the hook as absent, so the gate would **vanish silently** the moment you switched to a
  branch predating it. The stub always exists and **fails closed** when the script is
  missing: an ungated commit is refused rather than allowed. That means committing on a
  branch that predates the hook requires `git commit --no-verify` or a rebase — deliberate,
  because silent ungating is exactly what the gate exists to prevent.
- **Neither `core.hooksPath` nor a foreign hook is touched.** `hooksPath` *replaces* git's
  hook directory, disabling every other hook you have; the stub adds one file instead. It
  refuses to overwrite a hook it does not own, and `make uninstall-hooks` removes only what
  it created — a stub carrying its own marker line, or the pre-stub symlink it recognises
  as its own. Anything else is left alone.
- **What "its own" means is defined once.** `scripts/hooks/classify-hook` decides, and both
  recipes call it, so install and uninstall can never disagree. Identity is by the link
  target's *tail* and by file content, not by absolute path — a moved clone, a linked
  `git worktree` and macOS logical-vs-physical paths all make a path comparison misclassify
  the repository's own hook as foreign.
- **Install swaps atomically.** The new stub is copied to `pre-commit.tmp` and then moved
  over the old one, so a failed copy leaves the working hook in place rather than removing
  it first.

The hook is **git-native rather than forge-specific**: a file in `.git/hooks/` works
identically on any remote or none, needs no network, and survives a move away from any
particular hosting service. The trade-off is honest — this is local configuration, so each
clone must run `make install-hooks` once, and **a fresh clone is ungated until someone does**.
A forge-side gate would be universal but vendor-locked; this repository would rather be
portable than universal.

`make check` runs one group per target below — deliberately not "runs *N* groups", because a
count is a second place the list can go stale. This README already records what happens when one
vocabulary is enumerated in three places (the plan-package placeholder drifted before #11 settled
it); a number in front of the table has the same failure mode and none of the utility.

| Target | Checks |
| --- | --- |
| `make check-paths` | no `specs/` root other than `plans`/`truth`; no truth artifact read as package-local; the plan-package placeholder always prefixed by `specs/plans/` |
| `make check-tokens` | the fixed-token registry agrees with its definitions, and tokens are spelled canonically wherever they are named |
| `make check-names` | every backticked slash command names a real skill, and every `§N` names a real `STANDARDS.md` section |
| `make check-refs` | **candidate report, never fails** — normative references to issues, and rules asserting a delivery gate (a human decides whether the check behind each exists) |
| `make check-params` | every `Default Params` cell in the example tree conforms to `STANDARDS.md` §4.3 — the operand rule included |
| `make check-ui-plan` | every frame or page a `ui-plan` example refers to is one that plan declares (#24 item 3) |
| `make check-audit` | the DSL topology audit against `skills/axb-gherkin-and-dsl/examples/ecommerce/features`, this repo's own worked example |

Every group **fails** on violation except `check-refs`, which only **reports**, because its two
invariants need human triage: a citation that records provenance is fine while one a reader must
follow to comply is a defect, and a delivery claim is only wrong if the named check does not exist.
A check that fails on candidates it cannot triage gets disabled, so it reports instead.

### Exemptions are the expensive part

Three checker PRs (#21, #23, #27) have put **zero** defects in their invariants and every one of
their defects in the exemption machinery: a ±40-character context window, an operand read off the
value instead of the parameter, a 16-character lookbehind, a hard-coded exempt-token set, a
`STANDARDS.md` self-skip. That base rate is how review effort and fixture budget should be spent,
and it is why three rules are not negotiable here:

1. **Every exemption lives in `invariant_allowlist.json`.** An exemption expressed in code is one
   the staleness test cannot see, and a comment claiming the test covers it is worse than no
   comment — that was #27's finding 1, inside the checker that polices false claims.
2. **Every allowlist entry has a staleness test.** `scripts/test_check_invariants.py` fails if an
   entry stops matching live text, in either entry shape, and the scan itself has fixtures that
   are stale on purpose — a guard nothing has watched fail is a guard that may not exist.
3. **No exemption is expressible as a byte radius.** "Within 16 characters of the word Apache" is
   a rule about text layout, not about meaning: it excluded `Apache-2.0 §11(x)` and missed
   `Apache License 2.0 §11(x)` and `Apache-2.0, §11(x)`, which are the same citation. If a
   predicate cannot be written as "the line matches this", the exemption is not understood yet.

The consequence is worth stating plainly, because it is the *why* that keeps the rules from being
optimised away: **the exemption is the expensive part of adding a check.** Budget the fixtures
there, and review there, first.

Supporting files:

- `scripts/check_invariants.py` — stdlib only, PEP 723 header, hand-runnable with `--root`,
  `--only paths|tokens|names|refs`.
- `scripts/token_registry.json` — **the single enumeration** of fixed contract vocabulary. Other
  surfaces may name tokens because their readers need them, but they do not define them; where a
  surface duplicates a list, the registry is what keeps the copies honest.
- `scripts/invariant_allowlist.json` — the **only** place an exemption may live. Two entry shapes:
  `{path, contains}` for a mention-to-forbid, and `{path, line_matches}` for a context predicate
  that a substring cannot express (a licence name anywhere before the `§` on the line). Both are
  staleness-tested; see "Exemptions are the expensive part" above.
- `scripts/check_dsl_default_params.py` — executes `STANDARDS.md` §4.3 against the example tree's
  `Default Params` cells. Seeded from #19 and the seed for #24 item 5.
- `scripts/check_ui_plan_outputs.py` — executes "no reference to a frame or page the plan does not
  declare" against both `ui-plan` examples: every labelled screen line (`Corresponding … file:`,
  `Entry frame:`, `Multi-page entry:`), every `Keybinding Map` target frame and every `State
  Transition List` endpoint must appear on its own plan's `Planned output files:` line. Built from
  #24 item 3, whose two historical instances (#14) were contradictions of exactly that kind.
  Prose endpoints that name a state rather than a file are counted and printed, not failed — they
  are not machine-resolvable, and a check that fails on what it cannot triage gets deleted.
  Two structural rules, from the review of #28: **one fence mask**, because fenced content is
  documentation *about* the format (a quoted `Planned output files:` line made a filled plan look
  like a template; a fenced `Corresponding frame file:` example became a false failure); and **one
  classifying pass**, because two hand-synchronised parsers let an item vanish from the verdict
  *and* from the printed gap. The output prints `seen = checked + prose`, and `main()` fails when
  it audited no plans — `make check` runs it, `make test` does not, so a commit-time gate that
  judged nothing would otherwise pass every commit.
- `scripts/hooks/` — the tracked gate: `pre-commit` (snapshots the index, runs `make check`),
  `pre-commit-stub` (installed into `.git/hooks`, branch-independent, fails closed) and
  `classify-hook` (the single definition of which hook is ours).
- `scripts/test_hooks.py` — the hook lifecycle as tests: install, clean commit, staged and
  partial-staged violations, a branch without the gate script, a moved clone, a failed
  upgrade, uninstall, foreign hooks and a stale stub. Every one of these was a defect found
  by review or by probing, so they belong in `make test` rather than in a PR transcript.
- `scripts/test_check_invariants.py`, `scripts/test_check_dsl_default_params.py`,
  `scripts/test_check_ui_plan_outputs.py` — prove each check against **its own historical escape**
  rather than only against a clean tree. The `ui-plan` suite also pins the tree's reference count,
  the skipped set and the prose count, and asserts `checked + prose == seen` over the shipped tree,
  so a glob that stops matching or a parser that drops an item fails the suite instead of quietly
  checking nothing.

The rationale, the twelve failure modes these checks exist for, and the defect each would have
caught are recorded in [#12](https://github.com/gosharplite/aixbdd-en/issues/12).
