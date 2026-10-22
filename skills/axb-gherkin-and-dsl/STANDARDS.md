# Gherkin And DSL Standards

These standards are the detailed criteria for the `axb-gherkin-and-dsl` skill. There is only one principle:

> Gherkin must be readable by the PM; the DSL must let the AI / test author implement it as test code with almost no guessing.

## Project Language

- By default this standard assumes artifacts are written in **English**, but the language is **declared by the project, not hard-fixed by this standard**.
- A project MAY override the default language. The declaration must land in a **named home** (in order): the project's `.agents/constitution/shared.md`, the project's decision records (ADRs, e.g. `decisions/NNNN-*.md`), or an explicit constraint in `spec.md`. When no declaration is found, the default is English.
- The override **covers only the "project-declared language" parts**; the following DSL contract vocabulary is **fixed** and does not change with the project language:

| Aspect | Language | Basis |
| --- | --- | --- |
| feature file names (§2) | project-declared | non-contract tokens, translatable |
| Gherkin parameter key names (§3) | project-declared | must match the language of the Gherkin sentences |
| Gherkin sentences, keywords, and prose | project-declared | the audit script `audit_feature_dsl_topology.py`'s `STEP_RE` already accepts both English and Chinese keywords |
| §3's quoting and DataTable conventions | language-independent | always followed, unchanged with language |
| §4/§5's DSL meta-schema field tokens (`DSL Sentence`, `Gherkin Params`, `Data Table Params`, `Default Params`, implementation-semantics column) | **fixed** | the audit script identifies a table by its first column header being exactly `DSL Sentence` (the legacy upstream Chinese header `DSL 句型` is also accepted); translating that token makes the audit silently match zero and every step be misjudged as missing a DSL |
| §5.2's `Must-check` Then marker and channel labels (`Presented Result` / `Authoritative State` / `Re-read Confirmation` / `Cross-Perspective` / `Should Not Happen`), and §5.1's Given / When sub-labels (`How` / `State landing` / `Write-back` / `No-check`) | **fixed** | cross-project shared contract vocabulary; `Must-check` is the single Then marker for every interface kind (§5.2 defines it, §6 and §7 use it) |
| §7's CLI Given / When sub-labels (`Invocation` / `Working state` / `Landing` / `Captured outputs` / `No-check`) and Then channels (`Stdout` / `Stderr` / `Exit Code` / `Filesystem State` / `Re-read Confirmation` / `Should Not Happen`) | **fixed** | cross-project shared contract vocabulary; §7 is the single enumeration for CLI, and the two Then channels it shares with §5.2 keep their §5.2 definitions |

- In other words: **project-declared** = file names, parameter keys, sentences, and prose; **fixed** = the §4 meta-schema tokens and the §5 / §7 contract channel vocabulary. (§6's granularity labels are guidance for how to write frontend semantics, not fixed contract tokens, so they stay project-declared prose — which is why the table registers no §6 row.)
- This section and the governance layer's language rules (e.g. `.agents/constitution/shared.md`'s "descriptive text must be written in English") are complementary: governance-layer rules define the **default language and where it lands**; this section defines the **scope that a project declaration may override**.

## 1. Gherkin Language Boundaries & Sentence Convergence

- Gherkin sentences speak only business semantics — never API, HTTP, selectors, sessionStorage, polling, or fixture names.
- Interfaces such as frontend and backend are written separately; under each interface, feature files are grouped by functional module, and the DSL is carried hierarchically by the same-module `dsl.md` and the interface root shared `dsl.md`.
- Every test case must ultimately have a corresponding Gherkin entity.
- Sentences that are 100% semantically identical must share the same sentence.
- If a sentence is too fat, carrying multiple actions or multiple assertions at once, it should be split into more core, reusable steps.
- DataTables are used in only two situations:
  - Multi-row data
  - A single sentence that actually implies summary information of more than 3 fields
- Default-value comments only carry "business defaults that affect reading comprehension", not technical defaults.

## 2. Feature / Rule / Example Structure

- Split feature files by system functional aspect first; file names default to English (the language may be overridden by project declaration per the "Project Language" section) and must clearly express the action or aspect under test.
- `Rule` must be atomic: one Rule carries exactly one subject, and its multiple `Then` / `And` must be entailed by that subject's outcome (entailment). For criteria and the calibration set, see `axb-dsl-refine`'s `rules/interface-gherkin-atomization-and-single-act-criteria.md` Rule 2; non-entailed assertions must be split into new Rules. An Example title that merely sounds like another rule is only a smell, not a criterion.
- `Example` should describe data scenarios, not just repeat the Rule's name.
- `Background` is used only when, within the same feature, multiple Examples genuinely share the same setup, and extracting it would not make the Examples harder to read.
- `Scenario Outline` is used only for "the same rule, exactly the same flow, only the whole data set is swapped"; if they are actually different rules, do not force a Scenario Outline.

### 2.1 Functional Modules & DSL Ownership

- A feature file must be placed at `{interface}/{module}/*.feature`; `.feature` files must not be placed directly in the interface root directory.
- Modules should first reuse the functional boundaries of existing truth; create a new module only when no existing module fits. Do not hard-code one project's current module list as a universal rule.
- Module-specific sentences go in `{interface}/{module}/dsl.md`.
- Only rows used across modules, and whose sentence, Gherkin parameters, DataTable, defaults, and implementation contract are fully identical, go in `{interface}/dsl.md`.
- Identical text or appearing twice does not justify promotion; same-text-different-meaning must be split into sentences that can identify their semantics.
- Each sentence may have only one authoritative location. When promoting or demoting, delete the old row — do not keep duplicates in root and module.
- When reading a feature, merge the interface root and same-module DSL lookups; every Gherkin step must hit exactly one row.
- **The true boundary of DSL preamble prose**: the preface, module descriptions, or comment text of a `dsl.md` **must never record unwitnessed system behavior guarantees or internal invariants** (e.g. "this module's rollback has durability and atomicity", "all file writes are guaranteed fsync'd to disk"). If such guarantees exist, observable ones must be converged into Gherkin steps and DSL rows; non-observable ones must be carried by `[WITNESS]` unit/fault-injection witness tasks, or recorded as decisions on the project's declared decision surface (ADR) — never left as unwitnessed prose in a `dsl.md` preamble.

## 3. In-Sentence Parameters & DataTable Format

- In-sentence string parameters use double quotes: `"Alice"`, `"1234"`, `"waiting"`.
- In-sentence integer parameters have no quotes: `1`, `2`.
- Values in DataTables are never quoted.
- Parameter key names default to English and should match the spec as closely as possible, e.g. `player`, `match code`, `cipher`, `guess`; the language may be overridden by project declaration per the "Project Language" section, and must be consistent with that project's Gherkin sentence language.

## 4. DSL Required Fields

Every DSL row in the interface root and module `dsl.md` must have at least the following (the field tokens below are fixed contract vocabulary and do not change with the project language; see the "Project Language" section):

- `DSL Sentence`
- `Gherkin Params`
- `Data Table Params`
- `Default Params`
- implementation-semantics column

### 4.1 Gherkin Parameter Column

- Bullet-list each parameter
- Each parameter must contain at least: name, type, minimal necessary semantics
- Do not write supplements that are already obvious from the sentence itself

### 4.2 Data Table Parameter Column

- Each sentence must state explicitly whether DataTable is supported
- If not supported, write only `Not supported`
- If supported, list:
  - required / optional
  - type
  - minimal necessary semantics

### 4.3 Default Parameter Column

- Keep only the defaults where "if not stated clearly, the AI can easily guess wrong"
- Do not stuff all internal implementation decisions in here
- Example: `invalid match code = "12"` is a good default; `wait snapshot count = 1` should not appear in Gherkin, but may live in the frontend DSL

## 5. Backend DSL Implementation Semantics

The purpose of the backend DSL is not merely to tell the AI which endpoint to hit, but to specify the minimum truth sources on which this sentence must hold.

### 5.1 Given / When Granularity

Given / When must write at least:

- `How` (how to do it)
- `State landing` (authoritative state landing)
- `Write-back` (write-back)
- `No-check` (no need to check)

Principles:

- After the action completes, the authoritative state must first land in the store / DB
- Writing back only `last_response` is not enough
- For a failed request, it must be stated explicitly that the authoritative state must not be altered

### 5.2 Then Granularity

Then is written as a "verification contract", not force-fitted into a fixed template, but at least pick the relevant ones from these channels:

- `Presented Result`: this API response
- `Authoritative State`: store / DB truth
- `Re-read Confirmation`: still holds on a second read
- `Cross-Perspective`: whether another player sees the same
- `Should Not Happen`: must not be changed, must not be created, must not be leaked

**`Must-check` — the Then cell's opening marker.** A Then row's implementation-semantics cell opens
with `Must-check`, which declares the row a *mandatory verification contract*: the assertions that
follow are the evidence this step's outcome must produce, not optional commentary. It is the Then
counterpart of `No-check` in the Given / When cell (§5.1), and like `No-check` it is a **marker, not a
channel** — never write it as though it were one, and never write a Then cell without it.

After `Must-check`, the cell either:

- names the channel labels above and states the fact each must carry — `Must-check`: `Presented Result`:
  …; `Authoritative State`: …; and
- **or**, when a single straightforward assertion suffices, states that fact directly in one clause —
  `Must-check`: the screen and the backend discount status are consistent.

Both forms are conforming. What is *not* conforming is a Then cell that names no assertable fact, or one
that opens with any other prefix: this is the only Then prefix, and new ones must not be invented
(the registry in #12 is where such a thing would be registered if it ever needed adding).

`Must-check` is not backend-specific: the frontend (§6) and CLI (§7) Then cells open with it too,
followed by their own channels or a direct fact. §5.2 is its single definition.

Principles:

- Then must not stop at the response alone
- For business facts like "opened a new room", "joined an existing room", "guessed the cipher correctly", "this operation was rejected", at least verify both the response and the authoritative state
- Rejection-type Then must especially verify "the state was not corrupted by the failed request"

## 6. Frontend DSL Implementation Semantics

The frontend assumes implementation as Playwright BDD.

### 6.1 Things That Must Not Appear in the DSL Main Table

- raw selectors
- raw sessionStorage keys
- fragmented DOM implementation details
- helper internal implementations

These should live in page objects, fixture helpers, or the actual step definitions.

### 6.2 Given / When / Then Granularity

Frontend implementation semantics should prioritize around:

- `use fixtures`
- `Arrange source`
- `page operations`
- `wait conditions`
- `write-back data`

These five are guidance for how to write frontend semantics, not fixed contract tokens (which is why
the Project Language table scopes §6 as project-declared). One thing in a frontend Then cell *is* a
fixed token: it opens with **`Must-check`**, defined once in §5.2 — a frontend Then is a verification
contract exactly as a backend one is.

### 6.3 Strictness Requirements

- Frontend Then must not look only at on-screen text
- The room owner / cipher protection / turn hints shown on screen must be able to correspond to the backend authoritative state
- `guess action unavailable` must not only verify `disabled`, but also confirm the user really cannot submit that action
- `screen does not contain a certain cipher` must not only check the full string; where necessary, prevent the digits from being leaked by being split across multiple cells or segments

## 7. CLI DSL Implementation Semantics

The CLI surface is narrower than a web interface's and every channel of it is textual, numeric, or
filesystem-shaped. The DSL must therefore **name the channel**; "the output" is not a channel.

### 7.1 Given / When Granularity

Given / When must write at least:

- `Invocation` (the exact argv the step runs: command, flags, arguments, and stdin content if any)
- `Working state` (the pre-existing filesystem / config / database state the invocation acts on)
- `Landing` (where this step's effect lands: which file, which config key, which row)
- `Captured outputs` (the invocation's captured `stdout`, `stderr`, and exit status — the evidence §7.2's channels assert on)
- `No-check` (no need to check)

Principles:

- The "how" of a CLI step is the argv, not a shell line; when stdin content matters it is an input the row must state, not an environment detail the test guesses
- Every §7.2 channel asserts against what this step captured, so the capture itself is contracted here — as §5.1 requires `Write-back` rather than leaving the response implicit
- Exit status is an **output**, never a precondition — do not encode "the command succeeds" into `Given`
- For a command expected to fail, the row must state explicitly that the authoritative state must not be altered

### 7.2 Then Granularity

Then is written as a verification contract, and must at least pick the relevant channels. The cell opens
with **`Must-check`** — defined once in §5.2, and the single Then marker for every interface kind —
followed by the channels below or a directly stated fact.

- `Stdout`: this command's standard output
- `Stderr`: this command's diagnostics
- `Exit Code`: the numeric exit status
- `Filesystem State`: files, directories, or config keys written, removed, or left untouched
- `Re-read Confirmation`: still holds when re-observed through a **read-only** re-query — re-list, re-read the `Filesystem State`, or run a status subcommand. Never re-run a mutating invocation to confirm it: `create workspace` run twice fails with "already exists", so the confirmation would either be unimplementable or assert the opposite of what it should
- `Should Not Happen`: must not be written, must not be removed, must not leak

Principles:

- Then must not stop at the exit code alone
- A success Then must name at least one landing channel besides `Exit Code` — `Stdout` content, or `Filesystem State` — because a zero exit status alone cannot distinguish "did the work" from "did nothing and said nothing"
- A rejection or failure Then must verify the non-zero `Exit Code` **and** that the authoritative state was not corrupted by the failed invocation, mirroring §5.2's rejection rule
- Assert the fact the channel must carry, not the exact human-readable wording: error prose is not a contract, and pinning it makes every message edit a test failure. "`Stdout` is non-empty" is not an assertion — a greeting banner satisfies it

### 7.3 Things That Must Not Appear in the DSL Main Table

- raw executable paths, shell quoting, or pipeline operators
- ANSI escape sequences, box-drawing glyphs, or terminal-width assumptions
- internal module, function, or flag-parser names

These belong in the step definitions, helper fixtures, or the CLI's own source — the DSL states what the command must be observed to do.

### 7.4 Strictness Requirements

- `Exit Code` alone is never a sufficient Then for a command that changes state
- "prints a warning" is not verifiable: state the channel (`Stderr`) and the fact asserted, not the prose
- Terminal UX (screens, keybindings, repaint behaviour) is **not** a CLI DSL concern — an interactive TUI's surface is planned by `/axb-ui-plan` (terminal mode) and reviewed, not restated as DSL channels

## 8. Coverage & Implementability Checks

Final checks:

- Every test case's Arrange / Act / expected output / must-remain-invariant is absorbed by Gherkin + DSL
- There are no verification points that only remain in the original-text comments but are not covered by steps
- If any Gherkin step, after merging interface root and same-module `dsl.md` lookups, does not hit exactly one row, it counts as a gap; zero means an omission, multiple means duplicated authoritative locations or sentence ambiguity
- **Normative Claim Routing check**: unobservable requirements (unobservable NFRs / internal invariants) must not be silently dropped during conversion to Gherkin. All normative items originating from `spec.md` that do not enter Gherkin must be explicitly routed to the RD-side `[WITNESS]` tasks or the project decision surface, and included in the `Claim→Witness` inventory.
- Gherkin sentences remain PM-readable business language
- The DSL is already sufficient for the AI to reason out test code without massive guessing
- The mechanical audit only points out topology, duplicate, and matching problems; whether shared contracts are semantically consistent is still judged by the agent

## 9. Typical Refactoring Order

1. First move reviewable Gherkin drafts out of the testplan
2. Supplement `When` first, then `Given / Then`
3. Then converge shared sentences
4. First complete the sentences at the unique authoritative DSL location, then backfill the feature
5. Then do `Rule` / `Background` / `DataTable` / `Scenario Outline` structure optimization
6. Finally check coverage and strictness

## 10. When to Stop Abstracting Further

If further abstraction causes any of the following, stop:

- Rules become too large, no longer atomic
- Example titles lose their data-scenario feel
- DataTable columns become too numerous, actually reducing readability
- Scenario Outline force-mixes cases that are actually different rules
- Gherkin exposes technical details for implementation convenience
