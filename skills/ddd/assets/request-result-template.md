# Request and result bundles

These examples are the portable `ddd-routing-v1` contract. They contain no target-project facts. Legacy bundles without `extensions` remain valid but cannot authorize a handoff.

## Request schema

A request has one stage from `ddd-discover`, `ddd-strategic`, `ddd-tactical`, `ddd-adoption`, or `ddd-review`; one bounded objective/scope; artifact records; evidence/claims/provenance; assumptions/questions; allowed paths; and `return_to`.

```json
{
  "version": "ddd-routing-v1",
  "stage": "ddd-discover",
  "objective": "bound one selected increment",
  "scope": "named project/context/slice",
  "artifacts": [
    {"path": "docs/ddd/README.md", "lifecycle": "active", "validation": "validated", "availability": "available", "state": "current"}
  ],
  "evidence": [],
  "claims": [],
  "provenance": [],
  "assumptions": [],
  "open_questions": [],
  "allowed_paths": ["docs/ddd/"],
  "return_to": "ddd",
  "extensions": {}
}
```

Artifact record enums are: lifecycle `draft|active|superseded|archived|none`; validation `unvalidated|partially-validated|validated|stale|not-applicable`; availability `available|missing|partial|out-of-scope|none`; optional lean state `working|decision-needed|current|stale|superseded`. The state maps deterministically to legacy lifecycle/validation.

## Complete result schema

A result preserves the transport fields and adds one status, changed artifacts, findings, one handoff or stop, and invalidated stages. For a nonterminal result, the optional objective/scope/artifacts echo is complete and equals the next request/handoff; for a terminal result with `handoff: none`, it equals the prior request. Legacy results may omit the optional echo, in which case the orchestrator performs the documented merge/preservation. Status is one of `complete`, `partial`, `blocked`, `ready`, `not-fit-conflict`, `strategic-conflict`, `invalidated`, or `protocol-error`.

```json
{
  "version": "ddd-routing-v1",
  "stage": "ddd-discover",
  "objective": "bound one selected increment",
  "scope": "named project/context/slice",
  "artifacts": [{"path": "docs/ddd/README.md", "lifecycle": "active", "validation": "validated", "availability": "available", "state": "current"}],
  "status": "partial",
  "changed_artifacts": [],
  "findings": ["bounded evidence gap"],
  "handoff": "none",
  "stop": {"reason": "evidence gap", "owner": "ddd-discover", "action": "collect one example"},
  "invalidated_stages": [],
  "evidence": [],
  "claims": [],
  "provenance": [],
  "assumptions": [],
  "open_questions": ["which owner validates the policy?"],
  "allowed_paths": ["docs/ddd/"],
  "return_to": "ddd",
  "extensions": {}
}
```

A non-`none` handoff is one complete request object; a terminal result with `handoff: none` and an objective/scope/artifacts echo must equal the prior request's objective, scope, and artifact inventory. A non-`none` stop is one bounded string/object. Unknown fields that affect routing are rejected rather than repaired.

## Optional implementation-gate envelope

The optional transport extension is carried under `extensions.ddd-implementation-gate-v1`; it is not persisted inside an authoritative adoption artifact. It is one increment only. `ratification` is a state object; an authorized state requires the complete record and an accepted revision set equal to `authoritative_revisions`.

```json
{
  "extensions": {
    "ddd-implementation-gate-v1": {
      "version": "ddd-implementation-gate-v1",
      "increment_id": "stable-id",
      "target": {"repository": "repository identity", "runtime": "runtime identity", "baseline_revision": "exact repository revision"},
      "owner": "named implementation owner",
      "outcome": "one bounded outcome",
      "in_scope": ["one named behavior"],
      "out_of_scope": ["product/runtime changes"],
      "return_on_conflict": "ddd-tactical",
      "acceptance_signals": ["observable signal"],
      "containment": ["stop/rollback limit"],
      "documentation_readiness": "ready",
      "increment_gate": "authorized",
      "accepted_assumptions": [],
      "deferred_questions": [],
      "out_of_scope_questions": [],
      "question_dispositions": [{"id": "Q-001", "disposition": "resolved", "status": "resolved", "issue": "later hypothesis candidate", "impact": "no impact on this increment", "owner": "named product owner", "action": "record as later hypothesis", "affected_artifacts": [], "revisit_trigger": "next publishing increment"}],
      "ratification": {
        "state": "authorized",
        "record": {
          "decision": "authorized",
          "owner": "named decision owner",
          "date": "YYYY-MM-DD",
          "increment_id": "stable-id",
          "target_repository": "repository identity",
          "target_runtime": "runtime identity",
          "baseline_revision": "exact repository revision",
          "outcome": "one bounded outcome",
          "in_scope": ["one named behavior"],
          "out_of_scope": ["product/runtime changes"],
          "return_on_conflict": "ddd-tactical",
          "accepted_revisions": [{"path": "docs/ddd/adoption-plan.md", "sections": ["Increment identity and outcome"], "revision": "sha256:<64 lowercase hex digits>", "role": "scope-and-delivery"}],
          "accepted_assumptions": [],
          "deferred_questions": [],
          "out_of_scope_questions": [],
          "question_dispositions": [{"id": "Q-001", "disposition": "resolved", "status": "resolved", "issue": "later hypothesis candidate", "impact": "no impact on this increment", "owner": "named product owner", "action": "record as later hypothesis", "affected_artifacts": [], "revisit_trigger": "next publishing increment"}],
          "acceptance_signals": ["observable signal"],
          "containment_limitations": ["stop/rollback limit"]
        }
      },
      "authoritative_revisions": [{"path": "docs/ddd/adoption-plan.md", "sections": ["Increment identity and outcome"], "revision": "sha256:<64 lowercase hex digits>", "role": "scope-and-delivery"}]
    }
  }
}
```

## Manual fallback and normal transition

Manual fallback returns the exact request object unchanged, names the exact stage, and states that it did not run. Normal transition validates one result, merges nonempty `changed_artifacts` by path into the prior artifact inventory, preserves evidence/claims/provenance/assumptions/questions/allowed paths, and emits one next request with exact objective, scope, and inventory. A malformed result is one bounded protocol-error stop; it is never repaired or emulated.
