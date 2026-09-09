---
name: ddd-tactical
description: Model one evidence-backed bounded context with tactical DDD patterns, invariants, consistency, and integration assumptions from a validated strategic handoff. Use when one selected context is ready for tactical design before adoption planning.
---

# DDD tactical design

Turn one validated bounded-context slice into an explicit tactical model without turning generic DDD patterns into a checklist. This skill is standalone: it accepts a portable `ddd-strategic` handoff or an independently invoked tactical request and returns one model document plus a portable transition result.

## Purpose and boundaries

Use this skill to:

- start from commands, use cases, preconditions, outcomes, failures, and counterexamples;
- name invariants and distinguish immediate from eventual consistency before choosing patterns;
- model entities, value objects, aggregates and roots, repositories, services, specifications, factories, and past-tense domain events only when evidence requires them;
- document transaction, concurrency, integration, persistence, delivery, ordering, duplication, idempotency, retry, recovery, and privacy assumptions;
- produce one context model under `docs/ddd/models/` and additive tactical contributions to the selected context and language documents.

Do not invent domain facts or infer a model from modules, tables, schemas, existing classes, teams, or deployment topology alone. Do not create framework-specific classes, code, schemas, APIs, databases, ORM mappings, tests, configuration, generated output, or deployment changes. Tactical design is a modeling document, not implementation approval.

## Inputs and entry criteria

Accept either:

- a portable `ddd-strategic` result/request bundle with exactly one selected context; or
- an independently invoked tactical request with equivalent evidence and prerequisites.

Require all of the following before modeling:

- exactly one context identity and its already validated safe slug and permitted model path;
- purpose/outcome, context-specific vocabulary, concrete scenarios or commands, decision owner, relationships, assumptions, open questions, and candidate invariants;
- evidence and provenance sufficient to distinguish current behavior, desired policy/meaning, required obligation, proposal, interpretation, and assumption;
- explicit allowed paths and artifact ownership.

If prerequisites are missing, return the exact `ddd-strategic` handoff or a bounded stop. If more than one context is present, require an evidence-backed or user-prioritized selection and do not model all contexts. Never infer the selected context from modules, tables, schemas, or filenames.

Reuse the validated strategic slug exactly for `docs/ddd/models/<context-slug>.md`. Resolve the candidate and verify that its parent is exactly `docs/ddd/models`; preserve an existing owned model additively; ask before ambiguity, collision, structural, destructive, or ownership changes. When a request mixes a safe, explicitly owned additive documentation update with forbidden or out-of-scope paths, isolate and complete the safe subset, refuse only the forbidden paths, and report both outcomes. Stop the whole request only when the safe subset is materially ambiguous or cannot be isolated. Do not normalize a new slug in this stage.

## Evidence discipline

Classify each statement as current behavior, desired policy or meaning, required obligation, fact, interpretation, proposal, or assumption. Use users and domain experts for meaning and policy, behavior/tests/operations for current behavior, and explicit contracts or regulations for obligations. Every invariant and tactical decision needs named evidence, a scenario, or an explicitly recorded unresolved question.

A pattern is never evidence. Keep unsupported model elements `proposed`, `unvalidated`, or `deferred`. Preserve conflicting claims and report their impact. If tactical evidence challenges the strategic boundary, language, ownership, or relationship, do not silently repair the strategic model: preserve the conflict, mark the model and affected downstream work stale, include `invalidated_stages`, and return the exact `ddd-strategic` request.

## Ordered workflow

1. **Validate the handoff.** Check the single selected context, reused slug/path, outcome, vocabulary, scenarios, relationships, decision owner, evidence, assumptions, open questions, candidate invariants, allowed paths, and `return_to`.
2. **Check selection and conflicts.** Stop for multiple contexts or an unsupported selection. Preserve strategic conflicts and return to `ddd-strategic` when the boundary, language, ownership, or relationship no longer fits.
3. **Describe behavior first.** For each command or use case, record actor, preconditions, inputs, decisions, successful outcome, failures, counterexamples, observable acceptance signals, and affected relationships.
4. **Name invariants.** State each invariant, its evidence, scope, owner, failure consequence, and validation state. Mark whether consistency must be immediate or may be eventual, and explain why.
5. **Choose model elements.** Select an entity for identity and continuity; a value object for value equality and validation; and an aggregate/root only as the smallest boundary protecting a named immediate invariant. The root is the external access point. Record in/out boundaries, references, transaction and concurrency assumptions, and unresolved alternatives.
6. **Define contracts.** Add repositories only for required aggregate roots, with domain-facing intent, lookup/save behavior, failure semantics, and concurrency assumptions rather than persistence implementation. Distinguish domain services from application orchestration; use specifications or factories only for a named need, and explain why a simpler rule or constructor is insufficient.
7. **Describe events and flows.** Model past-tense domain events as facts, not commands. Record application flow, event delivery, ordering, duplication, idempotency, retry, recovery, privacy, and cross-aggregate effects. Make immediate versus eventual consistency explicit; if an invariant truly spans proposed aggregates with immediate consistency, revisit or merge the boundary instead of assuming a multi-aggregate transaction or event workaround.
8. **Evaluate optional patterns.** Treat CQRS and event sourcing as independent decisions with status `not-needed`, `deferred`, or `proposed`. Record evidence, full operational and conceptual costs, and a simpler alternative. Ordinary domain events do not imply event sourcing.
9. **Write owned artifacts.** Create `docs/ddd/models/<context-slug>.md` from the context-model template or make additive updates to owned sections of `docs/ddd/contexts/<slug>.md` and `docs/ddd/ubiquitous-language.md` only when evidence requires them. Preserve existing content and ownership. Refuse requests to edit product code or unrelated files.
10. **Prepare adoption handoff.** When one bounded model is sufficiently explicit, return exactly one `ddd-adoption` request with model path, context, commands/scenarios, invariants, decisions, integration and persistence assumptions, risks, evidence, validation, owners, allowed paths, open questions, acceptance signals to define, and `return_to`. A host without named-stage activation returns the exact manual stage name `ddd-adoption` and the unchanged request bundle; it must not claim that adoption ran.
11. **Summarize.** Return changed paths, behavior, invariants, model-element decisions, consistency and integration assumptions, optional-pattern decisions, risks, validation state, invalidations, open questions, and the exact next action.

## Owned outputs

The first release may create or update only:

- `docs/ddd/models/<validated-context-slug>.md` using [the context-model template](assets/context-model-template.md);
- additive tactical sections in the selected `docs/ddd/contexts/<slug>.md`;
- additive tactical term entries or conflict/translation notes in `docs/ddd/ubiquitous-language.md`.

Do not alter `docs/ddd/domain-map.md`, `docs/ddd/context-map.md`, strategic boundaries, or product files. Use the shared tactical subset in [the artifact contract](references/artifact-contracts.md). The output is repository documentation plus a chat summary, not implementation approval.

## Portable transition result

Return a result bundle containing:

- `stage`: `ddd-tactical`;
- `status`: `complete`, `partial`, `blocked`, or `strategic-conflict`;
- `scope`: exactly one context, capability, and selected slice;
- `changed_artifacts`: exact paths, lifecycle status, and validation status;
- `evidence`: claim type, source, owner, scenario, and observation or statement;
- `commands`, `scenarios`, `invariants`, `model_elements`, `consistency`, `integration`, `persistence`, and optional-pattern decisions;
- `assumptions`, `risks`, and `open_questions`;
- `invalidated_stages`: affected downstream stages or `strategic` when the boundary is challenged;
- `handoff`: one `ddd-adoption` request or a bounded stop/strategic fallback.

A successful `ddd-adoption` request must contain exactly one model path and context, commands/scenarios, invariants, decisions, integration and persistence assumptions, risks, evidence, validation, owners, allowed paths, open questions, acceptance signals to define, and `return_to`. It must not include a second context or claim that adoption ran.

## Completion and stop conditions

Complete only when one context, its behavior, invariants, tactical decisions, consistency assumptions, evidence, ownership, and validation state are explicit and one adoption handoff or bounded result is ready. Stop with `partial` or `blocked` for missing prerequisites, weak evidence, unsafe paths, collisions, unresolved ownership, or material decisions. Stop with `strategic-conflict` when tactical evidence challenges the strategic boundary or language and no explicit strategic resolution exists.

Never use aggregate, repository, service, event, CQRS, or event-sourcing labels without a named need. Never silently choose immediate consistency, persistence behavior, deployment topology, or a framework. Never edit product source, tests, schemas, configuration, generated output, or deployment files.

## References and evaluation

Read the [tactical method](references/tactical-method.md) and [tactical artifact contract](references/artifact-contracts.md) before writing. The model template is in `assets/`; package-local evaluation cases are in `evals/evals.json`.
