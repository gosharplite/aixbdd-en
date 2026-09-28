# Orders DSL

This module's specific sentences. For cross-module shared sentences see [`../dsl.md`](../dsl.md).

## When Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | StepDef Implementation Semantics |
| --- | --- | --- | --- | --- |
| `"{player}" views the order summary again` | `player`: string; the player name. | Not supported | `target-order`: defaults to that player's current checkout order. | `How`: re-read the order summary. `State landing`: this is a re-read confirmation; it does not change state. `Write-back`: the full latest order summary. |

## Then Sentences

| DSL Sentence | Gherkin Params | Data Table Params | Default Params | StepDef Implementation Semantics |
| --- | --- | --- | --- | --- |
| `the items in the cart remain as follows:` | none | Supported:`Product Code` (required, string), `Unit Price` (required, integer), `Quantity` (required, integer) | none | `Must-check`: `Authoritative State`: a failed operation does not change the original cart items. `Re-read Confirmation`: viewing the cart again still matches. |
