# Rule 1 - `axb-spec-by-example` produces only overall-acceptance-layer Gherkin

- Level: `MUST`
- The output of this layer is `features/acceptance/*.feature` within the spec package.
- This stage must not split into `frontend` / `backend` / `cli` first, nor produce `dsl.md` at the same time.
- Sentences express only the acceptance flows and business outcomes the PM needs to confirm; do not mix implementation-layer design in early.

## Good Example

- This example is good because it only describes the overall acceptance flow, without prematurely splitting into technical-layer artifacts.

```gherkin
Feature: Order placement and payment timeout

  Rule: pending-payment orders must be cancelled and resources released after timeout

    Example: a first-time member's order is cancelled and resources restored after payment timeout
      Given "Alice" is a first-time member
      When "Alice" confirms and submits the order
      Then the system creates a pending-payment order for "Alice"
      When the order has passed the payment window without completing payment
      Then the order status is "cancelled"
```

## Bad Example

- This example is bad because it prematurely splits into frontend/backend and DSL at the same stage.

```text
features/backend/orders/order-placement-and-payment-timeout.feature
features/frontend/orders/order-placement-and-payment-timeout.feature
features/backend/dsl.md
features/frontend/dsl.md
```

# Rule 2 - `Example` must describe acceptance flows at Journey granularity

- Level: `MUST`
- Each `Example` should preferentially describe one demonstrable long flow, rather than being split into many tiny operation tests.
- The number of cases should be fewer than implementation-layer tests, keeping only the main flow and a few high-variation ones.
- If a Journey can still be read naturally, it should not be chopped into pieces early for implementation convenience.

## Good Example

- This example is good because it puts order creation, inventory reservation, payment results, and subsequent states in the same acceptance journey.

```gherkin
Example: limited items reserve inventory first; after timeout the next member can order again
  Given "Alice" has 2 pairs of limited-edition sneakers in the cart
  And "Bob" has 1 pair of limited-edition sneakers in the cart
  When "Alice" confirms and submits the order
  Then the system creates a pending-payment order for "Alice"
  When "Bob" attempts to confirm and submit the order
  Then this operation was rejected
  When "Alice"'s order has passed the payment window without completing payment
  Then the sellable inventory is restored
  When "Bob" confirms and submits the order again
  Then the system creates a pending-payment order for "Bob"
```

## Bad Example

- This example is bad because it splits the same acceptance journey into too many tiny cases, losing the PM demo value.

```gherkin
Example: create a pending-payment order
  When "Alice" confirms and submits the order
  Then the system creates a pending-payment order for "Alice"

Example: Bob is rejected
  When "Bob" attempts to confirm and submit the order
  Then this operation was rejected

Example: Alice's order times out and is cancelled
  When "Alice"'s order has passed the payment window without completing payment
  Then the sellable inventory is restored
```

# Rule 3 - Gherkin sentences speak only business semantics

- Level: `MUST`
- Steps must not expose APIs, HTTP methods, data tables, selectors, fixture names, or other technical details.
- The acceptance layer must be directly readable by the PM, requirement owners, and test authors, without first understanding the system's internal implementation.
- If a sentence is only meaningful to engineers and does not help requirement acceptance, it should not appear at this layer.

## Good Example

- This example is good because it only describes the business outcomes the member can see and needs to confirm.

```gherkin
When "Alice" applies discount code "SPORT200"
Then the order summary is as follows:
  | Item             | Value |
  | Order Discount   | 200   |
  | Total Payable    | 2920  |
```

## Bad Example

- This example is bad because it exposes technical implementation details directly at the acceptance layer.

```gherkin
When the frontend calls POST /api/orders/apply-coupon with code "SPORT200"
Then response.status should be 200
And the order_summary.discount_amount field should be updated to 200
```

# Rule 4 - `Feature` / `Rule` / `Example` should be split by acceptance aspect

- Level: `SHOULD`
- `Feature` should focus on a single acceptance topic the PM cares about, e.g. payment timeout, shipping determination, or gift eligibility.
- `Rule` should stay atomic (a single acceptance aspect); an `Example` title that sounds like another rule is only a smell and may serve as a split hint, but the criterion is whether this `Rule` is describing another acceptance aspect; if so, split out a new `Rule` or a new feature file.
- `Example` titles should describe data scenarios or journey variants, not merely repeat the `Rule`'s name.

## Good Example

- This example is good because `Feature`, `Rule`, and `Example` each carry a different level of acceptance semantics.

```gherkin
Feature: Threshold gift and conditional cancellation

  Rule: when the threshold is met the gift must be added automatically, and cancelled automatically when the threshold is lost

    Example: the member adjusts the cart and toggles back and forth between gift eligibility and loss
```

## Bad Example

- This example is bad because the `Example` title merely repeats the rule sentence, providing no scenario information.

```gherkin
Feature: Threshold gift and conditional cancellation

  Rule: when the threshold is met the gift must be added automatically, and cancelled automatically when the threshold is lost

    Example: when the threshold is met the gift must be added automatically, and cancelled automatically when the threshold is lost
```

# Rule 5 - `Background` is kept only when multiple Examples truly share test semantics

- Level: `MUST`
- `Background` is an optional structure, not the default opening move of an acceptance feature.
- If a feature has only a single `Example`, by default start directly from `Rule` / `Example`; do not pad in a `Background` just for layout symmetry.
- `Background` should be kept only when multiple `Example`s truly share the same steps with test semantics, and extracting them makes each Journey shorter and clearer.
- Do not stuff `spec.md`'s known rules, the product worldview, global rule primers, or narrative merely introducing feature background into `Background`.
- If extracting `Background` forces readers to jump back and forth to piece the Journey back together, revert to `Given` / `And` inside each `Example`.

## Good Example

- This example is good because the same feature has two `Example`s sharing the same items, checkout rules, and promotion settings; extracting them into `Background` shortens the repeated steps while retaining clear test semantics.

```gherkin
Feature: Order placement and payment timeout

  Background:
    Given the shop has the following sellable items:
      | Item                  | Variant  | Unit Price | Sellable Inventory |
      | Water-Repellent Jacket | Black M  | 1280       | 5                  |
      | Wicking Pants          | Black L  | 980        | 5                  |
    And the shop provides the following checkout rules:
      | Rule           | Value      |
      | Home Delivery Fee | 80       |
      | Payment Window    | 15 minutes |
    And the shop provides discount code "NEW100" for first-time members to use

  Rule: after an order is placed, inventory must be reserved first and the payment result awaited

    Example: a first-time member completes payment within the payment window
      Given "Alice" is a first-time member
      When "Alice" confirms and submits the order
      Then the system creates a pending-payment order for "Alice"

    Example: a first-time member's order is cancelled after payment timeout
      Given "Alice" is a first-time member
      When "Alice" confirms and submits the order
      Then the system creates a pending-payment order for "Alice"
```

## Bad Example

- This example is bad because this feature has only a single `Example`, and the `Background` merely re-introduces the campaign rules without making the Journey any clearer.

```gherkin
Feature: Threshold gift and conditional cancellation

  Background:
    Given the shop provides the following gift campaigns:
      | Campaign             | Condition                            | Gift                 |
      | Spring Threshold Gift | campaign-item subtotal reaches 3000 | 1 cooler tote bag    |
    And the shop rules state that gift eligibility updates in real time with the cart contents

  Rule: when the threshold is met the gift must be added automatically, and cancelled automatically when the threshold is lost

    Example: the member adjusts the cart and toggles back and forth between gift eligibility and loss
      Given "Alice" has the following items in the cart:
        | Item           | Category      | Unit Price | Quantity |
        | Travel Backpack | Campaign Item | 1680       | 1        |
```
