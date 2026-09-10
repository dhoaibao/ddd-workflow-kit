# Tactical artifact contracts

New model output uses `scope` and `state`; add `owner` only when a named role must act. Legacy metadata remains readable.

## Required model content

The selected model includes only the selected outcome, representative success/failure examples, commands/use cases, rules/invariants, relevant state transitions, current-versus-desired differences, and integration/consistency failure semantics. Each material decision cites evidence near the claim.

Entities, value objects, aggregates, repositories, services, specifications, factories, events, CQRS, and event sourcing are conditional. A pattern section appears only for a named problem and records evidence, cost, simpler alternative, and revisit trigger. Unused patterns have no row.

## Safe updates

Reuse one validated slug, inspect and preserve existing content, and resolve `docs/ddd/models/<slug>.md` with its parent exactly `docs/ddd/models`; reject traversal, collision, or ambiguous ownership. Update only tactical-owned sections and verify model path containment. If strategic authority changes, mark the model stale and return to strategic. Never edit product/runtime files.
