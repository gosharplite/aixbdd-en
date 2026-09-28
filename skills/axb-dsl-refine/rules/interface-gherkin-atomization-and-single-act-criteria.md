# Rule 1 - Acceptance Journeys must be split into interface-level atomic rules

- Level: `MUST`
- `features/acceptance/**` may express complete business acceptance with multi-step Journeys; `features/{interface-name}/**` must not copy that flow granularity as-is.
- The business outcomes, failure invariants, and interface-observable results in the Journey should be extracted one by one and dispatched to the interfaces genuinely responsible for them, each forming independently executable Rules.
- The same set of Given / When repeating across different Rules is an acceptable test isolation cost; do not re-chains multiple rules back into a flow for deduplication.

## Good Example

- This example splits one three-guess Journey into three interface rules that can fail independently.

```gherkin
Rule: a valid three-guess must return all three scoring results at once
Rule: a missed three-guess only hands the turn to the opponent once
Rule: the opponent's cipher must not be revealed before the match ends
```

## Bad Example

- This example chains the shot, the not-your-turn rejection, the opponent's single guess, and the second shot all into one Example.

```gherkin
Rule: complete three-guess flow
  Example: Alice three-guesses then Bob single-guesses
    When "Alice" submits a three-guess
    Then it is now "Bob"'s turn
    When "Bob" submits a single guess
    Then it is now "Alice"'s turn
```

# Rule 2 - Each Rule may verify exactly one subject

- Level: `MUST`
- Each Rule has exactly one subject: one named business event or outcome. The multiple `Then` / `And` in the same Rule may only be evidence aspects of this subject's outcome; do not stuff all subsequent results into the same case just because one operation is shared.
- The judgment uses entailment: write the subject's outcome first, then ask one by one — under the domain model, does a valid state exist where "the subject outcome holds but this assertion does not"?
  - No such state (this assertion is entailed by the subject outcome) → it may stay in the same Rule.
  - Such a state exists (not entailed) → this is another aspect and must be split into a different Rule.
- Entailment looks only at "valid domain states", not at "whether it can fail alone after injecting an artificial bug". Any artificial bug can make a single assertion fail alone; using "can it fail alone" as the premise degenerates into exactly one `Then` per Rule, is not decidable, and must not be adopted (the original "if only one result is broken, could this Rule still pass" is exactly this invalid reading).
- If a `Then`'s predicate points to a new subject (another object or event nameable in domain terms), it is a second aspect regardless of whether the same operation is shared, and must be split into a separate Rule.
- `STANDARDS.md` §5.2's channel labels `Presented Result` / `Authoritative State` / `Re-read Confirmation` / `Cross-Perspective` / `Should Not Happen` are fixed contract vocabulary (see the Project Language section of `STANDARDS.md`); together with the exit / verdict channels they are the evidence-channel vocabulary for "the same subject", and they do not authorize merging independent non-entailed facts into one Rule.
- Whether the subject's outcome entails a sub-assertion depends on domain semantics; the author must point to the domain model, contract, or data definitions relied upon. When undecidable, converge the domain semantics first; do not split or merge on gut feeling.
- The following are smells, not criteria: if a Rule title contains success and failure, acceptance and rejection, presented result and state invariant, history write and turn switch at the same time, it can usually still be split.

## Calibration Set

- Any new atomization criterion must simultaneously reproduce all anchors in the table below; this table is also the convergence basis for issue #5.

| Case | Subject | Is the sub-assertion entailed? | Verdict |
| --- | --- | --- | --- |
| Rule 2 Good Example: `the match has ended` + `Alice wins` | one winning event | Yes (winning ⟹ match ended) | Merge into one Rule |
| CLI successfully creates workspace: response content + exit 0 (tellme#4 Q2) | one successful creation | Yes (under the contract definition, the response and verdict channel are determined by the success outcome) | Merge into one Rule |
| Rule 1 Good Example: the three three-guess Rules | three mutually independent results | No | Split into three Rules |
| Rule 6 Good Example: the "reject / no history added / turn unchanged" of not-your-turn | three prohibitions that can each fail | No (each prohibition can fail independently) | Split into three Rules |
| tellme#4 W2: `reuses the session workspace` + `workspace still holds the file` | depends on the domain definition of `reuse the workspace` | Determined by domain definition | Merge if entailed, else split |
| tellme#4 D2: `configuration resolved` + each sub-resolution result | depends on the domain definition of `resolved` | Determined by domain definition | Merge if entailed, else split |

- W2 and D2 are structurally isomorphic (container and its contents, aggregate and its sub-results), so they **must receive the same verdict**; if the domain definition cannot answer, supplement the domain semantics first — do not split one and merge the other.

## Good Example

- Match end and the winner together prove the single aspect "any 4A wins the match for the shooting player".

```gherkin
Rule: any 4A in a three-guess wins the match for the shooting player
  Example: Alice's first guess gets 4A
    When "Alice" submits a three-guess containing 4A
    Then the match has ended
    And "Alice" wins
```

## Bad Example

- One announcement, history grouping, turn switching, cipher protection, and not-your-turn rejection can each fail independently — this is not one aspect.

```gherkin
Rule: a three-guess announces results, writes history, switches turns, and also protects the cipher and rejects other players
```

# Rule 3 - Each Example must have exactly one Act

- Level: `MUST`
- Each Example must contain exactly one `When`, representing the single business action under test in this case.
- A backend case's one Act usually corresponds to one command or one query; a second command under test must not be called consecutively in the same Example.
- A frontend case's one Act usually corresponds to one user operation that triggers the outcome under test; entering data and pressing submit once can be converged into one business When, but after submitting there must be no refresh, resubmission, or mode switching to continue another flow.
- If a Rule verifies initial screen presentation, opening the screen may be the only Act; if a Rule verifies the submit operation, an already-opened screen should be prepared via Given instead.

## Good Example

- Only one three-guess submission; the other steps are Arrange and Assert.

```gherkin
Example: Alice submits three combinations in order
  Given the match between "Alice" and "Bob" has started and it is currently "Alice"'s turn
  When "Alice" chooses to use a three-guess and submits the following three guesses at once:
    | order | guess |
    | 1     | 1234  |
    | 2     | 5678  |
    | 3     | 9012  |
  Then this three-guess returns all three results at once
```

## Bad Example

- The same Example first submits a three-guess, then has the opponent submit a single guess — two Acts.

```gherkin
When "Alice" submits a three-guess
Then it is now "Bob"'s turn
When "Bob" submits a single guess "1234"
Then it is now "Alice"'s turn
```

# Rule 4 - Action-type And must not hide a second Act

- Level: `MUST`
- `And` inherits the semantics of the previous Gherkin keyword; an And that follows a When and changes system state is still a second Act — it does not qualify merely because no second `When` is written.
- When behaviors such as "submit again", "look again", "refresh", "submit after switching", "another player acts", "retry", or "switch to another operation" appear, treat them as a new Act by default.
- An And following a Then may only be an assertion; if it sends a command, operates the UI, or advances state, it must be split into another Example.
- A DataTable is merely the input or output of the same action and does not by itself form a second Act.

## Good Example

- The And after the Then jointly proves the same winning outcome, with no repeat operation.

```gherkin
When "Alice" submits a three-guess containing 4A
Then the match has ended
And "Alice" wins
```

## Bad Example

- "Look again" is a new business action, wrongly hidden in an And.

```gherkin
When "Alice" submits a three-guess
Then the order summary has been updated
And "Alice" looks at the summary again
Then the summary is still consistent
```

# Rule 5 - Journey prior operations must be converted into completed Given states

- Level: `MUST`
- If a later Journey action is to be verified, the results of prior operations should be rewritten as completed business states in Given, not actually replaying prior Acts in the same Example.
- Given must describe states understandable by the PM, e.g. "a batch of three-guesses was just rejected entirely and it is still Alice's turn", and must not expose fixtures, endpoints, selectors, or helpers.
- If a prior result is itself an aspect under test, it should have its own Rule; converting it to Given does not mean its independent coverage may be dropped.
- Given must not smuggle in the target Act this case really wants to verify; the target operation must stay in the single When.

## Good Example

- The earlier rejection has become Arrange; this case verifies only one retry.

```gherkin
Example: Alice resubmits after fixing
  Given a batch of "Alice"'s three-guesses was just rejected entirely and it is still "Alice"'s turn
  When "Alice" submits three legal guesses
  Then this three-guess is accepted
```

## Bad Example

- This case first produces a rejection, then retries — actually containing two actions under test.

```gherkin
When "Alice" submits an illegal three-guess
Then this three-guess is rejected
When "Alice" resubmits after fixing
Then this three-guess is accepted
```

# Rule 6 - Atomization must not lose or expand the Acceptance contract

- Level: `MUST`
- Before splitting, inventory every business outcome, failure invariant, and cross-perspective result of the acceptance; after splitting, each must be carried by at least one relevant interface Rule.
- Each interface is not required to repeat all results; the frontend only carries operable and observable responsibilities, the backend carries command, authoritative state, and contract responsibilities, and other interfaces are dispatched per the analysis outputs.
- Do not add restrictions, error outcomes, or technical behaviors not required by acceptance just to make atomic cases look complete.
- Unobservable requirements (Unobservable NFRs / internal invariants) that cannot be expressed as external Gherkin steps are **strictly forbidden from being silently dropped**, and must not be written as unwitnessed prose directly into a `dsl.md` preamble or interface comments; they must be explicitly routed downstream to `/axb-tasks` as `[WITNESS]` tasks or recorded on the project's declared decision surface (ADR).
- After splitting, every Example must be Arrange-able independently and must not depend on a previous Example having run to completion.

## Good Example

- The same acceptance outcomes are dispatched by responsibility, and overall coverage remains complete.

```gherkin
# frontend
Rule: both shot operations must be disabled when it is not your turn

# backend
Rule: a player whose turn it is not must not submit a three-guess
Rule: a not-your-turn player's three-guess must not add history
Rule: a not-your-turn player's three-guess must not change the turn
```

## Bad Example

- Only the on-screen disabling is kept, losing the acceptance-specified history and turn invariants.

```gherkin
Rule: the button must be disabled when it is not your turn
```

# Rule 7 - Structure convergence must pass the atomization checks item by item

- Level: `MUST`
- Before delivery, check one by one:
  - Whether each Rule title states exactly one independently-standable outcome.
  - Whether each Example has exactly one `When`.
  - Whether an action-type And that advances state exists after When or Then.
  - Whether Journey prior operations have been converted into independently establishable Given states.
  - Whether all multiple Then / And are entailed by the same subject's outcome (see Rule 2's entailment judgment); whether non-entailed ones have been split into separate Rules.
  - Whether acceptance's all outcomes and failure invariants are still covered after splitting.
  - Whether every new Given / When / Then has a DSL definition in the same interface.
- If any item fails, fix the feature files and `dsl.md` first; do not declare them ready to hand to test implementation.

## Good Example

- The check results can cite passing evidence item by item.

```md
- Rule: each title has exactly one outcome
- Example / When: 21 / 21
- Action-type And: 0
- Acceptance outcomes: all carried by at least one interface
- DSL gaps: 0
```

## Bad Example

- Only confirms the Gherkin parses, without checking test granularity and contract coverage.

```md
- The feature files have no syntax errors, therefore deliverable
```

# Rule 8 - Reference examples must not override this RuleFile's atomization requirements

- Level: `MUST`
- The examples of `axb-gherkin-and-dsl` may be used to understand business language, file splitting, DataTables, and the finished look of DSL, but their flow-type Examples must not be used to override this RuleFile.
- If a reference example contains a second When, an action-type And, or a Rule that can be split further, only the non-conflicting parts may be followed, and it must be refactored per this RuleFile before use.
- Reference examples are not the acceptance authority, nor a source of exceptions for relaxing interface test granularity.

## Good Example

- Only the table and sentence-pattern style of the reference example is followed; the case still maintains a single Act.

```gherkin
Example: shipping fee 60 is shown when the discounted product amount is 950
  Given an order has successfully applied a discount code and the discounted product amount is 950
  When "Alice" views the checkout page summary
  Then the checkout page shows a shipping fee of 60
```

## Bad Example

- Because a reference example once contained "look again", a second When is kept in the same Example.

```gherkin
When "Alice" applies a discount code
Then the checkout page shows a shipping fee of 60
When "Alice" views the checkout page summary again
Then the checkout page still shows a shipping fee of 60
```
