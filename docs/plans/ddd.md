# Plan: implement `ddd`

## Current status

`ddd` is unimplemented. It is the last implementation phase because it depends on the five independently invocable focused stages and their stable transition/result contracts. It owns routing and workflow state only.

## Purpose and boundaries

The orchestrator coordinates `ddd-discover → ddd-strategic → ddd-tactical → ddd-adoption → ddd-review` when prerequisites require that flow, while allowing focused direct invocation when entry criteria are satisfied. It emits exact stage requests and consumes exact stage results. Only a manual fallback preserves the request bundle unchanged; a normal transition constructs the next contract-valid request from the consumed result and routing state while preserving evidence, provenance, claims, and paths. It loops to the earliest invalidated stage and returns bounded partial/stop results.

It must never emulate discovery, strategic, tactical, adoption, or review behavior; invent evidence; silently repair artifacts; select deployment topology; or edit product code, tests, configuration, generated output, schemas, or deployment files. Implement the orchestrator only after the focused stages are complete and reviewed.

## Prerequisites and inputs

Require stable contracts for all focused stages, including their entry criteria, artifact ownership, status values, handoff fields, invalidation behavior, and manual fallback. Inputs include:

- user goal, target scope, desired outcome, constraints, and evidence boundary;
- existing `docs/ddd/` artifacts and their lifecycle/validation status;
- greenfield/brownfield mode, domain-expert availability, and requested depth;
- a request bundle or focused-stage result bundle when resuming a flow;
- allowed paths, ownership, assumptions, open questions, and `return_to`.

If the target or desired outcome is not identifiable, ask a material user question. If a focused result is missing or malformed, return a bounded stop rather than reconstructing it.

## Proposed portable package

Create last, after adoption and review are implemented and reviewed:

- `skills/ddd/SKILL.md` — routing/state-only instructions;
- `skills/ddd/references/orchestration-protocol.md` — exact request/result bundles, state transitions, invalidation, and fallback;
- `skills/ddd/references/artifact-contracts.md` — package-local orchestration state and index contract;
- `skills/ddd/assets/request-result-template.md` — portable request/result examples and schema without target facts;
- `skills/ddd/assets/ddd-readme-template.md` — package-local template for the orchestrator-owned sections of `docs/ddd/README.md`, including the canonical index sections and ownership markers;
- `skills/ddd/evals/evals.json` — package-local routing and transition scenarios.

The logical package may be hosted with the focused packages, but the contract must not depend on a specific runtime or activation API.

## Ordered implementation phases

1. **Freeze the transition contract.** Encode exact request/result bundle fields: stage, objective, scope, artifacts, evidence, assumptions, open questions, allowed paths, and return target; result status, changed paths, findings, handoff/stop reason, and invalidated stages.
2. **Define state and routing.** Track current stage, validation/lifecycle status, prerequisites, stale dependents, and the earliest invalidated stage. Routing must be deterministic and stage-owned behavior must remain outside the orchestrator.
3. **Define entry and direct invocation.** Start discovery for broad requests; permit focused starts only when their entry criteria are satisfied; return an exact manual stage invocation plus the unchanged request bundle when named activation is unavailable.
4. **Define transition behavior.** Emit one bounded request at a time, consume the exact result bundle, preserve its evidence/provenance/claims/paths without silent alteration, construct the next contract-valid request from that result and routing state, and route loops to the earliest invalidated stage.
5. **Define partial and stop results.** Handle non-fit, missing evidence, material user decisions, unavailable experts, unsafe paths, missing artifacts, and failed gates without claiming later stages ran.
6. **Define index stewardship.** `ddd` owns routing references for `docs/ddd/README.md`; `ddd-review` stewards its review link and findings. The orchestrator may update only its owned index sections and must preserve user-authored content.
7. **Add evaluations and validate.** Cover normal flow, direct stage invocation, unchanged-request manual fallback, contract-valid normal transitions, partial/stop states, invalidation loops, malformed results, package isolation, index-template coverage, and docs-only boundaries.
8. **Run full-suite transition checks.** Exercise all focused packages and reconcile current-status documentation only after local and live evaluation evidence is available.

## Ownership and request/result handoffs

Focused stages own their artifacts: discovery owns assessment/domain vision, strategic owns maps and contexts, tactical owns models, adoption owns `adoption-plan.md`, and review owns `review.md`. `ddd` coordinates state and owns the routing/index portions of `docs/ddd/README.md`; review retains stewardship of review status and findings. A manual fallback returns the exact unchanged request bundle. A normal transition consumes the exact result, preserves its paths, evidence, assumptions, open questions, validation, ownership, and stop/revisit conditions, then constructs the next request required by the transition contract. A stage result is consumed as returned, not simulated or rewritten. On invalidation, mark downstream artifacts stale and emit the earliest stage request.

## Evidence and safe-update invariants

- The orchestrator records and transports evidence; it does not establish target-project facts.
- Preserve claim types and provenance, including current/desired/required conflicts, across every transition.
- Never drop fields, normalize away claims, or alter artifact paths from a consumed result; only the manual fallback passes the request bundle unchanged.
- Inspect existing `docs/ddd/README.md` before additive updates; preserve all user-owned sections and links.
- Keep all changes within the agreed documentation boundary and never edit product/runtime files.
- A manual fallback must state the exact stage and unchanged bundle; it must not claim that activation or the next stage ran.
- Bounded partial/stop results must expose the reason, missing evidence/decision, owner, and next stage or caller.

## Evaluation scenario matrix

| Category | Observable scenario | Required result | Forbidden result |
| --- | --- | --- | --- |
| Normal flow | Complete evidence progresses through all needed stages | Emit one exact request per stage and final bounded summary | Perform focused-stage work in the orchestrator |
| Direct invocation | Valid tactical/adoption/review request starts at its stage | Preserve scope and enforce that stage entry criteria | Force discovery or invent prior artifacts |
| Manual fallback | Host cannot activate a named stage | Return the exact unchanged request bundle | Emulate the stage or claim transition ran |
| Normal transition | Focused stage returns a valid result bundle | Construct the next contract-valid request while preserving claims, provenance, and paths | Require byte-for-byte result/request identity or silently drop evidence |
| Missing evidence | Discovery/strategic/tactical prerequisite is absent | Bounded stop or earliest-stage handoff | Guess missing domain facts |
| Non-fit | Discovery reports `not-fit` | Stop with bounded result and simpler-path rationale | Continue every stage mechanically |
| Invalidation loop | Review or new evidence invalidates a later artifact | Mark later work stale and route to earliest affected stage | Restart at an arbitrary later stage |
| Malformed result | Focused stage returns incomplete/unknown result | Report bounded protocol error and stop | Repair or reinterpret stage behavior |
| Index ownership | `docs/ddd/README.md` exists with user prose | Update only owned routing/status sections; preserve review stewardship | Replace index or findings |
| Docs-only | Request includes source/deployment edit | Refuse outside scope | Edit product/runtime files |

## Observable acceptance criteria

- `SKILL.md` contains routing/state-only behavior, focused-stage entry gates, exact bundle schemas, manual fallback, invalidation loops, bounded partial/stop behavior, ownership, and non-goals.
- No orchestrator instruction duplicates focused-stage modeling, adoption, or review behavior.
- Manual fallback preserves the request bundle unchanged; normal transitions consume exact stage results and construct contract-valid next requests without dropping claims, provenance, or paths; malformed or missing results stop safely.
- Routing reaches the earliest invalidated stage and marks downstream artifacts stale without silent repair.
- `docs/ddd/README.md` ownership and `ddd-review` stewardship are explicit.
- The package is independently copyable; its package-local references, request/result asset, `ddd-readme-template.md`, and evals validate without relying on focused package internals, and the index template covers the canonical `docs/ddd/README.md` sections and ownership markers.
- Full-suite checks distinguish local static proof from deferred live host/model evaluation.

## Verification commands and gates

Run repository-local checks after implementation:

```text
python3 scripts/validate-skills.py
python3 -m json.tool skills/ddd/evals/evals.json
rtk git diff --check
```

Also run one-H1/rendered-local-link checks across all Markdown, standalone copies of all packages, exact request/result immutability probes, routing/invalidation semantic evaluations, forbidden runtime/vendor/machine-path probes, protected-scope preservation, whitespace, and exact candidate hashes. Apply the strategic prerequisite, incomplete-artifact, safe-boundary, and handoff-completeness gates from [quality-gates.md](../skill-design/quality-gates.md), then request independent review. Full-suite live evaluation remains conditional on an available host/model and must not be claimed otherwise.

## Risks and open decisions

- The host may expose activation differently or not at all; the unchanged manual fallback is mandatory.
- Bundle schemas may evolve as focused packages mature; version or reject incompatible results rather than guessing.
- Multiple invalidated artifacts may make the earliest route ambiguous; preserve evidence and request a bounded decision.
- Index ownership must avoid conflicts between orchestration status and review findings.
- Static checks cannot prove real host/model transition behavior; retain that residual risk.

## Non-goals

This phase does not implement any focused stage, create target-project model artifacts, edit product code, execute migration/deployment work, choose architecture topology, install optional validators, or claim live compatibility without evidence.
