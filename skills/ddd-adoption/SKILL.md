---
name: ddd-adoption
description: Turn validated DDD discovery, strategic, and tactical evidence into an incremental greenfield or brownfield adoption plan. Use when sequencing a bounded next slice, protecting a legacy seam, planning compatibility, or preparing a review handoff without executing migrations or editing product code.
---

# DDD adoption planning

Turn a bounded, evidence-backed domain slice into a practical adoption plan. This skill is standalone: it accepts a portable tactical handoff or a complete bounded direct request and returns one documentation-only plan plus a portable result for `ddd-review`.

## Purpose and boundaries

Use this skill to:

- choose a thin greenfield learning/delivery slice or a contained brownfield increment;
- sequence reversible documentation, boundary-protection, characterization, compatibility, data, observability, and delivery decisions;
- make dependencies, owners, acceptance signals, risks, decision points, and rollback or containment explicit;
- preserve current, desired, and required claims separately when they conflict;
- create or update only the adoption-owned `docs/ddd/adoption-plan.md` artifact;
- return exactly one complete `ddd-review` request when the plan is bounded and qualified.

Do not execute a migration, edit product source, tests, configuration, schemas, generated output, deployment files, or runtime behavior. Do not mandate a framework, database, deployment topology, or microservice split. A recommendation is not execution, and a bounded context is not automatically a service.

## Inputs and entry criteria

Accept either:

- a portable `ddd-tactical` result/request bundle; or
- an independently invoked adoption request with equivalent evidence and constraints.

Require a bounded outcome and evidence-backed next slice. A complete entry bundle identifies:

- mode: `greenfield` or `brownfield`;
- target outcome and one first slice;
- discovery fit, strategic context, tactical model decisions, or an explicit bounded direct request;
- evidence and provenance, assumptions, open questions, owners, dependencies, and delivery constraints;
- permitted documentation paths, artifact ownership, and `return_to`.

For brownfield work also require current behavior, a baseline, a seam, characterization evidence, compatibility or translation assumptions, observability, data reconciliation, ownership, and rollback or containment evidence. Missing or disputed prerequisites are not filled by inference.

If a gap belongs to discovery fit, scope, or current-system evidence, return the exact `ddd-discover` handoff. If it belongs to context ownership, vocabulary, or boundary relationships, return `ddd-strategic`. If it belongs to commands, invariants, model decisions, or tactical evidence, return `ddd-tactical`. Choose the earliest stage that owns the gap.

## Evidence discipline

Classify every substantive claim as current behavior, desired policy or meaning, required obligation, fact, interpretation, proposal, or assumption. Use behavior, tests, operations, and integration evidence for current state; users and domain experts for intended meaning; and explicit contracts, regulations, or security/privacy constraints for obligations.

Preserve conflicting claims with source, owner, scenario, impact, and validation state. A desired policy must not overwrite a legacy observation, and a current implementation must not silently define the desired model. Record the decision needed and the artifact or increment affected. Generic adoption advice can suggest questions but cannot establish target-project facts.

## Ordered workflow

1. **Validate entry.** Check the mode, bounded outcome, first slice, evidence, model prerequisites, owners, dependencies, allowed paths, and `return_to`. Reject incomplete or ambiguous input with the earliest-owner handoff.
2. **Select the owned artifact.** Use exactly `docs/ddd/adoption-plan.md`. Inspect whether it exists, preserve its metadata and prose, and update only adoption-owned sections additively. Ask or stop before collision, destructive, structural, or unclear ownership changes.
3. **Frame the outcome and slice.** State the target outcome, in/out scope, mode, first learning/delivery slice, evidence, assumptions, and the condition that would invalidate the plan. Do not plan the whole domain when one slice is enough.
4. **Sequence greenfield work.** Order the smallest useful learning, boundary, model, implementation-readiness, and verification increments. Each increment names an owner, dependency, decision point, observable acceptance signal, and rollback or containment assumption. Keep implementation as a future recommendation.
5. **Sequence brownfield work.** Require and record the current baseline, characterization evidence, seam, compatibility/translation boundary, ownership, observability, data reconciliation, privacy/integration constraints, and rollback or containment. Prefer one route, rule, or capability at a time. Reject big-bang rewrites and do not call an increment reversible when data, external contracts, or ownership make that uncertain.
6. **Handle risks and decisions.** Record data, integration, privacy, operational, ownership, dependency, and delivery risks. Keep optional architecture choices conditional with evidence, costs, and a simpler alternative. Preserve claim-type conflicts and mark affected downstream assumptions stale when adoption constraints invalidate modeling.
7. **Prepare the result.** If the plan is complete and bounded, emit exactly one `ddd-review` request containing the plan path, selected slice, evidence, prerequisites, acceptance signals, dependencies, owners, rollback/containment, open questions, allowed paths, and `return_to`. Otherwise return one bounded stop or earliest-stage handoff. Never claim review or execution ran.

## Greenfield rules

A greenfield plan should identify one valuable, high-learning outcome rather than a platform or complete domain rewrite. Sequence discovery clarification, boundary protection, tactical decision confirmation, the smallest implementation-ready increment, and observable verification only as recommendations. Keep unresolved language, ownership, privacy, and contract questions visible. Do not choose a deployment topology because a context exists.

## Brownfield rules

A brownfield plan must identify:

- observed baseline behavior and known failure modes;
- a seam or boundary that can be protected;
- characterization evidence or the explicit step that creates it before behavior changes;
- compatibility, translation, or anti-corruption assumptions;
- accountable owners for the legacy and target sides;
- observability and acceptance signals that detect regressions;
- data ownership, reconciliation, privacy, and integration constraints;
- rollback, recovery, or containment with its limits and trigger.

If any risky increment lacks an owner, characterization, compatibility, observability, data reconciliation, or rollback/containment decision, stop and name the missing decision. Never propose a big-bang migration, claim a data cutover is reversible without evidence, or execute the change.

## Safe documentation boundary

The only target-project artifact owned here is `docs/ddd/adoption-plan.md`. Resolve that exact path under `docs/ddd` before writing. Preserve existing content, metadata, links, provenance, and ownership. Refuse product-code edits, migration execution, tests, configuration, schemas, generated files, deployment changes, path traversal, and unrelated documentation. A mixed request may retain a safe documentation recommendation in the result while explicitly refusing the forbidden action; it must not claim that the safe artifact was changed unless an allowed update was actually authorized and unambiguous.

## Portable transition result

Return a result bundle containing:

- `stage`: `ddd-adoption`;
- `status`: `complete`, `partial`, `blocked`, or an explicit earliest-stage conflict result;
- `scope`: mode, target outcome, and one selected slice;
- `changed_artifacts`: exact paths with lifecycle and validation status, or an empty list when no write occurred;
- `evidence`: claim type, source, owner, scenario, impact, and validation;
- `assumptions`, `risks`, `dependencies`, `owners`, `acceptance_signals`, and `open_questions`;
- `plan`: increments, decision points, data/integration/privacy notes, and rollback/containment;
- `handoff`: exactly one `ddd-review` request or one bounded stop/earliest-stage request;
- `invalidated_stages`: affected stages when new adoption constraints invalidate modeling assumptions.

A successful `ddd-review` request contains exactly one plan path, selected mode and slice, prerequisites, evidence, dependencies, owners, acceptance signals, risks, rollback/containment, open questions, allowed paths, and `return_to`. A host without named-stage activation returns the exact manual stage name `ddd-review` and the unchanged request bundle; it must not claim that review ran.

## Completion and stop conditions

Complete only when one bounded adoption sequence is explicit, evidence and provenance are qualified, ownership and acceptance are named, and rollback/containment is credible for the stated scope. Stop with `partial` or `blocked` for missing evidence, unsafe migration, missing owner, absent rollback/containment, unresolved material claim conflict, ambiguous artifact ownership, or forbidden paths. Route modeling gaps backward to their earliest owner.

Never invent current behavior, silently resolve claim conflicts, call a recommendation execution, mark an unvalidated plan active without evidence, or edit product source, tests, configuration, generated output, schemas, or deployment files.

## References and evaluation

Read the [adoption method](references/adoption-method.md) and [adoption artifact contract](references/artifact-contracts.md) before writing. The target-project plan template is in `assets/adoption-plan-template.md`; package-local evaluation cases are in `evals/evals.json`.
