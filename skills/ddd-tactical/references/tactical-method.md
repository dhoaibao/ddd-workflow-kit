# Tactical modeling method

This reference keeps tactical design behavior-first and evidence-led. It is a method, not a mandatory pattern catalog.

## Start with behavior

For the selected context, list the command or use case, actor, preconditions, inputs, decisions, successful outcome, failures, counterexamples, observable acceptance signals, and related contexts. Prefer concrete scenarios over nouns. Distinguish current behavior from desired policy and required obligations.

## Invariants before boundaries

Name each invariant in plain language, cite its evidence, identify its owner and failure consequence, and state whether it needs immediate consistency or can tolerate eventual consistency. The smallest aggregate boundary that protects a named immediate invariant is a candidate, not a default. If an invariant spans proposed aggregates and must be immediate, revisit the boundary or merge the model rather than assuming a distributed transaction or event will repair it.

## Model-element questions

- **Entity:** Does the concept need identity and continuity across changes? Record identity, lifecycle, responsibilities, and status.
- **Value object:** Is equality based on values and does validation belong with the value? Record immutability assumptions, normalization, and examples/non-examples.
- **Aggregate and root:** Which immediate invariant does the boundary protect? What is explicitly in and out? Which references cross the boundary? What transaction and concurrency assumptions apply? The root is the external access point.
- **Repository:** Is retrieval or persistence of this aggregate root required by the use case? State domain-facing intent, failure semantics, and concurrency expectations without choosing an implementation.
- **Domain service:** Is a domain rule genuinely about multiple concepts and not naturally owned by an entity or value? Keep orchestration in the application flow.
- **Specification/factory:** Name the concrete need and why an inline rule or constructor is insufficient. Otherwise mark it `not-needed`.
- **Domain event:** Is a past-tense fact useful to another policy or context? Record payload facts, privacy, delivery, ordering, duplication, idempotency, retry, and recovery assumptions. An event is not a command and does not imply event sourcing.

## Optional patterns

CQRS and event sourcing are separate decisions. For each, use `not-needed`, `deferred`, or `proposed`; cite evidence, describe conceptual and operational costs, and record a simpler alternative. A high write/read difference does not by itself justify CQRS, and domain events do not justify event sourcing.

## Evidence and handoff

Mark decisions `proposed`, `unvalidated`, `validated`, or `deferred` with provenance. Record contradictions instead of smoothing them over. If evidence changes the strategic boundary, vocabulary, ownership, or relationship, preserve the tactical finding, mark affected work stale, and hand back to `ddd-strategic`. Otherwise the next request is exactly one `ddd-adoption` bundle containing the model path, selected context, behavior, invariants, decisions, assumptions, risks, evidence, validation, owners, allowed paths, open questions, acceptance signals to define, and `return_to`.
