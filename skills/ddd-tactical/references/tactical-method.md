# Lean tactical method

## Start with examples

For one context, record command/use case, actor, preconditions, inputs, decision, success, failures, counterexamples, state changes, and observable acceptance. Prefer examples over noun inventories.

## Invariants before patterns

Name each invariant, source/owner, affected scenario, failure consequence, and immediate/eventual consistency. Choose a boundary only to protect a named immediate invariant. If an immediate invariant crosses a proposed boundary, revisit strategic ownership rather than assuming a distributed transaction.

## Conditional pattern questions

Ask whether identity/continuity, value equality, an aggregate boundary, persistence lookup, a domain rule across concepts, construction, a past-tense event, or separate read/write/history is actually needed. Include a pattern section only when the answer and named pressure are material. Otherwise omit it.

## Failure semantics

For async or external relationships record delivery, ordering, duplication, retry, idempotency, repair, privacy, and contract compatibility only when triggered. For concurrent writes record transaction/conflict behavior. Do not turn a domain event into event sourcing without evidence.

## Handoff

Hand exactly one model and one `ddd-adoption` request with selected behavior, invariants, evidence, owners, risks, acceptance signals to define, and allowed paths. Boundary conflict returns to strategic with stale dependents.
