# Discovery method

Use this method to gather evidence without turning a workshop format into a mandatory ceremony. It works through interviews, examples, existing documents, tests, observation, or a combination.

## Start with outcomes and boundaries

Ask:

- What outcome matters, for whom, and why now?
- What capability or workflow is in scope?
- What is explicitly out of scope?
- Which decisions are costly, frequent, regulated, or difficult to change?
- Is the project greenfield, brownfield, or mixed?

Record the answer as a claim with source and claim type. A broad aspiration is not yet a domain fact.

## Explore concrete behavior

Use examples and counterexamples:

- Who acts, and what do they intend?
- What command, decision, or request starts the behavior?
- What must be true before and after it?
- What event indicates a meaningful change?
- Which policy, exception, or approval changes the outcome?
- Which terms are overloaded, disputed, or translated?

For brownfield work, compare desired policy with observed behavior. Capture tests, operational observations, integration contracts, and known seams without assuming the current module or table layout is the domain model.

## Assess fit

Signals supporting DDD include meaningful policy complexity, ambiguous language, strategic differentiation, multiple models of the same concept, costly change, or integration boundaries that need explicit translation. Signals against a broad DDD effort include straightforward CRUD, stable commodity behavior, low change risk, or a documentation cost that exceeds likely benefit.

Use:

- `fit` when domain complexity and evidence justify a focused DDD model;
- `limited-fit` when only a capability or slice justifies DDD;
- `not-fit` when a simpler approach is better supported.

State what evidence would change the classification.

## Preserve uncertainty

Keep separate lists for facts, interpretations, proposals, assumptions, and open questions. When claims conflict, retain both claims with source, owner, scope, and impact. Ask which policy or obligation governs instead of choosing the most convenient source.

## Handoff readiness

Discovery is ready for strategic work when it has:

- a bounded outcome and scope;
- a fit classification and rationale;
- enough terms and examples to identify candidate boundaries;
- current/desired/required claim distinctions;
- constraints, ownership, assumptions, and open questions;
- a documented evidence bundle and validation status.

If any of these is materially missing, return a bounded stop or ask one focused question.
