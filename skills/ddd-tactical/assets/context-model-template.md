# Context model

| Field | Value |
| --- | --- |
| `artifact` | `context-model:<context-slug>` |
| `status` | `draft` |
| `validation` | `unvalidated` |
| `owner` | `ddd-tactical` |
| `scope` | _one selected context and slice_ |
| `provenance` | _sources, contributors, and dates_ |
| `assumptions` | _explicit assumptions or none recorded_ |
| `open_questions` | _unresolved questions or none recorded_ |
| `last_updated` | _YYYY-MM-DD_ |

**Selected context authority:** The materialized model at `docs/ddd/models/<context-slug>.md` must link to `[Selected context](../contexts/<context-slug>.md)` and must not duplicate or silently revise strategic boundary facts.

## Claim and evidence ledger

Record every substantive statement as one of these claim types: `current behavior`, `desired policy/meaning`, `required obligation`, `fact`, `interpretation`, `proposal`, or `assumption`. Decisions and invariants cite the relevant `Claim ID` values rather than silently merging conflicting claims.

| Claim ID | Claim type | Statement | Source/provenance | Owner | Scenario | Validation | Referenced by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| _C-001_ | _claim type_ | _statement_ | _source and provenance_ | _owner_ | _scenario_ | _status_ | _invariant or decision IDs_ |

## Scope and outcome

- **Context and safe slug:** _exact validated strategic identity and reused slug._
- **Purpose/outcome:** _one bounded outcome._
- **In scope:** _commands, policies, terms, and workflows._
- **Out of scope:** _explicit exclusions and neighboring contexts._
- **Decision owner:** _person or group responsible for the model._

## Commands and scenarios

| Command/use case | Claim IDs | Actor and preconditions | Inputs/decisions | Successful outcome | Failures/counterexamples | Acceptance signal |
| --- | --- | --- | --- | --- | --- | --- |
| _command_ | _C-001_ | _actor and preconditions_ | _inputs and policy decisions_ | _outcome_ | _failure or counterexample_ | _observable signal_ |

## Invariants and consistency

| Invariant | Claim IDs | Evidence/owner | Immediate or eventual | Failure consequence | Validation |
| --- | --- | --- | --- | --- | --- |
| _named invariant_ | _C-001_ | _source and owner_ | _consistency need and why_ | _what must not happen_ | _status_ |

## Model elements

### Entities

| Entity | Claim IDs | Identity/continuity | Responsibilities | Status/evidence |
| --- | --- | --- | --- | --- |
| _entity or none needed_ | _C-001_ | _identity and lifecycle_ | _behavior_ | _proposal and source_ |

### Value objects

| Value object | Claim IDs | Equality/validation | Responsibilities | Examples/non-examples | Status/evidence |
| --- | --- | --- | --- | --- | --- |
| _value or none needed_ | _C-001_ | _value equality and rules_ | _behavior_ | _examples_ | _proposal and source_ |

### Aggregates and roots

| Aggregate/root | Protected immediate invariant | Claim IDs | In/out boundary | References | Transaction/concurrency | Status/evidence |
| --- | --- | --- | --- | --- | --- | --- |
| _aggregate or none yet_ | _named invariant_ | _C-001_ | _scope_ | _cross-boundary references_ | _assumptions_ | _proposal and source_ |

## Contracts and flows

### Repositories

| Contract | Claim IDs | Aggregate root | Needed behavior | Failure/concurrency semantics | Status/evidence |
| --- | --- | --- | --- | --- | --- |
| _repository or not-needed_ | _C-001_ | _root_ | _domain-facing intent_ | _failure and concurrency_ | _decision and source_ |

### Services, specifications, and factories

| Element | Claim IDs | Domain rule or application orchestration | Named need / simpler alternative | Status/evidence |
| --- | --- | --- | --- | --- |
| _element or not-needed_ | _C-001_ | _responsibility_ | _why it exists or why not_ | _decision and source_ |

### Events and delivery

| Past-tense event | Claim IDs | Facts and consumers | Ordering/duplication/idempotency | Retry/recovery/privacy | Status/evidence |
| --- | --- | --- | --- | --- | --- |
| _event or none needed_ | _C-001_ | _facts, not commands_ | _assumptions_ | _assumptions_ | _decision and source_ |

### Application flow and integration

| Decision area | Claim IDs | Decision and evidence |
| --- | --- | --- |
| Application flow | _C-001_ | _orchestration from command to outcome_ |
| Cross-aggregate consistency | _C-001_ | _immediate/eventual decision and boundary consequence_ |
| Integration translation | _C-001_ | _relationship, contract, mapping, and failure assumptions_ |
| Persistence assumptions | _C-001_ | _needed behavior and unknowns, not implementation choice_ |

## Optional pattern decisions

| Pattern | Claim IDs | Status (`not-needed`, `deferred`, or `proposed`) | Evidence | Costs/risks | Simpler alternative |
| --- | --- | --- | --- | --- | --- |
| CQRS | _C-001_ | _decision_ | _source_ | _conceptual/operational costs_ | _alternative_ |
| Event sourcing | _C-001_ | _decision_ | _source_ | _conceptual/operational costs_ | _alternative_ |

Ordinary domain events do not imply event sourcing. Do not choose an optional pattern without evidence.

## Assumptions, questions, and validation

- **Assumptions:** _explicit assumptions and impact._
- **Risks:** _model, consistency, integration, privacy, or delivery risks._
- **Open questions:** _owner and next evidence._
- **Validation:** _unvalidated, partially-validated, validated, or stale with evidence._
- **Downstream invalidation:** _stages/artifacts made stale, or none._
