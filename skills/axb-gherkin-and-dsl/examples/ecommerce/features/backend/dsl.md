# Backend Shared DSL

Cross-module shared sentences. Module-specific sentences are written in `{module}/dsl.md`.

## Given Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | StepDef Implementation Semantics |
| --- | --- | --- | --- | --- |
| `the platform has a usable discount code "{discount-code}"` | `discount-code`: string; the discount code text. | Not supported | `discount-amount`: integer; defaults to 100. | `How`: create a usable discount code. `State landing`: the backend discount code data exists and is enabled. `Write-back`: the discount code data. `No-check`: the cart contents and the order summary. |
| `the platform's checkout rules are as follows:` | none | Supported:`Rule` (required, string), `Value` (required, integer) | none | `How`: set every `Rule` / `Value` row the table passes — the discount amount, discount threshold, shipping fee, and free-shipping threshold — as backend checkout settings. `State landing`: the backend checkout settings have been updated. `Write-back`: a snapshot of the platform rules. `No-check`: the cart contents. |
| `the cart already contains the following items:` | none | Supported:`Product Code` (required, string), `Unit Price` (required, integer), `Quantity` (required, integer) | `player`: defaults to the current cart owner. | `How`: create the cart items row by row per the table. `State landing`: the backend cart contains all rows. `Write-back`: the cart details and product subtotal. `No-check`: the order summary and the discount state. |

## When Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | StepDef Implementation Semantics |
| --- | --- | --- | --- | --- |
| `"{player}" applies discount code "{discount-code}"` | `player`: string; the player name.<br>`discount-code`: string; the discount code text. | Not supported | `target-cart`: defaults to that player's current cart. | `How`: call the discount-code application entry. `State landing`: on success the discount code status, order summary, and shipping fee recalculation are all written; on failure the order state is unchanged. `Write-back`: the response, the latest order summary, and the discount code status. `No-check`: the resulting amounts, statuses, and fee — the following Then asserts those. |

## Then Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | StepDef Implementation Semantics |
| --- | --- | --- | --- | --- |
| `this operation was rejected` | none | Not supported | none | `Must-check`: `Presented Result`: this operation returns a rejection. `Authoritative State`: the order, discount code, and cart truths are not polluted by the failed operation. |
| `the order summary is as follows:` | none | Supported:`Item` (required, string), `Value` (required, string or integer) | none | `Must-check`: `Presented Result`: the summary in the response matches the table. `Authoritative State`: the backend order truth is consistent. `Re-read Confirmation`: viewing the order summary again still matches. |
