# Remaining implementation roadmap

## Current status

The approved [lean workflow redesign](complete/lean-workflow-redesign.md) is implemented across all six document-class packages, shared contracts, templates, evaluations, validator, README, roadmap, and changelog; that candidate is documentation-only and runtime-neutral, with one bounded increment as the progress unit.

The approved [`ddd-impl-fastapi-hdx` plan](complete/ddd-impl-fastapi-hdx.md) adds the suite's first `implementation`-class package, an opt-in FastAPI/`hdx-domain-kit` implementation package gated by a ratified `docs/ddd/implementation-handoff.md`. It is implemented, package-validated, and independently reviewed (READY WITH FOLLOW-UPS across two rounds).

Historical phase-0 and phase-4 records remain preserved. The local sanitized BonVoye-shaped fixture is recorded in [the redesign report](../evaluations/lean-workflow-redesign-v1-report.json); no external BonVoye repository was accessed.

The roadmap is grounded in the [skill routing design](../skill-design/skills-and-routing.md), [workflow rules](../skill-design/workflows.md), [artifact contracts](../skill-design/artifact-contracts.md), [quality gates](../skill-design/quality-gates.md), and [portability notes](../skill-design/portability.md).

## Ordered work

### 0. Run availability-gated validation and hardening

Attempt the deferred live host/model evaluation for the implemented `ddd-discover`, `ddd-strategic`, and `ddd-tactical` packages. Retain the evaluation inputs, package/version context, host/model availability, observed outputs, failures, and provenance needed to reproduce or qualify each result. Attempt optional official `skills-ref` validation only when it is already available; never install it. Any issue found in a focused package routes to that package for correction and re-review before adoption work begins.

**Dependency:** an available host/model and optional validator are not required to start the phase; their availability determines which checks can produce results.

**Execution record:** [phase-0 evaluation report](../evaluations/phase-0-report.json), with captured per-case outputs under [`docs/evaluations/phase-0-live/`](../evaluations/phase-0-live/). The optional `skills-ref` check remains explicitly deferred because the executable and Python module were unavailable; it was not installed.

**Exit criteria:** each focused package has either a recorded live result and resolved/reviewed issues, or an explicit `blocked`/`deferred` record naming the unavailable capability and residual risk. Static checks never claim live success, and adoption cannot be declared unblocked by an unrecorded evaluation gap.

### 1. Implement `ddd-adoption` — completed

The [adoption plan](complete/ddd-adoption.md) is implemented at [`skills/ddd-adoption/`](../../skills/ddd-adoption/SKILL.md). It produces documentation-only, incremental, reversible adoption planning for greenfield and brownfield work, with an owned `adoption-plan.md` artifact and an exact handoff to review.

**Dependencies:** validated enough discovery/strategic/tactical context for a bounded slice, or an explicit bounded request that satisfies adoption entry criteria.

**Exit criteria:** package validation, evaluation review, safe-update checks, and independent review pass; no migration or product-code edits occur. Phase 1 implementation and package checks are complete; live transition evaluation remains part of phase 4.

### 2. Implement `ddd-review` — completed

The [review plan](complete/ddd-review.md) is implemented at [`skills/ddd-review/`](../../skills/ddd-review/SKILL.md). It owns `review.md`, applies fit/provenance/lifecycle/schema/vocabulary/strategic-to-tactical/adoption/cross-artifact gates, preserves disputed facts, and routes stale work backward without silently repairing it.

**Dependencies:** the review scope and artifacts are identifiable; adoption implementation is not required for review cases that explicitly cover missing or partial adoption artifacts.

**Exit criteria:** package validation, evaluation review, safe-update checks, and independent review pass; readiness is documented readiness only, never implementation approval. Phase 2 implementation and package checks are complete; live transition evaluation remains part of phase 4.

### 3. Implement `ddd` last — completed

The [orchestrator plan](complete/ddd.md) is implemented at [`skills/ddd/`](../../skills/ddd/SKILL.md). It routes and holds state only: manual fallback returns the exact unchanged request bundle, while normal flow consumes an exact stage result and constructs the next contract-valid request while preserving evidence, provenance, claims, and paths. It uses named activation or exact manual fallback, loops to the earliest invalidated stage, and does not emulate any focused stage.

**Dependencies:** all five focused packages exist and their transition/result contracts are stable; adoption and review have passed their gates.

**Exit criteria:** orchestrator package validation, package isolation, transition-loop evaluations, portability checks, and independent review pass; `docs/ddd/README.md` index ownership and review stewardship are explicit. Phase 3 implementation and package checks are complete; live transition evaluation remains part of phase 4.

### 4. Run the full-suite transition and currentness pass — complete for candidate review

Exercise focused-stage invocation, orchestrated routing, package isolation, portability fallbacks, and evidence/claim preservation. Repeat phase-0 live evaluations only when a previously unavailable host/model or optional validator becomes available. Reconcile README/status links and document residual gaps.

**Dependencies:** stages 1–3 complete; any live evaluation run has the availability and evidence record required by phase 0.

**Execution record:** [phase-4 report](../evaluations/phase-4-report.json), [live capture manifest](../evaluations/phase-4-live-capture.json), [semantic judgments](../evaluations/phase-4-live-semantic-judgments.json), and [transition matrix](../evaluations/phase-4-transition-matrix.json). The 30 adoption/review/orchestrator cases were live-evaluated with 30/30 process and semantic passes. The unchanged 29 phase-0 cases are carried forward by matching package and evaluation hashes; they were not rerun. `skills-ref` remains unavailable and deferred without installation.

**Exit criteria:** all local checks pass, normal transitions construct contract-valid requests from stage results, manual fallbacks preserve unchanged requests, invalidation loops reach the earliest affected stage, documentation accurately distinguishes implemented, reviewed, and deferred work, and residual risks are recorded.

### 5. Implement `ddd-impl-fastapi-hdx` — completed

The [implementation-package plan](complete/ddd-impl-fastapi-hdx.md) is implemented at [`skills/ddd-impl-fastapi-hdx/`](../../skills/ddd-impl-fastapi-hdx/SKILL.md), with the `PACKAGES` package-class manifest, a `scripts/validate-skills.py` class/write-boundary gate, an optional `install.sh --skill` selection path (default document-class install unchanged), and synchronized `docs/skill-design/` and `README.md`/`AGENTS.md` boundary docs. It verifies a ratified `docs/ddd/implementation-handoff.md`'s authorization, authority revisions, and required headings before writing; may autonomously write target-repository domain code/tests for the ratified increment; gates migrations, composition-root edits, and dependency/config changes on explicit per-run approval; and owns exactly one target-project artifact, `docs/ddd/implementation/<increment-id>.md`.

**Dependencies:** the six document-class packages and their `implementation-handoff-v1` transport are stable; an existing `HdxApplication` composition root in the target repository (bootstrap is an approval-gated conditional, not the default path).

**Exit criteria:** `scripts/validate-skills.py` reports seven packages plus the `PACKAGES` manifest check; `scripts/test-installer.sh` passes including default/`--skill`/update/deselect/unknown-package/archive-listing cases; a built release installs 6 links by default and 7 with `--skill ddd-impl-fastapi-hdx`; no unqualified suite-wide `documentation-only` claim remains in `README.md`/`AGENTS.md`/`docs/`. An end-to-end trial against a scratch consumer FastAPI/`hdx-domain-kit` repository is explicitly out of scope for this increment and needs separate user approval.

## Shared exit gates

Every document-workflow implementation phase must preserve the documentation-only boundary, package-local self-containment, relative-link integrity, one H1 per Markdown file, deterministic package validation, evidence provenance, safe additive updates, and explicit stop behavior. A focused stage owns its artifact; the orchestrator coordinates but does not take ownership. A review result is scoped documentation readiness, not permission to edit product code. The `implementation`-class package instead preserves a class-scoped write boundary: autonomous domain code/tests for the ratified increment only, approval-gated migrations/composition-root/dependency changes, and its own single owned target-project artifact.

## Residual risks and decisions

- Named stage activation may be unavailable; every package therefore needs an exact manual invocation fallback.
- Existing target documents may contain conflicting current, desired, and required claims; no plan may collapse them silently.
- Brownfield work may lack ownership, characterization, compatibility, or rollback evidence; the correct result is a bounded stop or earlier-stage handoff.
- Static validation cannot substitute for official host/model execution or unavailable optional tooling.
- The first release's document-class packages remain language-, framework-, deployment-, and database-neutral; no plan assumes a microservice topology.
- `hdx-domain-kit` is unpublished and moving (0.1.0); `ddd-impl-fastapi-hdx` cites decisions and relies on target-repo preflight rather than hardcoding its API surface.
