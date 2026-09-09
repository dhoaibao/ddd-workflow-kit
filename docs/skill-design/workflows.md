# Workflows

The skill set supports an orchestrated flow and independently invocable stages. Both use the same evidence and artifact contracts.

## Orchestrated flow

`ddd` coordinates:

`discover → strategic → tactical → adoption → review`

The arrows are prerequisites, not an assumption that every stage is always needed. Discovery may stop with a non-fit recommendation. A focused request may start at strategic, tactical, adoption, or review only when its entry criteria are satisfied.

### Feedback loops

- New vocabulary or behavior can return tactical work to strategic design.
- A boundary conflict returns strategic work to discovery or expert questioning.
- An invariant that crosses contexts returns tactical work to strategic boundary review.
- A migration constraint can return adoption work to tactical or strategic modeling.
- Review marks affected downstream artifacts `stale` and routes to the earliest invalidated stage.
- A later stage must never silently repair a missing prerequisite from guesswork.

## Material-user-question gates

Pause and ask the user when a decision would materially change scope, safety, ownership, or output. Examples:

- whether DDD assessment should cover the whole project or one capability;
- whether an existing document may be revised or only annotated;
- whether a domain expert, private repository area, or operational evidence is available;
- whether a disputed boundary should remain unresolved or use a stated working hypothesis;
- whether a risky brownfield increment has an acceptable rollback/containment path;
- whether the user wants a recommendation only or permission for a future artifact update.

Questions should state the decision, why it matters, and the options or missing evidence. Routine terminology questions belong in the workflow; material gates pause it. A missing answer yields a bounded stop, not an invented choice.

## Claim-type-aware evidence and provenance

For each substantive claim:

1. Capture the source or observation and its date/owner where available.
2. Classify it as current behavior, intended domain policy/meaning, required obligation, interpretation, proposal, or unresolved question.
3. Use the authority appropriate to the claim: domain experts and users for intended policy and meaning; executable behavior, tests, and operational evidence for current behavior; explicit contracts and regulations for obligations; project documentation for intent and rationale.
4. Record conflicting evidence separately with its claim type, source, owner, and impact. Do not let a desired policy overwrite current legacy behavior, or let current behavior silently define the desired policy.
5. Mark dependent artifacts stale when a claim changes or a conflict affects their assumptions.
6. Include the relevant evidence and assumptions in the handoff.

For example, if an expert says a legacy order should require approval but observed behavior permits shipment without approval, record both the current-behavior claim and the desired-policy claim, identify the gap, and ask which obligation and migration decision applies. Do not resolve the disagreement by choosing one source class automatically. Generic DDD guidance can suggest questions or patterns but cannot establish target-project facts.

## Greenfield workflow

1. `ddd-discover` frames the outcome, actors, policies, complexity, and DDD fit.
2. `ddd-strategic` maps subdomains, language, contexts, ownership, and relationships.
3. `ddd-tactical` models one high-value slice and its invariants; optional patterns are justified only by a concrete need.
4. `ddd-adoption` sequences a thin, observable first increment with acceptance signals.
5. `ddd-review` checks artifacts and records what remains uncertain.

Keep the first release documentation-only. Recommendations may identify future implementation work, but the skill does not edit product code.

## Brownfield workflow

1. `ddd-discover` establishes a safe baseline from current behavior, tests, integrations, ownership, and known failure modes.
2. Identify a seam and add or reference characterization evidence before proposing a boundary change.
3. `ddd-strategic` compares existing seams with domain boundaries and defines translation or an anti-corruption layer where needed.
4. `ddd-tactical` models one contained capability without assuming the legacy structure is the domain model.
5. `ddd-adoption` sequences reversible increments, compatibility, data reconciliation, observability, and rollback/containment.
6. `ddd-review` checks that old and new assumptions are explicit and routes contradictions backward.

No brownfield plan should imply a big-bang rewrite. If safe containment or ownership is absent, stop with the missing decision.

## Incremental and reversible work

Every proposed increment should identify:

- smallest useful slice;
- evidence and assumptions;
- owner and dependencies;
- observable acceptance signals;
- compatibility or translation boundary;
- rollback, containment, or recovery path;
- condition that would invalidate or revisit the decision.

Prefer additive documents, explicit status changes, and one bounded context or slice at a time. Do not claim reversibility when data migration, external contracts, or ownership make rollback uncertain.

## Independent stage invocation

| Invocation | Required starting point | Must not assume |
| --- | --- | --- |
| Discover | problem scope and evidence boundary | any context or aggregate design |
| Strategic | discovery evidence or explicit bounded strategic request | deployment services or tactical rules |
| Tactical | validated context, language, and boundary | missing strategic decisions |
| Adoption | bounded outcome and evidence-backed next slice | permission to edit product code |
| Review | named artifacts and review scope | missing artifacts or unrecorded facts |

An independent stage returns a handoff to the next appropriate stage or a bounded stop. It may create only artifacts it owns and must follow the same safe-update rules.
