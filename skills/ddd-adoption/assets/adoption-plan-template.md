# Adoption plan

| Field | Value |
| --- | --- |
| `artifact` | `adoption-plan` |
| `status` | `draft` |
| `validation` | `unvalidated` |
| `owner` | `ddd-adoption` |
| `scope` | _one bounded outcome and first slice_ |
| `provenance` | _sources, contributors, and dates_ |
| `assumptions` | _explicit assumptions or none recorded_ |
| `open_questions` | _unresolved questions or none recorded_ |
| `last_updated` | _YYYY-MM-DD_ |

This is a recommendation for incremental work. It does not claim that a migration, implementation, deployment, or product-code change was executed.

## Mode and outcome

- **Mode:** _greenfield or brownfield._
- **Target outcome:** _one bounded outcome._
- **In scope:** _selected context, capability, and first slice._
- **Out of scope:** _explicit exclusions._
- **Entry validation:** _discovery, strategic, and tactical evidence with status and owner._

## Claim and evidence ledger

| Claim ID | Claim type | Statement | Source/provenance | Owner | Scenario/impact | Validation |
| --- | --- | --- | --- | --- | --- | --- |
| _A-001_ | _current behavior, desired policy/meaning, required obligation, fact, interpretation, proposal, decision, or assumption_ | _statement_ | _source and date_ | _owner_ | _scenario and impact_ | _status_ |

Preserve current, desired, and required claims separately when they conflict. Record the decision needed and affected increment.

## First slice and ordered increments

**First slice:** _smallest useful learning or delivery slice and why it is bounded._

| Order | Increment and outcome | Owner | Dependencies/prerequisites | Decision point | Acceptance signal | Risk | Rollback/containment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | _increment_ | _owner_ | _dependencies_ | _evidence that changes the plan_ | _observable signal_ | _risk_ | _recovery, containment, or limit_ |

## Ownership, dependencies, and decision points

- **Accountable owner:** _person/team and decision scope._
- **Contributors and dependencies:** _teams, contexts, contracts, data, or evidence._
- **Decision points:** _owner, evidence needed, and revisit trigger._
- **Invalidated stages/artifacts:** _none or explicit stale paths and reason._

## Brownfield baseline and safety

_Complete for brownfield; mark not applicable for greenfield._

- **Current behavior and failure modes:** _observed facts and provenance._
- **Characterization evidence:** _tests, operational observations, or first increment that creates it._
- **Seam and compatibility/translation:** _protected boundary and ownership._
- **Observability and acceptance:** _signals, dashboards/logs/measurements as recommendations only._
- **Data ownership and reconciliation:** _source of truth, migration/reconciliation assumptions, privacy constraints._
- **Rollback, recovery, or containment:** _trigger, steps, limits, and what cannot be reversed._
- **Big-bang check:** _explicitly rejected or not applicable with evidence._

## Data, integration, privacy, and operational risks

| Risk or unresolved decision | Claim IDs | Impact | Owner | Mitigation/containment | Acceptance or revisit trigger | Status |
| --- | --- | --- | --- | --- | --- | --- |
| _risk_ | _A-001_ | _impact_ | _owner_ | _mitigation_ | _signal_ | _open/proposed/accepted_ |

## Acceptance signals and validation

- **Acceptance signals:** _observable outcome for each increment._
- **Validation status:** _unvalidated, partially-validated, validated, or stale with evidence._
- **Open questions:** _owner and next evidence._
- **Revisit trigger:** _what would invalidate this plan._

## Explicit boundary and next handoff

- **Allowed paths:** `docs/ddd/adoption-plan.md` only for adoption-owned changes.
- **Forbidden actions:** product-code edits, tests/configuration/deployment changes, and migration execution.
- **Changed artifacts:** _exact path, or none if this is a recommendation only._
- **Next stage:** `ddd-review` with exactly one plan path and the complete evidence/acceptance/risk bundle.
- **Return to:** `ddd-adoption` unless an earlier modeling stage is invalidated.
