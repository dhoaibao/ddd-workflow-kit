# Implementation method

Ordered method for turning one ratified increment into target-repository code.

## 1. Verify the handoff

Read `docs/ddd/implementation-handoff.md` in the target repository. Confirm:

- `authorization.decision: authorized`. `pending` or `declined` stops immediately; do not proceed on an assumption that ratification is imminent.
- Every `authoritative_artifacts[].revision` (`sha256:<64 hex>`) matches the current byte content of its `path`. A mismatch means the authority has changed since ratification; stop and route to `return_on_conflict` rather than implementing against a stale decision.
- Every `authoritative_artifacts[].sections` heading is present, verbatim, as an H2 in its target file.
- `target.repository` and `target.runtime` match the repository and runtime this run is actually operating in.

## 2. Preflight the target

Confirm `hdx-domain-kit` is a declared dependency and locate the existing `HdxApplication` composition root. Resolve `target.placement` to the domain package path named in the handoff. Absence of the kit, absence of a composition root without bootstrap approval, or an unresolvable placement are all bounded stops, not silent inventions.

## 3. Write the owned technical-plan record

Before editing any code, create or update `docs/ddd/implementation/<increment-id>.md` (see [the artifact contract](artifact-contracts.md) and [the template](../assets/implementation-record-template.md)). Restate the ratified in-scope behavior in repository-specific terms: exact files, modules, and the kit constructs each behavior maps to. This record is the only artifact this package owns; it never edits the handoff itself.

## 4. Implement the smallest coherent slice

Map each in-scope behavior to its concrete `hdx-domain-kit` construct using [the mapping reference](hdx-mapping.md) rather than inventing a shape. Implement one slice at a time — the smallest change that makes one acceptance signal true — instead of scaffolding the whole increment speculatively.

## 5. Verify

Run the narrowest applicable tier first (unit, no DB). Add integration or acceptance-tier checks only when the increment's acceptance signals require crossing a real boundary (DB, event bus). An unambiguous in-scope defect is corrected and re-verified; a failure that reveals scope drift, an absent behavior, or a needed domain decision is a stop, not a workaround.

## 6. Report

Update the technical-plan record with the exact trace: files touched, checks run and their outcomes, every gated item proposed and its approval/deferred state, and any deviation from the handoff with its reason. Return the same trace as the result.

## Stop rules

Stop and route to `return_on_conflict` rather than guessing when any of the following hold:

- **Stale revision** — a listed `sha256` no longer matches its target file.
- **Missing H2** — a listed exact heading is absent from its target file.
- **Scope expansion** — the smallest correct implementation would exceed the ratified `in_scope` list.
- **New domain decision** — a mapping choice is not settled by the handoff or the mapping reference (for example, an undecided consistency boundary).
- **Absent behavior** — an in-scope behavior has no attachment point in the current target code.
- **Transaction-ownership violation** — satisfying the request would require a handler to own the transaction boundary directly (for example, calling `session.commit()`) instead of the kit.

A stop names the exact blocker, the evidence, and the `return_on_conflict` target from the handoff; it never silently narrows or widens the ratified scope.
