Feature: Checkout page discount code input

  Rule: the checkout page must show the successful discount code application result

    Example: applying WELCOME100 when the product subtotal is 1050
      Given the cart already contains the following items:
        | Product Code | Unit Price | Quantity |
        | SKU-A        | 600        | 1        |
        | SKU-B        | 450        | 1        |
      And the platform has a usable discount code "WELCOME100"
      When "Alice" enters discount code "WELCOME100" on the checkout page and applies it
      Then the checkout page shows the following information:
        | Item                      | Value      |
        | Discount Code             | WELCOME100 |
        | Discount Amount           | 100        |
        | Discounted Product Amount | 950        |
        | Shipping Fee              | 60         |
        | Total Payable             | 1010       |
      And the checkout page shows the discount code status is "applied"

  Rule: the checkout page must block discount codes that do not meet the threshold

    Example: applying WELCOME100 when the product subtotal is 600
      Given the cart already contains the following items:
        | Product Code | Unit Price | Quantity |
        | SKU-A        | 600        | 1        |
      And the platform has a usable discount code "WELCOME100"
      When "Alice" enters discount code "WELCOME100" on the checkout page and applies it
      Then the screen shows an error "below discount threshold"
      And the checkout page shows the following information:
        | Item                      | Value |
        | Discount Amount           | 0     |
        | Discounted Product Amount | 600   |
        | Shipping Fee              | 60    |
        | Total Payable             | 660   |
      And the discount code input area is still editable
