Feature: Order placement and payment timeout

  Background:
    Given the shop has the following sellable items:
      | Item                   | Variant  | Unit Price | Sellable Inventory |
      | Water-Repellent Jacket | Black M  | 1280       | 5                  |
      | Wicking Pants          | Black L  | 980        | 5                  |
      | Performance Socks      | Gray F   | 120        | 20                 |
    # [need clarification] Does the payment window start counting from "submitting the order" or from "entering the payment page"?
    And the shop provides the following checkout rules:
      | Rule                      | Value                                   |
      | Home Delivery Fee         | 80                                      |
      | Payment Window            | 15 minutes                              |
      | Order Placement Condition | Inventory reserved and total payable confirmed |
    And the shop provides the following promotions:
      | Promotion                     | Type      | Condition                            | Benefit           |
      | New-Customer Discount Code NEW100 | Deduction | first purchase with product subtotal reaching 2000 | 100 off           |
      | Threshold Gift                | Gift      | product subtotal reaches 2500        | 1 laundry bag     |

  Rule: after an order is placed, inventory must be reserved first and the payment result awaited

    Example: a first-time member completes payment within the payment window and a shipment-pending order is created
      Given "Alice" is a first-time member
      And "Alice" has the following items in the cart:
        | Item                   | Variant  | Unit Price | Quantity |
        | Water-Repellent Jacket | Black M  | 1280       | 1        |
        | Wicking Pants          | Black L  | 980        | 1        |
        | Performance Socks      | Gray F   | 120        | 2        |
      When "Alice" applies discount code "NEW100"
      And "Alice" chooses "Home Delivery" and fills in "Taipei Da'an District" shipping details
      And "Alice" confirms and submits the order
      Then the system creates a pending-payment order for "Alice"
      And the order summary is as follows:
        | Item             | Value         |
        | Product Subtotal | 2500          |
        | Discount         | 100           |
        | Gift             | 1 laundry bag |
        | Shipping Fee     | 80            |
        | Total Payable    | 2480          |
      And the sellable inventory of item "Water-Repellent Jacket / Black M" is down to 4
      And the sellable inventory of item "Wicking Pants / Black L" is down to 4
      And "Alice" can complete payment within 15 minutes
      When "Alice" completes payment within the payment window
      Then the order status is "awaiting shipment"
      And the gift "Laundry Bag" is established with the order
      And the warehouse pending-shipment list contains "Alice"'s order

    Example: a first-time member's order is cancelled and resources restored after payment timeout
      Given "Alice" is a first-time member
      And "Alice" has the following items in the cart:
        | Item                   | Variant  | Unit Price | Quantity |
        | Water-Repellent Jacket | Black M  | 1280       | 1        |
        | Wicking Pants          | Black L  | 980        | 1        |
        | Performance Socks      | Gray F   | 120        | 2        |
      When "Alice" applies discount code "NEW100"
      And "Alice" chooses "Home Delivery" and fills in "Taipei Da'an District" shipping details
      And "Alice" confirms and submits the order
      Then the system creates a pending-payment order for "Alice"
      And the sellable inventory of item "Water-Repellent Jacket / Black M" is down to 4
      And the sellable inventory of item "Wicking Pants / Black L" is down to 4
      When the order has passed the payment window without completing payment
      Then the order status is "cancelled"
      And the sellable inventory of item "Water-Repellent Jacket / Black M" is restored to 5
      And the sellable inventory of item "Wicking Pants / Black L" is restored to 5
      # [need clarification] After timeout cancellation, if the discount code has a daily usage limit or campaign quota, should those be restored too?
      And discount code "NEW100" becomes usable again
      And the gift "Laundry Bag" is not retained
      And "Alice"'s cart can start checkout again
