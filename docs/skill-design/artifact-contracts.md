# Lean artifact contracts

The document workflow (the six `document`-class packages) writes selective, documentation-only aids under a target project's `docs/ddd/`. A paragraph, field, or table is permitted only when removing it would change a decision, implementation behavior, boundary/contract, verification signal, or material risk. An installed `implementation`-class package's target-repository code and tests are outside this documentation-only contract; see [Implementation-owned artifact](#implementation-owned-artifact).

## Lean metadata contract

New artifacts use this small contract:

| Field | Requirement |
| --- | --- |
| `scope` | Bounded context, capability, or selected increment covered by the artifact. |
| `state` | `working`, `decision-needed`, `current`, `stale`, or `superseded`. |
| `owner` | Conditional: include only when a named person or role must decide, validate, or act. |

The path and H1 identify the artifact; do not repeat `artifact`. Do not maintain separate document lifecycle and validation axes. Record evidence next to material claims. Omit empty assumptions, questions, and `not applicable` rows. Repository history supplies update identity when available. `current` never authorizes implementation.

Legacy artifacts with `artifact`, `status`, `validation`, `provenance`, `assumptions`, `open_questions`, or `last_updated` remain readable. New output does not silently migrate or rewrite them. A legacy artifact is treated as `stale` when new evidence invalidates it, not as authorized work.

## Lean state compatibility with `ddd-routing-v1`

Legacy transport artifact records retain `lifecycle` and `validation`. A new lean artifact may additionally carry `state`; its deterministic compatibility mapping is:

| Lean `state` | Legacy `lifecycle` | Legacy `validation` |
| --- | --- | --- |
| `working` | `draft` | `unvalidated` |
| `decision-needed` | `draft` | `unvalidated` |
| `current` | `active` | `validated` |
| `stale` | preserve prior lifecycle (`draft`, `active`, `superseded`, or `archived`) | `stale` |
| `superseded` | `superseded` | `stale` |

On normal transition, preserve `state` and the mapped legacy values. Invalidation preserves the prior lifecycle (including `draft` or `active`) and changes lean `state` to `stale` plus legacy validation to `stale`; a stale record is therefore not forced to `active`. Legacy records without `state` remain valid; focused stages must not invent a lean state when reading them.

## Utility and authority rules

- Prefer concrete examples over generic DDD teaching.
- Link to one authoritative statement instead of copying it.
- Keep current behavior, desired behavior, obligations, decisions, and assumptions separate only when the distinction affects the selected increment.
- Fully specify one bounded increment; later work stays a short hypothesis.
- Tactical patterns are conditional decisions. Omit unused pattern sections rather than emitting empty or `not-needed` rows.
- Evidence beside a claim includes source/owner where material; unsupported inference remains a proposal or assumption.
- Existing target documents are preserved. Updates are additive and limited to the owning stage's sections.
- No skill edits product source, tests, configuration, schema, migration, deployment, generated output, or runtime behavior.

## Default and conditional artifact profile

For one selected slice, before authorization the default set is at most:

1. `docs/ddd/README.md` — outcome, selected context/increment, workflow state, readiness/gate, decision queue, next action, and current links.
2. `docs/ddd/contexts/<context-slug>.md` — selected purpose, boundary, owner, key terms, and touched relationships.
3. `docs/ddd/models/<slice-slug>.md` — examples, rules, invariants, behavior delta, and required integration semantics.
4. `docs/ddd/adoption-plan.md` — one complete candidate increment.
5. `docs/ddd/review.md` — exception-based readiness, gate, routed findings, and next action.

Only after explicit ratification may the orchestrator add `docs/ddd/implementation-handoff.md`.

Conditional artifacts are generated only for a recorded trigger:

| Artifact | Trigger |
| --- | --- |
| `assessment.md` | DDD fit is disputed, evidence-heavy, limited, or needs a durable decision record. |
| `domain-vision.md` | Outcome, stakeholders, or strategic intent is absent or materially disputed. |
| `domain-map.md` | Classification changes investment, sourcing, or ownership. |
| `context-map.md` | Multiple contexts and relationship direction/translation affect the selected slice. |
| `ubiquitous-language.md` | Terms are reused, overloaded, or materially conflicted. |
| Additional context/model file | Another context or tactical slice is selected or required by a current relationship. |

A non-fit flow may stop with its decision in the index. It must not create downstream artifacts merely to complete a sequence.

## Owned artifact contracts

### Index: `docs/ddd/README.md`

The broad-flow index is mandatory and should fit on one screen where practical. Its Status section leads with a plain-language "what's happening" summary and one plain-language next action, with the machine fields demoted into a collapsible block per [the index template](../../skills/ddd/assets/ddd-readme-template.md). It records target outcome; selected context and increment; current stage; `documentation_readiness`; `increment_gate`; blocking decision count and queue; exact next human action; current artifact links; and a handoff link or `not authorized`. `ddd` owns routing/status and authorization sections; `ddd-review` owns only the README decision-queue/latest-review markers plus `review.md`.

### Context

Require purpose and business-decision owner; explicit in/out boundary; and key slice terms. Add touched upstream/downstream relationships and translation responsibility only when a material relationship trigger exists; add unresolved boundary decisions only when they block the increment. Do not reproduce a whole context map.

### Tactical model

Require selected outcome; success/failure examples; commands/use cases; rules/invariants; relevant transitions; current-versus-desired differences; the smallest consistency boundary protecting each invariant; integration/consistency failure semantics; blocking decisions and evidence. Include entities, value objects, aggregates, repositories, services, specifications, factories, events, CQRS, or event sourcing only when a named problem requires them.

### Adoption plan

Require stable `increment_id`; repository/runtime and baseline; target placement (module/package/path in the target repository); intended outcome and concrete change; in/out scope; accountable implementation owner; dependencies; observable acceptance; and stop conditions. Add material risk/containment, a decision queue, an architecture-fit note, and accepted/deferred questions only when their recorded triggers affect this increment. Later increments are hypotheses.

Baseline revision requires an existing git repository with at least one commit; it is never a sentinel like `none` or `uninitialized`. A greenfield target with zero commits is a bounded stop: `ddd-adoption` asks the operator to create the first commit (typically the one holding the ratified DDD artifacts) and records its exact revision.

### Review

Review runs all relevant checks internally but emits exceptions only. It reports one increment and authority set; `documentation_readiness`; `increment_gate`; blocking/invalidating/decision-required findings; relevant accepted/deferred/out-of-scope items; earliest-owner routing; and one exact next action. Passed checks are one sentence, not a repeated gate table.

## Decision queue

`ddd-review` consolidates one queue with these fields:

| Field | Meaning |
| --- | --- |
| ID | Stable reference. |
| Issue | Exact conflict, missing decision, or missing evidence. |
| Increment impact | Why it affects or does not affect the selected increment. |
| Disposition | `blocking`, `invalidating`, `decision-required`, `accepted-assumption`, `deferred`, `out-of-scope`, or `resolved`. |
| Owner | Earliest owning stage and named human role where known. |
| Required decision/evidence | Smallest next action. |
| Affected artifacts | Exact paths. |
| Revisit trigger | Evidence or future increment that reopens it. |

A blocker cannot become `deferred` or `out-of-scope` without human confirmation and impact rationale. The earliest owner asks the smallest related question set and updates only its owned artifact.

## Readiness, ratification, and handoff

Every review records documentation readiness and its review gate, never an unqualified `ready`:

```yaml
documentation_readiness: ready | follow-up | blocked | invalidated
increment_gate: blocked | awaiting-ratification
```

After explicit human ratification, `ddd` separately records the transport/index gate as `authorized`; review-owned `review.md` remains the awaiting-ratification evidence.

`awaiting-ratification` requires no blocking/invalidating finding; resolved decision-required items; clear boundary, behavior, invariants, and obligations; sufficient acceptance and containment; explicit treatment of remaining uncertainty; and named target repository/runtime and accountable implementation owner. The state order is `blocked` with `not-yet-requested|declined`, `awaiting-ratification` with `pending`, then `authorized` with `authorized`; only explicit human ratification moves the separate gate to `authorized`.

The gate names the accountable implementation owner; the ratification record names the human decision owner in its own field (may equal or differ from the implementation owner), decision (`authorized` or `declined`), date, increment ID, target repository/runtime/baseline, accepted artifact revisions, accepted assumptions, deferred/out-of-scope questions, typed question dispositions with a unique `id`, exact `issue` text, owner/action/revisit trigger, and a status legal for its disposition; a `deferred` issue must appear exactly in `deferred_questions`, an `out-of-scope` issue exactly in `out_of_scope_questions`, and an `accepted-assumption` issue exactly in `accepted_assumptions`, with no orphan strings in any of the three lists and no disposition-less list entries. Acceptance signals and containment limitations are also required. `out_of_scope` may be an empty list when the increment has no material exclusion beyond its `in_scope` statement; this is a deliberate permissiveness, not an omission. Every list is typed and bound exactly to the gate and generated handoff. Ratification does not validate every source document.

Each disposition's `status` is legal only for its `disposition`, exactly as follows:

| Disposition | Legal status |
| --- | --- |
| `blocking` | `open`, `resolved` |
| `invalidating` | `open`, `resolved` |
| `decision-required` | `open`, `resolved` |
| `accepted-assumption` | `resolved` |
| `deferred` | `deferred` |
| `out-of-scope` | `closed` |
| `resolved` | `resolved` |

A disposition `id` is unique within the gate. `blocking`, `invalidating`, and `decision-required` items must reach `resolved` before the gate can be `awaiting-ratification` or `authorized`.

`implementation-handoff-v1` is owned by `ddd` at `docs/ddd/implementation-handoff.md` and is created only after `increment_gate: authorized` plus explicit authorization. It references exact authoritative sections and revisions rather than copying them. `authority-revision-v1` is `sha256:<64 lowercase hex digits>` computed over exact artifact UTF-8 bytes; `sections` lists exact H2 headings and consumers require both the digest and headings to match. Every `sections` entry is quoted: an unquoted flow-list entry with an internal comma (a real H2 heading can contain one) silently mis-splits under a YAML parser. The target baseline revision is separate.

```yaml
version: implementation-handoff-v1
authorization:
  decision: authorized
  owner: named decision owner
  date: YYYY-MM-DD
implementation_owner: named implementation owner
increment:
  id: stable-id
  outcome: bounded outcome
target:
  repository: repository identity
  runtime: runtime identity
  baseline_revision: exact revision
  placement: module/package/path in the target repository
authoritative_artifacts:
  - path: docs/ddd/adoption-plan.md
    sections: ["Increment identity and outcome", "Dependencies and acceptance"]
    revision: sha256:<64 lowercase hex digits>
    role: scope-and-delivery
in_scope: [one named behavior]
out_of_scope: [product/runtime changes]
accepted_assumptions: []
deferred_questions: []
out_of_scope_questions: []
question_dispositions:
  - id: Q-001
    disposition: resolved
    status: resolved
    issue: later hypothesis candidate
    impact: no impact on this increment
    owner: named product owner
    action: record as later hypothesis
    affected_artifacts: []
    revisit_trigger: next publishing increment
acceptance_signals: [observable signal]
containment: [stop/rollback limit]
return_on_conflict: ddd-tactical
```

Every scope, target, and evidence field is recorded exactly once; `authorization` names only the decision, owner, and date, not a second copy. `target.repository`, `target.runtime`, and `target.baseline_revision` must equal the ratified gate's target; `target.placement` names the module/package/path for this increment, taken from the ratified adoption plan. A handoff is invalid when authorization is missing, a listed artifact is stale, a revision no longer matches, a listed H2 heading is absent, or authorities conflict.

## Coding-agent consumption

A downstream coding workflow reads, in order: the handoff; the selected adoption increment; referenced tactical examples/rules/invariants; referenced context boundary/relationships; only explicitly listed strategic/vocabulary material; existing source/tests; and a repository-specific technical plan before editing. It implements only the authorized increment and returns to the named DDD stage when authority changes, sources are stale or conflict, behavior is absent, a new decision appears, or scope expands.

## Implementation-owned artifact

An installed implementation-class package (for example `ddd-impl-fastapi-hdx`) is one consumer of the handoff. It owns exactly one target-project artifact per increment, `docs/ddd/implementation/<increment-id>.md`, namespaced under `implementation/` so it never collides with the `ddd`-owned `docs/ddd/implementation-handoff.md`. That record carries the repository-specific technical plan, the files touched, checks run, gated items proposed/approved, and any deviation from the handoff. It never edits the handoff or any other document-workflow artifact.

## Safe create/update behavior

Inspect existing paths first. Create only missing owned documents. Preserve user prose, legacy metadata, links, and provenance. Never delete, rename, or replace without explicit approval. Record conflicts instead of choosing silently. Reject unsafe paths and all product/runtime mutations.
