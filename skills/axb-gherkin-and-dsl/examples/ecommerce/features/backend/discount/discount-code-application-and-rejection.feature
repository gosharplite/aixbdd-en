Feature: Discount code application and rejection

  Background:
    Given the platform has a usable discount code "WELCOME100"
    And the platform's checkout rules are as follows:
      | Rule                    | Value |
      | Discount Amount         | 100   |
      | Discount Threshold      | 1000  |
      | Shipping Fee            | 60    |
      | Free Shipping Threshold | 1000  |

  Rule: a discount code must be applied successfully when the order meets the threshold

    Example: applying WELCOME100 when the product subtotal is 1050
      Given the cart already contains the following items:
        | Product Code | Unit Price | Quantity |
        | SKU-A        | 600        | 1        |
        | SKU-B        | 450        | 1        |
      When "Alice" applies discount code "WELCOME100"
      Then the discount code status is "applied"
      And the order summary is as follows:
        | Item                      | Value |
        | Product Subtotal          | 1050  |
        | Discount Amount           | 100   |
        | Discounted Product Amount | 950   |
        | Shipping Fee              | 60    |
        | Total Payable             | 1010  |

  Rule: a discount code must be rejected when the order does not meet the threshold

    Example: applying WELCOME100 when the product subtotal is 600
      Given the cart already contains the following items:
        | Product Code | Unit Price | Quantity |
        | SKU-A        | 600        | 1        |
      When "Alice" applies discount code "WELCOME100"
      Then this operation was rejected
      And the error is "below discount threshold"
      And the order summary is as follows:
        | Item                      | Value |
        | Product Subtotal          | 600   |
        | Discount Amount           | 0     |
        | Discounted Product Amount | 600   |
        | Shipping Fee              | 60    |
        | Total Payable             | 660   |

  Rule: the same discount code must not be applied twice on the same order

    Example: applying WELCOME100 again after it has been applied successfully
      Given the cart already contains the following items:
        | Product Code | Unit Price | Quantity |
        | SKU-A        | 600        | 1        |
        | SKU-B        | 450        | 1        |
      And "Alice" applies discount code "WELCOME100"
      When "Alice" applies discount code "WELCOME100"
      Then this operation was rejected
      And the error is "discount code already applied"
      And the order summary is as follows:
        | Item                      | Value |
        | Product Subtotal          | 1050  |
        | Discount Amount           | 100   |
        | Discounted Product Amount | 950   |
        | Shipping Fee              | 60    |
        | Total Payable             | 1010  |
