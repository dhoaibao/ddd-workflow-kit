---
name: ddd-impl-fastapi-hdx

description: Implement one ratified DDD increment in a target Python/FastAPI repository built on hdx-domain-kit, from a verified implementation-handoff.md; the only code-writing package in the suite, with named write boundaries and per-run approval gates.
---

# DDD implementation: FastAPI + hdx-domain-kit

Implement exactly one ratified increment from `docs/ddd/implementation-handoff.md` in a target FastAPI repository that uses `hdx-domain-kit`. This package is opt-in and is the sole code-writing member of the suite; every other package stays documentation-only.

## Write boundary

In the target repository this package may autonomously write and edit domain code and tests for the one ratified increment. Database migrations, composition-root edits, and dependency/config changes are approval-gated on every run: propose the exact diff and stop for explicit approval before applying it. It never runs `git commit`, `git push`, or a migration against a live database, and it never edits `docs/ddd/implementation-handoff.md` or any other document-workflow artifact outside its own owned record.

It owns exactly one target-project artifact: `docs/ddd/implementation/<increment-id>.md`, namespaced under `implementation/` so it never collides with the `ddd`-owned `implementation-handoff.md`.

## Entry gate

Require a ratified `docs/ddd/implementation-handoff.md`. Verify, in this order, before touching any code:

1. `authorization.decision: authorized` — `pending`, `declined`, or a missing file is a bounded stop.
2. Every listed `sha256` authority revision matches the current byte content of its named target file.
3. Every listed exact H2 heading is present in its target file.
4. `target.repository` and `target.runtime` match the actual target repository and runtime.

Any mismatch, absence, or ambiguity stops the run and routes to the handoff's `return_on_conflict`; never reconstruct or guess a missing or stale handoff.

## Target preflight

MVP requires an existing `HdxApplication` composition root. Confirm `hdx-domain-kit` is a declared dependency of the target repository and that `target.placement` resolves to a real or creatable domain package path. Bootstrapping a brand-new application is an approval-gated conditional, not the default path — propose the bootstrap plan and stop for approval before creating it.

## Workflow

1. Verify the handoff (entry gate above).
2. Run target preflight.
3. Create or update the owned technical-plan record at `docs/ddd/implementation/<increment-id>.md` before editing code: restate in-scope behavior, name the target files, and list the checks that will be run.
4. Implement the smallest coherent slice using [the hdx-domain-kit mapping](references/hdx-mapping.md): map each in-scope behavior to its concrete kit construct rather than inventing a shape.
5. Run the narrowest useful verification (unit tier first; integration/acceptance tiers when the increment's acceptance signals require them).
6. Update the technical-plan record with the trace of files touched, checks run, gated items proposed/approved, and any deviation from the handoff.

Read [the method](references/implementation-method.md), [the mapping reference](references/hdx-mapping.md), [the artifact contract](references/artifact-contracts.md), [the record template](assets/implementation-record-template.md), and [the domain skeleton](assets/domain-skeleton.md) before writing.

## Gated effects

The following are never applied without explicit per-run approval, even when the increment's scope implies them:

- Database migrations (creating, editing, or running one).
- Composition-root edits (registering a new domain, consumer, or route in the `HdxApplication` root).
- Dependency or configuration changes (package manifests, environment/config files, `hdx-domain-kit` version bumps).
- Bootstrapping a new `HdxApplication` when none exists.

Propose the exact diff and stop; apply only after the user approves it in that run.

## Stop-and-return rules

Stop and return to `return_on_conflict` rather than guessing when:

- The handoff is absent, stale (revision mismatch), or missing a listed H2 heading.
- `authorization.decision` is not `authorized`.
- `target.repository`/`target.runtime` do not match the actual target.
- `hdx-domain-kit` is absent from the target's dependencies, or no `HdxApplication` composition root exists and bootstrap approval was not given.
- The requested change would expand scope beyond the ratified increment, or requires a new domain decision not covered by the handoff.
- An in-scope behavior has no corresponding target-repo code path to attach to (absent behavior).
- A transaction-ownership violation would be required to satisfy the mapping (for example, a handler calling `session.commit()` directly instead of the kit owning the transaction boundary).

## Result

Return the increment id, the exact files touched, the checks run and their outcomes, every gated item proposed and its approval/deferred state, deviations from the handoff, the changed path (`docs/ddd/implementation/<increment-id>.md`), and either "implementation complete for this increment" or a bounded stop naming the exact blocker and `return_on_conflict` target. No result from this package authorizes a second increment, a migration, a commit, or a push.
