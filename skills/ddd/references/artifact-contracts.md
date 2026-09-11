# Orchestrator artifact contracts

## Index

`docs/ddd/README.md` is mandatory for broad flows and should fit on one screen where practical. Its Status section leads with a plain-language "what's happening" summary and one plain-language next action, with the machine fields demoted into a collapsible block per [the index template](../assets/ddd-readme-template.md). It contains target outcome; selected context and increment; current stage; `documentation_readiness`; `increment_gate`; blocking decision count and queue; exact next human action; current artifact links; and `implementation-handoff.md` or `not authorized`.

`ddd` owns routing/status and authorization sections. `ddd-review` owns only the README `decision-queue` and `latest-review` markers plus `review.md`; `ddd` preserves those markers. Existing user prose and legacy metadata remain intact.

## Lean state compatibility

A `ddd-routing-v1` artifact record may carry optional `state`. Map it deterministically: `working` and `decision-needed` → `draft/unvalidated`; `current` → `active/validated`; `stale` → its prior lifecycle plus `stale` validation; `superseded` → `superseded/stale`. Invalidation preserves lifecycle, sets `state: stale`, and sets legacy validation to `stale`. Legacy records without `state` remain valid.

## Gate extension

`ddd-implementation-gate-v1` is a transport envelope carried under `extensions.ddd-implementation-gate-v1` from adoption through review; it is not persisted inside the adoption authority whose bytes it hashes. It must name stable ID, target repository/runtime, exact baseline, accountable implementation owner, outcome/in-out scope/return contract, acceptance, conditional containment, assumptions/questions, typed question dispositions with a unique id, exact issue text bound to the deferred/out-of-scope/accepted-assumption lists (no orphans, no disposition-less entries), impact/owner/action/affected paths/revisit trigger, readiness, gate, ratification state/record with a human decision owner in its own field (may equal or differ from the implementation owner), and authority revisions. It cannot authorize work by itself.

Each disposition's `status` is legal only for its `disposition`: `blocking`/`invalidating`/`decision-required` allow `open` or `resolved`; `accepted-assumption` and `resolved` require `resolved`; `deferred` requires `deferred`; `out-of-scope` requires `closed`. `blocking`, `invalidating`, and `decision-required` items must be `resolved` before the gate can be `awaiting-ratification` or `authorized`.

`authority-revision-v1` is `sha256:<64 lowercase hex digits>` computed over the exact artifact UTF-8 bytes. Each authority also lists exact H2 section headings. Consumers compare both the digest and section presence; target baseline revision is separate.

## Handoff

`docs/ddd/implementation-handoff.md` is created only when review returns `increment_gate: awaiting-ratification` and a human authorizes that exact increment, moving the gate to `authorized`. It uses `implementation-handoff-v1`, names the accountable implementation owner separately from the human authorization owner, one increment/outcome, target/baseline/placement, exact authoritative artifact paths/sections/revisions/roles, in/out scope, accepted assumptions, typed question dispositions with routing fields, deferred questions, acceptance signals, containment, and `return_on_conflict`. Each of these fields appears exactly once; `authorization` records only the ratifying decision, owner, and date, not a second copy of the scope/target/evidence it ratified.

The handoff is invalid when authorization is missing, a source is stale, a revision differs, or authorities conflict. A changed source never silently updates the handoff.

## Boundary

Routing and handoff records never permit product source, tests, configuration, schemas, migrations, deployment files, generated output, runtime behavior, or unrelated documentation changes. Legacy artifacts are read without destructive migration.
