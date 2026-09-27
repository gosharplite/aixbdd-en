Feature: Threshold gift and conditional cancellation

  Rule: when the threshold is met the gift must be added automatically, and cancelled automatically when the threshold is lost

    Example: the member adjusts the cart and toggles back and forth between gift eligibility and loss
      Given the shop provides the following gift campaigns:
        | Campaign              | Condition                            | Gift                |
        | Spring Threshold Gift | campaign-item subtotal reaches 3000  | 1 cooler tote bag   |
      # [need clarification] Does the gift threshold look at the campaign-item subtotal, the amount after discounts, or the final total payable?
      And the shop rules state that gift eligibility updates in real time with the cart contents
      And "Alice" has the following items in the cart:
        | Item            | Category      | Unit Price | Quantity |
        | Travel Backpack | Campaign Item | 1680       | 1        |
        | Quick-Dry Top   | Campaign Item | 920        | 1        |
        | Sports Shorts   | Campaign Item | 520        | 1        |
      When "Alice" views the cart summary
      Then the system automatically adds the gift "1 cooler tote bag"
      And the cart summary is as follows:
        | Item                   | Value             |
        | Campaign-Item Subtotal | 3120              |
        | Gift                   | 1 cooler tote bag |
      When "Alice" removes item "Sports Shorts"
      Then the gift "Cooler Tote Bag" is automatically cancelled
      And the cart summary is as follows:
        | Item                   | Value |
        | Campaign-Item Subtotal | 2600  |
        | Gift                   | None  |
      When "Alice" adds item "Sun Bucket Hat" again at unit price 580 quantity 1
      Then the system automatically adds the gift "1 cooler tote bag" again
      And the cart summary is as follows:
        | Item                   | Value             |
        | Campaign-Item Subtotal | 3180              |
        | Gift                   | 1 cooler tote bag |
      When "Alice" confirms and submits the order
      Then the order contains the gift "1 cooler tote bag"
      And "Alice" does not need to pay separately for the gift
