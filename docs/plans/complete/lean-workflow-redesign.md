# Plan: redesign `ddd-workflow-kit` for lean, decision-driven delivery

## Status

Implementation candidate complete after independent-review fixes; awaiting independent review. No commit or push has occurred.

This plan incorporates the BonVoye end-to-end workflow evidence and the agreed direction: retain the six existing skills, preserve the documentation-only boundary, reduce generated artifacts and required fields, add scoped human ratification, and produce one implementation handoff for one bounded increment.

## Goal

Redesign the workflow so it thinks rigorously but writes selectively. Generated documents must contain only information that supports:

1. a human decision;
2. a behavior or invariant that implementation must enforce;
3. a boundary or contract that affects code;
4. an observable acceptance signal; or
5. an uncertainty or risk that can change the next action.

If removing content would not change a decision, implementation, verification, or material risk, the workflow must not generate it.

## Foundation alignment

The redesign preserves the existing DDD foundation rather than weakening it:

- DDD makes important decisions visible, testable, and understandable; it does not reproduce every business detail.
- Models are purposeful hypotheses for a bounded context, not complete descriptions of reality.
- Tactical patterns are options, not a checklist.
- Adoption starts with one thin, high-learning slice and revises the model from implementation evidence.
- Pattern cargo cult, exhaustive up-front modeling, and big-bang migration are explicit failure modes.
- Architecture and operational detail are included only when a concrete risk or constraint requires it.

The foundation remains the comprehensive reference. Target-project artifacts are concise decision and implementation aids; they must not restate the foundation.

## Evidence motivating the redesign

The BonVoye workflow produced 16 Markdown files and 1,454 lines for one selected Storytelling Experience slice. Fifteen artifacts remained `draft`; none was `validated`. The review called the documentation `ready` while explicitly providing no implementation authority, the required `docs/ddd/README.md` was absent, and the human had no single implementation entry point.

This exposed five design defects:

1. minimum schemas became output checklists;
2. optional DDD concepts became mandatory sections;
3. evidence and decisions were duplicated across artifacts;
4. documentation readiness was easy to confuse with implementation readiness; and
5. the workflow optimized artifact completeness rather than delivery of one valuable increment.

## Resolved design decisions

- Keep the six packages: `ddd`, `ddd-discover`, `ddd-strategic`, `ddd-tactical`, `ddd-adoption`, and `ddd-review`.
- Do not add an implementation or delivery skill.
- Keep all six skills documentation-only; none edits target product source, tests, configuration, schemas, migrations, deployment files, or runtime behavior.
- Make one bounded implementation increment the unit of workflow progress.
- Generate artifacts progressively and conditionally rather than generating the complete catalog.
- Preserve rigorous internal checks, but emit pass details only when they affect a decision.
- Route conflicts to the earliest owning stage; `ddd-review` consolidates findings but does not decide domain policy.
- Require explicit human authorization for one increment.
- Create one durable `implementation-handoff-v1` only after authorization.
- Existing artifacts remain readable; the redesign does not delete or silently rewrite legacy documents.

## Content policy

Every generated paragraph, table, or field must pass the utility test in the Goal section. In addition:

- Prefer concrete examples over explanatory prose.
- Prefer a link to the authoritative statement over duplication.
- Cite evidence beside the material claim it supports.
- Preserve current behavior, desired behavior, obligations, decisions, and assumptions separately only when the distinction affects the selected increment.
- Omit empty sections and `not applicable` rows.
- Do not write generic DDD teaching content into a target project.
- Do not record speculative future design merely because a template has a place for it.
- Fully specify only the next increment; later increments remain short hypotheses until selected.

## Lean metadata contract

Replace the nine-field common metadata table with two required fields and one conditional field:

| Field | Requirement |
| --- | --- |
| `scope` | The bounded context, capability, or increment to which the document applies. |
| `state` | `working`, `decision-needed`, `current`, `stale`, or `superseded`. |
| `owner` | Required only when a named person or role must decide, validate, or act. |

Rules:

- The path and H1 identify the artifact; do not repeat an `artifact` field.
- Do not maintain separate document-level lifecycle and validation axes.
- Record evidence near material claims, not in a mandatory metadata summary.
- Omit assumptions and open-question sections when empty.
- Use repository history instead of a mandatory `last_updated` field when version history is available.
- A document being `current` never authorizes implementation. Authorization exists only in `implementation-handoff-v1`.

Legacy metadata remains accepted when reading existing projects. New output uses the lean contract.

## Default and conditional artifacts

### Default artifacts for one selected slice

Before human authorization, generate at most this working set unless a conditional trigger is recorded:

1. `docs/ddd/README.md` — entry point, outcome, selected slice, workflow state, decision queue, and next action.
2. `docs/ddd/contexts/<context-slug>.md` — selected context purpose, boundary, owner, key terms, and only the relationships touched by the slice.
3. `docs/ddd/models/<slice-slug>.md` — examples, rules, invariants, current-versus-desired behavior, and required integration semantics.
4. `docs/ddd/adoption-plan.md` — one fully specified candidate increment.
5. `docs/ddd/review.md` — concise readiness result, exceptions, and routed worklist.

After explicit authorization, add:

6. `docs/ddd/implementation-handoff.md` — the sole implementation entry point.

A non-fit flow may stop after recording the decision and simpler path in `docs/ddd/README.md`; it must not generate modeling artifacts merely to complete the sequence.

### Conditional artifacts

| Artifact | Generate only when |
| --- | --- |
| `assessment.md` | DDD fit is disputed, evidence-heavy, limited, or needs a durable standalone decision record. |
| `domain-vision.md` | The business outcome, stakeholders, or strategic intent is absent or materially disputed. |
| `domain-map.md` | Subdomain classification changes investment, sourcing, or ownership decisions. |
| `context-map.md` | Two or more contexts and their relationship direction or translation affect the selected slice. |
| `ubiquitous-language.md` | Terms are reused across artifacts, overloaded across contexts, or materially conflicted. |
| Additional `contexts/` files | Another context is selected or its boundary is required by the current integration. |
| Additional `models/` files | Another tactical slice is explicitly selected. |

Potential future contexts may remain one-line hypotheses in the index or context map. They do not receive full documents until selected or required by a current relationship.

## Required content by artifact

### `docs/ddd/README.md`

Keep it readable in one screen where practical. It contains:

- target outcome;
- selected context and increment;
- current workflow stage;
- documentation readiness;
- increment gate;
- blocking decision count and decision-queue link or inline queue;
- exact next human action;
- links to current artifacts;
- implementation-handoff link or `not authorized`.

For an orchestrated run, creating and updating this index is mandatory. Failure to create or safely update it is a bounded workflow error.

### Selected context document

Require only:

- purpose and business decision ownership;
- explicit in-scope and out-of-scope boundary;
- key terms whose meanings affect the slice;
- touched upstream/downstream relationships and translation responsibility;
- unresolved boundary decisions that block the slice.

Do not repeat a full context map, generic stakeholder inventory, or unrelated workflows.

### Tactical model

Require only:

- selected outcome;
- representative success and failure examples;
- commands or use cases;
- rules and invariants;
- relevant state transitions;
- current-versus-desired behavior differences;
- consistency and integration failure semantics that affect the slice;
- blocking decisions and validation evidence.

Entities, value objects, aggregates, repositories, services, specifications, factories, events, CQRS, and event sourcing are conditional. Include a pattern only when it solves a named problem. Do not generate `not-needed` rows for every unused pattern.

### Adoption plan

Fully specify only the immediate candidate increment:

- stable `increment_id`;
- target repository/runtime and baseline revision;
- intended outcome and concrete change;
- in-scope and excluded behavior;
- accountable owner;
- required dependencies;
- observable acceptance signals;
- material risk and containment or rollback;
- stop conditions;
- questions that block this increment;
- accepted assumptions and deferred questions relevant to later work.

Later increments are short hypotheses without exhaustive dependencies, risks, or acceptance tables until selected.

### Review

Review continues to run all quality gates internally, but output is exception-based. Require only:

- named increment and authority set;
- documentation readiness;
- increment gate;
- blocking, invalidating, or decision-required findings;
- accepted assumptions, deferred items, and out-of-scope items that matter to the increment;
- earliest-owner routing;
- one exact next action.

Do not print full passing gate tables, duplicate artifact inventories, or repeat evidence ledgers. Summarize passed checks in one sentence.

## Trigger-based depth

Generate operational detail only when its trigger exists:

| Trigger | Required detail |
| --- | --- |
| Data mutation or migration | Source of truth, reconciliation, irreversible effects, recovery. |
| Asynchronous communication | Delivery, ordering, duplication, retry, idempotency, repair. |
| Personal or sensitive data | Collection purpose, access, retention, deletion, privacy owner. |
| External consumer or published contract | Compatibility, versioning, ownership, failure behavior. |
| Concurrent writes or immediate consistency need | Transaction boundary, conflict behavior, invariant enforcement. |
| Risky brownfield routing | Baseline, characterization, containment or rollback, observability. |
| Optional architecture pattern | Concrete pressure, simpler alternative, cost, and revisit signal. |

When no trigger exists, omit the section rather than writing `not applicable`.

## Decision queue and question policy

`ddd-review` consolidates unresolved items into one decision queue:

| Field | Purpose |
| --- | --- |
| ID | Stable reference. |
| Issue | Exact conflict, missing decision, or missing evidence. |
| Increment impact | Why it does or does not affect the selected increment. |
| Disposition | Current treatment. |
| Owner | Earliest stage and named human role where known. |
| Required decision/evidence | Smallest action needed. |
| Affected artifacts | Exact current paths. |
| Revisit trigger | Evidence or future increment that reopens the issue. |

Allowed dispositions:

- `blocking` — affects behavior, invariant, boundary, obligation, safety, or acceptance;
- `invalidating` — makes an authoritative artifact or downstream assumption stale;
- `decision-required` — a named human/domain owner must choose;
- `accepted-assumption` — bounded uncertainty explicitly accepted by the human;
- `deferred` — relevant to a later increment and assigned a revisit trigger;
- `out-of-scope` — demonstrably irrelevant to the selected increment;
- `resolved` — settled by evidence or a recorded human decision.

A blocker cannot be relabeled as deferred or out of scope without human confirmation and an impact rationale. Review does not repeatedly question the user. It groups findings by earliest owning stage; that stage asks the smallest related question set and updates only its owned artifact.

## Readiness and ratification

Do not emit an unqualified `ready` result. Every review records two separate states:

```yaml
documentation_readiness: ready | follow-up | blocked | invalidated
increment_gate: blocked | awaiting-ratification
```

`ddd-review` may set `awaiting-ratification` only when, for the named increment:

- no blocking or invalidating finding remains;
- every decision-required item is resolved;
- authoritative boundaries, behavior, invariants, and obligations are clear;
- acceptance and containment are sufficient for the actual risk;
- every remaining uncertainty is explicitly accepted, deferred, or out of scope with owner and revisit trigger;
- target repository/runtime and accountable implementation owner are named.

The orchestrator records `authorized` only after explicit human ratification. Ratification applies to one increment, not the whole domain model or project, and it does not mark every source document validated.

The ratification record contains:

- decision: authorized or declined;
- named human decision owner;
- date;
- increment ID;
- target repository/runtime;
- exact artifact revisions accepted;
- accepted assumptions;
- deferred and out-of-scope questions;
- acceptance signals;
- containment limitations.

## `implementation-handoff-v1`

The `ddd` orchestrator owns `docs/ddd/implementation-handoff.md`. It may create the file only after a review returns `increment_gate: awaiting-ratification` and a human authorizes that exact increment.

The implemented candidate's canonical, currently enforced contract is [`skills/ddd/assets/implementation-handoff-template.md`](../../../skills/ddd/assets/implementation-handoff-template.md); that template, not this planning note, is authoritative for field shape (runtime binding, implementation owner, typed question dispositions with `issue`, complete ratification record, and exact accepted/authoritative revision equality). This plan no longer duplicates that schema to avoid drift.

The handoff references authoritative sections instead of copying them. It is invalid when an artifact is stale, its recorded revision no longer matches, authorization is missing, or a listed source conflicts with another authority.

## Coding-agent consumption contract

A downstream coding workflow reads in this order:

1. `docs/ddd/implementation-handoff.md`;
2. the selected increment in `adoption-plan.md`;
3. the referenced tactical examples, rules, and invariants;
4. the referenced context boundary and relationship sections;
5. referenced vocabulary or strategic material only when listed;
6. existing source and tests;
7. a repository-specific technical plan produced before editing code.

The coding agent implements only the authorized increment. It must stop and return the conflict to the named DDD stage when:

- an authoritative revision changed;
- a source artifact is stale;
- authoritative sources disagree;
- required behavior is absent;
- the implementation exposes a new domain decision;
- the requested change exceeds the handoff scope.

Existing source/tests remain authoritative evidence of current brownfield behavior. Human-ratified scenarios and invariants define desired behavior. The handoff defines scope and authorization.

## Package changes

### `ddd`

Update:

- `skills/ddd/SKILL.md`;
- `skills/ddd/references/orchestration-protocol.md`;
- `skills/ddd/references/artifact-contracts.md`;
- `skills/ddd/assets/request-result-template.md`;
- `skills/ddd/assets/ddd-readme-template.md`;
- `skills/ddd/evals/evals.json`.

Add:

- `skills/ddd/assets/implementation-handoff-template.md`.

Required behavior:

- make the index mandatory for broad flows;
- preserve the lean artifact profile and conditional triggers;
- carry one candidate increment and decision queue;
- pause at human ratification;
- create exactly one authorized handoff;
- invalidate the handoff when its authority set becomes stale or changes;
- never implement product changes.

Keep `ddd-routing-v1` as the base transport contract for compatibility. Add an explicitly versioned `ddd-implementation-gate-v1` extension carried from adoption through review and orchestration. Older requests remain valid but cannot produce an implementation handoff.

### `ddd-discover`

Update its skill, method, artifact contract, templates, and evaluations so that:

- discovery returns the smallest evidence-backed fit decision;
- a broad fit result may be recorded in the index without forcing standalone assessment and vision documents;
- `assessment.md` and `domain-vision.md` are conditional artifacts;
- non-fit stops without generating downstream artifacts;
- only material current-versus-desired conflicts are persisted.

### `ddd-strategic`

Update its skill, method, artifact contract, templates, and evaluations so that:

- strategic work is slice-first;
- it creates one selected context document by default;
- direct dependencies are documented only to the depth required by the selected slice;
- domain map, context map, glossary, and additional context documents use their conditional triggers;
- it does not exhaustively model all plausible contexts;
- it still preserves overloaded terms and relationship direction when they affect implementation.

### `ddd-tactical`

Update its skill, method, artifact contract, template, and evaluations so that:

- examples, rules, invariants, and failure behavior are primary;
- tactical patterns are conditional rather than mandatory schema sections;
- optional pattern decisions are documented only when evaluated for a concrete pressure;
- no empty or `not-needed` pattern inventory is emitted;
- output remains sufficient for implementation and tests.

### `ddd-adoption`

Update its skill, method, artifact contract, template, and evaluations so that:

- one candidate increment with stable ID is the primary output;
- only that increment is fully specified;
- target and baseline are required before implementation readiness;
- risk detail is trigger-based;
- blockers, assumptions, and deferred questions use the shared disposition contract;
- it emits the versioned implementation-gate extension to review;
- it never claims authorization or execution.

### `ddd-review`

Update its skill, method, artifact contract, template, and evaluations so that:

- review scope is one named increment and authority set;
- gate checking remains rigorous internally;
- output reports exceptions instead of full pass tables;
- documentation readiness and increment gate are separate;
- all questions receive an increment-impact disposition;
- it emits one consolidated routed worklist;
- it never creates the implementation handoff or resolves domain decisions.

### Shared design, validation, and release records

Update:

- `docs/skill-design/workflows.md`;
- `docs/skill-design/artifact-contracts.md`;
- `docs/skill-design/quality-gates.md`;
- `docs/skill-design/skills-and-routing.md` where routing descriptions change;
- `docs/skill-design/README.md`;
- `scripts/validate-skills.py`;
- `README.md`;
- `CHANGELOG.md` under `[Unreleased]` before any commit;
- `docs/plans/README.md` when implementation status changes.

Add a new versioned evaluation report for this redesign; do not rewrite phase-0 or phase-4 historical evidence.

## Ordered implementation plan

### Phase 1 — Freeze lean contracts

1. Add evaluation cases that fail under the current verbose schemas.
2. Define the lean metadata, default/conditional artifact profile, utility test, conditional triggers, decision dispositions, dual readiness, ratification, and implementation-handoff contracts in shared design docs.
3. Define backward-compatible reading of existing target artifacts.

Done when the contracts answer what is written, why it is needed, who consumes it, and what safely happens to existing documents.

### Phase 2 — Make discovery and strategic output progressive

1. Make assessment and vision conditional.
2. Default strategic work to one selected context and touched relationships.
3. Generate maps, glossary, and additional contexts only on recorded triggers.
4. Group owner questions and stop rather than expanding speculative documentation.

Done when a single-context flow does not generate a whole-domain document set and a non-fit flow stops with only its decision record.

### Phase 3 — Make tactical output example-driven

1. Replace mandatory pattern sections with examples, rules, invariants, deltas, and relevant failure semantics.
2. Add conditional triggers for aggregate, repository, event, specification, factory, CQRS, and event-sourcing decisions.
3. Reject generic or empty pattern inventories in evaluations.

Done when an engineer can derive behavior and tests without reading unused pattern commentary.

### Phase 4 — Make adoption and review increment-driven

1. Introduce the stable candidate-increment contract.
2. Detail only the immediate increment.
3. Add the shared question dispositions and consolidated decision queue.
4. Separate documentation readiness from the increment gate.
5. Make review output exception-based while retaining internal gate rigor.

Done when unrelated domain questions cannot block a selected slice and unresolved slice blockers cannot be hidden as follow-ups.

### Phase 5 — Add ratification and implementation handoff

1. Add the `ddd-implementation-gate-v1` extension.
2. Make `docs/ddd/README.md` mandatory and update its first-screen status.
3. Add explicit human ratification handling to `ddd`.
4. Add the `implementation-handoff-v1` asset and owned target artifact.
5. Add revision/stale/conflict invalidation.
6. Document the downstream coding-agent consumption contract.

Done when no handoff exists without explicit authorization and one authorized handoff identifies one exact authority set for one increment.

### Phase 6 — Validate portability and real workflow value

1. Extend `scripts/validate-skills.py` for new assets, dispositions, gate fields, conditional artifacts, and negative cases.
2. Validate every changed `evals.json` with `python3 -m json.tool`.
3. Run package isolation, relative-link, one-H1, forbidden host/path, and safe-update checks.
4. Run live semantic evaluations where the existing host/model is available.
5. Re-run the BonVoye scenario only with permission, or use a repository-local sanitized BonVoye-shaped fixture.
6. Freeze the exact candidate snapshot and obtain independent `b-review` before completion.

Done when repository checks pass and observed model outputs satisfy the lean acceptance cases below.

## Required evaluation cases

Add positive and negative cases proving:

1. a simple/non-fit request stops without generating downstream artifacts;
2. a one-context slice does not generate documents for unrelated contexts;
3. optional artifacts appear only when their triggers are present;
4. optional tactical patterns are omitted rather than emitted as empty or `not-needed` rows;
5. passed review gates are summarized rather than fully repeated;
6. documentation can be ready while the increment remains blocked;
7. unrelated questions can be human-confirmed as deferred or out of scope;
8. a blocking question cannot be silently reclassified;
9. findings are grouped by earliest owner into one decision queue;
10. missing target, baseline, owner, acceptance, containment, or authorization prevents a handoff;
11. human authorization creates exactly one handoff for exactly one increment;
12. stale or revision-mismatched artifacts invalidate an existing handoff;
13. the coding-agent reading order includes only the exact authority set;
14. legacy artifacts are preserved and read without destructive migration;
15. all stages retain the documentation-only boundary.

## BonVoye acceptance scenario

The redesigned workflow passes the motivating scenario when it produces:

- a mandatory `docs/ddd/README.md`;
- one selected Storytelling Experience context and tactical slice;
- no detailed documents for unrelated contexts unless a current relationship requires them;
- one candidate characterization increment;
- one concise decision queue rather than scattered unresolved questions;
- an explicit `documentation_readiness` and `increment_gate` pair;
- no implementation handoff while completion ownership, target, or accountable owners block the increment;
- an authorized characterization-only handoff, if approved, naming the seven deterministic fixture scenarios and exact authoritative revisions;
- no requirement for the coding agent to interpret every file under `docs/ddd/`.

The scenario is not considered successful merely because Markdown schemas validate. A human must be able to identify the next decision from the index, and an engineer must be able to plan the authorized increment without resolving undocumented domain ambiguity.

## Verification

Required repository checks after implementation:

```text
python3 scripts/validate-skills.py
python3 -m json.tool skills/ddd/evals/evals.json
python3 -m json.tool skills/ddd-discover/evals/evals.json
python3 -m json.tool skills/ddd-strategic/evals/evals.json
python3 -m json.tool skills/ddd-tactical/evals/evals.json
python3 -m json.tool skills/ddd-adoption/evals/evals.json
python3 -m json.tool skills/ddd-review/evals/evals.json
rtk git diff --check
```

Also verify:

- one H1 per Markdown file;
- all rendered local links resolve;
- every package remains independently copyable;
- no host-, vendor-, framework-, language-, database-, or machine-specific requirement enters a portable package;
- no target product source, test, configuration, migration, generated output, or deployment file is modified by a DDD skill;
- existing user-authored artifacts are preserved;
- live evaluation claims identify host/model/version and do not overstate static validation;
- the exact final snapshot receives independent changed-code review.

## Success criteria

The redesign is complete when:

- the default workflow produces no more than the default working set unless every extra artifact has a recorded trigger;
- documents omit unused fields, empty sections, generic teaching, and duplicate claims;
- one selected increment is the unit of adoption, review, ratification, and handoff;
- review reports exceptions and a consolidated decision queue;
- documentation readiness cannot be mistaken for implementation authorization;
- a human can identify the current decision and next action from `README.md` without reading the full artifact set;
- a coding agent can identify exact behavior, boundaries, acceptance signals, and authority from one handoff;
- stale or conflicting authority stops implementation rather than being silently resolved;
- all repository, portability, semantic evaluation, and independent review gates pass.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Concision hides important evidence | Keep evidence beside material or disputed claims and expand only on explicit risk triggers. |
| Conditional artifacts make outputs inconsistent | Define deterministic triggers and test both presence and absence. |
| Shared information drifts across files | Assign one authoritative location and require links instead of copies. |
| Existing projects depend on legacy schemas | Read legacy documents, preserve them, and migrate only through additive or explicitly superseding updates. |
| Models still produce verbose prose | Add negative semantic evals for generic teaching, duplication, empty sections, and unrelated artifacts. |
| `current` is mistaken for authorized | Reserve authorization exclusively for `implementation-handoff-v1`. |
| Handoff becomes stale after documentation changes | Record exact artifact revisions and invalidate on mismatch or stale state. |
| Lean defaults are insufficient for high-risk work | Trigger additional depth for data, privacy, async, external-contract, concurrency, and brownfield risks. |

## Non-goals

This redesign does not:

- add a seventh skill;
- make DDD mandatory for simple work;
- implement target product code;
- approve deployment, migration, release, or architecture topology;
- require microservices, CQRS, event sourcing, repositories, factories, or any other tactical pattern;
- erase unresolved evidence or silently choose among conflicting claims;
- impose hard line limits that encourage omission of material risk;
- rewrite historical evaluation records;
- treat passing static validation as proof of host/model or real-project effectiveness.
