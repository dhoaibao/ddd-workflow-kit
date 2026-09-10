# Selected bounded context

| Field | Value |
| --- | --- |
| `scope` | _one selected capability/increment_ |
| `state` | _working, decision-needed, current, stale, or superseded_ |

## Purpose and boundary

- **Purpose/outcome:** _decision-bearing purpose._
- **Decision owner:** _who owns policy meaning._
- **In scope:** _terms, workflow, capability, and current slice._
- **Out of scope:** _neighboring behavior._

## Key terms and scenarios

| Term or scenario | Meaning/behavior that affects the increment | Evidence/owner |
| --- | --- | --- |
| _term/scenario_ | _concrete meaning or boundary consequence_ | _source_ |

<!-- Conditional fragment: emit `## Touched relationships` only when a material relationship is selected; otherwise omit it. If emitted, record direction, other context, ownership/translation, consistency/failure assumption, and evidence. -->
<!-- Conditional fragment: emit `## Blocking boundary decisions` only when an unresolved decision blocks this increment; otherwise omit it and route any queue item to the earliest owner. -->
