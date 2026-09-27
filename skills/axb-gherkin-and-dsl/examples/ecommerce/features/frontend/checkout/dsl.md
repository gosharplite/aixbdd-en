# Checkout DSL

This module's specific sentences. For cross-module shared sentences see [`../dsl.md`](../dsl.md).

## Given Sentences

| DSL 句型 | Gherkin 參數 | Data Table 參數 | 預設參數 | Playwright BDD 實作語意 |
| --- | --- | --- | --- | --- |
| `the cart already contains the following items:` | none | 支援：`Product Code` (required, string), `Unit Price` (required, integer), `Quantity` (required, integer) | `player`: defaults to the current checkout player. | `怎麼做`: prepare the cart contents via a fixture. `權威狀態落地`: the backend cart truth already exists. `回寫`: the frontend initial cart state. |
| `the platform has a usable discount code "{discount-code}"` | `discount-code`: string; the discount code text. | 不支援 | none | `怎麼做`: use a fixture to prepare an applicable discount code. `權威狀態落地`: the backend discount code is usable. |

## When Sentences

| DSL 句型 | Gherkin 參數 | Data Table 參數 | 預設參數 | Playwright BDD 實作語意 |
| --- | --- | --- | --- | --- |
| `"{player}" enters discount code "{discount-code}" on the checkout page and applies it` | `player`: string; the player name.<br>`discount-code`: string; the discount code text. | 不支援 | `initial-screen`: string; defaults to the checkout page. | `怎麼做`: open the checkout page from that player's perspective, enter the discount code, and click apply. `權威狀態落地`: on success the backend order recalculation is complete; on failure the backend order is unchanged. `回寫`: the discount information on screen and the latest order summary. |
| `"{player}" views the checkout page summary again` | `player`: string; the player name. | 不支援 | `target-page`: defaults to the checkout page. | `怎麼做`: refresh or re-enter the checkout page. `權威狀態落地`: this is a re-read confirmation and must not change the order state. `回寫`: the latest on-screen summary. |

## Then Sentences

| DSL 句型 | Gherkin 參數 | Data Table 參數 | 預設參數 | Playwright BDD 實作語意 |
| --- | --- | --- | --- | --- |
| `the checkout page shows the following information:` | none | 支援：`Item` (required, string), `Value` (required, string or integer) | none | `必查`: `呈現結果`: the checkout page displays the table content row by row. `權威狀態`: the backend order summary is consistent. `再讀確認`: still consistent after a refresh. |
| `the checkout page shows the discount code status is "{status}"` | `status`: string; e.g. `applied`. | 不支援 | none | `必查`: the screen and the backend discount status are consistent. |
| `the screen shows an error "{error}"` | `error`: string; a readable business error. | 不支援 | none | `必查`: the screen shows the business error, and the backend truth has not been wrongly changed. |
| `the discount code input area is still editable` | none | 不支援 | none | `必查`: after the application fails, the input area is still editable and can be submitted again. `不該發生`: the UI must not be locked up after a failure. |
