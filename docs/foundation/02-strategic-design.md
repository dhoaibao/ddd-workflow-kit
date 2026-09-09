# 2. Strategic design

Strategic design establishes boundaries and relationships before selecting code-level patterns. The terms below describe useful lenses; they are not necessarily separate deployables or teams.

## Domain and subdomains

The **domain** is the broad business area the product addresses. A **subdomain** is a coherent capability or area of knowledge within it. A common classification is:

- **Core subdomain:** a differentiating capability where the organization expects meaningful competitive or strategic advantage. It usually deserves focused discovery and investment, but not every organization has one.
- **Supporting subdomain:** important to the business but not usually a differentiator. It may be built in-house, simplified, or obtained from a partner depending on constraints.
- **Generic subdomain:** a broadly understood capability available through a commodity product, standard, or reusable solution. Fit, cost, and dependency risk still need evaluation.

These classifications are hypotheses and can change with strategy. A supporting capability can become core; a generic solution may be unsuitable when local rules are distinctive.

## Bounded contexts

A **bounded context** is a boundary within which a model and its language have consistent meaning. The word `account`, for example, may represent a billing relationship in one context and an authenticated identity in another. The boundary protects each model from accidental coupling and makes translation explicit.

A bounded context is a modeling boundary, not automatically a service, database, team, or repository. Those physical boundaries may be useful, but they should follow a justified need such as independent change, ownership, scaling, security, or failure isolation.

Signals for a boundary include:

- a term has materially different meanings or rules;
- different stakeholders own decisions;
- change cadence or lifecycle differs;
- consistency, security, or availability needs differ;
- translation is already happening between groups.

## Context maps and relationships

A **context map** documents bounded contexts and the relationships between them. It makes dependencies, ownership, and translation visible. Record the direction of influence and the mechanism used for communication; avoid treating a label as proof that integration is healthy.

Common relationship patterns include:

- **Shared kernel:** contexts share a small model or contract and coordinate changes. This can reduce duplication but increases coordination and coupling.
- **Customer–supplier:** an upstream context supplies capabilities to a downstream context and considers the downstream needs in planning.
- **Conformist:** the downstream adopts the upstream model because it has little practical influence or the translation cost is not justified.
- **Anti-corruption layer:** the downstream translates and isolates an upstream model so it does not shape the downstream domain model.
- **Open host service / published language:** an upstream exposes a documented protocol or language intended for multiple consumers.
- **Separate ways:** contexts do not integrate directly when the cost or value of integration is low; duplication can be an intentional trade-off.

Other relationships may be appropriate. Choose based on ownership, risk, and change patterns rather than applying a catalog mechanically.

## Strategic checklist

- [ ] Name the domain outcome and important stakeholders.
- [ ] Identify candidate subdomains and explain their classifications.
- [ ] Record overloaded terms and context-specific meanings.
- [ ] Draw bounded contexts around coherent models and decision ownership.
- [ ] Document context-map relationships, direction, contracts, and translation.
- [ ] Identify the highest-risk or highest-value assumptions to validate next.
