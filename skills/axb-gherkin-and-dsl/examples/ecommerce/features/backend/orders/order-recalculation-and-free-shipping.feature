Feature: Order recalculation and free-shipping determination

  Background:
    Given the platform has a usable discount code "WELCOME100"
    And the platform's checkout rules are as follows:
      | Rule                    | Value |
      | Discount Amount         | 100   |
      | Discount Threshold      | 1000  |
      | Shipping Fee            | 60    |
      | Free Shipping Threshold | 1000  |

  Rule: a shipping fee must be charged when the discounted amount does not reach the free-shipping threshold

    Example: a shipping fee of 60 is still charged when the discounted product amount is 950
      Given the cart already contains the following items:
        | Product Code | Unit Price | Quantity |
        | SKU-A        | 600        | 1        |
        | SKU-B        | 450        | 1        |
      When "Alice" applies discount code "WELCOME100"
      Then the order summary is as follows:
        | Item                      | Value |
        | Discounted Product Amount | 950   |
        | Shipping Fee              | 60    |
        | Total Payable             | 1010  |
      And "Alice" views the order summary again
      Then the order summary is as follows:
        | Item                      | Value |
        | Discounted Product Amount | 950   |
        | Shipping Fee              | 60    |
        | Total Payable             | 1010  |

  Rule: shipping must be free when the discounted amount reaches the free-shipping threshold

    Example: free shipping when the discounted product amount is 1050
      Given the cart already contains the following items:
        | Product Code | Unit Price | Quantity |
        | SKU-A        | 700        | 1        |
        | SKU-B        | 450        | 1        |
      When "Alice" applies discount code "WELCOME100"
      Then the order summary is as follows:
        | Item                      | Value |
        | Discounted Product Amount | 1050  |
        | Shipping Fee              | 0     |
        | Total Payable             | 1050  |

  Rule: a failed discount code application must not change the cart or amounts

    Example: the cart details are unchanged after being rejected for not meeting the threshold
      Given the cart already contains the following items:
        | Product Code | Unit Price | Quantity |
        | SKU-A        | 600        | 1        |
      When "Alice" applies discount code "WELCOME100"
      Then this operation was rejected
      And the items in the cart remain as follows:
        | Product Code | Unit Price | Quantity |
        | SKU-A        | 600        | 1        |
      And the order summary is as follows:
        | Item             | Value |
        | Product Subtotal | 600   |
        | Discount Amount  | 0     |
        | Total Payable    | 660   |
