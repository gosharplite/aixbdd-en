# Orders DSL

This module's specific sentences. For cross-module shared sentences see [`../dsl.md`](../dsl.md).

## When Sentences

| DSL 句型 | Gherkin 參數 | Data Table 參數 | 預設參數 | StepDef 實作語意 |
| --- | --- | --- | --- | --- |
| `"{player}" views the order summary again` | `player`: string; the player name. | 不支援 | `target-order`: defaults to that player's current checkout order. | `怎麼做`: re-read the order summary. `權威狀態落地`: this is a re-read confirmation; it does not change state. `回寫`: the full latest order summary. |

## Then Sentences

| DSL 句型 | Gherkin 參數 | Data Table 參數 | 預設參數 | StepDef 實作語意 |
| --- | --- | --- | --- | --- |
| `the items in the cart remain as follows:` | none | 支援：`Product Code` (required, string), `Unit Price` (required, integer), `Quantity` (required, integer) | none | `必查`: `權威狀態`: a failed operation does not change the original cart items. `再讀確認`: viewing the cart again still matches. |
