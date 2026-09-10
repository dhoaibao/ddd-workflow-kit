# Implementation handoff

This artifact is owned by `ddd` and is valid only after explicit human authorization for one increment. It is the sole implementation entry point. Do not create it for `current`, `ready`, or `awaiting-ratification` without the complete ratification record. `authority-revision-v1` is `sha256:<64 lowercase hex digits>` over exact artifact UTF-8 bytes; each `sections` value is an exact H2 heading and both digest and heading presence are checked.

```yaml
version: implementation-handoff-v1
authorization:
  decision: authorized
  owner: named decision owner
  date: YYYY-MM-DD
  increment_id: stable-id
  target_repository: repository identity
  target_runtime: runtime identity
  baseline_revision: exact repository revision
  outcome: bounded outcome
  in_scope: [one named behavior]
  out_of_scope: [product/runtime changes]
  return_on_conflict: ddd-tactical
  accepted_revisions:
    - path: docs/ddd/adoption-plan.md
      sections: [Increment identity and outcome, Dependencies and acceptance]
      revision: sha256:<64 lowercase hex digits>
      role: scope-and-delivery
    - path: docs/ddd/models/storytelling-experience.md
      sections: [Outcome and examples, Commands, rules, and transitions, Invariants and current-versus-desired delta]
      revision: sha256:<64 lowercase hex digits>
      role: behavior
    - path: docs/ddd/contexts/storytelling-experience.md
      sections: [Purpose and boundary, Key terms and scenarios]
      revision: sha256:<64 lowercase hex digits>
      role: boundary
  accepted_assumptions: []
  deferred_questions: []
  out_of_scope_questions: []
  question_dispositions:
    - id: Q-001
      disposition: resolved
      status: resolved
      issue: later hypothesis candidate
      impact: no impact on this increment
      owner: named product owner
      action: record as later hypothesis
      affected_artifacts: []
      revisit_trigger: next publishing increment
  acceptance_signals: [observable signal]
  containment_limitations: [stop/rollback limit]
implementation_owner: named implementation owner
increment:
  id: stable-id
  outcome: bounded outcome
target:
  repository: repository identity
  runtime: runtime identity
  baseline_revision: exact repository revision
authoritative_artifacts:
  - path: docs/ddd/adoption-plan.md
    sections: [Increment identity and outcome, Dependencies and acceptance]
    revision: sha256:<64 lowercase hex digits>
    role: scope-and-delivery
  - path: docs/ddd/models/storytelling-experience.md
    sections: [Outcome and examples, Commands, rules, and transitions, Invariants and current-versus-desired delta]
    revision: sha256:<64 lowercase hex digits>
    role: behavior
  - path: docs/ddd/contexts/storytelling-experience.md
    sections: [Purpose and boundary, Key terms and scenarios]
    revision: sha256:<64 lowercase hex digits>
    role: boundary
in_scope: [one named behavior]
out_of_scope: [product/runtime changes]
accepted_assumptions: []
deferred_questions: []
out_of_scope_questions: []
question_dispositions:
  - id: Q-001
    disposition: resolved
    status: resolved
    issue: later hypothesis candidate
    impact: no impact on this increment
    owner: named product owner
    action: record as later hypothesis
    affected_artifacts: []
    revisit_trigger: next publishing increment
acceptance_signals: [observable signal]
containment: [stop/rollback limit]
return_on_conflict: ddd-tactical
```

`authorization.accepted_revisions` must equal `authoritative_artifacts` exactly, including `sections` and `role`, not only path and revision. `target_runtime`, `baseline_revision`, question dispositions, assumptions/questions, acceptance signals, and containment limitations must match the ratified gate exactly. Each disposition names a unique `id` and its exact `issue` text; a `deferred` issue must appear in `deferred_questions` and an `out-of-scope` issue must appear in `out_of_scope_questions`, with no orphan strings in either list. The handoff references authoritative sections instead of copying them.

## Consumer order

1. this handoff;
2. the selected adoption increment;
3. referenced tactical examples, rules, and invariants;
4. referenced context boundary and relationships;
5. explicitly listed vocabulary/strategic sections;
6. existing source/tests;
7. a repository-specific technical plan before code edits.

## Invalidation

The handoff is invalid when authorization is missing, any authority is stale, an exact revision differs, a listed H2 is absent, authorities conflict, required behavior is absent, a new domain decision appears, or scope expands. Return to `return_on_conflict`; do not silently repair the authority set.
