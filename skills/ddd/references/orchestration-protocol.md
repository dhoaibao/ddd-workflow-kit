# Orchestration protocol

The orchestrator transports evidence-backed bundles. It does not establish domain facts or emulate a focused stage.

## Request bundle

Every request uses `version: ddd-routing-v1` and includes exactly one stage, one bounded objective, an identifiable scope, artifact paths and lifecycle/validation state, evidence, claims, provenance, assumptions, open questions, allowed paths, and `return_to`. The stage is one of `ddd-discover`, `ddd-strategic`, `ddd-tactical`, `ddd-adoption`, or `ddd-review`. A request may include only explicit versioned extensions; unknown routing-affecting extensions stop the flow.

A minimal request shape is:

```json
{
  "version": "ddd-routing-v1",
  "stage": "ddd-discover",
  "objective": "bound the approval domain",
  "scope": "approval slice",
  "artifacts": [{"path": "docs/ddd/assessment.md", "lifecycle": "draft", "validation": "unvalidated", "availability": "available"}],
  "evidence": ["requester outcome"],
  "claims": ["desired-policy: approval is traceable"],
  "provenance": ["requester statement"],
  "assumptions": [],
  "open_questions": ["which owner validates the policy?"],
  "allowed_paths": ["docs/ddd/"],
  "return_to": "ddd"
}
```

## Result bundle

A result uses the same version and includes stage, exact stage status, changed artifact records, findings, one handoff or `none`, one stop or `none`, invalidated stages, evidence, claims, provenance, assumptions, open questions, allowed paths, and `return_to`. Each changed artifact record has `path`, `lifecycle`, `validation`, and `availability`; an empty list is explicit absence. A valid result does not need to be successful; `partial`, `blocked`, and `not-fit-conflict` are meaningful stage outcomes.

A result is malformed when version, stage, status, required preservation fields, or handoff/stop shape is absent or unknown. Return one `protocol-error` stop naming the field and do not reconstruct it.

## Routing order and entry gates

Use this fixed order for invalidation: discover, strategic, tactical, adoption, review. Broad requests start at discovery. Direct starts are allowed only when their focused entry criteria are present:

- discovery: target/problem scope and permitted evidence boundary;
- strategic: discovery fit/evidence or a bounded strategic objective, terms, and outcome;
- tactical: exactly one validated context, language, boundary, and relationship evidence;
- adoption: bounded outcome, evidence-backed first slice, ownership, and safety constraints;
- review: named artifacts, review scope, acceptance criteria, and evidence boundary.

Missing entry evidence returns the earliest owner rather than a guessed bundle. A non-fit result stops and preserves the simpler path. A material choice or unavailable evidence produces a bounded stop.

## Manual fallback

When a named stage cannot be activated, pass the request object byte-for-byte unchanged to the caller with the exact manual stage name. Do not inject status, defaults, timestamps, normalized paths, new questions, or reordered records. The fallback says the stage did not run.

## Normal transition

When a valid result is available:

1. verify version, stage, status, and all result fields;
2. copy evidence, claims, provenance, assumptions, open questions, artifacts, lifecycle/validation values, and allowed paths into routing state;
3. apply only explicit invalidation and handoff fields from the result;
4. select one next stage from the handoff or canonical earliest invalidation order;
5. construct one contract-valid request with the preserved records and next-stage objective;
6. return the request and consumed-result identity.

Routing may add a next-stage objective or stale markers, but it must not alter a domain claim, source, artifact path, or allowed boundary. It must not require byte-for-byte identity between a result and a next request because the request shape is stage-specific.

## Invalidation and stale dependents

If a result invalidates a later stage, preserve every affected path and lifecycle value, mark its validation state `stale` in routing state, and retain its provenance. Include `invalidated_stages`, the earliest stage, affected dependents, invalidating evidence, owner, and revisit trigger in the next request or stop. If multiple stages are invalidated, route to the earliest canonical stage. If ordering or ownership is disputed, stop and ask for the bounded decision.

## Index stewardship

The orchestrator may update only the routing/status marker sections in `docs/ddd/README.md`. The canonical sections are project/domain scope, current status, artifact index, active contexts, validation summary, open questions, provenance policy, safe-update policy, and latest review. `ddd-review` owns the latest-review link and review findings marker; `ddd` must preserve that section and all user prose. The index is not a substitute for a focused artifact.
