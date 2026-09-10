# Lean decision-driven workflows

The canonical flow remains `ddd-discover → ddd-strategic → ddd-tactical → ddd-adoption → ddd-review`, but progress is one bounded implementation increment, not completion of an artifact catalogue.

## Orchestrated flow

The orchestrator creates the mandatory index, carries `ddd-routing-v1`, and carries the explicitly versioned `ddd-implementation-gate-v1` extension from adoption through review. It emits one stage request at a time. A non-fit result stops with the simpler path. A focused stage never silently repairs an earlier owner's evidence.

Before authorization the default artifact set is the index, one selected context, one tactical model, one adoption plan, and one review. Conditional artifacts require a recorded trigger. After `documentation_readiness: ready` and `increment_gate: awaiting-ratification`, the human may ratify one increment; ratification moves the gate to `authorized`, and only then does `ddd` create one `implementation-handoff-v1`.

## Increment loop

1. State one target outcome and one selected context/slice.
2. Record only evidence, behavior, boundary, acceptance, decision, or material risk needed for that increment.
3. Route missing decisions to the earliest owner and consolidate them in the review queue.
4. Keep later increments as hypotheses.
5. Review exception-first, separating documentation readiness from authorization.
6. Pause for explicit human ratification.
7. Invalidate the handoff whenever an authoritative revision changes, becomes stale, or conflicts.

## Questions and dispositions

Ask only the smallest grouped question set that changes scope, safety, ownership, behavior, boundary, obligation, or acceptance. Use the shared dispositions: `blocking`, `invalidating`, `decision-required`, `accepted-assumption`, `deferred`, `out-of-scope`, and `resolved`. A blocker cannot be hidden by relabeling it deferred or out of scope without human confirmation and impact rationale.

## Greenfield and brownfield

Greenfield work starts with one high-learning slice, not a complete domain model. Brownfield work starts with baseline, characterization, seam, compatibility, observability, ownership, reconciliation, and containment only when the increment triggers those risks. Neither flow performs implementation.

## Feedback and stale routing

New evidence routes to the earliest owner: discovery for fit/scope/current-system evidence; strategic for boundary/language/relationship; tactical for behavior/invariants/consistency; adoption for sequencing/compatibility/containment; review for aggregation. Later artifacts remain readable but are marked stale. A changed authority set invalidates an existing handoff rather than being silently resolved.

## Documentation-only boundary

All six packages write only owned target-project `docs/ddd/` documentation and portable chat/result bundles. They never edit source, tests, configuration, schemas, migrations, deployment files, generated output, or runtime behavior. Static validation covers repository conventions; it does not establish host/model effectiveness.
