# Backend Shared DSL

Cross-module shared sentences. Module-specific sentences are written in `{module}/dsl.md`.

## Given Sentences

| DSL 句型 | Gherkin 參數 | Data Table 參數 | 預設參數 | StepDef 實作語意 |
| --- | --- | --- | --- | --- |
| `the platform has a usable discount code "{discount-code}"` | `discount-code`: string; the discount code text. | 不支援 | `discount-amount`: integer; defaults to 100. | `怎麼做`: create a usable discount code. `權威狀態落地`: the backend discount code data exists and is enabled. `回寫`: the discount code data. |
| `the platform's checkout rules are as follows:` | none | 支援：`Rule` (required, string), `Value` (required, integer) | none | `怎麼做`: set the shipping fee, discount threshold, and free-shipping threshold. `權威狀態落地`: the backend checkout settings have been updated. `回寫`: a snapshot of the platform rules. |
| `the cart already contains the following items:` | none | 支援：`Product Code` (required, string), `Unit Price` (required, integer), `Quantity` (required, integer) | `player`: defaults to the current cart owner. | `怎麼做`: create the cart items row by row per the table. `權威狀態落地`: the backend cart contains all rows. `回寫`: the cart details and product subtotal. |

## When Sentences

| DSL 句型 | Gherkin 參數 | Data Table 參數 | 預設參數 | StepDef 實作語意 |
| --- | --- | --- | --- | --- |
| `"{player}" applies discount code "{discount-code}"` | `player`: string; the player name.<br>`discount-code`: string; the discount code text. | 不支援 | `target-cart`: defaults to that player's current cart. | `怎麼做`: call the discount-code application entry. `權威狀態落地`: on success the discount code status, order summary, and shipping fee recalculation are all written; on failure the order state is unchanged. `回寫`: the response, the latest order summary, and the discount code status. |

## Then Sentences

| DSL 句型 | Gherkin 參數 | Data Table 參數 | 預設參數 | StepDef 實作語意 |
| --- | --- | --- | --- | --- |
| `this operation was rejected` | none | 不支援 | none | `必查`: `呈現結果`: this operation returns a rejection. `權威狀態`: the order, discount code, and cart truths are not polluted by the failed operation. |
| `the order summary is as follows:` | none | 支援：`Item` (required, string), `Value` (required, string or integer) | none | `必查`: `呈現結果`: the summary in the response matches the table. `權威狀態`: the backend order truth is consistent. `再讀確認`: viewing the order summary again still matches. |
