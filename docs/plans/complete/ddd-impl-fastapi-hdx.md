# Plan: implement `ddd-impl-fastapi-hdx`

## Current status

`ddd-impl-fastapi-hdx` is implemented at `skills/ddd-impl-fastapi-hdx/`, package-validated, and independently reviewed (READY WITH FOLLOW-UPS across two review rounds; all blocking findings fixed and re-verified). It is the first implementation-class package in the suite. The six existing packages (`ddd`, `ddd-discover`, `ddd-strategic`, `ddd-tactical`, `ddd-adoption`, `ddd-review`) stay the default install and stay documentation-only. An end-to-end trial against a scratch consumer FastAPI/`hdx-domain-kit` repository remains out of scope for this increment and needs separate user approval.

## Purpose and boundaries

`ddd-impl-fastapi-hdx` consumes a ratified `docs/ddd/implementation-handoff.md` and implements that one increment in a target Python/FastAPI repository built on `hdx-domain-kit`. It is opt-in (installed only when a user selects it) and it is the only package in the suite that writes to a target repository's product source and tests.

Write boundary in the target repo:

- Autonomous: domain code and tests for the one ratified increment.
- Approval-gated per run: database migrations, composition-root edits, and dependency/config changes.
- Never: `git commit`, `git push`, or running a migration against a live database.

It owns exactly one target-project artifact, `docs/ddd/implementation/<increment-id>.md` — a repo-specific technical plan plus a trace of files touched, checks run, gated items, and deviations. This is namespaced under `implementation/` so it never collides with `ddd`-owned `docs/ddd/implementation-handoff.md`.

It must not: modify the document workflow stages or the `ddd-routing-v1`/`ddd-implementation-gate-v1` transport, publish a release, edit `hd-domain-kit` (read-only upstream reference), widen scope beyond the ratified handoff, or silently reinterpret a declined/ambiguous authorization.

## Entry gate

Require a ratified `docs/ddd/implementation-handoff.md` in the target repo. Verify, in order:

1. `authorization.decision: authorized` (not `pending`, `declined`, or absent).
2. Every listed `sha256` authority revision matches the current byte content of its target file.
3. Every listed exact H2 heading is present in its target file.
4. `target.repository` and `target.runtime` match the actual target repo/runtime.

Any mismatch, absence, or ambiguity is a bounded stop routed to the handoff's `return_on_conflict`. The package never reconstructs or guesses a missing/stale handoff.

## Target preflight (existing composition root)

MVP requires an existing `HdxApplication` composition root in the target repo. Bootstrapping a brand-new application is an approval-gated conditional path, not the default. Preflight confirms `hdx-domain-kit` is present in the target's dependencies and that the declared `target.placement` resolves to a real or creatable domain package path before any code is written.

## Mapping reference (`hdx-domain-kit`)

- Bounded context → domain package with its own DB schema and `DomainBuilder`/`DomainDefinition`.
- Consistency boundary → aggregate; one aggregate per transaction.
- Command → `Command` + `@domain.command`.
- Query → `Query`/`ListQuery` + DTO + filter/sort bindings.
- Domain event → `DomainEvent` + `ctx.audit.record_all`.
- Cross-context effect → `IntegrationEvent` (schema_version, stable name) + `ctx.outbox.append` (never a second aggregate write).
- Transitions → `StateMachine` + private status property.
- Failure semantics → error subclass of the kernel taxonomy; no per-route try/except.
- Concurrency → `Versioned` + `optimistic_update`; `get_for_update` only on demand.
- Idempotency → `IdempotencyPolicy`.
- Authorization → `access` label.
- Eventual consistency → consumer domain + `EventConsumerDefinition`.
- Acceptance → unit (no DB) / integration / acceptance tiers.
- `target.placement` → the domain package path.

hdx-domain-kit is unpublished/moving (0.1.0); the reference cites decisions and relies on target-repo preflight rather than hardcoded API assumptions.

## Ordered implementation phases

1. **Package classes.** Add root `PACKAGES` manifest (`name<TAB>class<TAB>label`, class in `{document, implementation}`); extend `scripts/validate-skills.py` to parse it, require exact 1:1 correspondence with `skills/` directories, validate class/label, add `ddd-impl-fastapi-hdx` to `PACKAGE_REQUIREMENTS` (required assets, `minimum_evals: 10`), and assert every implementation package's `SKILL.md` states its write boundary and approval gates. Update `scripts/build-release.sh` to copy `PACKAGES` into the release archive.
2. **Write the package.** `skills/ddd-impl-fastapi-hdx/SKILL.md` (scope/boundary, entry gate, target preflight, workflow, gated effects, stop-and-return, result contract), `references/implementation-method.md`, `references/hdx-mapping.md`, `references/artifact-contracts.md`, `assets/implementation-record-template.md`, `assets/domain-skeleton.md`, and `evals/evals.json` (>=10 cases).
3. **Optional install.** `install.sh` reads `PACKAGES`; default `SELECTED_SKILLS` is every `document`-class row; add `--skill NAME[,NAME...]` (including `--skill all`) and an interactive multi-select step for `implementation`-class rows; deselection removes only the exact recorded link (same safety as a deleted skill); persist selection in `manifest.json` and honor it on `--update`; add `PACKAGES` to both archive allowlists (the installer's own `validate_archive_listing` and the generated manager's embedded `validate_archive`). `scripts/test-installer.sh` gets new cases for default/explicit/update/deselect/unknown-skill/archive-listing behavior.
4. **Docs sync.** `docs/skill-design/skills-and-routing.md` (new "Implementation packages" section), `portability.md` (document vs. implementation scope split), `artifact-contracts.md` (name the impl-owned artifact path), `docs/skill-design/README.md` (class-scoped release boundary), `README.md` (package table plus optional stack-pack install), `AGENTS.md` (documentation-only boundary becomes class-scoped), `CHANGELOG.md` under `[Unreleased]`, `docs/plans/README.md` roadmap entry.

## Ownership and handoffs

`ddd-impl-fastapi-hdx` owns only `docs/ddd/implementation/<increment-id>.md` in the target repo, plus the domain code/tests for the ratified increment. It never edits `docs/ddd/implementation-handoff.md` or any other `docs/ddd/*` document-workflow artifact. On scope expansion, a new domain decision, an absent behavior, or a stale/mismatched handoff, it stops and returns to `return_on_conflict` rather than guessing.

## Evidence and safe-update invariants

- Document packages stay documentation-only and runtime-neutral; `ddd-impl-fastapi-hdx` is the only code-writing package and declares that in its `SKILL.md`.
- Package-local relative links only; exactly one H1 per Markdown file; no absolute host paths or agent/vendor names anywhere under `skills/`.
- Default install set is unchanged for existing users; no existing link is repointed or removed without an exact recorded-target match.
- Migrations, composition-root edits, and dependency/config changes are approval-gated every run; the package never commits, pushes, or runs a migration against a database.

## Verification

1. `python3 scripts/validate-skills.py` passes and reports 7 packages plus the `PACKAGES` manifest check.
2. `bash scripts/test-installer.sh` passes, including the new selection cases.
3. `bash scripts/build-release.sh /tmp/ddd-rel` then installing with `--source-dir` into a temp `HOME`: default yields exactly 6 symlinks, `--skill ddd-impl-fastapi-hdx` yields 7, update preserves the selection, deselect removes exactly one link.
4. `rg -n "documentation-only" README.md AGENTS.md docs/` shows no remaining unqualified suite-wide claim.
5. `CHANGELOG.md` `[Unreleased]` records the new package class, installer flag, and validator gate.

## Extension: greenfield bootstrap residue (approved follow-on)

The MVP's target preflight already named bootstrapping a brand-new `HdxApplication` as an approval-gated conditional but left it unfulfilled — no reference or asset backed it. This follow-on closes that gap, greenfield only (no retrofit of an existing non-`hdx-domain-kit` FastAPI app), inside the same package (no new package, no `PACKAGES`/installer/validator-class changes, no change to the entry gate).

**Added:**

- `references/bootstrap.md` — the residue decision list for a brand-new consumer repository: settings/config layer (no `BaseSettings` anywhere in the kit despite the README composition example referencing `settings.database_url`), authorizer wiring (the unstated `AllowAll()` default when `authorizer=` is omitted, and the `authorizer=`/`query_authorizer=` split `AccessPolicyAuthorizer` needs to cover both commands and queries), publisher choice (`NoopPublisher` recognized by `isinstance`, not by behavior), consumer Alembic history and migration ordering (kit infrastructure first, consumer's own second; never a literal DSN in a committed `alembic.ini`), test tiers (unit/integration/acceptance mirroring the kit's own split), and project layout/tooling (`uv`, `[dependency-groups]`, `mypy --strict`). Closes with an explicitly-not-decided list (auth provider behind `X-Actor-Id`, deployment, CI, observability exporter) returned to the user rather than prescribed.
- `assets/service-skeleton.md` — the greenfield repository tree, composition root shape, `migrations/env.py` HDX_DATABASE_URL-first precedence, migration run order, and `pyproject.toml` shape; derived from the kit's `tests/fixtures/external_consumer/` (the only consumer-shaped, independently installable example) for everything outside a domain package, and from `assets/domain-skeleton.md`/`examples/booking/` for a domain package's own internals — explicitly not from the fixture's older hand-written handler/router pattern, which decisions 0016/0018 record as intentionally kept on the primitive rather than the ergonomic (`DomainBuilder`/`domain_runtime_dep`) layer new code should use.
- `SKILL.md`'s target preflight gained a named, ordered bootstrap procedure (confirm no composition root exists → read the residue decisions → propose the exact plan and file tree → **stop for explicit approval before any file is created** → only then scaffold) and links to both new files.
- Four new eval cases (16 total): bootstrap attempted without explicit approval, a composition root accepted with no authorizer (must surface the `AllowAll` default as a decision), a scaffold copying a literal DSN, and consumer migrations run before the kit's own.

**Also folded in** (accepted, non-blocking follow-ups from the MVP's round-2 review): `domain-skeleton.md` now names `examples/booking/` explicitly rather than an unqualified "documented folder convention"; its consumer-only skeleton gained `infrastructure/models.py`; `README.md` now states package selection is recorded once per local install state, not per destination; `test-installer.sh`'s legacy-manifest regression case now copies only `install.sh`/`VERSION`/`PACKAGES`/`skills/` instead of the whole repository (including `.git`).

**Verification:** `python3 scripts/validate-skills.py` (7 packages + manifest), `bash scripts/test-installer.sh` (all 11 sections), a full `build-release.sh` + `--source-dir` install (6 default / 7 with `--skill ddd-impl-fastapi-hdx`, package contents match archive), forbidden-pattern and literal-DSN/absolute-host `rg` scans over the new/edited files (none found), and relative-link resolution for every new cross-reference — all re-run fresh after these changes.
