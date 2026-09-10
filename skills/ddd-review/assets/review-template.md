# Increment review

| Field | Value |
| --- | --- |
| `scope` | _one named increment and authority set_ |
| `state` | _working, decision-needed, current, stale, or superseded_ |

`ready` is documentation readiness only. It does not authorize implementation, deployment, migration, release, or product changes. The owned target is `docs/ddd/review.md`; README ownership is limited to the decision-queue and latest-review markers.

## Increment and authority set

- **Increment ID:** _stable ID._
- **Authority set:** _exact paths, sections, and revisions._
- **Target/runtime/baseline:** _identity and revision._
- **Accountable implementation owner:** _named human; same field as the gate's `owner` and the eventual handoff's `implementation_owner`._
- **Acceptance and containment:** _signals and limits._

## Readiness

```yaml
documentation_readiness: ready | follow-up | blocked | invalidated
increment_gate: blocked | awaiting-ratification
```

- **passed gates:** _one concise sentence; do not repeat a full pass table._
- **Material assumptions/deferred/out-of-scope items:** _only those affecting this increment._

<!-- Conditional fragment: emit `## Findings and decision queue` only when a finding or unresolved decision affects this increment; otherwise omit it. If emitted, each row must carry issue/evidence, Increment impact, Disposition, a Status legal for that disposition (blocking/invalidating/decision-required: open or resolved; accepted-assumption/resolved: resolved; deferred: deferred; out-of-scope: closed), Owner/earliest stage, Required action, Affected artifacts, and Revisit trigger. A blocker cannot be silently relabeled deferred or out of scope without human confirmation and impact rationale. -->

## Next action

- **Exact next action:** _one action by one owner._
- **Review summary:** _passed checks, exceptions, and next stage._
- **Authorization:** _not authorized; only `ddd` may create the handoff after explicit ratification._

<!-- Conditional fragment: only when a stale or invalidated authority exists for this increment, add one more line here in this exact form and do not render it otherwise: "- **Stale/invalidated authorities:** paths, evidence, preserved revisions." -->
