# Rule 1 - The system interface inventory must start from the requirement parts

- Level: `MUST`
- When inventorying system interfaces, first cut out the requirement parts from identifiable user behaviors, external dependencies, data responsibilities, or operational boundaries in the requirement text, then derive the corresponding technical endpoint types.
- Do not presuppose a fixed technical list like "there must be a frontend, backend, and database" and then retroactively invent requirement rationales for them.
- If a system interface cannot point to which part of the requirement it is derived from, the interface is not yet sufficiently justified and should not be written directly into the inventory result.

## Good Example

- This example is good because it starts from the payment, activation, and query responsibilities in the requirement, then inventories the corresponding endpoints.

````md
### System interface inventory

1. `Frontend subscription & checkout interface`
   - Endpoint type: `frontend endpoint`
   - Main interfaces: plan listing page, checkout form, payment result page
   - Requirement basis: the requirement asks "users can browse subscription plans" and "pay by credit card".

2. `Third-party payment service interface`
   - Endpoint type: `payment endpoint`
   - Main interfaces: card charge page, Webhook notifications
   - Requirement basis: the requirement asks "pay by credit card".
````

## Bad Example

- This example is bad because it lists technical endpoints first and force-fits corresponding rationales, not really inventorying from requirement parts.

````md
### System interface inventory

1. `Frontend`
   - Reason: systems usually have a frontend.

2. `Backend`
   - Reason: systems usually have an API.

3. `Database`
   - Reason: feels like it will be needed later.
````

# Rule 2 - Every system interface must account for endpoint type, main interfaces, and requirement basis

- Level: `MUST`
- Every system interface in the inventory result must contain at least the three fields `endpoint type`, `main interfaces`, and `requirement basis`.
- `Endpoint type` explains which category of endpoint the interface belongs to: frontend, backend, database, third-party, mobile, hardware, cloud, or other.
- `Main interfaces` account for the entry points, contracts, data responsibilities, or operation surfaces the downstream analysis should focus on.
- `Requirement basis` must quote concrete sentences from the requirement, requirement summaries, or already-formed `FR` / `NFR` / key entities — not just abstract judgments.

## Good Example

- This example is good because every field is complete and can connect directly to analysis planning.

````md
1. `Order & subscription persistence interface`
   - Endpoint type: `database endpoint`
   - Main interfaces: user, order, payment record, subscription status, and retry data fields
   - Requirement basis: the requirement asks "the back office can look up order and payment status" and "membership permissions activate immediately after successful payment".
````

## Bad Example

- This example is bad because it has only a name, revealing none of the core fields needed for downstream analysis.

````md
1. `Database`
````

# Rule 3 - Split into a separate system interface only when the analysis responsibility boundary is independent

- Level: `SHOULD`
- If multiple requirement parts fall under the same category of technical endpoint but their analysis responsibilities, dependencies, or delegation targets are clearly different, split them into different system interfaces.
- If multiple requirement parts would be handled together by the same analysis perspective, the same contract, or the same kind of skill, prefer merging them to avoid over-fragmenting the inventory.
- Do not automatically split every API, page, or table under an endpoint into separate system interfaces just because several exist.

## Good Example

- This example is good because it splits the inventory only when the responsibility boundaries really differ.

````md
1. `Backend order & subscription API interface`
   - Endpoint type: `backend endpoint`
   - Main interfaces: create order, receive payment results, activate subscription

2. `Order & subscription persistence interface`
   - Endpoint type: `database endpoint`
   - Main interfaces: order, payment, and subscription status persistence
````

## Bad Example

- This example is bad because it merely over-fragments the same backend responsibility without providing new analysis value.

````md
1. `Create order API`
2. `Query order API`
3. `Webhook API`
4. `Payment status API`
````
