# Rule 1 - Wave order must reflect requirement dependencies and information-supply order

- Level: `MUST`
- The ordering of `Wave`s must reflect whether later analysis depends on information converged by the previous wave — not merely whether endpoint names group nicely.
- If an endpoint's analysis must first know another endpoint's user flows, third-party constraints, input/output contracts, or data boundaries, it should be placed in a later `Wave`.
- The purpose of `Wave` is to express "which analysis should be done first and which later", not to distribute all endpoints evenly.

## Good Example

- This example is good because it reviews the PM-delivered user flows and converges external constraints in Wave 1 first, then analyzes the internal designs that depend on them.

````md
#### Wave 1

- Parallel analysis interfaces:
  - `Frontend subscription & checkout interface` — review-only of PM's existing `ui/ui-plan.md` and static prototypes; no redo, no delegation
  - `Third-party payment service interface`
- Arrangement rationale: review the user flows and converge third-party constraints first, for backend and database to take over later.

#### Wave 2

- Parallel analysis interfaces:
  - `Backend order & subscription API interface`
  - `Order & subscription persistence interface`
- Arrangement rationale: backend and database analysis depends on the UI flows and payment contract reviewed in the previous wave.
````

## Bad Example

- This example is bad because it merely splits endpoints evenly without expressing the real dependency order.

````md
#### Wave 1

- Parallel analysis interfaces:
  - `Backend`
  - `Database`

#### Wave 2

- Parallel analysis interfaces:
  - `Frontend`
  - `Third-party`
````

# Rule 2 - One Wave holds only interfaces that can be analyzed in parallel

- Level: `MUST`
- Only when the analysis work of two or more system interfaces does not need to wait for each other's concrete conclusions may they proceed in parallel within the same `Wave`.
- If one interface's analysis needs to know another interface's analysis result first, it must be split into a later `Wave`; do not force them side by side just because they belong to different endpoints.
- The parallelism criterion is analysis dependency, not the number of executors or a subjective "seems doable together".
- Review-type work (frontend `ui/**`, and the terminal UX surface of a CLI shipping an interactive TUI — both produced by the PM's `/axb-ui-plan`) and low-coupling third-party interfaces usually can be reviewed in parallel in the same wave with each other, because neither needs to wait for the other's conclusions first.

## Good Example

- This example is good because both ends can each converge their own input material first, then hand results to later analysis.

````md
#### Wave 1

- Parallel analysis interfaces:
  - `Frontend photo workspace interface` — review-only of PM's existing UI; no redo, no delegation
  - `Third-party payment service interface`
````

## Bad Example

- This example is bad because the database analysis is actually still waiting for the backend contract definition, yet it is placed in the same wave for parallel processing.

````md
#### Wave 1

- Parallel analysis interfaces:
  - `Backend order & subscription API interface`
  - `Order & subscription persistence interface`
- Arrangement rationale: doing it together first is faster.
````

# Rule 3 - Every Wave should state both analysis focus and arrangement rationale

- Level: `SHOULD`
- A `Wave` should not just list interface names; it should also account for the analysis focus this wave actually converges, and why these interfaces are placed in the same wave.
- `Analysis focus` reveals each endpoint's work focus in this wave; `Arrangement rationale` explains dependency order, parallelism, and handoff logic.
- Without these two kinds of information, downstream sub-skills or sub-agents can easily miss the real goals and boundaries of each wave.

## Good Example

- This example is good because it not only lists interfaces but clearly states what each wave does and why it is arranged that way.

````md
#### Wave 1

- Parallel analysis interfaces:
  - `Frontend subscription & checkout interface` — review-only of PM's existing UI; no redo, no delegation
  - `Third-party payment service interface`
- Analysis focus:
  - Frontend first reviews the PM-delivered UI/UX flows, states, and error feedback, confirming implementability within technical boundaries (no redo, no delegation).
  - Payment end first analyzes third-party docs, Webhook specs, and integration constraints.
- Arrangement rationale: both can converge independently first and will directly affect the next wave's backend and database analysis.
````

## Bad Example

- This example is bad because it has only a list, revealing neither analysis focus nor dependency rationale.

````md
#### Wave 1

- Parallel analysis interfaces:
  - `Frontend`
  - `Payment`
````

# Rule 4 - The plan artifact only plans the analysis process; it does not write out analysis results early

- Level: `MUST`
- The responsibility of the `Analysis Process Planning` section is to inventory system interfaces and arrange the subsequent analysis order, wave splits, and focus — not to directly produce each interface's actual analysis conclusions.
- If some content has started defining final API fields, data table schemas, third-party parameter mappings, or concrete UI component designs, it has exceeded this artifact's planning level.
- In this artifact, stay at the granularity of "which interfaces to analyze, why this order, what each wave focuses on".

## Good Example

- This example is good because it accounts for subsequent analysis tasks, not completed design results.

````md
#### Wave 2

- Parallel analysis interfaces:
  - `Backend order & subscription API interface`
  - `Order & subscription persistence interface`
- Analysis focus:
  - Backend analysis focuses on the responsibility boundaries of creating orders, receiving webhooks, and activating subscriptions.
  - Database analysis focuses on the persistence needs of order life cycles, payment status, and subscription status.
````

## Bad Example

- This example is bad because it has already written concrete design answers into the planning section.

````md
#### Wave 2

- The backend API must have `POST /checkout`, `POST /webhook`, and `GET /subscription-status`.
- The `orders` table must include `status`, `provider_ref`, and `retry_count` fields.
````
