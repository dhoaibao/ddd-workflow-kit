# Lean adoption method

## Entry triage

Check one outcome, one selected slice, target repository/runtime, baseline, owner, evidence, and allowed path. Route the earliest missing prerequisite rather than inferring it.

## Candidate increment

Fully specify only the next increment: stable ID, intended outcome/change, in/out scope, owner, dependencies, acceptance, stop conditions, and questions that can change the action. Add risks and containment/rollback only when a trigger exists; later increments are one-line hypotheses.

## Trigger-based safety

Data/migration requires source of truth, reconciliation, irreversible effects, and recovery. Async requires delivery/order/duplication/retry/idempotency/repair. Privacy requires purpose/access/retention/deletion/owner. External contracts require compatibility/versioning/ownership/failure. Concurrent writes require transaction/conflict/invariant detail. Brownfield routing requires baseline/characterization/seam/containment/observability.

## Review handoff

Adoption emits `ddd-implementation-gate-v1` as a result extension and exactly one review request only after target, baseline, accountable implementation owner, dependencies, and acceptance are sufficient; `ddd` carries the extension and performs ratification/authorization. Add containment when a trigger exists. `awaiting-ratification` is a review state, not authorization. Return earliest gaps to discovery/strategic/tactical/adoption.
