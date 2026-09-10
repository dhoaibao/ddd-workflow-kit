---
name: ddd-adoption
description: Specify one evidence-backed candidate increment with stable identity, target and baseline, acceptance, risk containment, and review handoff; carry the implementation gate without authorizing or executing product changes.
---

# DDD adoption planning

Turn one selected tactical slice into one fully specified candidate increment. Later increments remain hypotheses.

## Entry and boundary

Require one bounded outcome, one selected context/slice, tactical behavior/invariants or an explicit bounded request, evidence/provenance, accountable implementation owner, dependencies, allowed paths, and `return_to`. For brownfield/data/async/privacy/external-contract/concurrency risks, require only the triggered baseline, characterization, compatibility, observability, reconciliation, privacy, delivery, or containment details.

Adoption owns only `docs/ddd/adoption-plan.md`. It never executes migrations, edits product source/tests/configuration/schemas/deployment files, or claims implementation/deployment/release.

## One-increment workflow

1. Assign a stable `increment_id`.
2. Name target repository/runtime and exact baseline revision before implementation readiness.
3. State intended outcome, concrete change, in-scope and excluded behavior.
4. Name accountable implementation owner, dependencies, observable acceptance signals, and stop conditions; add material risk and containment/rollback only when a trigger exists.
5. Classify questions as `blocking`, `invalidating`, `decision-required`, `accepted-assumption`, `deferred`, `out-of-scope`, or `resolved`; retain impact and revisit trigger.
6. Keep later increments short hypotheses.
7. Emit the `ddd-implementation-gate-v1` result extension and exactly one `ddd-review` request only when the candidate is complete; `ddd` carries the extension and performs ratification/authorization. Never claim authorization.

## Brownfield and trigger depth

A brownfield candidate cannot be ready without baseline, characterization, seam, compatibility/translation, observability, data reconciliation, owner, and containment when those risks exist. A missing safety element is a bounded stop. No trigger means no generic operational section.

## Safe updates and legacy

Inspect the adoption path, preserve legacy metadata/user prose/links, update only owned sections additively, and stop for ambiguity. Existing artifacts remain readable; no silent schema migration occurs.

## Result

Return one plan path, stable increment, target/baseline, outcome/scope, owner/dependencies, acceptance, risk/containment, stop conditions, dispositions, gate extension, and one review handoff or earliest-owner stop. The review handoff does not authorize implementation.

Read [the method](references/adoption-method.md), [the contract](references/artifact-contracts.md), and [the plan template](assets/adoption-plan-template.md) before writing.
