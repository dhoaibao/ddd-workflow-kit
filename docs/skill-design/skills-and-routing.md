# Skills and routing

The suite ships two package classes, listed in the release-root `PACKAGES` manifest. Six `document`-class packages — `ddd`, `ddd-discover`, `ddd-strategic`, `ddd-tactical`, `ddd-adoption`, and `ddd-review` — install by default, preserve the documentation-only/runtime-neutral boundary, and use one bounded increment as the unit of progress. `implementation`-class packages (currently `ddd-impl-fastapi-hdx`) are explicit opt-in installs that write target-project code for one ratified increment; see [Implementation packages](#implementation-packages).

## Shared rules

Every package keeps evidence near material claims, preserves current/desired/obligation distinctions when consequential, omits empty or generic content, and updates only owned `docs/ddd/` sections. Existing legacy artifacts remain readable. A package stops for missing evidence, material choice, unsafe path, stale authority, or forbidden product changes.

The common transport remains `ddd-routing-v1`. Adoption, review, and orchestration carry `ddd-implementation-gate-v1` with stable increment ID, target/runtime, baseline, owner, acceptance, containment, dual readiness, ratification, and authority revisions.

## Responsibilities

| Package | Owns | Default output |
| --- | --- | --- |
| `ddd` | Routing/status, authorization markers, index, ratification gate, sole authorized handoff; preserves review markers | `README.md`, then `implementation-handoff.md` after authorization |
| `ddd-discover` | Fit, scope, evidence, current/desired conflicts | Index decision; conditional assessment/vision/language |
| `ddd-strategic` | One selected context, touched relationships, material language/boundaries | One context file; conditional maps/glossary/additional contexts |
| `ddd-tactical` | One slice's examples, rules, invariants, transitions, failure semantics | One model file; conditional pattern decisions |
| `ddd-adoption` | One stable candidate increment and trigger-based safety | `adoption-plan.md` |
| `ddd-review` | Internal gates, exception output, one decision queue, routing; owns only README queue/review markers and `review.md` | `review.md` plus two README markers |

## Orchestrator

`ddd` routes one request at a time in canonical order. It makes `docs/ddd/README.md` mandatory for broad flows, preserves user prose and focused ownership, pauses at `awaiting-ratification`, moves the separate gate to `authorized` only after explicit human confirmation, creates exactly one `implementation-handoff-v1`, and invalidates it on stale/revision/conflict. It never creates focused modeling facts or product changes.

## Discover

Discovery returns the smallest evidence-backed fit decision. A non-fit result may stop in the index without downstream artifacts. `assessment.md`, `domain-vision.md`, and `ubiquitous-language.md` are conditional on fit evidence, disputed intent, or material terminology reuse/conflict. Discovery persists only material current-versus-desired differences.

## Strategic

Strategic work is slice-first. It creates one selected context by default, documenting direct relationships only as deeply as the current slice requires. Domain map, context map, glossary, additional context files, and additional model dependencies require recorded triggers. A context is not a deployment service.

## Tactical

Tactical work is example-driven. It records commands, success/failure cases, rules, invariants, state changes, current-versus-desired deltas, and integration/consistency semantics. Entities, values, aggregates, repositories, services, specifications, factories, events, CQRS, and event sourcing appear only for a named pressure; unused patterns are omitted.

## Adoption

Adoption fully specifies one candidate increment with stable ID, target/runtime, baseline, accountable implementation owner, outcome, in/out scope, dependencies, acceptance, stop conditions, and typed question dispositions carrying impact, owner, action, affected paths, and revisit trigger. Risk/containment is conditional on a trigger. Later increments remain hypotheses. It emits the implementation-gate result extension; `ddd` carries it and performs human ratification, never adoption.

## Review

Review checks all gates internally and emits exceptions. It records `documentation_readiness: ready|follow-up|blocked|invalidated` and `increment_gate: blocked|awaiting-ratification`; `ddd` separately moves the transport index gate to `authorized` after human ratification. Review consolidates findings by earliest owner, emits one exact next action, never creates the handoff, and never decides domain policy.

## Routing

| Signal | Primary package | Route backward when |
| --- | --- | --- |
| Fit, scope, current behavior, terminology | `ddd-discover` | evidence is absent or non-fit |
| Context, boundary, language, relationship | `ddd-strategic` | ownership or direction is disputed |
| Examples, invariants, consistency, tactical pattern pressure | `ddd-tactical` | behavior or invariant is missing |
| One increment, acceptance, risk, containment | `ddd-adoption` | target/baseline/owner/safety is missing |
| Exception review, readiness, decision queue | `ddd-review` | earliest owner must resolve a finding |
| Broad request, ratification, handoff | `ddd` | any upstream stage is invalidated |

## Consumption contract

A downstream coding workflow reads the exact authorized handoff first, then only listed increment, tactical, boundary, and strategic sources, followed by current source/tests and a technical plan. Any changed revision, stale authority, conflicting source, new domain decision, or scope expansion returns to the named DDD stage.

## Implementation packages

An `implementation`-class package is a separate, opt-in, stack-specific consumer of `docs/ddd/implementation-handoff.md`; it is the only package class that writes target-project product code and tests. It never touches the document-workflow stages, the `ddd-routing-v1`/`ddd-implementation-gate-v1` transport, or another package's owned artifact. `ddd` names only the generic consumption contract above; it does not link to or assume any specific implementation package.

`ddd-impl-fastapi-hdx` is the first such package: it implements one ratified increment in a target Python/FastAPI repository built on `hdx-domain-kit`. It verifies the handoff's authorization, authority revisions, and required headings before writing anything; may autonomously write domain code and tests for the ratified increment; gates migrations, composition-root edits, and dependency/config changes on explicit per-run approval; and owns exactly one target-project artifact, `docs/ddd/implementation/<increment-id>.md`.
