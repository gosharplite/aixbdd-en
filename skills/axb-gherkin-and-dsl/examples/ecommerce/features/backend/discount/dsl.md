# Discount DSL

This module's specific sentences. For cross-module shared sentences see [`../dsl.md`](../dsl.md).

## Given Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | StepDef Implementation Semantics |
| --- | --- | --- | --- | --- |
| `"{player}" has already applied discount code "{discount-code}"` | `player`: string; the player name.<br>`discount-code`: string; the discount code text. | Not supported | `target-cart`: the current cart of `{player}`, established by the preceding cart step. | `How`: call the discount-code application entry (the shared `../dsl.md` When sentence's entry) once in setup — do not replay the application as a visible act. `State landing`: the discount code is applied to the backend order, and the order summary reflects it. `Write-back`: the order with the discount applied, its order summary, and the applied discount code's status. `No-check`: the first application's response and the discount code status — the applied state is verified by the scenario's final Then. |

## Then Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | StepDef Implementation Semantics |
| --- | --- | --- | --- | --- |
| `the discount code status is "{status}"` | `status`: string; e.g. `applied`, `rejected`. | Not supported | none | `Must-check`: `Presented Result`: the discount code status in the response is correct. `Authoritative State`: the discount code status in the backend order is consistent. |
| `the error is "{error}"` | `error`: string; the business error name. | Not supported | none | `Must-check`: `Presented Result`: the error name in the response is correct. `Authoritative State`: the order and discount data are not polluted after the failure. |
