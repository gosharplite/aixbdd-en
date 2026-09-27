Feature: Shipping zones and free-shipping determination

  Rule: when the delivery zone or delivery method changes, shipping fees and free-shipping results must be recalculated in sync

    Example: the same order goes main-island home delivery with free shipping, then switches to offshore-island home delivery with a fee, then switches to store pickup restoring free shipping
      Given the shop provides the following shipping rules:
        | Delivery Method          | Zone          | Base Fee | Free-Shipping Condition                  |
        | Home Delivery            | Main Island   | 80       | discounted product amount reaches 1200   |
        | Home Delivery            | Offshore Islands | 220   | free shipping not applicable             |
        | Convenience Store Pickup | Main Island   | 60       | discounted product amount reaches 799    |
      # [need clarification] Which administrative districts count as "offshore islands" — a fixed list, or determined by the logistics provider's deliverable range?
      And the shop has the following sellable items:
        | Item                    | Unit Price | Quantity Limit |
        | UV-Protection Hooded Jacket | 980    | 5              |
        | Folding Water Bottle    | 320        | 5              |
      And "Alice" has the following items in the cart:
        | Item                    | Unit Price | Quantity |
        | UV-Protection Hooded Jacket | 980    | 1        |
        | Folding Water Bottle    | 320        | 1        |
      When "Alice" chooses "Home Delivery" and fills in "Taipei Xinyi District" shipping details
      Then the order summary is as follows:
        | Item             | Value          |
        | Product Subtotal | 1300           |
        | Delivery Method  | Home Delivery  |
        | Delivery Zone    | Main Island    |
        | Shipping Fee     | 0              |
        | Total Payable    | 1300           |
      When "Alice" changes the shipping details to "Penghu Magong City"
      Then the order summary is as follows:
        | Item             | Value             |
        | Product Subtotal | 1300              |
        | Delivery Method  | Home Delivery     |
        | Delivery Zone    | Offshore Islands  |
        | Shipping Fee     | 220               |
        | Total Payable    | 1520              |
      # [need clarification] When a member switches from home delivery to store pickup, must they re-select a store, and must all items be re-validated as deliverable?
      When "Alice" switches to "Convenience Store Pickup" and chooses "Kaohsiung Cianjhen District store"
      Then the order summary is as follows:
        | Item             | Value                  |
        | Product Subtotal | 1300                   |
        | Delivery Method  | Convenience Store Pickup |
        | Delivery Zone    | Main Island            |
        | Shipping Fee     | 0                      |
        | Total Payable    | 1300                   |
      And "Alice" can continue to submit the order with the new delivery method
