# Discount DSL

This module's specific sentences. For cross-module shared sentences see [`../dsl.md`](../dsl.md).

## Then Sentences

| DSL 句型 | Gherkin 參數 | Data Table 參數 | 預設參數 | StepDef 實作語意 |
| --- | --- | --- | --- | --- |
| `the discount code status is "{status}"` | `status`: string; e.g. `applied`, `rejected`. | 不支援 | none | `必查`: `呈現結果`: the discount code status in the response is correct. `權威狀態`: the discount code status in the backend order is consistent. |
| `the error is "{error}"` | `error`: string; the business error name. | 不支援 | none | `必查`: `呈現結果`: the error name in the response is correct. `權威狀態`: the order and discount data are not polluted after the failure. |
