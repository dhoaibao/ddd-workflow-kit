# Lean orchestration protocol

## Base transport

`ddd-routing-v1` remains the compatibility transport. A request contains `version`, one `stage`, one `objective`, `scope`, `artifacts`, `evidence`, `claims`, `provenance`, `assumptions`, `open_questions`, `allowed_paths`, and `return_to`; it may additionally carry an optional `extensions` object. A result contains the preserved transport fields plus `status`, `changed_artifacts`, `findings`, `handoff`, `stop`, `invalidated_stages`, and the same optional `extensions`. For a nonterminal result, an optional objective/scope/artifacts echo must be complete and equal to the next request/handoff; for a terminal result with `handoff: none`, that echo must equal the prior request. Legacy results may omit the echo, in which case the orchestrator performs the documented merge/preservation. The base `ddd-routing-v1` shape remains valid without extensions.

A stage request is valid only when its required entry evidence is present. A malformed request/result produces a bounded protocol stop; it is never repaired or simulated.

## Lean artifact state on the legacy transport

Artifact records retain `lifecycle` and `validation` for `ddd-routing-v1` compatibility and may carry one lean `state`. The mapping is `working`/`decision-needed` → `draft/unvalidated`, `current` → `active/validated`, `stale` → prior lifecycle plus `stale` validation, and `superseded` → `superseded/stale`. Invalidation preserves lifecycle and sets `state` and legacy validation to `stale`; a legacy record without state is preserved unchanged.

## Implementation-gate extension

Adoption and review may carry this optional envelope:

```yaml
extensions:
  ddd-implementation-gate-v1:
    version: ddd-implementation-gate-v1
    increment_id: stable-id
    target:
      repository: repository identity
      runtime: runtime identity
      baseline_revision: exact repository revision
    owner: accountable implementation owner
    outcome: bounded outcome
    in_scope: [one named behavior]
    out_of_scope: [product/runtime changes]
    return_on_conflict: ddd-tactical
    acceptance_signals: [observable signal]
    containment: [stop/rollback limit]
    documentation_readiness: follow-up
    increment_gate: blocked
    accepted_assumptions: []
    deferred_questions: []
    out_of_scope_questions: []
    question_dispositions: []
    ratification:
      state: not-yet-requested
    authoritative_revisions: []
```

The extension is scoped to one increment and is carried under `extensions.ddd-implementation-gate-v1`. It does not authorize product work. Only explicit human ratification can move `increment_gate` from `awaiting-ratification` to `authorized`, and only the orchestrator can create the handoff.

An authority revision uses `authority-revision-v1`: read the exact artifact as UTF-8 bytes, compute lowercase SHA-256, and serialize `revision` as `sha256:<64 lowercase hex digits>`. `sections` lists the exact H2 headings used by the authority. Consumers require both a matching digest and every listed heading; the repository baseline revision is a separate target field. Uncommitted artifacts therefore remain portable and comparable.

## Normal transitions

Validate the result, copy preserved evidence/claims/provenance/assumptions/questions/allowed paths, apply explicit versioned state updates, merge `changed_artifacts` by path into the prior artifact inventory, and emit one next request. Preserve artifact lifecycle and revision identity. Never emit competing requests or silently fill missing facts.

## Manual fallback

When a named stage cannot run, return the exact request object byte-for-byte, the exact stage name, and a statement that it did not run. Do not add timestamps, defaults, status, questions, or reordered arrays.

## Invalidation

Use canonical order `ddd-discover → ddd-strategic → ddd-tactical → ddd-adoption → ddd-review`. Mark affected later artifacts `stale` while preserving their paths, lifecycle, and provenance. Route to the earliest invalidated owner and include evidence, action, owner, and revisit trigger. Any handoff whose authoritative revision no longer matches is invalid and cannot be consumed.

## Index and handoff ownership

`ddd` owns routing/status and authorization markers in `docs/ddd/README.md` and the authorized `implementation-handoff.md`. Review owns only the `decision-queue` and `latest-review` markers in the index plus `review.md`; `ddd` preserves those markers. The index is mandatory for broad flows and is not a substitute for focused artifacts. The handoff references authority; it never duplicates or silently rewrites it.
