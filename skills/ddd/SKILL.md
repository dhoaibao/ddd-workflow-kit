---
name: ddd
description: Route one bounded DDD increment through discover, strategic, tactical, adoption, and review stages; preserve exact transport state, pause for human ratification, and create one revision-bound implementation handoff without editing product code.
---

# DDD lean orchestrator

Coordinate the six-stage package set without doing focused-stage work. The unit of progress is one bounded increment, not a complete domain catalogue.

## Scope and boundaries

Use this package to:

- create and maintain the mandatory `docs/ddd/README.md` index for broad flows;
- route one `ddd-routing-v1` request at a time through `ddd-discover`, `ddd-strategic`, `ddd-tactical`, `ddd-adoption`, and `ddd-review`;
- carry the `ddd-implementation-gate-v1` extension from the candidate increment through review;
- pause at `increment_gate: awaiting-ratification` and record explicit human authorization for one increment;
- create exactly one `implementation-handoff-v1` at `docs/ddd/implementation-handoff.md` only after authorization;
- invalidate that handoff when an authority is stale, revision-mismatched, or conflicting.

The package owns routing/status and authorization sections of the index plus the authorized handoff. `ddd-review` owns only the index decision-queue/latest-review markers and `review.md`; `ddd` preserves those markers. It never invents focused facts, resolves domain policy, edits focused artifacts, or changes product source, tests, configuration, schemas, migrations, deployment files, generated output, or runtime behavior.

## Transport contracts

Base requests and results remain version `ddd-routing-v1`. A request has one stage, one objective, scope, artifact records, evidence, claims, provenance, assumptions, open questions, allowed paths, and `return_to`. A valid result has the preserved transport fields plus status, changed artifacts, findings, one handoff or stop, and invalidated stages; a nonterminal modern result may echo objective/scope/artifacts only as the complete exact next-request set, while a terminal result with that optional echo must preserve the prior request inventory. Legacy results may omit the optional echo; the orchestrator then performs the documented merge/preservation. New artifact records may carry lean `state`; map `working`/`decision-needed` to `draft/unvalidated`, `current` to `active/validated`, `stale` to the prior lifecycle plus `stale` validation, and `superseded` to `superseded/stale`. Legacy records without state remain valid.

The optional `ddd-implementation-gate-v1` extension is carried under `extensions.ddd-implementation-gate-v1` and carries exactly one stable `increment_id`, outcome, in-scope/out-of-scope lists, focused return-on-conflict target, target repository/runtime, baseline revision, accountable implementation owner, acceptance signals, containment, assumptions/questions, typed question dispositions with a unique id, exact issue text (bound to `deferred_questions`/`out_of_scope_questions` with no orphans), impact/owner/action/affected paths/revisit trigger, documentation readiness, increment gate, ratification record naming a human decision owner in its own field (which may name the same or a different person than the implementation owner), and authoritative artifact revisions. An authority revision is `sha256:<64 lowercase hex digits>` over exact artifact UTF-8 bytes plus an explicit list of exact H2 headings. Older routing requests remain readable but cannot produce an implementation handoff.

Read [the protocol](references/orchestration-protocol.md), [the artifact contract](references/artifact-contracts.md), and the examples in [request/result assets](assets/request-result-template.md) before routing.

## Lean artifact profile

Before authorization, generate at most the default working set: `README.md`, one selected context, one tactical model, `adoption-plan.md`, and `review.md`. Generate assessment, vision, maps, glossary, extra contexts, or extra models only when a recorded conditional trigger exists. A non-fit flow may stop in the index without downstream artifacts.

The index must state the target outcome, selected context/increment, current stage, `documentation_readiness`, `increment_gate`, blocking decision count and queue, exact next human action, current links, and `not authorized` or the handoff link. Preserve user prose and review-owned sections.

## Deterministic routing

1. Broad requests start at discovery after scope and evidence boundary are identifiable.
2. Direct starts are allowed only when that stage's entry evidence is present; otherwise route to the earliest owner.
3. Emit one stage request at a time and do not emulate the stage.
4. Consume only complete, known-version results. A malformed result is a bounded `protocol-error` stop; never repair it.
5. Preserve evidence, claims, provenance, assumptions, open questions, artifact paths, and allowed paths across normal transitions.
6. On invalidation, mark affected later artifacts `stale`, preserve lifecycle/provenance, and route to the earliest invalidated stage.

Manual fallback returns the exact unchanged request object and exact stage name, saying that the stage did not run. Do not normalize, reorder, add defaults, or claim a transition.

## Ratification and handoff

Review may return `documentation_readiness: ready` and `increment_gate: awaiting-ratification` only when the named increment has no blocking/invalidating findings, all decision-required items are resolved, boundaries/behavior/invariants/obligations are clear, acceptance and containment fit the risk, remaining uncertainty is explicitly dispositioned, and target/runtime plus accountable implementation owner are named.

The orchestrator then asks for explicit human ratification of that exact increment. Record the authorized implementation owner separately from the human decision owner, plus the decision, date, stable ID, target repository/runtime/baseline, exact outcome/scope/return contract, accepted artifact revisions, assumptions/questions, typed question dispositions, acceptance signals, and containment limitations. A declined decision also records its reason and remains persisted in the authorization marker; a declined or absent decision creates no handoff. Authorization moves the transport gate to `authorized`.

After authorization, create exactly one `docs/ddd/implementation-handoff.md` using [the handoff template](assets/implementation-handoff-template.md). Reference authoritative sections and exact revisions; do not copy their content. The handoff is the sole implementation entry point and returns conflicts to its named DDD stage.

## Legacy and safe updates

Read legacy metadata and existing artifacts without destructive migration. Inspect paths first, preserve user-authored content, and update only owned index/handoff sections. `current` or `ready` never means authorized. Never overwrite a stale or conflicting authority to make the gate pass.

## Result summary

Return the current stage, one increment, status, changed paths, preserved fields, findings/decision queue, readiness/gate pair, stale dependents, exact next action, and whether authorization exists. Static validation is not host/model validation. No implementation, deployment, migration, or release approval is implied.
