# Frontend / UI & Static Prototype Planning

## Interface Scope

- Target system interface: `Frontend product browsing, cart, and checkout interface`
- Requirement source: `User Stories 1 to 4, FR-002, FR-005, FR-011, FR-014, and NFR-003`
- Upstream basis: `spec.md, research.md, techstack.md, plan.md Wave 1`
- Output sequence: `Finalize ui/ui-plan.md first, then produce the ui/*.html static prototypes per this plan.`

## Visual Direction

- Style source: `When the requirements carry no visual spec, first converge brand tone, color hierarchy, and product presentation via clarify.`
- Style conclusion this time: `A bright, clean, modern-lifestyle-leaning e-commerce interface; product info and CTAs must scan easily.`
- Visual focus: `Large product cards, clear price hierarchy, an easily understood cart summary, and trust-building design that does not interrupt checkout.`
- Aesthetic principles: `Screens must look like a real product — no documentation tone, and analysis notes must not be written directly into the HTML screens.`

## Screens & Flows

### 1. `Product Listing Entry Screen`

- Corresponding prototype file: `ui/index.html`
- Main purpose: `Let users quickly search or browse the product list, serving as the entrance to the entire shopping flow.`
- Entry condition: `The user enters the store homepage for the first time and has not selected any product.`
- Primary actions: `Type search keywords, view product cards, switch featured categories, and click into product details.`
- Success transitions: `After choosing a product, navigate to the product detail screen.`
- Error feedback: `When search conditions are empty, no results are found, or data temporarily fails to load, show a retryable message in place.`

### 2. `Product Detail Screen`

- Corresponding prototype file: `ui/product-detail.html`
- Main purpose: `Let users view product images and text, price, specs, and shipping info, and decide whether to add to cart.`
- Entry condition: `The user clicks into a specific product from the product list or recommendations.`
- Primary actions: `Switch product images, choose specs, adjust quantity, review shipping promises, and add to cart.`
- Success transitions: `After successfully adding to cart, navigate to the cart and checkout screen.`
- Error feedback: `On out-of-stock, unselected specs, or add-to-cart failure, clear status hints must be shown.`

### 3. `Cart & Checkout Screen`

- Corresponding prototype file: `ui/checkout.html`
- Main purpose: `Let users confirm cart contents, delivery method, payment info, and order amount.`
- Entry condition: `The user has added at least one item to the cart.`
- Primary actions: `Adjust item quantities, apply promotions, fill in shipping details, choose a payment method, and submit the order.`
- Success transitions: `After the order is successfully submitted, navigate to the order success screen.`
- Error feedback: `On unfilled fields, payment failure, or inventory updates, the current form context must be preserved with understandable hints.`

### 4. `Order Success Screen`

- Corresponding prototype file: `ui/order-success.html`
- Main purpose: `Show the successful order state, order summary, and follow-up tracking CTAs.`
- Entry condition: `The user completed payment or successfully submitted a cash-on-delivery order.`
- Primary actions: `View the order number, shipping summary, delivery schedule, and return to continue shopping or view the order.`
- Success transitions: `Can return to the product list, or go to the order query flow.`
- Error feedback: `If order data is not yet synchronized, show loading or retry hints instead of a blank success page.`

## Interaction & Fake Data Principles

- Fake data strategy: `Fake data such as product names, prices, discounts, delivery methods, shipping detail summaries, and order numbers may be used to help users directly feel the product flow.`
- Interaction principles: `Buttons, page switches, forms, and state toggles in the HTML prototypes should all be operable, simulating the real product rhythm.`
- Content principles: `Screen text contains only content the product would really show users; analysis explanations, component trees, or implementation notes are not written onto screens.`

## States & Information Disclosure

- User-visible information: `Product images, specs, prices, promotion amounts, cart items, delivery methods, payment summary, and order results.`
- Information that must be hidden: `Unauthorized internal inventory logic, complete payment credentials, and any server-internal judgment info that should not be exposed.`
- Main UI states: `Homepage browsing, product loading, add-to-cart available, cart editing, submitting order, order success, error hints.`
- Role or permission differences: `Guests can browse and add to cart; logged-in members can bring in existing addresses, view orders, and use member promotions.`

## Validation & Error Feedback

- Input validation: `The search bar, spec selection, shipping details, and payment info all need on-screen real-time validation.`
- State conflict handling: `When a user action conflicts with the current product or order state, preserve the on-screen context and show why the action is unavailable.`
- User-understandable error messages: `Error messages should explain the cause, current state, and recommended next step, e.g. search again, re-select specs, try later, or switch payment method.`

## Static Prototype Output Planning

- Multi-page entry: `If this feature needs a cross-page flow, fixedly use ui/index.html as the prototype entry page.`
- Planned output files: `ui/index.html`, `ui/product-detail.html`, `ui/checkout.html`, `ui/order-success.html`
- Page transition principles: `Only switch pages when the real product flow would switch screens anyway; otherwise prefer in-page state switching.`
- Review goal: `Let users click, switch pages, and feel the product rhythm directly without reading Markdown.`

## Frontend Implementation Split Suggestions

- Page / container split: `Split into at least four screen kinds: product list, product detail, cart / checkout, order success.`
- Shared components or blocks: `Product card, price info block, cart summary, error hint block, and checkout form.`
- Dependencies on backend contracts: `Product list query, product detail, inventory status, cart sync, promotion calculation, order submission, and payment error events.`
- Acceptance focus: `The flow from browsing products to completing one order must be continuous and understandable, and must not expose unnecessary payment or backend internal information.`

