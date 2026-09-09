---
name: ddd-strategic
description: Define evidence-backed subdomains, bounded contexts, ubiquitous language, and context relationships from a DDD discovery result or a focused strategic request. Use when domain boundaries and model relationships need to be explored before tactical design.
---

# DDD strategic design

Turn discovery evidence into explicit strategic boundaries without treating deployment topology as domain truth. This skill is standalone: it accepts a portable discovery result or an independently invocable strategic request and returns strategic repository documents plus a portable transition result.

## Purpose and boundaries

Use this skill to:

- classify candidate subdomains as core, supporting, generic, or unresolved hypotheses;
- define bounded contexts around coherent models, language, and decision ownership;
- preserve overloaded terms by context instead of forcing one shared meaning;
- document directional context relationships, ownership, communication, translation, consistency, failure assumptions, evidence, and uncertainty;
- validate boundary hypotheses against scenarios, lifecycle/change, consistency, ownership, security, and availability evidence;
- create or update only strategic-owned documents under `docs/ddd/`.

Do not design entities, value objects, aggregates, repositories, services, schemas, or infrastructure. Do not infer contexts from modules or tables, choose services/databases/teams, or assume microservices. A bounded context is a model and language boundary; a deployment choice requires separate evidence.

## Inputs and entry criteria

Accept either:

- a portable `ddd-discover` result/request bundle; or
- an independently invocable strategic request with its objective, scope, evidence, artifacts, assumptions, open questions, allowed paths, and `return_to`.

Proceed only when all of these hold:

- the discovery result is `fit` or `limited-fit`, or the user made an explicit bounded strategic request;
- one meaningful outcome or capability is in scope;
- vocabulary and evidence are adequate to propose boundaries;
- the allowed documentation path and ownership are clear.

If a discovery result says `not-fit`, do not silently override it. Preserve the result and conflict, then request new evidence or an explicit decision before strategic modeling. If scope, vocabulary, or evidence is weak, return the exact `ddd-discover` handoff or a bounded stop.

## Evidence discipline

Classify claims as current behavior, desired policy or meaning, required obligation, interpretation, proposal, or assumption. Use domain experts and users for intended meaning, behavior/tests/operations for current behavior, and explicit contracts or regulations for obligations. Preserve disagreements as separate claims with source, owner, impact, and validation status.

A strategic hypothesis is not a fact. Subdomain classification, context boundaries, relationship labels, and ownership remain `proposed` or `unvalidated` until named evidence and scenarios support them. Generic DDD guidance can suggest questions but cannot establish project facts.

## Ordered workflow

1. **Validate the request.** Check fit result or explicit bounded request, meaningful outcome, vocabulary, evidence bundle, assumptions, open questions, allowed paths, and ownership. Reject missing prerequisites without guessing.
2. **Check non-fit conflicts.** If discovery says `not-fit`, preserve that artifact and return a bounded decision request; continue only with explicit user direction or new evidence.
3. **Classify subdomains.** Identify candidate capabilities and classify each as core, supporting, generic, or unresolved. Record rationale, evidence, owner, status, and revisit signal. Do not force a classification.
4. **Reconcile language.** Preserve context-specific meanings for overloaded terms. Update only strategic-owned language sections and record translation or conflict notes.
5. **Propose contexts.** Define boundaries around coherent models, language, lifecycle, and decision ownership. Record what is in/out, stakeholders, constraints, and why the boundary is useful.
6. **Map relationships.** For each relationship record direction, upstream/downstream ownership, communication or contract, translation, consistency and failure assumptions, evidence, and uncertainty. Relationship labels are optional descriptions, not a mechanical catalog.
7. **Challenge hypotheses.** Test boundaries against concrete scenarios, change and lifecycle, consistency, ownership, security, and availability evidence. Mark unsupported proposals unresolved.
8. **Write owned artifacts.** Create missing documents from the templates or make additive updates to strategic-owned sections. Preserve existing content and ownership. Derive context filenames with the safe-slug rule below; ask before destructive, ambiguous, structural changes, or filename collisions.
9. **Mark downstream impact.** If a strategic change affects tactical or adoption assumptions, include `tactical` and/or `adoption` in `invalidated_stages` and mark affected artifacts stale without silently rewriting them.
10. **Prepare the next step.** Identify the contexts that are sufficiently validated. If none is ready, return a bounded stop with the missing evidence. If one is ready, select it. If several are ready, use the explicit objective, user priority, and evidence to select exactly one; when that choice is material or unsupported, return a bounded decision request and ask the user rather than guessing. Once one context is selected, emit a `ddd-tactical` request for that context only; never emit a multi-context tactical bundle.
11. **Summarize.** Return changed paths, classifications, boundary and relationship rationale, assumptions, open questions, validation state, invalidations, and the exact next action.

## Owned outputs

The first release may create or update only:

- `docs/ddd/domain-map.md` using [the domain-map template](assets/domain-map-template.md);
- `docs/ddd/context-map.md` using [the context-map template](assets/context-map-template.md);
- `docs/ddd/contexts/<safe-slug>.md` using [the context template](assets/context-template.md);
- strategic sections of `docs/ddd/domain-vision.md`;
- strategic sections of `docs/ddd/ubiquitous-language.md`.

Use the shared strategic subset in [the artifact contract](references/artifact-contracts.md). For a context filename, lowercase an ASCII label, replace each run of non-alphanumeric separators with one hyphen, trim hyphens, and require only lowercase ASCII letters, digits, and single hyphens. Reject or ask when the label contains non-ASCII input, normalization is empty or ambiguous, the slug collides with another context label, or the target already exists. Before writing, resolve `docs/ddd/contexts/<safe-slug>.md` and verify its parent is exactly `docs/ddd/contexts`; never follow a path that escapes that directory. The output is repository documentation plus a chat summary, not implementation approval.

## Portable transition result

Return a result bundle containing:

- `stage`: `ddd-strategic`;
- `status`: `complete`, `partial`, `blocked`, or `not-fit-conflict`;
- `scope`: project, capability, and selected context scope;
- `changed_artifacts`: exact paths, lifecycle status, and validation status;
- `evidence`: claim type, source, owner, scenario, and relevant observation or statement;
- `assumptions` and `open_questions`;
- `subdomains`: classifications with rationale and status;
- `contexts`: boundaries, ownership, language, relationships, and uncertainty;
- `invalidated_stages`: affected downstream stages, if any;
- `handoff`: one `ddd-tactical` request or a bounded-stop explanation.

A `ddd-tactical` request must select exactly one sufficiently validated context and include its purpose, vocabulary, concrete scenarios, invariants to investigate, relationships, ownership, assumptions, open questions, allowed paths, and `return_to`. When multiple contexts are ready, the selection must follow the explicit objective, user priority, and evidence; if those do not support a material choice, return a decision request instead of selecting silently. A host without named-stage activation returns the exact manual stage name `ddd-tactical` and the unchanged request bundle. It must not claim that the next stage ran.

## Completion and stop conditions

Complete when candidate subdomains, contexts, relationships, evidence, ownership, uncertainty, and validation state are explicit, and either exactly one context is selected for tactical work or a bounded decision/stop result is delivered. A result with multiple ready contexts must not emit more than one tactical context. Stop with `partial` or `blocked` for weak evidence, missing vocabulary, unresolved ownership, user-authored filename collisions, unsafe updates, or material decisions. Stop with `not-fit-conflict` when discovery's non-fit result conflicts with the request and no explicit decision or new evidence resolves it.

Never invent domain facts, silently resolve overloaded language, infer boundaries from code structure alone, mark hypotheses validated without evidence, or edit product source, tests, configuration, generated output, or deployment files.

## References and evaluation

Read the [strategic method](references/strategic-method.md) and [strategic artifact contract](references/artifact-contracts.md) before writing. Templates are in `assets/`; package-local evaluation cases are in `evals/evals.json`.
