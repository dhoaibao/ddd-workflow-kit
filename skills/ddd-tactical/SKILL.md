---
name: ddd-tactical

description: Model one selected context slice through concrete examples, rules, invariants, state changes, and relevant failure semantics; include tactical patterns only for a named problem and never edit product code.
---

# DDD tactical design

Turn one selected strategic context into behavior and invariant evidence sufficient for one candidate increment.

## Entry and boundary

Require exactly one selected validated context, purpose, boundary, key language, scenarios/commands, owner, relationships, evidence, candidate invariants, and allowed model/context paths. Reuse the validated slug. Return to strategic when selection, boundary, language, or ownership is missing or challenged.

Own one model file plus additive tactical notes in the selected context/language artifacts. Never edit strategic maps, product source, tests, schemas, configuration, migrations, deployment files, or runtime behavior.

## Behavior-first workflow

1. Describe representative success and failure examples, actor, preconditions, command/use case, outcome, and acceptance signal.
2. State rules, invariants, relevant state transitions, current-versus-desired behavior, and immediate/eventual consistency.
3. Name the smallest boundary that protects each immediate invariant; preserve unresolved alternatives.
4. Include integration failure semantics only when a relationship is touched.
5. Add an entity, value object, aggregate, repository, service, specification, factory, event, CQRS, or event-sourcing decision only when it solves a named problem with evidence. Omit unused pattern sections entirely; do not emit empty or `not-needed` rows.
6. Hand exactly one bounded model to adoption or route a conflict back to strategic.

## Optional patterns and trigger-based detail

optional patterns are conditional: include one only for a named problem with evidence; otherwise omit it. Async communication requires delivery, ordering, duplication, retry, idempotency, repair, and privacy semantics. Concurrent writes require transaction/conflict/invariant semantics. Data, privacy, external contracts, or brownfield routing require only their concrete risk detail. No trigger means no filler section.

## Authority and stale handling

Keep current behavior, desired policy/meaning, and obligations separate when they conflict. A pattern name is not evidence. If a tactical scenario challenges a strategic boundary, mark downstream work stale and return the exact strategic decision; do not silently repair the map.

## Result

Return one context/model path, examples, rules, invariants, behavior deltas, relevant pattern decisions, integration/consistency semantics, evidence, assumptions, risks, decision dispositions, and exactly one adoption handoff or bounded stop. Modeling is not authorization.

Read [the method](references/tactical-method.md), [the contract](references/artifact-contracts.md), and [the model template](assets/context-model-template.md) before writing.
