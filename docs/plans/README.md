# Remaining implementation roadmap

## Current status

The repository has reviewed, committed focused MVP packages for `ddd-discover`, `ddd-strategic`, and `ddd-tactical`. The remaining executable stages are `ddd-adoption`, `ddd-review`, and the routing-only `ddd` orchestrator. This roadmap plans those stages without creating their packages or claiming that they are implemented.

The roadmap is grounded in the [skill routing design](../skill-design/skills-and-routing.md), [workflow rules](../skill-design/workflows.md), [artifact contracts](../skill-design/artifact-contracts.md), [quality gates](../skill-design/quality-gates.md), and [portability notes](../skill-design/portability.md).

## Ordered work

### 0. Run availability-gated validation and hardening

Attempt the deferred live host/model evaluation for the implemented `ddd-discover`, `ddd-strategic`, and `ddd-tactical` packages. Retain the evaluation inputs, package/version context, host/model availability, observed outputs, failures, and provenance needed to reproduce or qualify each result. Attempt optional official `skills-ref` validation only when it is already available; never install it. Any issue found in a focused package routes to that package for correction and re-review before adoption work begins.

**Dependency:** an available host/model and optional validator are not required to start the phase; their availability determines which checks can produce results.

**Exit criteria:** each focused package has either a recorded live result and resolved/reviewed issues, or an explicit `blocked`/`deferred` record naming the unavailable capability and residual risk. Static checks never claim live success, and adoption cannot be declared unblocked by an unrecorded evaluation gap.

### 1. Implement `ddd-adoption`

Use the [adoption plan](ddd-adoption.md). It must produce documentation-only, incremental, reversible adoption planning for greenfield and brownfield work, with an owned `adoption-plan.md` artifact and an exact handoff to review.

**Dependencies:** validated enough discovery/strategic/tactical context for a bounded slice, or an explicit bounded request that satisfies adoption entry criteria.

**Exit criteria:** package validation, evaluation review, safe-update checks, and independent review pass; no migration or product-code edits occur.

### 2. Implement `ddd-review`

Use the [review plan](ddd-review.md). It must own `review.md`, apply fit/provenance/lifecycle/schema/vocabulary/strategic-to-tactical/adoption/cross-artifact gates, preserve disputed facts, and route stale work backward without silently repairing it.

**Dependencies:** the review scope and artifacts are identifiable; adoption implementation is not required for review cases that explicitly cover missing or partial adoption artifacts.

**Exit criteria:** package validation, evaluation review, safe-update checks, and independent review pass; readiness is documented readiness only, never implementation approval.

### 3. Implement `ddd` last

Use the [orchestrator plan](ddd.md). It must route and hold state only: manual fallback returns the exact unchanged request bundle, while normal flow consumes an exact stage result and constructs the next contract-valid request while preserving evidence, provenance, claims, and paths. It must use named activation or exact manual fallback, loop to the earliest invalidated stage, and not emulate any focused stage.

**Dependencies:** all five focused packages exist and their transition/result contracts are stable; adoption and review have passed their gates.

**Exit criteria:** orchestrator package validation, package isolation, transition-loop evaluations, portability checks, and independent review pass; `docs/ddd/README.md` index ownership and review stewardship are explicit.

### 4. Run the full-suite transition and currentness pass

Exercise focused-stage invocation, orchestrated routing, package isolation, portability fallbacks, and evidence/claim preservation. Repeat phase-0 live evaluations only when a previously unavailable host/model or optional validator becomes available. Reconcile README/status links and document residual gaps.

**Dependencies:** stages 1–3 complete; any live evaluation run has the availability and evidence record required by phase 0.

**Exit criteria:** all local checks pass, normal transitions construct contract-valid requests from stage results, manual fallbacks preserve unchanged requests, invalidation loops reach the earliest affected stage, documentation accurately distinguishes implemented, reviewed, and deferred work, and residual risks are recorded.

## Shared exit gates

Every implementation phase must preserve the documentation-only boundary, package-local self-containment, relative-link integrity, one H1 per Markdown file, deterministic package validation, evidence provenance, safe additive updates, and explicit stop behavior. A focused stage owns its artifact; the orchestrator coordinates but does not take ownership. A review result is scoped documentation readiness, not permission to edit product code.

## Residual risks and decisions

- Named stage activation may be unavailable; every package therefore needs an exact manual invocation fallback.
- Existing target documents may contain conflicting current, desired, and required claims; no plan may collapse them silently.
- Brownfield work may lack ownership, characterization, compatibility, or rollback evidence; the correct result is a bounded stop or earlier-stage handoff.
- Static validation cannot substitute for official host/model execution or unavailable optional tooling.
- The first release remains language-, framework-, deployment-, and database-neutral; no plan assumes a microservice topology.
