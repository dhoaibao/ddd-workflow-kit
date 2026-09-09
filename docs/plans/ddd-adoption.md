# Plan: implement `ddd-adoption`

## Current status

`ddd-adoption` is unimplemented. The design assigns it ownership of practical sequencing after a bounded, evidence-backed modeling slice. The existing `ddd-discover`, `ddd-strategic`, and `ddd-tactical` packages may provide inputs, but this plan does not alter them.

## Purpose and boundaries

The package turns validated domain insight into a greenfield or brownfield adoption plan. Its only first-release target-project artifact is `docs/ddd/adoption-plan.md`. It recommends incremental, reversible slices and records acceptance, ownership, dependencies, rollback/containment, and data/integration/privacy risks.

It must never execute a migration, edit product code, edit tests/configuration/deployment artifacts, choose a deployment topology without evidence, or treat every bounded context as a service. A recommendation is not execution.

## Prerequisites and inputs

Require a bounded outcome and evidence-backed next slice, plus the available artifacts and constraints relevant to that slice:

- discovery fit, current-system mode, vocabulary, assumptions, and open questions;
- strategic context purpose, owner, relationships, boundary questions, and validation status;
- tactical commands, scenarios, invariants, model decisions, integration/persistence assumptions, and risks;
- greenfield or brownfield mode, ownership, dependencies, delivery constraints, compatibility needs, and rollback/containment evidence;
- permitted documentation paths and existing `docs/ddd/` content.

If the prerequisites are missing, ambiguous, unsafe, or materially disputed, stop and return to discovery, strategic, or tactical design—the earliest stage that owns the gap.

## Proposed portable package

Create only after approval and implementation planning:

- `skills/ddd-adoption/SKILL.md` — portable instructions and entry/stop rules;
- `skills/ddd-adoption/references/adoption-method.md` — greenfield, brownfield, slicing, reversibility, and risk questions;
- `skills/ddd-adoption/references/artifact-contracts.md` — package-local handoff and `adoption-plan.md` contract;
- `skills/ddd-adoption/assets/adoption-plan-template.md` — documentation-only artifact template;
- `skills/ddd-adoption/evals/evals.json` — package-local scenario manifest.

The package must remain independently invocable, language/framework-neutral, and free of host-specific activation assumptions.

## Ordered implementation phases

1. **Define entry and stop behavior.** Accept validated stage bundles or bounded direct requests; distinguish greenfield, brownfield, and insufficient-evidence paths; route missing modeling prerequisites to the earliest owner.
2. **Define the adoption artifact.** Specify metadata, lifecycle/validation state, provenance, scope, ownership, and additive update rules for `docs/ddd/adoption-plan.md`.
3. **Define greenfield sequencing.** Plan the smallest learning/delivery slice, dependencies, acceptance signals, ownership, decision points, and reversible boundaries without prescribing implementation technology.
4. **Define brownfield sequencing.** Require current behavior, characterization evidence, seams, compatibility/translation, observability, ownership, data reconciliation, and rollback/containment before recommending a risky increment; reject big-bang rewrites.
5. **Define risk and decision handling.** Cover data, integration, privacy, operational, ownership, and dependency risks; mark optional architecture choices conditional; preserve unresolved decisions and claim-type conflicts.
6. **Define handoff and results.** Return one complete review request containing the plan path, selected slice, evidence, prerequisites, acceptance signals, dependencies, rollback/containment, open questions, and `return_to`; never claim review or execution ran.
7. **Add evaluations and validate.** Add package-local cases for greenfield, brownfield, missing rollback, missing owner, unsafe migration, conflicts, preservation, and docs-only refusal; validate package isolation and portable links before review.

## Ownership and handoffs

`ddd-adoption` owns `docs/ddd/adoption-plan.md`; it may consult all modeling artifacts and may contribute no strategic or tactical boundary rewrite. `ddd-review` owns `docs/ddd/review.md` and validates the plan. A result bundle must contain the exact changed path, lifecycle/validation status, evidence/provenance, assumptions, open questions, selected slice, dependencies, owners, acceptance signals, rollback/containment, and the exact next stage or bounded stop. If a migration constraint invalidates modeling assumptions, mark affected downstream artifacts stale and return to the earliest affected modeling stage.

## Evidence and safe-update invariants

- Separate current behavior, desired policy/meaning, required obligation, fact, interpretation, proposal, and assumption claims.
- Use behavior, tests, operations, and integration evidence for current-state claims; users/experts for intended meaning; contracts/regulations for obligations.
- Preserve conflicting claims with source, owner, scenario, impact, and validation state; never silently convert desired behavior into current behavior.
- Inspect existing artifacts, preserve user-authored content and metadata, update only owned sections, and ask or stop before destructive or ambiguous changes.
- Write only the owned documentation artifact under `docs/ddd/`; never edit product source or execute a migration.
- Do not call a step reversible when data, external contracts, ownership, or containment evidence makes rollback uncertain.

## Evaluation scenario matrix

| Category | Observable scenario | Required result | Forbidden result |
| --- | --- | --- | --- |
| Greenfield slice | Complex greenfield model has one bounded outcome | Thin ordered plan with owner, dependencies, acceptance, and rollback/containment | Architecture implementation or topology mandate |
| Brownfield baseline | Legacy seam has current behavior and characterization evidence | Incremental compatibility/translation plan | Big-bang rewrite assumption |
| Unsafe migration | Data/integration change lacks containment or rollback | Bounded stop or return with missing decision | Migration execution or false reversibility |
| Ownership gap | No accountable owner for a risky increment | Stop and identify owner decision | Invented owner |
| Claim conflict | Current behavior conflicts with desired policy or obligation | Separate claims and record impact | Silent resolution |
| Partial modeling | Strategic/tactical prerequisite is absent | Exact earliest-stage handoff | Invented model or plan |
| Existing artifact | User-authored adoption document exists | Preserve and update owned sections additively | Destructive replacement |
| Docs-only boundary | Request includes product-code or migration execution | Refuse those actions and retain documentation scope | Source edit or executed migration |
| Review handoff | Plan is complete and bounded | One complete `ddd-review` request | Claim review ran |

## Observable acceptance criteria

- `SKILL.md` states purpose, triggers, inputs, entry gates, greenfield/brownfield behavior, artifact ownership, stop conditions, handoff schema, and explicit non-goals.
- The only target-project artifact owned is `docs/ddd/adoption-plan.md`, with the required adoption sections and provenance/validation metadata.
- Every positive evaluation input includes sufficient bounded evidence; stop cases remain intentionally incomplete and have explicit expected/forbidden outcomes.
- Brownfield guidance requires characterization, compatibility, observability, ownership, data/integration/privacy review, and rollback/containment.
- Outputs contain no product-code edits, migration execution, invented facts, or silent conflict resolution.
- The package is independently copyable and its package-local references/assets/evals validate without other focused packages.

## Verification commands and gates

Run repository-local checks after implementation:

```text
python3 scripts/validate-skills.py
python3 -m json.tool skills/ddd-adoption/evals/evals.json
rtk git diff --check
```

Also run the repository Markdown check for one H1 and resolving rendered local links, package-copy/isolation checks, forbidden runtime/vendor/machine-path probes, semantic evaluation checks, foundation/design preservation checks, and an exact frozen hash/status snapshot. Apply the fit/scope, brownfield, incomplete-artifact, safe-boundary, and handoff-completeness gates from [quality-gates.md](../skill-design/quality-gates.md), then request independent review before reporting completion.

## Risks and open decisions

- The right first slice may depend on user priorities, delivery capacity, or evidence unavailable to the package; stop rather than optimize by guesswork.
- Brownfield rollback may be containment rather than reversal; the plan must state that distinction.
- Ownership of shared language and integration contracts may remain disputed; preserve the dispute and route it backward.
- The exact host activation mechanism is intentionally open; use the portable request/result bundle and manual fallback.

## Non-goals

This phase does not implement `ddd-adoption`, create a package, edit `docs/ddd/`, execute a migration, edit product code, choose frameworks/databases/deployment, implement `ddd-review`, or implement `ddd`.
