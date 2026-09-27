# Rule 1 - Features must be placed into existing functional modules

- Level: `MUST`
- Every feature file must be located at `{interface}/{module}/*.feature`; `{interface}` is an interface root such as `backend` or `frontend`, and placing `.feature` files directly in the interface root directory is forbidden.
- `module` must first be identified by the functional boundaries of existing truth, not ad-hoc splits by filename convenience, one-off task names, or sentence counts.
- Only when no existing functional boundary can reasonably carry it may a new module be added; before adding, it must be explained why the new capability does not belong to any existing module.
- A universal rule must not hard-code one project's current module list; for example, one project's six existing modules can only be that project's truth — they must not be written as a taxonomy every project must adopt.

## Good Example

- This example first reuses the existing "orders" boundary in truth, and the feature sits one module level below the interface root.

```text
features/
└── backend/
    └── orders/
        └── order-submit-recalc.feature
```

## Bad Example

- This example leaves the feature at the interface root and mistakes one specific project's six modules for a universal limit.

```text
features/backend/order-submit-recalc.feature

Regulation: all projects may only use the six modules: matching & rooms, preparation &
ciphers, match turns, three-guess, health & cipher-swap, and room chat.
```

# Rule 2 - A DSL row is shared or module-specific per the complete contract

- Level: `MUST`
- A DSL sentence used by only one module, or valid only in one module's context, must live in `{interface}/{module}/dsl.md`.
- A DSL row may live in `{interface}/dsl.md` only if it is used across two or more modules and its `DSL 句型`, `Gherkin 參數`, `Data Table 參數`, `預設參數`, and implementation contract are all identical.
- If any parameter type, DataTable field, default value, authoritative state, wait condition, write-back, or verification responsibility differs, it is not the same shared contract; it must stay in its respective module and be rewritten into different sentences that can identify their semantics.
- The interface root `dsl.md` is a cross-module contract — not a master list of all DSL rows, nor a staging area for centralizing first and splitting later as convenient.

## Good Example

- Two modules use the exact same sentence and contract, so the interface root carries it uniquely.

```text
discount/discount-code-application.feature
  Given the cart already contains the following items:

orders/order-recalculation.feature
  Given the cart already contains the following items:

backend/dsl.md
  `the cart already contains the following items:`
  The DataTable, defaults, landing state, and write-back contract are exactly identical in both modules.
```

## Bad Example

- Although two modules use the same text, one establishes authoritative data while the other only verifies the screen projection — the implementation contracts differ and it cannot be promoted to a shared row.

```text
Inventory module: `product inventory is as follows:` means writing DB inventory.
Product page module: `product inventory is as follows:` means verifying the page display.

Wrong approach: merge into the interface root dsl.md just because the sentences are identical.
```

# Rule 3 - Text duplication cannot replace semantic judgment

- Level: `MUST`
- Do not promote a sentence to the interface root merely because its DSL text is identical, found twice in search, or seems to reduce the row count.
- Before promoting, compare the sentence, parameters, DataTable, defaults, and implementation contract column by column, and confirm the modules using it truly share the same business action or verification responsibility.
- Same-text-different-meaning sentences must be rewritten into different, identifiable DSL sentences; do not keep an ambiguous same-text row and then require the step definition to guess semantics by which feature, tag, or call order it is in.
- The mechanical audit can point out duplicates, single-module usage, or matching ambiguity, but must not replace the agent's judgment of whether two contracts are semantically identical.

## Good Example

- When identical text carries different responsibilities, the sentence is split into two directly expressive ones.

```gherkin
Given the backend inventory is set as follows:
Then the product page shows inventory as follows:
```

## Bad Example

- The same sentence switches between arrange and assertion by context; the step definition must guess which module it is in.

```gherkin
Given product inventory is as follows:
Then product inventory is as follows:

# Only because the text appears twice, an ambiguous `product inventory is as follows:` is kept at the interface root.
```

# Rule 4 - Each sentence may have only one authoritative location

- Level: `MUST`
- Within the same interface, the same sentence may exist in only one authoritative `dsl.md`; for any feature step, merging the interface root and same-module DSL lookups must hit exactly one DSL row.
- When a sentence is promoted from a module to the interface root, all old rows in the modules must be removed; when a sentence is demoted from the interface root to a module, the old root row must be removed.
- Duplicate rows must not be kept simultaneously in root and module, or across multiple modules, for reasons of a compatibility period, index convenience, or avoiding the move.
- After completing a move, all features using that sentence must be re-checked; if it is still used by multiple modules after demotion, rewrite them into semantically explicit sentences, or maintain a single root row when the complete contract is identical.

## Good Example

- After the shared contract is confirmed, the sentence remains only in the root; merged lookups from both modules each hit it exactly once.

```text
backend/dsl.md
  `this operation was rejected`

backend/discount/dsl.md
  (no such row)

backend/orders/dsl.md
  (no such row)
```

## Bad Example

- The old location was not deleted after promotion, causing the discount feature's merged lookup to hit twice.

```text
backend/dsl.md
  `this operation was rejected`

backend/discount/dsl.md
  `this operation was rejected`
```
