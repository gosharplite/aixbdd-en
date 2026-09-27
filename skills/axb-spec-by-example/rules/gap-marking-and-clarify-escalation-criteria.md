# Rule 1 - High-impact undecided items must be marked in place with `# [need clarification]`

- Level: `MUST`
- Any undecided item that would change the Journey direction, acceptance results, rule ownership, file splitting, or success criteria must be marked beside the corresponding feature's rule or step.
- The marker format is fixed as `# [need clarification] ...`; do not change the spelling or hide it in an end-of-file summary.
- The marker should be placed as close as possible to the business rule or step line that raised the question, so the user can directly see the question's context.
- Do not add a `Background` section that was not otherwise needed just to host a `# [need clarification]`.

## Good Example

- This example is good because the question is pasted right next to the payment-deadline rule, so readers immediately know what is not yet decided.

```gherkin
Rule: after an order is placed, inventory must be reserved first and the payment result awaited

  Example: a first-time member's order is cancelled and resources restored after payment timeout
    Given the shop provides the following checkout rules:
      | Rule           | Value     |
      | Payment Window | 15 minutes |
    # [need clarification] Does the payment window start counting from "submitting the order" or from "entering the payment page"?
    When "Alice" confirms and submits the order
```

## Bad Example

- This example is bad because the question is hidden at the end of the file, so readers cannot map it to a concrete rule location.

```gherkin
Feature: Order placement and payment timeout

  Rule: after an order is placed, inventory must be reserved first and the payment result awaited

    Example: a first-time member's order is cancelled and resources restored after payment timeout
      When the order has passed the payment window without completing payment
      Then the order status is "cancelled"

# [need clarification] There are a few things above to ask about later
```

# Rule 2 - Produce the Gherkin and markers first, then immediately escalate to /axb-clarify

- Level: `MUST`
- `axb-spec-by-example` must first write out the acceptance feature files and `# [need clarification]`, so the questions land on concrete artifacts.
- After marking is done, as long as high-impact gaps remain, `/axb-clarify` must be delegated immediately; do not delay asking until later skills or the implementation phase.
- Do not throw vague requirements at `/axb-clarify` verbally before they are placed into feature files.

## Good Example

- This example is good because it lands the questions in the feature file first, then immediately hands the highest-impact questions to `/axb-clarify`.

```text
1. First write features/acceptance/order-placement-and-payment-timeout.feature
2. Mark # [need clarification] ... beside the payment window
3. Immediately call /axb-clarify to ask about the payment window's starting point
```

## Bad Example

- This example is bad because it asks abstractly before any artifact is formed, making explicit write-back impossible later.

```text
1. After reading spec.md, something feels off
2. Directly ask the user many vague questions
3. Only after the answers decide how to write the feature files
```

# Rule 3 - Each /axb-clarify round asks only the 1 to 3 highest-impact questions

- Level: `MUST`
- When handing off to `/axb-clarify`, first sort by acceptance impact and hand over only the 1 to 3 questions most needing a decision this round.
- Sorting priority: whether it changes acceptance results, whether it changes Journey branches, whether it changes feature splitting or Rule ownership.
- Do not dump all local questions on the user at once, causing the clarify session to lose focus.

## Good Example

- This example is good because it asks first only the few questions that most affect the rules and results.

```text
This round's /axb-clarify:
1. From which point in time does the payment window start?
2. Which discounted amount level does the free-shipping threshold look at?
3. Are mutually exclusive promotions rejected, or allowed to replace existing promotions?
```

## Bad Example

- This example is bad because it mixes high- and low-impact questions and asks too many at once.

```text
This round's /axb-clarify:
1. How is the payment window calculated?
2. Should the column name "Value" in the table be renamed?
3. How are offshore islands defined?
4. Should gift copy use full-width parentheses?
5. How is the free-shipping threshold calculated?
6. Should the color be written as black or ink black?
```

# Rule 4 - High-impact gaps must not be filled in with imagination

- Level: `MUST`
- If a gap would change the acceptance criteria or flow direction, do not assume an answer and write it as an established rule before `/axb-clarify` answers.
- Before the answer returns, the `# [need clarification]` and a temporary feature structure may be kept, but guesses must not be disguised as confirmed requirements.
- Only local details that do not affect the main acceptance judgment may be kept as follow-up items after the write-back.

## Good Example

- This example is good because it keeps the undecided question without sneaking in an assumed answer.

```gherkin
# [need clarification] Does the gift threshold look at the campaign-item subtotal, the amount after discounts, or the final total payable?
And the shop rules state that gift eligibility updates in real time with the cart contents
```

## Bad Example

- This example is bad because the author assumes a rule on their own; even if the user disagrees later, it will be hard to trace back.

```gherkin
And the shop rules state that the gift threshold definitely only looks at the final total payable
```

# Rule 5 - Do not over-stamp markers for low-impact wording differences

- Level: `SHOULD`
- `# [need clarification]` should focus on high-impact business gaps; do not escalate pure copy preferences, field naming preferences, or minor touch-ups that can wait into clarify.
- If a question does not affect how the acceptance cases run, just converge it yourself at write-back; no need to interrupt `/axb-clarify`.

## Good Example

- This example is good because it only marks the question that affects the shipping rules.

```gherkin
# [need clarification] Which administrative districts count as "offshore islands" — a fixed list, or determined by the logistics provider's deliverable range?
Given the shop provides the following shipping rules:
```

## Bad Example

- This example is bad because it escalates a low-impact wording preference into clarify.

```gherkin
# [need clarification] Should "Product Subtotal" be changed to "Product Amount Subtotal"?
Then the order summary is as follows:
```
