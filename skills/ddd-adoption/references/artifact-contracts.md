# Adoption artifact contracts

These contracts define the documentation-only adoption slice without prescribing implementation technology or migration execution.

## Common metadata and claims

`docs/ddd/adoption-plan.md` begins with one H1 and a metadata table containing `artifact`, `status`, `validation`, `owner`, `scope`, `provenance`, `assumptions`, `open_questions`, and `last_updated`. Lifecycle values are `draft`, `active`, `superseded`, or `archived`; validation values are `unvalidated`, `partially-validated`, `validated`, or `stale`.

The body distinguishes current behavior, desired policy/meaning, required obligation, fact, interpretation, proposal, decision, and assumption. Each material claim names source/provenance, owner, scenario, impact, and validation. Conflicting claims remain separate and may block an increment.

## Minimum plan schema

The plan includes:

- mode: `greenfield` or `brownfield`;
- target outcome, scope, first slice, and explicit exclusions;
- entry prerequisites and validation state;
- ordered increments with owner, dependencies, decision point, acceptance signal, risk, and rollback/containment;
- ownership and unresolved decisions;
- data, integration, privacy, observability, compatibility, and reconciliation considerations;
- claim/evidence ledger and conflict impact;
- rollback, recovery, or containment limits and triggers;
- explicit statement that the plan is a recommendation and no migration or product-code change was executed;
- one `ddd-review` handoff with exact artifact path, evidence, acceptance signals, risks, allowed paths, open questions, and `return_to`.

Brownfield plans additionally record current behavior, characterization evidence, seam, compatibility/translation, observability, data ownership/reconciliation, and accountable owners before recommending a risky increment.

## Safe ownership and paths

1. Adoption owns only `docs/ddd/adoption-plan.md`.
2. Inspect the path and preserve existing prose, metadata, links, provenance, and user ownership.
3. Update only adoption-owned sections and use additive, reviewable changes.
4. Stop before destructive, structural, ambiguous, colliding, traversal-like, or ownership changes.
5. Never edit product source, tests, configuration, schemas, generated output, deployment files, or execute a migration.
6. If a request mixes a safe documentation recommendation with forbidden actions, report both outcomes and do not claim forbidden work occurred.

## Transition contract

A complete result hands exactly one adoption plan to `ddd-review`. It includes `plan_path: docs/ddd/adoption-plan.md`, mode, selected slice, prerequisites, evidence, assumptions, dependencies, owners, acceptance signals, risks, rollback/containment, data/integration/privacy notes, open questions, allowed paths, invalidated stages, and `return_to: ddd-adoption`. A bounded stop names the earliest stage or owner that must resolve the gap.
