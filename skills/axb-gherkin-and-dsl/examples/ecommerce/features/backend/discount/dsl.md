# Discount DSL

This module's specific sentences. For cross-module shared sentences see [`../dsl.md`](../dsl.md).

## Then Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | StepDef Implementation Semantics |
| --- | --- | --- | --- | --- |
| `the discount code status is "{status}"` | `status`: string; e.g. `applied`, `rejected`. | Not supported | none | `Must-check`: `Presented Result`: the discount code status in the response is correct. `Authoritative State`: the discount code status in the backend order is consistent. |
| `the error is "{error}"` | `error`: string; the business error name. | Not supported | none | `Must-check`: `Presented Result`: the error name in the response is correct. `Authoritative State`: the order and discount data are not polluted after the failure. |
