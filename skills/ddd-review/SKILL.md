---
name: ddd-review
description: Review a bounded set of DDD discovery, strategic, tactical, and adoption artifacts for scoped documentation readiness. Use when checking evidence, lifecycle, vocabulary, boundaries, cross-artifact consistency, stale routing, and safe handoff without approving implementation or deployment.
---

# DDD documentation review

Review named DDD artifacts against their evidence and contracts. Produce one bounded review result and, when authorized and unambiguous, one additive review document. This skill is independently invocable: it accepts a complete or partial review request and reports findings without reconstructing missing facts.

## Purpose and boundaries

Use this skill to:

- establish an identifiable review scope, requested acceptance criteria, and artifact set;
- check DDD fit, evidence and provenance, lifecycle/schema, vocabulary, strategic-to-tactical prerequisites, adoption safety, and cross-artifact consistency;
- record observable findings with severity, evidence/provenance, owner, action, status, affected artifact, and earliest stage to revisit;
- preserve conflicts and stale dependents, routing to the earliest invalidated stage without silently repairing source artifacts;
- create or update only the review-owned `docs/ddd/review.md` artifact additively;
- return a portable result that distinguishes documentation readiness from implementation or deployment approval.

Do not invent absent artifacts or facts, rewrite disputed domain claims, take ownership from discovery/strategic/tactical/adoption, edit product code or runtime files, execute migrations, approve deployment, approve implementation, or infer that a bounded context is a service.

## Entry criteria and scope

Require:

- a named review scope and one review objective;
- requested artifacts and their exact target paths, including explicit missing or partial artifacts;
- acceptance criteria, permitted documentation paths, and artifact ownership context;
- available evidence, provenance, lifecycle/validation metadata, assumptions, open questions, and prior findings when supplied.

A partial or missing artifact set is valid review input but produces findings. An absent artifact is reported by exact path; its contents are never reconstructed. If the review scope is not identifiable, return a bounded stop naming the missing scope, owner, and evidence needed.

The only target-project artifact owned by this stage is `docs/ddd/review.md`. Resolve that exact path under `docs/ddd`, inspect it before writing, preserve user-authored prose and metadata, and make only additive updates to review-owned sections. Refuse source, test, configuration, schema, generated-output, deployment, migration, traversal, and unrelated-document changes. A mixed request may retain a safe review recommendation while explicitly refusing forbidden actions; it must not claim a write occurred unless an allowed update was actually made.

## Finding contract

Every finding is observable and complete. It contains:

- `severity`: `info`, `follow-up`, `blocked`, or `invalidated`;
- `evidence`: the observed statement, missing section, path, example, or gate result;
- `provenance`: source, owner, date, or an explicit statement that provenance is missing;
- `owner`: the accountable stage or project owner;
- `action`: the smallest next action or evidence request;
- `status`: `open`, `routed`, `accepted`, or `resolved`;
- `affected_artifact`: exact path or `none` for a scope-level finding;
- `earliest_stage`: `ddd-discover`, `ddd-strategic`, `ddd-tactical`, `ddd-adoption`, or `ddd-review`.

Do not use generic DDD guidance as target-project evidence. Classify substantive claims as current behavior, desired policy/meaning, required obligation, fact, interpretation, proposal, decision, or assumption. Keep current, desired, and required claims separate when they conflict.

## Ordered review gates

1. **Identify scope.** Confirm the objective, scope, requested artifacts, acceptance criteria, permitted paths, and review depth. Stop if scope cannot be named.
2. **Inventory artifacts.** Inspect each requested path and metadata. Report missing, partial, stale, superseded, archived, or out-of-scope artifacts; never fill gaps from filenames, code structure, or generic patterns.
3. **Check fit and evidence.** Verify the DDD-fit decision and simpler alternative where relevant. Check evidence authority, source, provenance, assumptions, open questions, and validation scope. An assumption is not a validated fact.
4. **Check lifecycle and schema.** Verify artifact status, validation, owner, scope, provenance, assumptions, open questions, last update, and minimum sections. Record exact missing or stale fields.
5. **Check vocabulary.** Compare terms by context, meaning, examples, owner, source, status, and translation. Same spelling is not same meaning. Preserve conflicts instead of merging them.
6. **Check strategic-to-tactical prerequisites.** Verify context identity, purpose, owner, boundary, language, relationship direction, tactical scope, commands/scenarios, invariants, consistency, and integration assumptions. Route missing or invalidated strategic facts to `ddd-strategic` or `ddd-discover` as the earliest owner.
7. **Check adoption safety.** When adoption is in scope, verify bounded slices, owners, dependencies, acceptance signals, compatibility, observability, data/integration/privacy risks, and rollback or containment. Unsafe or missing evidence is a finding, not an approval.
8. **Check cross-artifact consistency.** Compare claims and links across assessment, vision, language, maps, contexts, models, and adoption plan. Preserve conflicts; mark affected dependents `stale`; route to the earliest stage whose evidence or decision is invalidated. Do not silently repair either side.
9. **Write the owned review artifact.** If scope and section ownership are clear, create or update only `docs/ddd/review.md` additively with gate results, findings, stale/conflicting artifacts, owners/actions, next step, and chat-summary text. If placement or ownership is ambiguous, stop without writing.
10. **Return the result.** Emit status `ready`, `follow-up`, `blocked`, or `invalidated`, exact changed paths, findings, gate outcomes, stale routing, assumptions, open questions, and one next stage or bounded stop. `ready` means documentation is coherent for the stated scope only; it never approves implementation, deployment, migration, or release.

## Gate interpretation and stale routing

A gate is `pass`, `follow-up`, `blocked`, or `not-applicable`, with its question, evidence, owner, and revisit trigger. A review aggregates gate failures rather than erasing them. A fit `not-fit` result remains authoritative unless new evidence or explicit approval changes it.

Route to `ddd-discover` for missing fit, scope, current-system, or baseline evidence; to `ddd-strategic` for context purpose, ownership, language, relationship, or boundary conflicts; to `ddd-tactical` for missing commands, scenarios, invariants, model, or consistency decisions; and to `ddd-adoption` for sequencing, compatibility, observability, data reconciliation, or rollback/containment gaps. Route review-owned completeness issues to `ddd-review`.

When a source claim changes or a conflict affects assumptions, list every affected dependent artifact and mark it stale in the result. Preserve its path and provenance. Do not update another stage's artifact to make the review pass. A stale route is complete only when the earliest stage, owner, evidence request, affected artifacts, and revisit trigger are named.

## Documentation-ready result

A `ready` result requires identifiable scope, named artifacts, sufficient evidence and provenance, lifecycle/schema completeness, vocabulary and strategic-to-tactical coherence, adoption safety when applicable, no unresolved blocking cross-artifact conflict, and a complete review record. It may still contain bounded follow-ups if they do not invalidate the stated scope, but every follow-up has an owner and revisit trigger.

The result must state: `ready` is documentation readiness only. It does not authorize implementation, deployment, migration, data cutover, product-code edits, or a microservice split. If any required gate is blocked or the scope is unsafe, return `blocked`, `follow-up`, or `invalidated` instead.

## Portable transition result

Return a result bundle containing:

- `stage`: `ddd-review`;
- `status`: `ready`, `follow-up`, `blocked`, or `invalidated`;
- `scope`: named objective, domain/context/slice, review depth, and acceptance criteria;
- `artifacts`: exact requested, available, missing, stale, and affected paths;
- `gate_results`: fit, evidence/provenance, lifecycle/schema, vocabulary, strategic-to-tactical, adoption safety, and cross-artifact outcomes;
- `findings`: complete finding objects using the schema above;
- `stale_routing`: affected dependents, earliest stage, owner, action, evidence, and revisit trigger;
- `changed_artifacts`: exact paths and lifecycle/validation status, or an empty list when no write occurred;
- `assumptions`, `open_questions`, `next_step`, and `return_to`.

A complete result names the exact manual next stage when review is not ready, or states `ddd-review` as the return stage for review-owned follow-up. It never claims that implementation, deployment, migration, or live validation ran.

## References and evaluation

Read the [review method](references/review-method.md) and [review artifact contract](references/artifact-contracts.md) before writing. The review document template is in `assets/review-template.md`; package-local evaluation cases are in `evals/evals.json`.
