# Artifact contract

This package owns exactly one target-project artifact: `docs/ddd/implementation/<increment-id>.md`, one file per implemented increment. It never edits `docs/ddd/implementation-handoff.md` or any other `docs/ddd/*` document-workflow artifact.

## Required sections

Using [the template](../assets/implementation-record-template.md):

- **Increment identity** — `increment_id`, the handoff path, and the authority revisions it was verified against.
- **Preflight** — `hdx-domain-kit` presence, composition-root location, resolved `target.placement`.
- **Technical plan** — repository-specific restatement of in-scope behavior, named target files/modules, and the kit construct each behavior maps to (written before code changes).
- **Trace** — exact files touched, checks run and outcomes, gated items proposed and their approval/deferred state, and any deviation from the handoff with its reason.
- **Result** — "implementation complete for this increment" or a bounded stop naming the exact blocker and `return_on_conflict` target.

## Naming and collision safety

`<increment-id>` is the exact `increment.id` named in the ratified handoff. This keeps the artifact namespaced under `implementation/` so it can never collide with the `ddd`-owned `docs/ddd/implementation-handoff.md`, and so multiple increments accumulate one record each rather than overwriting a shared file.

## Preservation

Preserve any pre-existing content in `docs/ddd/implementation/<increment-id>.md` from a prior partial run; append/update the trace and result sections rather than discarding prior evidence. Never touch another increment's record.
