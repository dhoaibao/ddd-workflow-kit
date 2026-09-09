# 6. Pitfalls and best practices

DDD patterns can clarify a difficult domain, but they also have costs. Review the benefit and evidence for each choice.

## Common pitfalls

### Treating DDD as microservices
A bounded context is a model boundary; a service is a deployment and operational boundary. They may align, but do not split a system merely to claim DDD. A modular monolith can express strong boundaries with less distributed-systems overhead.

### Building a shared “one true” model
Different contexts may need different models for the same real-world subject. Forcing one model across contexts often creates ambiguous language and coupling. Translate deliberately at the boundary.

### Anemic models and rule leakage
Entities that only expose data while controllers, handlers, or database triggers own the rules can make invariants difficult to discover and protect. Put behavior with the concept that has the knowledge, while keeping orchestration in application services.

### Pattern cargo cult
Repositories, factories, domain services, CQRS, and events are not mandatory ceremonies. Extra abstractions can obscure simple behavior, increase testing surface, or slow delivery. Add a pattern when it solves a named problem.

### Oversized aggregates
Loading or locking an entire object graph may create contention and fragile transactions. Define the smallest boundary that protects the invariant, then coordinate across boundaries when eventual consistency is acceptable.

### Accidental coupling through infrastructure
Shared tables, ORM navigation, generated models, and direct calls can bypass context boundaries. Make ownership, schemas, contracts, and translation visible even when components share a process.

### Ignoring operational semantics
Asynchronous events introduce delivery, ordering, duplication, retries, and failure concerns. Document whether handlers are idempotent, what consistency users see, and how errors are repaired.

### Big-bang modeling or migration
A perfect map is not a prerequisite for learning. Large rewrites hide uncertainty and make rollback difficult. Work in slices with evidence and a reversible path where possible.

## Best-practice checklist

### Strategic

- [ ] Use context-specific language and record disputed terms.
- [ ] Explain each boundary and relationship with business or operational evidence.
- [ ] Revisit core/supporting/generic classifications as strategy changes.
- [ ] Make ownership and translation explicit.

### Tactical

- [ ] Tie each aggregate to named invariants and a consistency need.
- [ ] Prefer value objects for validated values with value equality.
- [ ] Keep domain policy independent from persistence and transport details.
- [ ] Define event and repository failure semantics.

### Delivery and operations

- [ ] Start with a thin slice and executable examples.
- [ ] Preserve characterization tests and rollback plans in brownfield work.
- [ ] Measure user outcomes, defects, lead time, and operational cost.
- [ ] Treat privacy, audit, retention, and recovery as domain constraints when applicable.

## A decision record template

For a significant DDD choice, record:

- **Decision:** what boundary, pattern, or architecture was selected.
- **Context:** domain need, constraints, and evidence.
- **Alternatives:** including the simpler option.
- **Trade-offs:** consistency, complexity, cost, coupling, and operability.
- **Revisit signal:** what observation would justify changing it.
