# Selected tactical slice

| Field | Value |
| --- | --- |
| `scope` | _one selected context and increment_ |
| `state` | _working, decision-needed, current, stale, or superseded_ |

**Selected context:** _exact path and authority; do not silently duplicate strategic boundaries._

## Claim and evidence ledger

| Claim ID | Claim type | Material claim | Evidence/owner | Referenced by |
| --- | --- | --- | --- | --- |
| _C-001_ | _current behavior, desired policy/meaning, obligation, fact, interpretation, proposal, or assumption_ | _claim_ | _source_ | _example/rule/invariant_ |

## Outcome and examples

- **Selected outcome:** _one bounded outcome._
- **Success example:** _concrete command, preconditions, result, acceptance signal._
- **Failure/counterexample:** _concrete rejected or unsafe behavior._

## Commands, rules, and transitions

| Command/use case | Preconditions | Rule/invariant | State change | Failure semantics | Acceptance |
| --- | --- | --- | --- | --- | --- |
| _command_ | _conditions_ | _behavior rule_ | _relevant transition_ | _observable failure_ | _signal_ |

## Invariants and current-versus-desired delta

| Invariant | Evidence/owner | Immediate/eventual consistency | Consistency boundary | Failure consequence | Current behavior | Desired behavior |
| --- | --- | --- | --- | --- | --- | --- |
| _invariant_ | _source_ | _why_ | _smallest boundary/aggregate that protects this invariant_ | _what must not happen_ | _observed_ | _required_ |

<!-- Conditional fragment: omit this entire section when no relationship, async, external-contract, concurrency, privacy, data, or brownfield trigger exists. -->
## Relevant integration semantics

- **Relationship/translation:** _only if the selected slice touches another context._
- **Failure/delivery/ordering/idempotency/retry/repair:** _only when async/external trigger exists._
- **Concurrency/transaction/conflict:** _only when concurrent-write trigger exists._
- **Privacy/contract/data detail:** _only when its trigger exists._

<!-- Conditional fragment: omit this entire section when no named tactical pattern problem exists. -->
## Conditional model decisions

Add a subsection only for a named problem:

- **Pattern/problem:** _why this pattern is evaluated now._
- **Decision:** _selected option and evidence._
- **Cost/simpler alternative:** _material trade-off._
- **Revisit trigger:** _what changes it._

Do not emit empty or `not-needed` pattern rows.

## Blocking decisions and evidence

- **Blocking decision:** _owner, increment impact, smallest evidence/action, affected path, revisit trigger._
- **Assumption/deferred item:** _only when it changes this increment._
