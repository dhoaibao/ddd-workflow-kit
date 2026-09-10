# Candidate implementation increment

| Field | Value |
| --- | --- |
| `scope` | _one context/slice_ |
| `state` | _working, decision-needed, current, stale, or superseded_ |

This is documentation, not implementation, migration, deployment, or release approval.

## Increment identity and outcome

- **increment_id:** _stable-id._
- **Target repository/runtime:** _identity._
- **Baseline revision:** _exact revision._
- **Target placement:** _module/package/path in the target repository._
<!-- Conditional fragment: add only when this increment needs a new boundary/deployable; otherwise omit. -->
<!-- If triggered: **Architecture fit:** the new boundary/deployable and its rationale. -->
- **Intended outcome:** _bounded outcome._
- **Concrete change:** _one candidate change._
- **In scope:** _behavior._
- **Excluded:** _behavior explicitly out._
- **Accountable implementation owner:** _named person/role._

## Dependencies and acceptance

- **Dependencies:** _required evidence, decisions, or contracts._
- **Observable acceptance signals:** _signals an engineer/test can observe._
- **Stop conditions:** _when to stop and return to a DDD stage._

<!-- Conditional fragment: emit the following section only when a data, async, privacy, external-contract, concurrency, or brownfield risk trigger is recorded; otherwise omit it. -->
<!-- If triggered: ## Material risk and containment, with the risk, impact, containment/rollback/recovery, and revisit trigger. -->

<!-- Conditional fragment: Decision queue is emitted only when an unresolved question/conflict affects this increment; otherwise omit it. -->
<!-- If triggered: record ID, issue, impact, disposition, owner, smallest action, affected path, and revisit trigger. -->
<!-- Record accepted assumptions or deferred questions only when they affect this increment. -->
