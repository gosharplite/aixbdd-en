Feature: Inventory reservation and overselling protection

  Rule: the same batch of limited inventory must not be sold twice, but must become sellable again after timeout

    Example: the first to place a pending-payment order reserves the last two pairs of sneakers; after timeout the next member can order again
      Given the shop has the following sellable items:
        | Item                              | Variant          | Unit Price | Sellable Inventory |
        | Limited-Edition Co-Branded Sneakers | 27 cm          | 4200       | 2                  |
        | Basic Sports Socks                | Black F          | 120        | 50                 |
      And the shop rules state that pending-payment orders reserve product inventory first
      And the shop rules state that reserved inventory from payment timeouts must be released automatically
      And "Alice" has the following items in the cart:
        | Item                              | Variant | Unit Price | Quantity |
        | Limited-Edition Co-Branded Sneakers | 27 cm | 4200       | 2        |
      And "Bob" has the following items in the cart:
        | Item                              | Variant | Unit Price | Quantity |
        | Limited-Edition Co-Branded Sneakers | 27 cm | 4200       | 1        |
      When "Alice" confirms and submits the order
      Then the system creates a pending-payment order for "Alice"
      And the sellable inventory of item "Limited-Edition Co-Branded Sneakers / 27 cm" is down to 0
      # [need clarification] Should the latecomer be rejected only "when submitting the order", or see an out-of-stock notice earlier on the cart or product page?
      When "Bob" attempts to confirm and submit the order
      Then this operation was rejected
      And the error is "insufficient inventory"
      And "Bob"'s cart still retains the originally intended items
      When "Alice"'s order has passed the payment window without completing payment
      Then "Alice"'s order status is "cancelled"
      And the sellable inventory of item "Limited-Edition Co-Branded Sneakers / 27 cm" is restored to 2
      # [need clarification] After the inventory is released, must "Bob" refresh prices and inventory, or can the original cart be used to submit the order directly again?
      When "Bob" confirms and submits the order again
      Then the system creates a pending-payment order for "Bob"
      And the sellable inventory of item "Limited-Edition Co-Branded Sneakers / 27 cm" is down to 1
      And "Bob" can continue with the payment flow
