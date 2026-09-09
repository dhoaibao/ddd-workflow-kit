# Review artifact contracts

## Owned artifact and metadata

`ddd-review` owns exactly `docs/ddd/review.md`. The document begins with one H1 and a metadata table containing `artifact`, `status`, `validation`, `owner`, `scope`, `provenance`, `assumptions`, `open_questions`, and `last_updated`. Lifecycle values are `draft`, `active`, `superseded`, or `archived`; validation values are `unvalidated`, `partially-validated`, `validated`, or `stale`.

The review body distinguishes facts, interpretations, proposals, decisions, and assumptions. Every finding and material gate result names evidence/provenance and owner. A review may annotate other artifact paths in findings but never rewrites them.

## Minimum review schema

The document includes:

- review scope, objective, date, depth, and requested acceptance criteria;
- requested, available, missing, partial, stale, superseded, archived, and out-of-scope artifact inventory;
- DDD-fit result and simpler alternative where relevant;
- gate results for fit, evidence/provenance, lifecycle/schema, vocabulary, strategic-to-tactical prerequisites, adoption safety, and cross-artifact consistency;
- findings grouped by severity;
- stale/conflicting artifacts and complete earliest-stage routing;
- required owner/action, assumptions, open questions, revisit triggers, and next step;
- chat-summary text;
- explicit statement that `ready` is documentation readiness only and no implementation, deployment, migration, or product change was approved or executed.

## Finding schema

Every finding is an object with these required fields:

| Field | Allowed or required meaning |
| --- | --- |
| `severity` | `info`, `follow-up`, `blocked`, or `invalidated` |
| `evidence` | Observable statement, path, example, missing section, or gate result |
| `provenance` | Source/owner/date, or explicit missing-provenance statement |
| `owner` | Accountable stage or project owner |
| `action` | Smallest next action or evidence request |
| `status` | `open`, `routed`, `accepted`, or `resolved` |
| `affected_artifact` | Exact path, or `none` for scope-level issue |
| `earliest_stage` | `ddd-discover`, `ddd-strategic`, `ddd-tactical`, `ddd-adoption`, or `ddd-review` |

A stale-routing entry additionally names all affected dependent paths, earliest stage, owner, action, evidence, and revisit trigger.

## Safe updates and boundaries

1. Inspect `docs/ddd/review.md` before creating or updating it.
2. Preserve existing prose, metadata, links, provenance, lifecycle history, and user ownership.
3. Update only review-owned sections and use additive, reviewable changes.
4. Stop before destructive, structural, ambiguous, colliding, or ownership changes.
5. Never edit another stage's artifact to clear a finding.
6. Refuse product source, tests, configuration, schemas, generated output, deployment files, migrations, path traversal, and unrelated documentation.
7. A mixed request may report a safe review recommendation while refusing forbidden actions; do not claim an artifact write unless it occurred.

## Transition contract

A complete result returns `stage: ddd-review`, status, scope, exact artifact inventory, gate outcomes, complete findings, stale routing, changed paths, assumptions, open questions, next step, and `return_to`. `ready` is scoped documentation readiness only. A non-ready result identifies the exact earliest stage or review-owned action needed next.
