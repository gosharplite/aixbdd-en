# Checkout DSL

This module's specific sentences. For cross-module shared sentences see [`../dsl.md`](../dsl.md).

## Given Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | Playwright BDD Implementation Semantics |
| --- | --- | --- | --- | --- |
| `the cart already contains the following items:` | none | Supported:`Product Code` (required, string), `Unit Price` (required, integer), `Quantity` (required, integer) | `player`: defaults to the current checkout player. | `How`: prepare the cart contents via a fixture. `State landing`: the backend cart truth already exists. `Write-back`: the frontend initial cart state. |
| `the platform has a usable discount code "{discount-code}"` | `discount-code`: string; the discount code text. | Not supported | none | `How`: use a fixture to prepare an applicable discount code. `State landing`: the backend discount code is usable. |

## When Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | Playwright BDD Implementation Semantics |
| --- | --- | --- | --- | --- |
| `"{player}" enters discount code "{discount-code}" on the checkout page and applies it` | `player`: string; the player name.<br>`discount-code`: string; the discount code text. | Not supported | `initial-screen`: string; defaults to the checkout page. | `How`: open the checkout page from that player's perspective, enter the discount code, and click apply. `State landing`: on success the backend order recalculation is complete; on failure the backend order is unchanged. `Write-back`: the discount information on screen and the latest order summary. |
| `"{player}" views the checkout page summary again` | `player`: string; the player name. | Not supported | `target-page`: defaults to the checkout page. | `How`: refresh or re-enter the checkout page. `State landing`: this is a re-read confirmation and must not change the order state. `Write-back`: the latest on-screen summary. |

## Then Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | Playwright BDD Implementation Semantics |
| --- | --- | --- | --- | --- |
| `the checkout page shows the following information:` | none | Supported:`Item` (required, string), `Value` (required, string or integer) | none | `Must-check`: `Presented Result`: the checkout page displays the table content row by row. `Authoritative State`: the backend order summary is consistent. `Re-read Confirmation`: still consistent after a refresh. |
| `the checkout page shows the discount code status is "{status}"` | `status`: string; e.g. `applied`. | Not supported | none | `Must-check`: the screen and the backend discount status are consistent. |
| `the screen shows an error "{error}"` | `error`: string; a readable business error. | Not supported | none | `Must-check`: the screen shows the business error, and the backend truth has not been wrongly changed. |
| `the discount code input area is still editable` | none | Not supported | none | `Must-check`: after the application fails, the input area is still editable and can be submitted again. `Should Not Happen`: the UI must not be locked up after a failure. |
