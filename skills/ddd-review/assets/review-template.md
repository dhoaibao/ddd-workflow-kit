# DDD review

| Field | Value |
| --- | --- |
| `artifact` | `review` |
| `status` | `draft` |
| `validation` | `unvalidated` |
| `owner` | `ddd-review` |
| `scope` | _named domain/context/slice_ |
| `provenance` | _review inputs, sources, contributors, and dates_ |
| `assumptions` | _explicit assumptions or none recorded_ |
| `open_questions` | _unresolved questions or none recorded_ |
| `last_updated` | _YYYY-MM-DD_ |

`ready` means documentation readiness for the stated scope only. It does not approve implementation, deployment, migration, data cutover, release, or product-code changes.

## Review scope and objective

- **Objective:** _requested review objective._
- **Scope:** _domain, context, capability, or slice._
- **Depth and acceptance criteria:** _what this review must establish._
- **Review date:** _YYYY-MM-DD._

## Artifact inventory and validation summary

| Path | Availability/lifecycle | Validation | Owner | Provenance | Scope note |
| --- | --- | --- | --- | --- | --- |
| _docs/ddd/example.md_ | _available/missing/partial/stale_ | _status_ | _owner_ | _source/date or missing_ | _scope_ |

Missing artifacts are findings; their contents are not reconstructed.

## DDD fit and quality-gate results

| Gate | Question | Evidence | Status | Owner | Revisit trigger |
| --- | --- | --- | --- | --- | --- |
| Fit and scope | _question_ | _evidence_ | _pass/follow-up/blocked/not-applicable_ | _owner_ | _trigger_ |
| Evidence and provenance | _question_ | _evidence_ | _status_ | _owner_ | _trigger_ |
| Lifecycle and schema | _question_ | _evidence_ | _status_ | _owner_ | _trigger_ |
| Vocabulary and translation | _question_ | _evidence_ | _status_ | _owner_ | _trigger_ |
| Strategic-to-tactical | _question_ | _evidence_ | _status_ | _owner_ | _trigger_ |
| Adoption safety | _question_ | _evidence_ | _status_ | _owner_ | _trigger_ |
| Cross-artifact consistency | _question_ | _evidence_ | _status_ | _owner_ | _trigger_ |

## Findings by severity

| Severity | Evidence | Provenance | Owner | Action | Status | Affected artifact | Earliest stage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| _info/follow-up/blocked/invalidated_ | _observable evidence_ | _source/owner/date_ | _owner_ | _next action_ | _open/routed/accepted/resolved_ | _exact path or none_ | _stage_ |

## Stale and conflicting artifacts

| Artifact | Conflict or invalidating evidence | Dependents | Earliest stage | Owner/action | Revisit trigger |
| --- | --- | --- | --- | --- | --- |
| _path_ | _evidence_ | _dependent paths_ | _stage_ | _owner/action_ | _trigger_ |

Preserve conflicting claims and do not silently repair source artifacts.

## Ownership and documentation boundary

- **Owned artifact:** `docs/ddd/review.md` only.
- **Forbidden actions:** product-code, test, configuration, schema, generated-output, deployment, and migration changes.

## Next step and chat summary

- **Next step:** _one exact stage, owner action, or bounded stop._
- **Return to:** `ddd-review` or the earliest affected stage.
- **Changed artifacts:** _exact paths, or none._
- **Chat summary:** _scope, gate status, findings, stale routing, open questions, and explicit documentation-only readiness statement._
