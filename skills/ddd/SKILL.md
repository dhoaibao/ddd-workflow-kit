---
name: ddd
description: Route a bounded DDD request through independently invocable discover, strategic, tactical, adoption, and review stages using exact versioned request/result bundles. Use for broad end-to-end DDD flow, direct stage routing, manual fallback, transition state, and earliest-stage invalidation without emulating stage behavior.
---

# DDD routing orchestrator

Coordinate the five focused DDD stages through versioned request/result bundles. This skill owns routing and workflow state only. It never performs discovery, strategic design, tactical modeling, adoption planning, or review work itself.

## Scope and boundaries

Use this orchestrator to:

- route a broad request to `ddd-discover` and then one focused stage at a time;
- validate direct starts against the named focused stage's entry contract;
- preserve evidence, claim types, provenance, assumptions, open questions, artifact paths, and allowed paths across transitions;
- return an exact unchanged request when named-stage activation is unavailable;
- consume a valid stage result, construct the next contract-valid request, and route invalidation to the earliest affected stage;
- steward only routing/status sections of `docs/ddd/README.md`, while `ddd-review` retains review link and findings stewardship.

Do not emulate any focused stage, infer missing facts, repair malformed results, silently alter claims or paths, select deployment topology, edit product code, tests, configuration, schemas, generated output, deployment files, migrations, or unrelated target documents. A result from a focused stage is consumed as returned, not rewritten into a better result.

## Versioned request contract

Every request is version `ddd-routing-v1` and contains exactly these routing fields plus explicitly versioned extension fields only when a caller supplies them:

- `version`: `ddd-routing-v1`;
- `stage`: exactly one of `ddd-discover`, `ddd-strategic`, `ddd-tactical`, `ddd-adoption`, or `ddd-review`;
- `objective`: one bounded objective;
- `scope`: identifiable target project, domain, context, capability, or slice;
- `artifacts`: artifact records with `path`, `lifecycle`, `validation`, and `availability`, or an empty list for explicit absence;
- `evidence`: evidence and claim/source records;
- `claims`: current-behavior, desired-policy/meaning, required-obligation, fact, interpretation, proposal, decision, or assumption records;
- `provenance`: sources, owners, dates, and validation context;
- `assumptions`: explicit assumptions;
- `open_questions`: unresolved questions and owners where known;
- `allowed_paths`: documentation boundary and ownership constraints;
- `return_to`: `ddd` or the named caller.

Do not normalize an input request before a manual fallback. An unknown version, stage, required field, path boundary, or extension that changes routing is a protocol error and returns a bounded stop.

## Versioned result contract

A focused-stage result is version `ddd-routing-v1` and contains:

- `version` and `stage`;
- `status`: the exact stage result status, such as `complete`, `partial`, `blocked`, `not-fit-conflict`, `strategic-conflict`, or `protocol-error`;
- `changed_artifacts`: artifact records with `path`, `lifecycle`, `validation`, and `availability`, or an empty list;
- `findings`: observable findings or an empty list;
- `handoff`: one complete next request or `none`;
- `stop`: a bounded reason, owner, missing evidence/decision, and next action or `none`;
- `invalidated_stages`: stages invalidated by new evidence, in workflow order;
- `evidence`, `claims`, `provenance`, `assumptions`, and `open_questions`;
- `allowed_paths` and `return_to`.

Reject malformed or unknown results. Do not repair them, reinterpret a missing field, or simulate the stage that should have produced them. Preserve a protocol finding that identifies the malformed field and stops routing.

## Entry and deterministic routing

1. **Broad request.** Require an identifiable target and objective. Route exactly one request to `ddd-discover`. If scope or objective is missing, stop with the material question and do not invent it.
2. **Direct discovery.** Require a target/problem scope and evidence boundary; otherwise stop.
3. **Direct strategic.** Require discovery fit/evidence or an explicit bounded strategic request with meaningful outcome and terms; otherwise route to `ddd-discover`.
4. **Direct tactical.** Require exactly one validated context, purpose, language, boundary, and strategic relationships; otherwise route to `ddd-strategic`.
5. **Direct adoption.** Require a bounded outcome, evidence-backed slice, ownership, and adoption constraints; otherwise route to the earliest discovery, strategic, or tactical owner.
6. **Direct review.** Require named artifacts, identifiable scope, acceptance criteria, and evidence boundary; missing artifacts become review findings rather than reconstructed inputs.

Emit one stage request at a time. Do not force every stage: a non-fit discovery result stops with its simpler-path rationale; partial results stop or hand off according to the returned owner and status. Material user choices, unavailable experts, unsafe paths, and missing evidence remain bounded stops.

## Manual fallback and normal transition

If named-stage activation is unavailable, return the exact request object unchanged: same version, field values, list order, claims, provenance, artifact paths, allowed paths, assumptions, open questions, objective, scope, and return target. State the exact manual stage name and say that it did not run. Do not add defaults, reorder lists, change paths, or claim a transition occurred.

For normal activation, consume a valid result and construct the next request from the result and routing state. Preserve every evidence, claims, provenance, assumptions, open-question, artifact record, allowed-path, lifecycle, validation, and availability value unless the result explicitly supplies a versioned state update. Routing may change only `stage`, `objective`, and routing metadata required by the next stage's contract; it must not drop or alter domain records. Emit one contract-valid request, never multiple competing requests.

## Invalidation and stale routing

If `invalidated_stages` is nonempty, use the earliest stage in canonical order `ddd-discover → ddd-strategic → ddd-tactical → ddd-adoption → ddd-review`. Preserve later affected artifacts' lifecycle values, mark their validation state `stale` in routing state, and preserve their paths and provenance. Route the next request to the earliest invalidated stage, include the invalidation evidence and affected dependents, and retain all unchanged claims. Do not restart at an arbitrary later stage or rewrite the invalidated artifact.

If the earliest route is ambiguous, return a bounded `partial` or `blocked` stop naming the competing owners, evidence, and decision required. A later stage never silently repairs an earlier stage's boundary or evidence.

## Index stewardship

The orchestrator may create or update only its owned routing/status sections in `docs/ddd/README.md`, after inspecting the file and confirming section ownership. Preserve user-authored prose, metadata, links, review findings, and review status. Canonical index sections are project/domain scope, current status, artifact index, active contexts, validation summary, open questions, provenance policy, safe-update policy, and a latest-review link. `ddd` owns routing references and current status only; `ddd-review` retains the latest-review link and findings. Do not replace the index or edit focused artifacts.

## Portable routing result

Return a routing result containing version, current stage, status, objective, scope, exact request/result bundle, preserved evidence/claims/provenance, assumptions, open questions, allowed paths, changed index paths if any, findings, handoff or stop, invalidated stages, stale dependents, and `return_to`. A manual fallback includes the unchanged request and exact stage name. A normal transition includes the consumed result identity and one next request. A non-fit or malformed result includes one bounded stop.

The orchestrator never claims that a focused stage ran unless a valid result was actually consumed. It never claims implementation, deployment, migration, or live validation approval. No transition changes product/runtime behavior.

## References and evaluation

Read the [orchestration protocol](references/orchestration-protocol.md) and [orchestration artifact contract](references/artifact-contracts.md) before routing. The request/result examples are in `assets/request-result-template.md`; the index-owned sections are in `assets/ddd-readme-template.md`; package-local cases are in `evals/evals.json`.
