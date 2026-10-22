# Checkout DSL

This module's specific sentences. For cross-module shared sentences see [`../dsl.md`](../dsl.md).

## Given Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | Playwright BDD Implementation Semantics |
| --- | --- | --- | --- | --- |
| `the cart already contains the following items:` | none | Supported:`Product Code` (required, string), `Unit Price` (required, integer), `Quantity` (required, integer) | `player`: defaults to the current checkout player. | `use fixtures`: create the cart contents through the cart fixture. `Arrange source`: the backend cart truth. `write-back data`: the frontend's initial cart state. `No-check`: the checkout page's rendered summary — this step only arranges the cart. |
| `the platform has a usable discount code "{discount-code}"` | `discount-code`: string; the discount code text. | Not supported | none | `use fixtures`: prepare an applicable discount code through the discount fixture. `Arrange source`: the backend discount code truth. `write-back data`: the code the next When step types. `No-check`: the cart contents and the order summary. |

## When Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | Playwright BDD Implementation Semantics |
| --- | --- | --- | --- | --- |
| `"{player}" enters discount code "{discount-code}" on the checkout page and applies it` | `player`: string; the player name.<br>`discount-code`: string; the discount code text. | Not supported | `initial-screen`: string; defaults to the checkout page. | `page operations`: open the checkout page as that player, type the discount code, click apply. `Arrange source`: the cart and discount code the Given steps prepared. `wait conditions`: wait for the order summary to finish recalculating before reading it. `write-back data`: the discount information on screen and the latest order summary. `No-check`: the resulting amounts and statuses — the following Then asserts those; this step only performs the action. |
| `"{player}" views the checkout page summary again` | `player`: string; the player name. | Not supported | `target-page`: defaults to the checkout page. | `page operations`: refresh the checkout page, or re-enter it. `Arrange source`: the cart state left by the preceding steps — a re-read changes nothing. `wait conditions`: wait for the summary to render before reading it. `write-back data`: the latest on-screen summary. `No-check`: the summary values themselves — re-reading must not alter them; the following Then compares them. |

## Then Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | Playwright BDD Implementation Semantics |
| --- | --- | --- | --- | --- |
| `the checkout page shows the following information:` | none | Supported:`Item` (required, string), `Value` (required, string or integer) | none | `Must-check`: `Presented Result`: the checkout page displays the table content row by row. `Authoritative State`: the backend order summary is consistent. `Re-read Confirmation`: still consistent after a refresh. |
| `the checkout page shows the discount code status is "{status}"` | `status`: string; e.g. `applied`. | Not supported | none | `Must-check`: the screen and the backend discount status are consistent. |
| `the screen shows an error "{error}"` | `error`: string; a readable business error. | Not supported | none | `Must-check`: the screen shows the business error, and the backend truth has not been wrongly changed. |
| `the discount code input area is still editable` | none | Not supported | none | `Must-check`: after the application fails, the input area is still editable and can be submitted again. `Should Not Happen`: the UI must not be locked up after a failure. |
