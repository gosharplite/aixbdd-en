Feature: Discount stacking and mutual exclusion

  Rule: stackable promotions must take effect in order, and mutually exclusive promotions must be explicitly rejected

    Example: a Platinum member applies a brand voucher then a free-shipping voucher, then attempts a mutually exclusive new-arrival voucher
      Given the shop provides the following promotion rules:
        | Promotion               | Type        | Condition                                  | Benefit                       |
        | Platinum Member Discount | Auto Discount | Platinum member                          | 5% off product subtotal       |
        | Brand Voucher SPORT200   | Deduction   | designated sports brands totaling 2000     | 200 off                       |
        | Free-Shipping Voucher SHIPFREE | Deduction | discounted product amount reaches 1500   | shipping deducted to 0        |
        | New-Arrival Voucher NEWITEM10 | Coupon  | valid on new arrivals                      | 10% off designated new arrivals |
      # [need clarification] When a mutually exclusive promotion is attempted, should the system reject it directly, or allow the member to "replace the existing promotion with the new one"?
      And the shop rules state that "SPORT200" and "NEWITEM10" cannot be in effect at the same time
      # [need clarification] Does "discounted product amount reaches 1500" look at the amount after the member discount, after order deductions, or after all product-level discounts are calculated?
      And the shop rules state the promotion application order is as follows:
        | Order | Rule                                    |
        | 1     | calculate member discount first         |
        | 2     | then apply order deductions             |
        | 3     | finally calculate shipping deductions   |
      And "Alice" is a Platinum member
      And "Alice" has the following items in the cart:
        | Item              | Brand    | Attribute  | Unit Price | Quantity |
        | Trail Running Shoes | SPORT-X | Regular    | 1800       | 1        |
        | Compression Leg Sleeves | SPORT-X | Regular | 450        | 1        |
        | New Windbreaker   | CITY-LAB | New Arrival | 950       | 1        |
      When "Alice" enters the checkout flow
      Then the system automatically applies the "Platinum Member Discount"
      And the order summary is as follows:
        | Item             | Value |
        | Product Subtotal | 3200  |
        | Member Discount  | 160   |
        | Order Discount   | 0     |
        | Shipping Fee     | 80    |
        | Total Payable    | 3120  |
      When "Alice" applies discount code "SPORT200"
      Then the order summary is as follows:
        | Item             | Value |
        | Product Subtotal | 3200  |
        | Member Discount  | 160   |
        | Order Discount   | 200   |
        | Shipping Fee     | 80    |
        | Total Payable    | 2920  |
      When "Alice" applies discount code "SHIPFREE"
      Then the order summary is as follows:
        | Item             | Value |
        | Product Subtotal | 3200  |
        | Member Discount  | 160   |
        | Order Discount   | 200   |
        | Shipping Fee     | 0     |
        | Total Payable    | 2840  |
      When "Alice" applies discount code "NEWITEM10" again
      Then this operation was rejected
      And the error is "this promotion cannot be used together with existing discounts"
      And the applied promotions remain as follows:
        | Promotion                |
        | Platinum Member Discount |
        | SPORT200                 |
        | SHIPFREE                 |
      And the order summary remains as follows:
        | Item             | Value |
        | Product Subtotal | 3200  |
        | Member Discount  | 160   |
        | Order Discount   | 200   |
        | Shipping Fee     | 0     |
        | Total Payable    | 2840  |
