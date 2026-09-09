---
name: ddd-discover
description: Assess whether Domain-Driven Design fits a project and capture evidence-backed domain discovery artifacts. Use when a project needs scope, domain vocabulary, complexity assessment, greenfield discovery, or a brownfield baseline before strategic modeling.
---

# DDD discovery

Establish a bounded evidence base for deciding whether and how to use Domain-Driven Design. This skill is standalone: it may be invoked directly, or its portable transition result may be handed to a later strategic stage.

## Purpose and boundaries

Use this skill to:

- establish the requested project or capability scope and evidence boundary;
- assess DDD fit as `fit`, `limited-fit`, or `not-fit`;
- capture outcomes, actors, terms, examples, events, policies, constraints, and open questions;
- distinguish current behavior, desired policy or meaning, and required obligations;
- create or update only the discovery-owned documents under `docs/ddd/`;
- return a portable result and, when appropriate, a request for `ddd-strategic`.

Do not perform strategic context mapping, tactical modeling, migration execution, service decomposition, or product-code changes. A bounded context is not assumed to be a deployable service. DDD fit is assessed rather than presumed.

## Inputs and entry criteria

Accept:

- a user goal and the project or capability in scope;
- available domain-expert statements, examples, contracts, documentation, tests, current behavior, integrations, and operational evidence;
- greenfield, brownfield, or mixed mode when known;
- existing `docs/ddd/assessment.md`, `domain-vision.md`, and `ubiquitous-language.md` when present;
- constraints on access, ownership, privacy, and allowed documentation paths.

Begin only when the target scope and permitted evidence boundary are clear. Ask a material user question before reading or changing an ambiguous area. If an existing artifact is user-authored, preserve it and request explicit approval before destructive, ambiguous, or structural changes.

## Evidence discipline

Classify every substantive claim as one of:

- **Current behavior:** what the existing system, tests, integrations, or operations demonstrate.
- **Desired policy or meaning:** what users or domain experts say should happen or what a term means.
- **Required obligation:** what a contract, regulation, security requirement, or explicit constraint requires.
- **Interpretation:** a reasoned reading of evidence.
- **Proposal:** a working model or next step.
- **Assumption:** something needed to proceed but not yet supported.

Use the source appropriate to the claim. Do not let a desired policy overwrite observed legacy behavior, or let legacy behavior silently define desired policy. Preserve disagreements as separate claims with source, owner, impact, and open decision. Generic DDD guidance can suggest questions but cannot establish project facts.

## Ordered workflow

1. **Frame scope.** Record the requested outcome, in-scope capability, users or stakeholders, constraints, evidence boundary, mode, and desired depth.
2. **Check fit signals.** Look for meaningful domain rules, ambiguous language, competing policies, strategic differentiation, change risk, integration complexity, or costly mistakes. Record signals that favor a simpler approach too.
3. **Gather discovery evidence.** Capture actors, outcomes, commands or decisions, examples, events, policies, constraints, terminology, dependencies, ownership, and unresolved questions. Prefer concrete examples over general adjectives.
4. **Handle brownfield evidence.** Record observed behavior, tests, seams, dependencies, ownership, and failure modes. Treat code structure as evidence of current implementation, not proof of domain boundaries or desired policy.
5. **Classify fit.** Choose `fit`, `limited-fit`, or `not-fit` with evidence and a simpler alternative when appropriate. `limited-fit` may recommend DDD for one capability while keeping another area simpler.
6. **Prepare owned artifacts.** Create missing documents from the templates, or make additive updates only to discovery-owned sections. Preserve existing prose, metadata, links, and provenance. Mark uncertain or affected artifacts with the appropriate lifecycle and validation status.
7. **Check the handoff.** If strategic work is justified and the terms and scope are sufficient, prepare a transition request for `ddd-strategic`. Otherwise return a bounded stop with the missing evidence, decision, or next question.
8. **Summarize.** Return changed paths, fit result, evidence summary, assumptions, open questions, validation state, and the exact next action in the chat summary.

## Owned outputs

The first release may create or update only:

- `docs/ddd/assessment.md` using [the assessment template](assets/assessment-template.md);
- `docs/ddd/domain-vision.md` using [the domain-vision template](assets/domain-vision-template.md);
- `docs/ddd/ubiquitous-language.md` using [the language template](assets/ubiquitous-language-template.md).

Use the shared metadata and lifecycle rules in [the artifact contract](references/artifact-contracts.md). The output is repository documentation plus a chat summary. It is not implementation approval.

## Portable transition result

Return a result bundle with these fields:

- `stage`: `ddd-discover`;
- `status`: `complete`, `partial`, `blocked`, or `not-fit`;
- `scope`: project, capability, and mode;
- `changed_artifacts`: exact paths, lifecycle status, and validation status;
- `evidence`: claim type, source, owner, and relevant observation or statement;
- `assumptions`: explicit assumptions;
- `open_questions`: unresolved decisions or missing evidence;
- `fit`: `fit`, `limited-fit`, or `not-fit` with rationale;
- `handoff`: either a `ddd-strategic` request or a bounded-stop explanation;
- `invalidated_stages`: later stages to treat as stale, if any.

A `ddd-strategic` request contains the exact stage name, one objective, scope, artifact bundle, evidence bundle, assumptions, open questions, allowed paths, and `return_to`. A host that cannot activate the next stage must return the exact manual stage name `ddd-strategic` and the unchanged request bundle. Never claim that an unavailable stage ran.

## Completion and stop conditions

Complete when the scope, DDD-fit result, evidence, owned artifacts, validation state, and next step are explicit. Stop with `partial` or `blocked` when a material user question, missing evidence, inaccessible expert, conflicting claim, unsafe file update, or out-of-scope request prevents a reliable result. Stop with `not-fit` when a simpler approach is better supported.

Never invent domain facts, silently resolve conflicting vocabulary, mark an unvalidated artifact as validated, or update product source, tests, configuration, generated output, or deployment files.

## References and evaluation

Read the [discovery method](references/discovery-method.md) for workshop-neutral prompts and the [artifact contract](references/artifact-contracts.md) before writing. The templates in `assets/` are the minimum useful schemas. Evaluation cases are in `evals/evals.json`.
