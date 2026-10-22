# System Analysis Plan

## Project Structure

### Document Structure (this feature)

```text
specs/plans/001-course-subscription-checkout/
├── spec.md
├── checklists/
│   └── requirements.md
├── truth-delta.md
├── features/
│   └── acceptance/
│       ├── plan-browsing-and-selection.feature
│       └── checkout-payment-and-activation.feature
├── ui/
│   ├── ui-plan.md
│   ├── index.html
│   ├── product-detail.html
│   ├── checkout.html
│   └── order-success.html
├── research.md
├── plan.md
└── tasks.md
```

The plan package holds plan-side artifacts only. This round's API contract is not stored here.

**Truth this feature maintains**: the subscription checkout API contract in
`specs/truth/contracts/checkout-api.yaml` (new endpoints for order creation, payment initiation and
status queries) and the payment webhook contract in `specs/truth/contracts/payment-webhook.yaml`
(extended event set); the order, payment and subscription tables in `specs/truth/data/**`
(`orders.dbml`, `subscriptions.dbml`); and the `specs/truth/techstack.md` entries for the payment
provider SDK and the webhook verification library. No `specs/truth/features/**` change: this
feature's interfaces reuse the existing backend and frontend DSL rows.

### Source Structure (repository root)

```text
backend/
├── src/
│   ├── app.js
│   ├── routes/
│   │   ├── plans.routes.js
│   │   ├── checkout.routes.js
│   │   └── webhook.routes.js
│   ├── controllers/
│   ├── services/
│   ├── integrations/
│   │   └── stripe/
│   ├── repositories/
│   └── config/
├── prisma/
│   ├── schema.prisma
│   └── migrations/
└── tests/
    ├── integration/
    └── unit/

frontend/
├── index.html
├── src/
│   ├── main.js
│   ├── pages/
│   ├── components/
│   ├── api/
│   ├── checkout/
│   └── state/
└── tests/
```

**Structure Decision**: Adopt a Web application structure with `frontend/`, `backend/`, and third-party payment integration coexisting. The frontend handles plan display, the checkout flow, and payment result feedback; the backend handles order creation, initiating payment requests, verifying webhooks, and activating subscriptions; the payment end takes over actual charges and payment status notifications via the third-party service; the database persists users, orders, payments, and subscription status.

## Analysis Process Planning

### System Interface Inventory

This requirement's inventory finds `4` system interfaces.

1. `Frontend subscription & checkout interface`
   - Endpoint type: `frontend endpoint`
   - Main interfaces: plan listing page, subscription plan selection, checkout form, payment result page, failure retry and status hints
   - Requirement basis: the requirement asks "users can browse subscription plans", "pay by credit card", "show understandable errors and allow retries on payment failure", and "see activation results immediately after successful payment".
   - Delegation: `Taken over by: the PM's ui/ui-plan.md and ui/*.html via /axb-ui-plan (review-only, no redo)`

2. `Backend order & subscription API interface`
   - Endpoint type: `backend endpoint`
   - Main interfaces: create checkout orders, start the payment flow, receive payment completion results, activate subscription permissions, provide the frontend with payment and subscription status queries
   - Requirement basis: the requirement asks "membership permissions activate immediately after successful payment", and the system needs trackable order and payment status to support success, failure, and retry flows.
   - Delegation: `/axb-api-plan`

3. `Third-party payment service interface`
   - Endpoint type: `payment endpoint`
   - Main interfaces: card charge checkout page, payment status return mechanism, Webhook notifications, third-party API docs and integration constraints
   - Requirement basis: the requirement asks "pay by credit card", meaning the system must rely on an external payment service for actual charges, and payment success or failure will both be affected by the third-party interface's capabilities and constraints.
   - Delegation: `/axb-api-plan` (the integration and webhook contracts this system must honour)

4. `Order & subscription persistence interface`
   - Endpoint type: `database endpoint`
   - Main interfaces: user, order, payment record, subscription plan, subscription status, and retry-related data fields
   - Requirement basis: the requirement asks "the back office can look up order and payment status" and "membership permissions activate immediately after successful payment", meaning the system must persist payment and activation results reliably to support queries, reconciliation, and state recovery.
   - Delegation: `/axb-data-plan`

### Analysis Process Arrangement

#### Wave 1

- Parallel analysis interfaces:
  - `Frontend subscription & checkout interface`
  - `Third-party payment service interface`
- Analysis focus:
  - Frontend only reviews the PM-delivered UI/UX interfaces, the user's operation path from choosing a plan to submitting payment, success and failure states, retry entries, and what information must be clearly disclosed on screen — confirming implementability within current technical boundaries (no redo, no delegation).
  - The payment end's analysis focuses on third-party docs, available APIs, Webhook specs, the payment page's responsibility boundaries, return fields, error codes, and integration constraints; downloading docs or organizing interface contracts first if necessary.
- Arrangement rationale: the frontend is nearly the earliest visible entry of all requirements, but the UI is already done by the PM via `/axb-ui-plan`; this wave only reviews whether its user flows and screens are implementable within current technical boundaries (no redo, no delegation); the payment end couples relatively loosely with the internal system and usually can be expanded independently from third-party docs first. Once "what users will experience" and "what the third party provides" are both confirmed, analyzing the backend afterwards makes it easier to decide API shapes and error feedback.
- Delegation order:
  - 1. Review the PM's `ui/ui-plan.md` and `ui/*.html` for implementability — no delegation
  - 2. Launch `/axb-api-plan` for the third-party payment integration and webhook contract

#### Wave 2

- Parallel analysis interfaces:
  - `Backend order & subscription API interface`
  - `Order & subscription persistence interface`
- Analysis focus:
  - Backend analysis focuses on how to take over the frontend flow and payment returns, designing the responsibility boundaries of order creation, payment initiation, webhook receiving, status queries, subscription activation, and failure compensation.
  - Database analysis focuses on providing a persistent data model for the above flows, covering order life cycles, payment status, subscription status, retry records, and reconciliation fields.
- Arrangement rationale: backend and database analysis highly depends on the two kinds of results converged in Wave 1 — what interactions and states the frontend really needs, and what callbacks, fields, and constraints the payment end actually provides. Only after these peripheral interfaces are clear can the backend and database be analyzed together, avoiding premature wrong assumptions in API design and schema modeling; this wave is also suitable for opening two sub-agents in parallel, delegating to the backend analysis skill and the database analysis skill respectively.
- Delegation order:
  - 1. Launch `/axb-api-plan` for the backend order & subscription API
  - 2. Launch `/axb-data-plan` for the order, payment and subscription data model (distinct artifact boundary from the API contract, so not merged)
- Both entries may be launched in parallel, as the rationale above allows; the order fixes only which starts first.
