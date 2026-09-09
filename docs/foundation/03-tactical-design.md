# 3. Tactical design

Tactical patterns help a bounded context express rules and protect consistency. They are options, not a checklist. Use the smallest set that makes important behavior explicit.

## Building blocks

- **Entity:** an object defined by continuity and identity, even when its attributes change. Identity should be meaningful within the context.
- **Value object:** an object defined by its attributes and usually treated as immutable. Equality is based on value, such as a currency amount, date range, or address. It can validate its own representation.
- **Aggregate:** a consistency boundary containing related objects that must change together under stated invariants. It is a transaction and access boundary, not simply a convenient object graph.
- **Aggregate root:** the designated entry point to an aggregate. External code refers to the root rather than directly mutating internal members. The root coordinates invariant checks.
- **Repository:** an abstraction for retrieving and storing domain objects or aggregates in a way that matches the model. Its contract belongs near the domain boundary; its persistence implementation belongs outside it.
- **Domain service:** stateless domain behavior that does not naturally belong to one entity or value object and is meaningful in domain terms. It should not become a general utility bag.
- **Application service:** an orchestration boundary for a use case. It coordinates authorization, transactions, repositories, domain operations, and response shaping without owning core business rules that belong in the domain model.
- **Domain event:** a record that something meaningful happened in the domain, named in past tense and carrying facts relevant to consumers. Events can support decoupling, but delivery, ordering, duplication, and failure semantics must be designed.
- **Specification:** a reusable, named business predicate or rule that can be combined, tested, and used for validation or selection. Keep it cohesive and avoid hiding an entire use case in a predicate.
- **Factory:** a named creation mechanism for an object or aggregate when construction has meaningful rules, choices, or setup. Simple constructors are often sufficient when creation is straightforward.

## Invariants and aggregate design

An **invariant** is a condition that must hold for a model to be valid. State which invariants belong inside one consistency boundary and which can be coordinated asynchronously or by a higher-level process. Smaller aggregates can reduce contention and accidental loading, while larger aggregates can make strongly consistent rules easier to enforce; the right choice depends on the business invariant and workload.

A useful test is: “What must be true immediately after this command succeeds?” Put the state and behavior needed to guarantee that answer behind the aggregate root. Do not make every database relationship part of one aggregate merely because objects are related.

## Application flow

A typical use-case flow is:

1. Accept a command or request at an application boundary.
2. Load the required aggregate through a repository.
3. Invoke domain behavior that checks invariants.
4. Persist the changed aggregate.
5. Publish or dispatch resulting domain events according to defined reliability needs.
6. Return a result without leaking persistence concerns into the domain model.

The exact sequence can vary. For example, an event may be recorded transactionally before a separate publisher delivers it. The important point is to make consistency and failure behavior explicit.

## Tactical checklist

- [ ] Name the invariant each aggregate protects.
- [ ] Distinguish identity-based concepts from value-based concepts.
- [ ] Keep aggregate access through the root.
- [ ] Keep domain rules in domain concepts rather than controllers or persistence hooks.
- [ ] Define repository and event semantics, including failure and retry behavior.
- [ ] Test examples and edge cases in the ubiquitous language.
