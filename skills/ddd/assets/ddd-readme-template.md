# DDD artifact index

For broad flows, create `docs/ddd/README.md` before downstream artifacts. Keep it concise and preserve user-authored prose outside owned markers.

## Target outcome and selected increment

<!-- ddd-owned:outcome:start -->
- **Target outcome:** _one bounded outcome._
- **Selected context/slice:** _one context and stable increment ID._
<!-- ddd-owned:outcome:end -->

## Workflow status

<!-- ddd-owned:routing-status:start -->
- **Current stage:** _stage._
- **documentation_readiness:** _ready, follow-up, blocked, or invalidated._
- **increment_gate:** _blocked, awaiting-ratification, or authorized._
- **Blocking decisions:** _count and queue link._
- **Exact next human action:** _one action._
<!-- ddd-owned:routing-status:end -->

## Current artifacts

<!-- ddd-owned:artifact-index:start -->
| Path | Owner | State | Why it exists |
| --- | --- | --- | --- |
| _docs/ddd/path_ | _stage_ | _working/current/stale_ | _decision, behavior, boundary, acceptance, or risk_ |
<!-- ddd-owned:artifact-index:end -->

## Decision queue

<!-- ddd-review-owned:decision-queue:start -->
<!-- ddd-review may update this marker and latest-review marker only after validating its review result; ddd preserves both. -->
No open decisions for the selected increment.

<!-- Conditional fragment: only when the increment has an unresolved finding or decision, replace the line above with this exact table shape and one row per open item; do not render the table otherwise:
| ID | Issue | Increment impact | Disposition | Status | Owner | Required action | Affected paths | Revisit trigger |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DQ-001 | issue | impact | blocking/invalidating/decision-required/accepted-assumption/deferred/out-of-scope/resolved | open/resolved/deferred/closed, legal for its disposition | owner | smallest action | paths | trigger |
-->
<!-- ddd-review-owned:decision-queue:end -->

## Authorization

<!-- ddd-owned:authorization:start -->
<!-- ddd owns routing/status and authorization markers; ddd-review owns only decision-queue/latest-review markers. -->
- **Ratification:** _not requested, pending, declined, or authorized for one increment._
- **Implementation handoff:** `not authorized` or `docs/ddd/implementation-handoff.md`.

<!-- Conditional fragment: only when the ratification state is declined, add these two lines here in this exact form; do not render them otherwise:
- **Declined decision:** decision, named human, date, target/baseline identity, and reason.
- **declined decision persisted record:** decision, owner, date, increment ID, target repository/runtime/baseline, and reason are retained in this marker.
-->
<!-- ddd-owned:authorization:end -->

## Review link

<!-- ddd-review-owned:latest-review:start -->
- Review artifact: `docs/ddd/review.md` — documentation readiness, increment gate, and one next action.
<!-- ddd-review-owned:latest-review:end -->
