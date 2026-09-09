# Orchestration artifact contracts

## Versioned request

A request is a JSON-like portable object with `version: ddd-routing-v1` and these required fields:

| Field | Contract |
| --- | --- |
| `stage` | One focused stage name |
| `objective` | One bounded objective |
| `scope` | Identifiable target/domain/context/slice |
| `artifacts` | Artifact records with `path`, `lifecycle`, `validation`, and `availability`; empty list is explicit absence |
| `evidence` | Evidence records |
| `claims` | Claim-type-aware records |
| `provenance` | Sources, owners, dates, and validation context |
| `assumptions` | Explicit assumptions |
| `open_questions` | Unresolved questions |
| `allowed_paths` | Documentation boundary and ownership constraints |
| `return_to` | `ddd` or named caller |

The request is valid only when all required fields are present and routing-affecting values are known. Manual fallback returns the exact original object without normalization.

## Versioned result

A result has `version`, `stage`, `status`, `changed_artifacts`, `findings`, `handoff`, `stop`, `invalidated_stages`, `evidence`, `claims`, `provenance`, `assumptions`, `open_questions`, `allowed_paths`, and `return_to`. `changed_artifacts` uses the same artifact-record schema as `artifacts`; `handoff` is one complete request or `none`; `stop` is one bounded reason/owner/action object or `none`.

The orchestrator preserves evidence, claims, provenance, assumptions, open questions, artifact records including path/lifecycle/validation/availability, and allowed paths from a valid result. Invalidation preserves lifecycle and changes validation to `stale` for affected dependents. It may add routing metadata and stale state but cannot rewrite those values.

## Routing state

Routing state records current stage, objective, scope, consumed result identity, pending request, invalidated stages in canonical order, stale dependent paths, findings, and next action. Unknown or malformed state stops with a protocol finding. The state does not own focused artifacts.

## Index ownership

The only target artifact the orchestrator may update is `docs/ddd/README.md`, and only its routing/status sections. The canonical index contains:

1. project/domain scope;
2. current status;
3. artifact index;
4. active contexts;
5. validation summary;
6. open questions;
7. provenance policy;
8. safe-update policy;
9. latest review link and findings.

`ddd` owns routing/status markers. `ddd-review` owns the latest review link and findings marker. Preserve all other content and never replace the index wholesale.

## Boundary

No request or result grants permission to edit product source, tests, configuration, schemas, generated output, deployment files, migrations, or unrelated docs. The orchestrator passes allowed paths through unchanged and refuses outside-scope requests.
