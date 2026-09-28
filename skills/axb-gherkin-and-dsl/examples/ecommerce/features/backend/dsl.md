# Backend Shared DSL

Cross-module shared sentences. Module-specific sentences are written in `{module}/dsl.md`.

## Given Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | StepDef Implementation Semantics |
| --- | --- | --- | --- | --- |
| `the platform has a usable discount code "{discount-code}"` | `discount-code`: string; the discount code text. | Not supported | `discount-amount`: integer; defaults to 100. | `How`: create a usable discount code. `State landing`: the backend discount code data exists and is enabled. `Write-back`: the discount code data. |
| `the platform's checkout rules are as follows:` | none | Supported:`Rule` (required, string), `Value` (required, integer) | none | `How`: set the shipping fee, discount threshold, and free-shipping threshold. `State landing`: the backend checkout settings have been updated. `Write-back`: a snapshot of the platform rules. |
| `the cart already contains the following items:` | none | Supported:`Product Code` (required, string), `Unit Price` (required, integer), `Quantity` (required, integer) | `player`: defaults to the current cart owner. | `How`: create the cart items row by row per the table. `State landing`: the backend cart contains all rows. `Write-back`: the cart details and product subtotal. |

## When Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | StepDef Implementation Semantics |
| --- | --- | --- | --- | --- |
| `"{player}" applies discount code "{discount-code}"` | `player`: string; the player name.<br>`discount-code`: string; the discount code text. | Not supported | `target-cart`: defaults to that player's current cart. | `How`: call the discount-code application entry. `State landing`: on success the discount code status, order summary, and shipping fee recalculation are all written; on failure the order state is unchanged. `Write-back`: the response, the latest order summary, and the discount code status. |

## Then Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | StepDef Implementation Semantics |
| --- | --- | --- | --- | --- |
| `this operation was rejected` | none | Not supported | none | `Must-check`: `Presented Result`: this operation returns a rejection. `Authoritative State`: the order, discount code, and cart truths are not polluted by the failed operation. |
| `the order summary is as follows:` | none | Supported:`Item` (required, string), `Value` (required, string or integer) | none | `Must-check`: `Presented Result`: the summary in the response matches the table. `Authoritative State`: the backend order truth is consistent. `Re-read Confirmation`: viewing the order summary again still matches. |
