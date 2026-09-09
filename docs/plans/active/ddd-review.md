# Plan: implement `ddd-review`

## Current status

`ddd-review` is unimplemented. The design assigns it ownership of cross-artifact findings and `docs/ddd/review.md`; it validates documentation readiness but never silently repairs disputed facts or approves implementation.

## Purpose and boundaries

The package reviews requested DDD artifacts for fit, provenance, lifecycle/schema completeness, vocabulary, strategic-to-tactical prerequisites, adoption safety, and cross-artifact consistency. It records findings with severity, evidence, owner, action, and earliest stage to revisit. A `ready` result means documentation is coherent for its stated scope only.

It must not reconstruct missing artifacts, rewrite disputed domain facts, change strategic or tactical ownership, edit product code, approve deployment, or claim that implementation is ready.

## Prerequisites and inputs

Require identifiable review scope, requested acceptance criteria, and the available artifacts. Accept complete, partial, stale, conflicting, or missing artifact sets so review can report the exact gap:

- `assessment.md`, `domain-vision.md`, `ubiquitous-language.md`, strategic maps/context documents, tactical models, and `adoption-plan.md` when in scope;
- metadata, lifecycle/validation status, ownership, provenance, assumptions, open questions, and prior review results;
- evidence/source records and claim types; quality-gate outcomes and permitted documentation paths;
- the intended scope, current status, and any user-requested review depth.

If scope is not identifiable, stop with a bounded request. If an artifact is absent, report it; do not infer its contents.

## Proposed portable package

Create only after approval and implementation planning:

- `skills/ddd-review/SKILL.md` — portable review instructions and result contract;
- `skills/ddd-review/references/review-method.md` — gate application, finding classification, stale routing, and evidence rules;
- `skills/ddd-review/references/artifact-contracts.md` — package-local `review.md` and finding schema;
- `skills/ddd-review/assets/review-template.md` — documentation-only review artifact template;
- `skills/ddd-review/evals/evals.json` — package-local scenario manifest.

The package must be independently invocable and remain language/framework/host neutral.

## Ordered implementation phases

1. **Define review scope and entry gates.** Require named artifacts and intended scope; handle partial/missing inputs as findings rather than reconstructed facts.
2. **Define the finding schema.** Require severity, evidence/provenance, owner, action, status, affected artifact, and earliest stage to revisit; distinguish ready, follow-up, blocked, and invalidated results.
3. **Implement fit and evidence checks.** Check DDD fit, requested depth, claim type, source authority, provenance, assumptions, and unresolved questions.
4. **Implement modeling checks.** Check lifecycle/schema/ownership, vocabulary meanings and translations, strategic boundaries, relationship direction, tactical prerequisites, invariants, and cross-artifact consistency.
5. **Implement adoption-safety checks.** Check bounded slices, ownership, dependencies, acceptance signals, data/integration/privacy risks, reversibility, rollback/containment, and the product-code boundary.
6. **Implement stale routing.** When evidence or a conflict invalidates an artifact, preserve it as stale, identify dependents, and route to the earliest affected stage; never repair the disputed source silently.
7. **Write the review artifact and result.** Own `docs/ddd/review.md`, preserve existing content additively, include gate results and chat-summary text, and return exact paths plus the next stage or bounded stop.
8. **Add evaluations and validate.** Cover pass, follow-up, blocked, invalidated, missing-artifact, conflict, stale lifecycle, vocabulary, adoption safety, and docs-only cases before independent review.

## Ownership and handoffs

`ddd-review` owns `docs/ddd/review.md`; it validates every other artifact but does not take ownership of their content. Review findings must include severity, evidence/source, affected artifact, required owner, action, status, and earliest stage to revisit. A result bundle returns exact artifact paths, gate outcomes, stale/conflict notices, assumptions, open questions, and the next stage or bounded stop. If an adoption risk invalidates a model, route to adoption or the earliest modeling stage as evidence dictates. If a strategic claim changes tactical assumptions, mark downstream work stale and route backward.

## Evidence and safe-update invariants

- Every substantive claim is sourced or explicitly labeled as fact, current behavior, desired policy/meaning, required obligation, interpretation, proposal, or assumption.
- Apply source authority by claim type and preserve current/desired/required conflicts separately.
- Findings cite observable evidence and do not use generic DDD guidance as target-project fact.
- Inspect target paths first; preserve user-authored prose, metadata, links, lifecycle history, and ownership; update only review-owned sections additively.
- Mark affected artifacts `stale` rather than silently rewriting or deleting them.
- Keep review documentation under `docs/ddd/review.md`; no product-code, tests, configuration, generated-output, schema, or deployment changes.
- `ready` is scoped documentation readiness, not approval of implementation, deployment, migration, or a microservice split.

## Evaluation scenario matrix

| Category | Observable scenario | Required result | Forbidden result |
| --- | --- | --- | --- |
| Fit | Assessment says simple CRUD is sufficient | Record non-fit/follow-up with evidence and no forced modeling | Force contexts or patterns |
| Provenance | Claim lacks source or is labeled assumption | Finding identifies provenance gap and owner | Mark fact validated |
| Lifecycle/schema | Artifact has missing metadata or stale status | Exact missing/stale finding and owner action | Reconstruct or silently validate |
| Vocabulary | Same term has context-specific meanings | Preserve meanings and translation/conflict finding | Merge by spelling |
| Strategic→tactical | Model lacks validated context or boundary | Route to earliest strategic/discovery stage | Approve tactical readiness |
| Adoption safety | Plan lacks owner, acceptance, or rollback/containment | Block/follow up with evidence and action | Approve unsafe increment |
| Cross-artifact | Context map, model, language, or plan conflicts | Preserve conflict, mark dependents stale, route backward | Silent repair |
| Missing artifact | Requested artifact does not exist | Report exact missing path | Invent contents |
| Ready | Artifacts pass scoped gates | Write documentation-readiness result and next step | Claim implementation approval |
| Docs-only | Request asks for source or deployment edits | Refuse outside boundary | Edit product/runtime files |

## Observable acceptance criteria

- `SKILL.md` checks fit, provenance, lifecycle/schema, vocabulary, strategic-to-tactical prerequisites, adoption safety, cross-artifact consistency, and safe-update boundaries.
- `review.md` contains scope/date, artifact and validation summary, fit result, gate results, findings by severity, stale/conflicting artifacts, owner/action, earliest stage, next step, and chat-summary text.
- Every finding contains severity, evidence, owner, action, affected artifact, and earliest-stage routing; unresolved conflicts are not silently repaired.
- `ready` is explicitly documentation readiness only.
- Positive evaluations include complete review scope and evidence; stop/blocked cases are explicit and observable.
- The package is independently copyable and its package-local assets/references/evals validate without other focused packages.

## Verification commands and gates

Run repository-local checks after implementation:

```text
python3 scripts/validate-skills.py
python3 -m json.tool skills/ddd-review/evals/evals.json
rtk git diff --check
```

Also run one-H1/rendered-local-link checks, package isolation, semantic finding-schema and stale-routing probes, forbidden runtime/vendor/machine-path checks, protected-scope preservation, whitespace, and exact snapshot hashing. Apply the fit/scope, conflicting-vocabulary, expert-availability, strategic-prerequisite, incomplete-artifact, safe-boundary, and handoff-completeness gates from [quality-gates.md](../../skill-design/quality-gates.md), then request independent review.

## Risks and open decisions

- Review quality depends on the supplied evidence and cannot replace domain-expert validation.
- Finding severity and earliest-stage routing may require a user decision when ownership or impact is disputed.
- Existing review documents may have user-owned sections; additive ownership must be explicit.
- Host activation is intentionally unresolved; use the portable bundle and exact manual fallback.

## Non-goals

This phase does not implement `ddd-review`, create a package, edit target-project artifacts, repair disputed facts, implement adoption or orchestration, approve product changes, or claim live host/model validation.
