# Discount DSL

This module's specific sentences. For cross-module shared sentences see [`../dsl.md`](../dsl.md).

## Given Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | StepDef Implementation Semantics |
| --- | --- | --- | --- | --- |
| `"{player}" has already applied discount code "{discount-code}"` | `player`: string; the player name.<br>`discount-code`: string; the discount code text. | Not supported | `target-cart`: defaults to that player's current cart. | `How`: arrange the order so that the code is already applied to this player's cart — call the same entry once in setup and keep the resulting order, rather than replaying the application as a visible act. `State landing`: the discount code is applied to the backend order, and the order summary reflects it. `Write-back`: the applied order state the scenario starts from. `No-check`: how the application happened — this step establishes the precondition, and the scenario does not verify the first application. |

## Then Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | StepDef Implementation Semantics |
| --- | --- | --- | --- | --- |
| `the discount code status is "{status}"` | `status`: string; e.g. `applied`, `rejected`. | Not supported | none | `Must-check`: `Presented Result`: the discount code status in the response is correct. `Authoritative State`: the discount code status in the backend order is consistent. |
| `the error is "{error}"` | `error`: string; the business error name. | Not supported | none | `Must-check`: `Presented Result`: the error name in the response is correct. `Authoritative State`: the order and discount data are not polluted after the failure. |
