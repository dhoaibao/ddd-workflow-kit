# Skills and routing

This design has one portable orchestrator, `ddd`, and five focused stages: `ddd-discover`, `ddd-strategic`, `ddd-tactical`, `ddd-adoption`, and `ddd-review`. Names identify responsibilities, not implementation technology.

## Shared operating rules

Every skill:

1. States its scope, inputs, assumptions, and evidence before drawing conclusions.
2. Preserves existing target-project documents and makes additive, reviewable changes by default.
3. Separates observed facts, interpretations, proposals, and unresolved questions.
4. Uses the artifact contracts in [artifact-contracts.md](artifact-contracts.md).
5. Stops for a material user decision, a safety boundary, or evidence that invalidates the current model.
6. Returns a compact summary and an explicit handoff or stop reason.

### Claim-type-aware evidence

Evidence authority depends on the claim being made:

- **Intended domain policy and meaning:** user and domain-expert statements, validated examples, and agreed language are primary.
- **Current system behavior:** executable behavior, tests, operational observations, and integration evidence are primary.
- **Required obligations:** explicit contracts, regulations, and security or privacy constraints are primary.
- **Project intent and rationale:** current project documentation and decision records provide context, but do not override observed behavior or explicit obligations.
- **DDD guidance:** generic guidance suggests questions and options; it cannot establish target-project facts.

When sources disagree, represent separate current-state, desired-policy, and required-obligation claims with their sources and owners. Record the gap and its impact; never silently overwrite one claim with another or auto-resolve a disagreement by source class.

## Portable package and transition protocol

The implemented logical package set has one `ddd` orchestrator package, five independently invocable stage packages (`ddd-discover`, `ddd-strategic`, `ddd-tactical`, `ddd-adoption`, `ddd-review`), and shared artifact contracts. This is a logical portability boundary, not a required directory layout or runtime.

The orchestrator owns routing and workflow state only. It never performs focused-stage work. A transition is represented by a portable request bundle:

- `stage`: exact stage name;
- `objective`: one bounded objective;
- `scope`: target project, context, or slice;
- `artifacts`: paths, lifecycle/validation status, and relevant excerpts or references;
- `evidence`: claim/source records and provenance;
- `assumptions` and `open_questions`;
- `allowed_paths`: documentation boundary and ownership constraints;
- `return_to`: orchestrator or named caller.

A stage returns a portable result bundle containing `stage`, `status`, changed artifact paths, findings, updated evidence/assumptions, handoff or stop reason, and `invalidated_stages` when feedback requires a loop. A host that supports named stage activation may activate the requested stage with this bundle. A host without such activation must return the exact next manual invocation—stage name plus the unchanged request bundle—to the user; it must not duplicate stage behavior or claim the transition ran. Focused stages accept the same bundle directly and return the same result shape, so standalone use does not depend on the orchestrator. The orchestrator consumes the result, updates routing state, and emits the next transition or final summary.

## Orchestrator: `ddd`

**Purpose.** Coordinate a complete DDD assessment and modeling flow without owning the detail of any stage.

**Triggers.** A request to apply DDD broadly, assess a project, create a domain model, or run the full discover-to-review flow.

**Inputs.** User goal; target-project documentation and allowed source evidence; existing `docs/ddd/` artifacts if present; constraints such as greenfield or brownfield, domain-expert availability, and desired depth.

**Entry criteria.** The target project and desired outcome are identified well enough to begin discovery. If not, ask a material user question before proceeding.

**Ordered behavior.**

1. Establish scope, DDD-fit hypotheses, constraints, and evidence boundaries.
2. Emit a transition request for `ddd-discover`.
3. Emit a transition request for `ddd-strategic` only when discovery supplies sufficient domain evidence.
4. Emit a transition request for `ddd-tactical` only after strategic outputs are sufficiently validated.
5. Emit a transition request for `ddd-adoption` to sequence practical next steps.
6. Emit a transition request for `ddd-review` for cross-artifact consistency and readiness.
7. Loop back to the earliest invalidated stage when review or new evidence changes a boundary; preserve later artifacts as stale rather than silently rewriting them.

**Outputs.** A staged set of `docs/ddd/` artifacts, a stage summary, open questions, assumptions, validation status, and recommended next step. No product-code changes.

**Completion / stop conditions.** Complete when the requested stages pass review or the user receives a bounded partial result with explicit gaps. Stop when DDD is a poor fit, evidence is insufficient, a material decision needs the user, or the requested change exceeds the documentation-only boundary.

**Handoff contract.** Pass the artifact paths, evidence ledger, assumptions, unresolved questions, validation status, and the exact next-stage objective. A downstream stage must not infer missing strategic context.

**Non-goals.** It does not duplicate stage-specific modeling, force every stage to run, choose deployment topology, or override a focused-stage decision without evidence.

## Discovery: `ddd-discover`

**Purpose.** Establish whether DDD is useful and capture the domain evidence needed for later modeling.

**Triggers.** Unfamiliar project, request to assess fit, missing domain vocabulary, greenfield exploration, or brownfield baseline work.

**Inputs.** Business goal; user and domain-expert accounts; current behavior, documentation, tests, integrations, and constraints when available.

**Entry criteria.** A target project or problem space and a permitted evidence scope exist. Ask for scope or access when either is missing.

**Ordered behavior.**

1. Describe the outcome, users, important decisions, and constraints.
2. Identify complexity, change risk, ambiguity, and whether simpler CRUD may be sufficient.
3. Collect terms, examples, events, policies, actors, and open questions without treating guesses as facts.
4. In brownfield work, record current behavior, seams, ownership, dependencies, and safe migration constraints.
5. Produce or update the assessment and discovery portions of the domain vision and ubiquitous language.
6. State whether to continue, simplify, or stop the DDD path.

**Outputs.** `assessment.md`, initial `domain-vision.md`, initial `ubiquitous-language.md`, evidence/provenance notes, fit recommendation, and questions for the next stage.

**Completion / stop conditions.** Complete when DDD fit and the relevant domain evidence are explicit enough for strategic design. Stop for simple/non-fit work, absent scope, unavailable critical evidence, or unresolved material contradictions.

**Handoff contract.** Provide fit rationale, evidence hierarchy, confirmed terms, assumptions, contradictions, and the minimum strategic questions remaining. Never hand off an invented domain fact.

**Non-goals.** It does not define bounded contexts, aggregate boundaries, service topology, or a migration plan.

## Strategic design: `ddd-strategic`

**Purpose.** Define domain structure and model boundaries from validated discovery evidence.

**Triggers.** Sufficient discovery evidence exists, or a focused request explicitly asks for subdomains, bounded contexts, or a context map.

**Inputs.** Validated discovery artifacts; expert statements; domain vocabulary; business capabilities, ownership, lifecycle, and integration evidence; existing strategic artifacts.

**Entry criteria.** `assessment.md` indicates DDD is useful or the user explicitly requests strategic modeling; core terms and at least one meaningful outcome are available. If not, hand back to discovery.

**Ordered behavior.**

1. Classify candidate subdomains as core, supporting, generic, or unresolved with rationale.
2. Define bounded contexts around consistent models and language, not deployment assumptions.
3. Record context-map relationships, ownership, translation, contracts, and uncertainty.
4. Reconcile vocabulary conflicts by preserving context-specific meanings and marking unresolved conflicts.
5. Validate boundaries against concrete scenarios and change/consistency needs.
6. Publish or update `domain-map.md`, `context-map.md`, and the strategic portions of `domain-vision.md` and `ubiquitous-language.md`.

**Outputs.** Strategic artifacts with boundary rationale, relationship map, vocabulary decisions, assumptions, open questions, and validation status.

**Completion / stop conditions.** Complete when contexts and relationships are coherent enough to guide tactical modeling. Stop or return to discovery when boundaries depend on unknown facts, domain experts disagree materially, or the proposed split is only a deployment preference.

**Handoff contract.** Pass the selected context, its purpose, language, invariants to investigate, upstream/downstream relationships, ownership, and unresolved boundary questions to tactical design.

**Non-goals.** It does not design classes, aggregates, schemas, services, or infrastructure, and it does not equate a bounded context with a microservice.

## Tactical design: `ddd-tactical`

**Purpose.** Model rules and consistency boundaries inside a sufficiently understood bounded context.

**Triggers.** A strategic context is selected and the request concerns entities, value objects, aggregates, events, repositories, services, specifications, factories, or models.

**Inputs.** Validated strategic artifacts; context-specific language; concrete commands, events, examples, invariants, consistency needs, and existing context/model artifacts.

**Entry criteria.** A target bounded context, its purpose, vocabulary, and boundary relationships are sufficiently validated. If strategic context is incomplete, stop and hand back to `ddd-strategic`.

**Ordered behavior.**

1. Identify commands, outcomes, domain events, policies, and examples.
2. State invariants and the consistency boundary that protects each one.
3. Choose entities, value objects, aggregate roots, repositories, domain/application services, specifications, factories, and events only where they clarify a named need.
4. Describe model boundaries and integration translations without selecting a framework.
5. Check aggregate size, transaction assumptions, failure semantics, and optional patterns such as CQRS or event sourcing.
6. Write or update the context model and model artifacts with examples and unresolved questions.

**Outputs.** `contexts/` and `models/` artifacts, tactical decisions, invariant examples, optional-pattern rationale, and validation status.

**Completion / stop conditions.** Complete when the selected context has an explainable model and invariants sufficient for implementation planning. Stop for missing strategic context, invented rules, unresolved contradictions, or a request to change product code.

**Handoff contract.** Pass model decisions, invariant examples, persistence/integration assumptions, unresolved risks, and adoption implications to `ddd-adoption` and `ddd-review`.

**Non-goals.** It does not generate implementation code, mandate patterns, choose an ORM/database, or redesign unrelated contexts.

## Adoption: `ddd-adoption`

**Purpose.** Turn validated domain insights into an incremental, reversible greenfield or brownfield adoption plan.

**Triggers.** A user asks how to introduce the model, sequence work, migrate a legacy area, or decide what to do next.

**Inputs.** Assessment, strategic and tactical artifacts, current-system constraints, ownership, risk, delivery capacity, rollback options, and user priorities.

**Entry criteria.** At least a bounded outcome and evidence-backed next slice exist. If not, return to discovery or the relevant modeling stage.

**Ordered behavior.**

1. Choose greenfield or brownfield workflow and identify the first learning/delivery slice.
2. Sequence documentation, boundary protection, characterization, migration, or implementation work without editing product code.
3. Define acceptance signals, dependencies, rollback/containment, and decision points.
4. Identify operational, data, integration, privacy, and ownership risks.
5. Mark optional architecture choices as conditional decisions, not prerequisites.
6. Write or update `adoption-plan.md` and link each step to its evidence and artifact.

**Outputs.** A phased adoption plan, next action, acceptance signals, risks, reversibility notes, and questions requiring user or expert input.

**Completion / stop conditions.** Complete when a bounded, actionable, reversible sequence exists. Stop for unsafe migration, missing ownership, absent rollback for a risky step, or unresolved material decisions.

**Handoff contract.** Pass the plan, selected slice, prerequisites, acceptance signals, rollback/containment strategy, and dependencies to review.

**Non-goals.** It does not execute migrations, edit product code, promise a deployment topology, or turn every model into a service.

## Review: `ddd-review`

**Purpose.** Check fit, evidence, cross-artifact consistency, completeness, and safe next steps.

**Triggers.** End of an orchestrated flow, request to review DDD artifacts, new evidence, or a proposed boundary/model/adoption change.

**Inputs.** All requested artifacts; evidence and provenance; assumptions and open questions; quality-gate outcomes; requested scope and acceptance criteria.

**Entry criteria.** The artifacts to review and their intended scope are identifiable. Missing artifacts are reported rather than silently reconstructed.

**Ordered behavior.**

1. Check DDD fit and whether the requested depth matches the problem.
2. Verify each claim has provenance or is labeled an assumption/proposal.
3. Check strategic-to-tactical prerequisites, vocabulary consistency, boundary rationale, and relationship direction.
4. Check artifact schemas, lifecycle/validation status, ownership, completeness, and safe-update history.
5. Apply the relevant gates in [quality-gates.md](quality-gates.md).
6. Classify findings as ready, follow-up, blocked, or invalidated; route invalidated work to the earliest affected stage.
7. Write or update `review.md` and return a compact chat summary.

**Outputs.** `review.md`, findings with evidence, gate results, stale-artifact notices, recommended next stage, and a bounded summary.

**Completion / stop conditions.** Complete when findings and next steps are explicit. Stop with blocked status for missing evidence, unresolved material conflict, unsafe update, or incomplete acceptance criteria.

**Handoff contract.** Return exact artifact paths, finding severity, evidence, required owner, and the earliest stage to revisit. A ready result never implies product-code readiness.

**Non-goals.** It does not silently repair disputed facts, approve implementation outside the documentation scope, or replace domain-expert validation.

## Routing and overlap rules

| Request signal | Primary skill | Route next when needed |
| --- | --- | --- |
| Fit, unfamiliar domain, missing evidence, baseline | `ddd-discover` | strategic or stop |
| Subdomains, contexts, vocabulary boundaries, context map | `ddd-strategic` | discovery if evidence is weak; tactical when ready |
| Invariants, aggregates, entities, events, repositories, models | `ddd-tactical` | strategic if context is insufficient; adoption/review when modeled |
| Sequencing, migration, rollout, greenfield/brownfield plan | `ddd-adoption` | discovery/modeling for missing prerequisites; review |
| Consistency, completeness, contradictions, readiness | `ddd-review` | earliest invalidated stage |
| Broad “apply DDD” or end-to-end request | `ddd` | orchestrated stage flow |

If multiple signals match, choose the earliest stage that owns the missing prerequisite. A focused request may invoke one stage directly, but it must enforce that stage's entry criteria and handoff contract. Review owns findings, not the underlying model; discovery owns fit and evidence, not boundary design.
