Feature: Order summary and free-shipping display

  Rule: the shipping fee must be shown when the discounted amount does not reach the free-shipping threshold

    Example: showing a shipping fee of 60 when the discounted product amount is 950
      Given the cart already contains the following items:
        | Product Code | Unit Price | Quantity |
        | SKU-A        | 600        | 1        |
        | SKU-B        | 450        | 1        |
      And the platform has a usable discount code "WELCOME100"
      When "Alice" enters discount code "WELCOME100" on the checkout page and applies it
      Then the checkout page shows the following information:
        | Item                      | Value |
        | Discounted Product Amount | 950   |
        | Shipping Fee              | 60    |
        | Total Payable             | 1010  |
      When "Alice" views the checkout page summary again
      Then the checkout page shows the following information:
        | Item                      | Value |
        | Discounted Product Amount | 950   |
        | Shipping Fee              | 60    |
        | Total Payable             | 1010  |

  Rule: free shipping must be shown when the discounted amount reaches the free-shipping threshold

    Example: showing free shipping when the discounted product amount is 1050
      Given the cart already contains the following items:
        | Product Code | Unit Price | Quantity |
        | SKU-A        | 700        | 1        |
        | SKU-B        | 450        | 1        |
      And the platform has a usable discount code "WELCOME100"
      When "Alice" enters discount code "WELCOME100" on the checkout page and applies it
      Then the checkout page shows the following information:
        | Item                      | Value |
        | Discounted Product Amount | 1050  |
        | Shipping Fee              | 0     |
        | Total Payable             | 1050  |
