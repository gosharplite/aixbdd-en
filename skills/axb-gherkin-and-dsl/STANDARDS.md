# Gherkin And DSL Standards

These standards are the detailed criteria for the `axb-gherkin-and-dsl` skill. There is only one principle:

> Gherkin must be readable by the PM; the DSL must let the AI / test author implement it as test code with almost no guessing.

## Project Language

- By default this standard assumes artifacts are written in **Traditional Chinese**, but the language is **declared by the project, not hard-fixed by this standard**.
- A project MAY override the default language. The declaration must land in a **named home** (in order): the project's `.agents/constitution/shared.md`, the project's decision records (ADRs, e.g. `decisions/NNNN-*.md`), or an explicit constraint in `spec.md`. When no declaration is found, the default is Traditional Chinese.
- The override **covers only the "project-declared language" parts**; the following DSL contract vocabulary is **fixed** and does not change with the project language:

| Aspect | Language | Basis |
| --- | --- | --- |
| feature file names (§2) | project-declared | non-contract tokens, translatable |
| Gherkin parameter key names (§3) | project-declared | must match the language of the Gherkin sentences |
| Gherkin sentences, keywords, and prose | project-declared | the audit script `audit_feature_dsl_topology.py`'s `STEP_RE` already accepts both English and Chinese keywords |
| §3's quoting and DataTable conventions | language-independent | always followed, unchanged with language |
| §4/§5's DSL meta-schema field tokens (`DSL 句型`, `Gherkin 參數`, `Data Table 參數`, `預設參數`, implementation-semantics column) | **fixed** | the audit script identifies a table by its first column header being exactly `DSL 句型`; translating that token makes the audit silently match zero and every step be misjudged as missing a DSL |
| §5.2's channel labels (`呈現結果` / `權威狀態` / `再讀確認` / `跨視角` / `不該發生`) and §5.1's Given / When sub-labels (`怎麼做` / `權威狀態落地` / `回寫` / `不必查`) | **fixed** | cross-project shared contract vocabulary |

- In other words: **project-declared** = file names, parameter keys, sentences, and prose; **fixed** = the §4/§5 meta-schema tokens and contract channel vocabulary.
- This section and the governance layer's language rules (e.g. `.agents/constitution/shared.md`'s "descriptive text must be written in Traditional Chinese") are complementary: governance-layer rules define the **default language and where it lands**; this section defines the **scope that a project declaration may override**.

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

- Split feature files by system functional aspect first; file names default to Traditional Chinese (the language may be overridden by project declaration per the "Project Language" section) and must clearly express the action or aspect under test.
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
- Parameter key names default to Traditional Chinese and should match the spec as closely as possible, e.g. `玩家` (player), `配對碼` (match code), `密文` (cipher), `猜測` (guess); the language may be overridden by project declaration per the "Project Language" section, and must be consistent with that project's Gherkin sentence language.

## 4. DSL Required Fields

Every DSL row in the interface root and module `dsl.md` must have at least the following (the field tokens below are fixed contract vocabulary and do not change with the project language; see the "Project Language" section):

- `DSL 句型`
- `Gherkin 參數`
- `Data Table 參數`
- `預設參數`
- implementation-semantics column

### 4.1 Gherkin Parameter Column

- Bullet-list each parameter
- Each parameter must contain at least: name, type, minimal necessary semantics
- Do not write supplements that are already obvious from the sentence itself

### 4.2 Data Table Parameter Column

- Each sentence must state explicitly whether DataTable is supported
- If not supported, write only `不支援`
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

- `怎麼做` (how to do it)
- `權威狀態落地` (authoritative state landing)
- `回寫` (write-back)
- `不必查` (no need to check)

Principles:

- After the action completes, the authoritative state must first land in the store / DB
- Writing back only `last_response` is not enough
- For a failed request, it must be stated explicitly that the authoritative state must not be altered

### 5.2 Then Granularity

Then is written as a "verification contract", not force-fitted into a fixed template, but at least pick the relevant ones from these channels:

- `呈現結果`: this API response
- `權威狀態`: store / DB truth
- `再讀確認`: still holds on a second read
- `跨視角`: whether another player sees the same
- `不該發生`: must not be changed, must not be created, must not be leaked

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

### 6.3 Strictness Requirements

- Frontend Then must not look only at on-screen text
- The room owner / cipher protection / turn hints shown on screen must be able to correspond to the backend authoritative state
- `guess action unavailable` must not only verify `disabled`, but also confirm the user really cannot submit that action
- `screen does not contain a certain cipher` must not only check the full string; where necessary, prevent the digits from being leaked by being split across multiple cells or segments

## 7. Coverage & Implementability Checks

Final checks:

- Every test case's Arrange / Act / expected output / must-remain-invariant is absorbed by Gherkin + DSL
- There are no verification points that only remain in the original-text comments but are not covered by steps
- If any Gherkin step, after merging interface root and same-module `dsl.md` lookups, does not hit exactly one row, it counts as a gap; zero means an omission, multiple means duplicated authoritative locations or sentence ambiguity
- **Normative Claim Routing check**: unobservable requirements (unobservable NFRs / internal invariants) must not be silently dropped during conversion to Gherkin. All normative items originating from `spec.md` that do not enter Gherkin must be explicitly routed to the RD-side `[WITNESS]` tasks or the project decision surface, and included in the `Claim→Witness` inventory.
- Gherkin sentences remain PM-readable business language
- The DSL is already sufficient for the AI to reason out test code without massive guessing
- The mechanical audit only points out topology, duplicate, and matching problems; whether shared contracts are semantically consistent is still judged by the agent

## 8. Typical Refactoring Order

1. First move reviewable Gherkin drafts out of the testplan
2. Supplement `When` first, then `Given / Then`
3. Then converge shared sentences
4. First complete the sentences at the unique authoritative DSL location, then backfill the feature
5. Then do `Rule` / `Background` / `DataTable` / `Scenario Outline` structure optimization
6. Finally check coverage and strictness

## 9. When to Stop Abstracting Further

If further abstraction causes any of the following, stop:

- Rules become too large, no longer atomic
- Example titles lose their data-scenario feel
- DataTable columns become too numerous, actually reducing readability
- Scenario Outline force-mixes cases that are actually different rules
- Gherkin exposes technical details for implementation convenience
