---
name: ddd-review

description: Review one named increment and its authority set with rigorous internal gates but concise exception output; separate documentation readiness from ratification and route conflicts to the earliest owner without creating the handoff.
---

# DDD exception review

Review one named increment, its authority set, and its implementation-gate extension. Think rigorously; emit only findings that change the next action.

## Entry and boundary

Require review scope, named increment, requested/available artifact paths, acceptance criteria, evidence boundary, and allowed review path. Missing artifacts are findings; never reconstruct them. Review owns `docs/ddd/review.md` and only the `decision-queue`/`latest-review` markers in `docs/ddd/README.md`; `ddd` owns and preserves all other index markers. It never edits another stage's authority, resolves domain policy, creates the implementation handoff, or edits product/runtime files.

## Internal gates, concise output

Run fit, evidence/provenance, lifecycle/schema, vocabulary, strategic-to-tactical, adoption safety, cross-artifact consistency, utility, and authority revision checks internally. The output records one sentence summarizing passed checks and only blocking, invalidating, or decision-required findings plus materially relevant accepted/deferred/out-of-scope items. Do not print a full passing table or duplicate artifact inventory.

## Dual readiness and queue

Every review records:

```yaml
documentation_readiness: ready | follow-up | blocked | invalidated
increment_gate: blocked | awaiting-ratification
```

`awaiting-ratification` is allowed only when the increment has no blocking/invalidating findings, decision-required items are resolved, behavior/boundary/invariants/obligations are clear, acceptance/containment are sufficient, all remaining uncertainty has an owner/revisit trigger, and target/runtime plus accountable implementation owner are named. It is not authorization.

Consolidate all unresolved issues in one queue with stable ID, exact issue, increment impact, disposition, earliest owner, smallest action, affected paths, and revisit trigger. Allowed dispositions are `blocking`, `invalidating`, `decision-required`, `accepted-assumption`, `deferred`, `out-of-scope`, and `resolved`. A blocker cannot be silently relabeled deferred/out-of-scope; human confirmation and impact rationale are required.

## Earliest-owner routing

Discovery owns fit/scope/current behavior; strategic owns boundary/language/relationships; tactical owns examples/rules/invariants/consistency; adoption owns target/baseline/owner/acceptance/containment; review owns aggregation. Mark dependents stale and route to the earliest owner. Do not repair source artifacts to pass review.

## Result

Return named increment/authority set, dual readiness, exception queue, stale routing, accepted/deferred/out-of-scope items that matter, one exact next action, changed review path, and a statement that review readiness is not implementation authorization. Only the orchestrator moves the transport index gate to `authorized` and creates `implementation-handoff-v1` after explicit ratification; this review record remains the evidence of `awaiting-ratification`.

Read [the method](references/review-method.md), [the contract](references/artifact-contracts.md), and [the review template](assets/review-template.md) before writing.
