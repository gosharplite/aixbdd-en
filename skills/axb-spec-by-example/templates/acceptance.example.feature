Feature: Order placement and payment timeout

  Rule: after an order is placed, inventory must be reserved first and the payment result awaited

    Example: a first-time member's order is cancelled and resources restored after payment timeout
      Given the shop provides the following checkout rules:
        | Rule                 | Value          |
        | Home Delivery Fee    | 80             |
        | Payment Window       | 15 minutes     |
        | Order Placement Condition | Inventory Reserved |
      And the shop provides discount code "NEW100" for first-time members to use
      # [need clarification] Does the payment window start counting from "submitting the order" or from "entering the payment page"?
      And "Alice" is a first-time member
      And "Alice" has the following items in the cart:
        | Item                   | Unit Price | Quantity |
        | Water-Repellent Jacket | 1280       | 1        |
        | Wicking Pants          | 980        | 1        |
      When "Alice" applies discount code "NEW100"
      And "Alice" confirms and submits the order
      Then the system creates a pending-payment order for "Alice"
      And the order summary is as follows:
        | Item             | Value |
        | Product Subtotal | 2260  |
        | Discount         | 100   |
        | Total Payable    | 2240  |
      When the order has passed the payment window without completing payment
      Then the order status is "cancelled"
      And discount code "NEW100" becomes usable again
      And "Alice"'s cart can start checkout again
