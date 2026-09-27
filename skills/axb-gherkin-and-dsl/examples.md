# Example Index

The complete demonstration of this skill is no longer crammed into a single file; it is now an e-commerce spec package that can be read directly.

## Complete E-commerce Package

Path: `examples/ecommerce/features/`

Structure:

```text
examples/ecommerce/
└── features/
    ├── backend/
    │   ├── dsl.md
    │   ├── discount/
    │   │   ├── dsl.md
    │   │   └── discount-code-application-and-rejection.feature
    │   └── orders/
    │       ├── dsl.md
    │       └── order-recalculation-and-free-shipping.feature
    └── frontend/
        ├── dsl.md
        └── checkout/
            ├── dsl.md
            ├── checkout-page-discount-code-input.feature
            └── order-summary-and-free-shipping-display.feature
```

## How to Read

1. First read `features/backend/` and `features/frontend/` to see how features are first split by functional module, then placed as `.feature` files. Each module has its own `dsl.md`; the interface root `dsl.md` keeps only cross-module sentences whose complete contract is identical (e.g. the backend's "this operation was rejected").
2. Then read the respective `dsl.md` to confirm how Gherkin sentences land in test code.
3. For the complete sentence and rule summaries, return to `SKILL.md` and `STANDARDS.md`.
