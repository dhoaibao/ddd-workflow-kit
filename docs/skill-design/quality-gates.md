# Quality gates

Quality gates prevent the skill set from turning DDD vocabulary into unsupported design decisions. Each gate produces pass, follow-up, blocked, or not-applicable status with evidence and owner.

## Gate format

For every gate, record:

- **Question:** what is being checked.
- **Evidence:** facts, sources, examples, or missing information.
- **Status:** `pass`, `follow-up`, `blocked`, or `not-applicable`.
- **Owner:** stage or project owner for the next action.
- **Revisit trigger:** evidence that could change the result.

A `pass` is scoped to the documented evidence; it is not an absolute guarantee.

## Fit and scope gates

### Simple CRUD or non-fit problem

**Question:** Are the rules, language, change risk, and integration needs simple enough that DDD would add more ceremony than value?

**Pass condition:** A simpler approach is appropriate, with the reasons and boundaries recorded in `assessment.md`.

**Follow-up/block:** If complexity is uncertain, ask for examples or domain evidence. Do not force subdomains, contexts, or tactical patterns merely to complete the workflow.

### Complex greenfield

**Question:** Is there evidence of meaningful domain complexity, ambiguity, strategic differentiation, or change risk?

**Pass condition:** Discovery identifies a high-value slice, domain experts or credible evidence, and a bounded strategic hypothesis before tactical modeling.

**Follow-up/block:** If only generic architecture preferences exist, remain in discovery and label the hypothesis.

### Brownfield or legacy

**Question:** Is current behavior understood well enough to change a bounded area safely?

**Pass condition:** Existing behavior, dependencies, ownership, characterization evidence, seam, compatibility, observability, and rollback/containment are recorded.

**Follow-up/block:** Missing baseline or unsafe data/integration change blocks a migration recommendation; route back to discovery or adoption planning.

## Modeling gates

### Conflicting vocabulary

**Question:** Are overloaded or disputed terms represented by context-specific meanings and explicit translation?

**Pass condition:** Conflicting definitions have sources, owners, affected contexts, and a decision or open question in `ubiquitous-language.md`.

**Follow-up/block:** Never merge terms because spelling matches. Ask the responsible experts or preserve the conflict as unresolved.

### Domain expert unavailable

**Question:** Can claims be validated without the relevant domain expert?

**Pass condition:** Available behavior, tests, contracts, and documentation support only a bounded provisional model, with assumptions and validation debt recorded.

**Follow-up/block:** Mark affected artifacts `partially-validated` or `unvalidated`; do not present inferences as domain facts. Ask for expert access before irreversible conclusions.

### Strategic prerequisite

**Question:** Does tactical work have a sufficiently validated bounded context, language, boundary, and relationship map?

**Pass condition:** The context, invariants to investigate, and unresolved boundary questions are explicit.

**Follow-up/block:** Route to `ddd-strategic` or `ddd-discover`; tactical patterns cannot substitute for missing strategic context.

### Oversized aggregate

**Question:** Does each proposed aggregate protect a named invariant without loading unrelated lifecycle or consistency concerns?

**Pass condition:** Aggregate scope, root access, transaction needs, contention, and cross-boundary coordination are justified by examples.

**Follow-up/block:** Split or revisit the boundary when the aggregate is an object graph, a database mirror, or a source of avoidable contention. Do not split solely for aesthetics.

## Architecture and pattern gates

### Premature microservices

**Question:** Is a deployment split being proposed because of demonstrated ownership, scaling, security, failure isolation, or independent change needs rather than because DDD is assumed to require it?

**Pass condition:** The context map, operational evidence, contracts, observability, and distributed failure costs are explicit; a modular monolith remains an evaluated alternative.

**Follow-up/block:** Keep the proposal at a modeling boundary or modular architecture when deployment evidence is absent. A bounded context is not automatically a microservice.

### Optional CQRS or event sourcing

**Question:** Does the concrete problem justify separate read/write models or event history as the primary record?

**Pass condition:** The decision records the problem, benefits, synchronization/replay/evolution costs, operational capability, privacy implications, and simpler alternative.

**Follow-up/block:** Mark the pattern `not-needed` or deferred when evidence is insufficient. Domain events or messaging alone do not imply event sourcing.

## Artifact and delivery gates

### Incomplete artifacts

**Question:** Do requested artifacts meet their minimum schemas and state what remains unknown?

**Pass condition:** Required metadata, ownership, provenance, assumptions, open questions, lifecycle status, validation status, and scope are present; missing sections are explicitly marked.

**Follow-up/block:** Review reports exact missing paths/sections and routes to the owning stage. It must not silently create facts or mark an artifact validated.

### Safe documentation boundary

**Question:** Does the proposed output remain within the agreed modeling-document scope?

**Pass condition:** Changes are limited to `docs/ddd/`, preserve existing docs, and return a chat summary; no product code or runtime behavior is edited.

**Follow-up/block:** Stop for requests to edit source, tests, configuration, generated output, or deployment artifacts in this first release.

### Handoff completeness

**Question:** Can the next stage act without guessing?

**Pass condition:** Handoff includes artifact paths, evidence, assumptions, validation status, open questions, owner, exact objective, and stop/revisit conditions.

**Follow-up/block:** Return to the current owner when any material element is absent.

## Review result

`ddd-review` aggregates gate results but does not erase failures. A ready documentation result means the stated artifacts are coherent and appropriately qualified. It does not approve implementation, deployment, a microservice split, or a claim that the domain model is final.
