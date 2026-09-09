# Adoption planning method

This method keeps adoption incremental, evidence-led, and documentation-only. It does not prescribe a language, framework, database, deployment topology, or migration tool.

## Entry triage and earliest owner

Start by classifying the request as greenfield or brownfield and checking one bounded outcome and one first slice. Confirm the available discovery fit, strategic boundary and ownership, tactical behavior and invariants, evidence/provenance, allowed paths, and `return_to`.

Route the earliest missing prerequisite instead of filling it in:

- `ddd-discover` owns missing scope, fit, current-system mode, terminology evidence, and baseline observations.
- `ddd-strategic` owns missing context purpose, ownership, language, relationship direction, and boundary decisions.
- `ddd-tactical` owns missing commands, scenarios, invariants, model decisions, and consistency assumptions.
- `ddd-adoption` owns sequencing, acceptance, dependencies, compatibility, observability, data reconciliation, rollback/containment, and review readiness.

Preserve later artifacts as stale when a new adoption constraint changes their assumptions. Do not silently repair the earlier artifact in this stage.

## Thin increments

For every increment record:

1. the smallest useful outcome and what is explicitly out of scope;
2. evidence, claim types, assumptions, and the owner;
3. prerequisites and dependencies;
4. a decision point and the evidence that would change the plan;
5. observable acceptance signals;
6. integration, privacy, data, and operational risks;
7. rollback, recovery, or containment and its limits;
8. the revisit trigger.

A slice can be documentation, characterization, boundary protection, compatibility, data reconciliation, implementation readiness, or verification. Keep implementation recommendations separate from execution and avoid sequencing unrelated contexts together.

## Greenfield loop

1. Frame the outcome, users, constraints, and learning question.
2. Confirm the selected context and tactical slice with evidence.
3. Establish language, invariant, ownership, and integration decisions needed for the first increment.
4. Recommend the smallest implementation-ready change and its acceptance signals.
5. Define how the result will be observed and what would invalidate the boundary or model.
6. Record the next increment only when its dependency and owner are explicit.

Do not front-load every future capability, select a service topology because a context exists, or call an unvalidated proposal a commitment.

## Brownfield loop

1. Record observed current behavior, dependencies, ownership, data flows, integration contracts, and failure modes.
2. Identify a seam that can be protected without assuming the legacy structure is the domain boundary.
3. Require characterization evidence before changing behavior; if absent, make characterization the first increment.
4. Define a compatibility or translation boundary and state which side owns each decision.
5. Plan one route, rule, or capability at a time with observability and acceptance signals.
6. Define data reconciliation, privacy, ordering, retry, and external-contract assumptions.
7. Define rollback, recovery, or containment, including what cannot be reversed and the trigger to stop.
8. Reassess the boundary and ownership after the first observable increment.

If the seam, owner, compatibility, observability, data reconciliation, or rollback/containment is missing, stop. Do not use a big-bang rewrite, dual-write promise, or event stream as a substitute for missing evidence.

## Claim conflicts and risk ledger

Keep current behavior, desired policy/meaning, and required obligation as separate claims with source, owner, scenario, impact, and validation. Record whether the conflict blocks the next increment, requires an owner decision, or can be contained. Risk rows should identify likelihood or uncertainty, consequence, owner, mitigation, acceptance signal, and revisit trigger.

Optional architecture choices are conditional decisions. Record the concrete need, evidence, cost, privacy and operational impact, and simpler alternative. A plan may recommend a future investigation without deciding the architecture.

## Review handoff

A complete review request must name exactly one `docs/ddd/adoption-plan.md` artifact, its mode and slice, the ordered increments, evidence and provenance, prerequisites, owners, dependencies, acceptance signals, risks, rollback/containment, data/integration/privacy assumptions, open questions, allowed paths, invalidated stages, and `return_to: ddd-adoption`. It says that `ddd-review` is the next manual stage and never claims review or implementation ran.
