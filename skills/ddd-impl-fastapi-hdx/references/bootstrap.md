# Bootstrap reference: greenfield residue decisions

`hdx-domain-kit` decides the domain/CQRS/transaction/audit/outbox shape. A brand-new consumer repository still needs several decisions the kit deliberately leaves to its composition root. This reference names exactly that residue — the gap between "kit installed" and "a running service" — for the greenfield bootstrap path only. It does not restate the kit's README or ARCHITECTURE; read those for wiring detail and treat this file as the decision list layered on top.

Retrofitting bootstrap onto an existing FastAPI application that does not yet use `hdx-domain-kit` is out of scope for this reference; the bootstrap conditional in `SKILL.md` covers greenfield only.

**Provenance:** every item below is anchored to a named decision record (`docs/decisions/NNNN-*.md`) or a named file in the read-only `hdx-domain-kit` reference repository. `hdx-domain-kit` is unpublished and moving (0.1.0) — verify each item against the *installed* version during target preflight before applying it; a mismatch is a stop, not a silent adaptation.

## 1. Settings / configuration layer

**What the kit decides:** nothing. There is no settings module, `BaseSettings` subclass, or configuration primitive anywhere in `hdx-domain-kit` — it reads exactly one variable from the process environment, `HDX_DATABASE_URL` (per decision 0025's "no guessed defaults" fix), and it is read in two places: `HdxApplication.__init__` itself when `database_url=` is omitted, and the migration CLI. Every other value is an explicit keyword-only constructor argument to `HdxApplication` — `domains=`, `publisher=`, `database_url=`/`engine=`, `authorizer=`/`query_authorizer=`, `response_builder=`, `error_status_overrides=`/`extra_error_handlers=`, `worker_config=`/`runner_config=`/`idempotency_config=`, `lifespan=`. Confirm this exact parameter list against the installed version before writing a composition root; it is the kind of detail a moving 0.1.0 library changes without notice.

**What the consumer must decide:** how configuration reaches those constructor arguments. The kit's own README composition example (`## 8. Compose the FastAPI application`) references `settings.database_url` without ever defining `settings` — that is the kit's own doc pointing at consumer-owned code, not an omission to copy literally.

**Failure mode of skipping it:** hardcoding connection strings or secrets directly in the composition root, or re-deriving an ad hoc settings object per module instead of one seam the composition root reads once.

**Decided shape for this reference:** one `pydantic_settings.BaseSettings` subclass, `env_prefix` scoped to the consumer (for example `env_prefix="APP_"`), read once at process start and passed explicitly into `HdxApplication(...)`. Do not rely on the kit finding a prefixed variable itself — the kit reads `HDX_DATABASE_URL` unprefixed, both inside `HdxApplication.__init__` (when `database_url=` is omitted) and in its migration CLI, so a prefixed settings class must still resolve `database_url=` explicitly and pass it in; the prefix does not propagate into the kit.

## 2. Authorizer and access labels

**What the kit decides:** the authorization seam and its fail-closed evaluation order (`kernel/policies/authorization.py`), plus one built-in implementation, `AccessPolicyAuthorizer`, that authorizes commands and queries from an `access` label each `Command`/`Query` class declares.

**What the consumer must decide:** whether to wire an authorizer at all, and if so, which one.

**Failure mode of skipping it:** `HdxApplication`'s `authorizer=` parameter defaults to `AllowAll()` when omitted (`adapters/runtime.py`, `coarse_authorizer=authorizer or AllowAll()`) — an application that never passes `authorizer=` is unauthenticated-by-default, silently, with no error at boot. This is the single highest-value item in this reference precisely because it fails silent rather than loud.

**A second, separate trap inside the same decision:** `AccessPolicyAuthorizer` answers both the command and the query authorization protocols through one `authorize` method, but `HdxApplication` only asks it about the side it is wired to. Passing it as `authorizer=policy` alone authorizes commands only; queries pass through unauthorized regardless of their declared `access` label. The correct wiring, when using this class for both sides, is `authorizer=policy, query_authorizer=policy` (both keyword arguments, the same instance). Decision 0017 records the opt-in, boot-time validation this class runs when wired this way — that validation only ever sees the side(s) it was actually given.

**Required action, not a suggestion:** confirm at target preflight whether the installed kit version's default is still `AllowAll()` (this is a security-relevant claim about a moving library, not a fact to assume from this document), and then make the authorizer choice an explicit line in the technical-plan record — "AllowAll, chosen because `<reason>`" is an acceptable answer; an unexamined default is not.

## 3. Publisher choice

**What the kit decides:** the outbox contract and a `Publisher` Protocol with exactly one shipped implementation, `NoopPublisher`, added by decision 0023 specifically to end every consumer hand-writing its own no-op.

**What the consumer must decide:** where domain integration events go outside the process, if anywhere.

**Failure mode of skipping it:** `publisher=` has no default at all — `HdxApplication(...)` raises without it, so this cannot be silently skipped. The trap is choosing the wrong *kind* of no-op: `NoopPublisher` is the kit's declared class, checked by `isinstance`, and it is what makes the outbox worker's lazy-start condition (decision 0023) recognize "nothing to deliver" and skip starting a polling task at all. A hand-written no-op publisher that behaves identically is invisible to that check — decision 0023's docstring calls this "opt-in by type, not by flag": passing any object that is not literally `NoopPublisher` starts the worker regardless of what that object's `publish` method actually does internally.

**Decided shape for this reference:** if the increment declares no `event_consumers` and needs no outward delivery yet, pass `NoopPublisher()` explicitly, not a hand-written equivalent. The moment a real destination exists, replace it with a publisher of the consumer's own — never make one "temporarily inert" implementation double as both cases.

## 4. Consumer Alembic history and migration ordering

**What the kit decides:** its own Alembic history for the `hdx_kit` infrastructure schema, run through `python -m hdx_domain_kit.migrations upgrade`, using its own `hdx_kit.alembic_version` table. It also refuses to guess a database: `HDX_DATABASE_URL` (or `--database-url`) is required with no fallback DSN, by decision 0025.

**What the consumer must decide:** its own, separate Alembic history for its own domain schema(s), including its own `version_table` name so the two histories cannot collide.

**Failure mode of skipping it:** two concrete anti-patterns, both evidenced in the kit's own external-wheel test fixture (`tests/fixtures/external_consumer/`, kept intentionally minimal to exercise the primitive rather than to serve as a security example):

- `migrations/env.py` reading `sqlalchemy.url` from a static `alembic.ini` instead of the environment: the fixture's `env.py` reads `HDX_DATABASE_URL` first and falls back to `config.get_main_option("sqlalchemy.url")` only if that is unset — copy that precedence, not the fallback.
- `alembic.ini` carrying a literal development connection string (the fixture's own `sqlalchemy.url` line names the kit maintainers' local Postgres instance) — decision 0025 names exactly this pattern (a hardcoded local development DSN reaching a document or template meant for reuse) as a defect it fixed elsewhere. Leave a real service's `alembic.ini` `sqlalchemy.url` empty or a placeholder; the URL is supplied at runtime through the environment.

**Ordering:** kit infrastructure migrations run first, then the consumer's own:

```bash
export HDX_DATABASE_URL=<resolved-from-settings>
python -m hdx_domain_kit.migrations upgrade   # kit infrastructure — always first
alembic upgrade head                          # consumer's own domain schema history
```

Never run the consumer's migrations before the kit's; the kit's infrastructure tables (`hdx_kit.outbox`, `hdx_kit.idempotency_keys`, `hdx_kit.audit_business_history`, and friends) are what the domain code depends on at runtime.

## 5. Test tiers

**What the kit decides:** its own three-tier split, evidenced by its own suite — unit tests need no database at all; integration and acceptance tiers need a live PostgreSQL, configured through `HDX_TEST_DATABASE_URL`.

**What the consumer must decide:** to mirror the same split for the increment's own tests rather than defaulting everything to one tier.

**Failure mode of skipping it:** an all-integration suite that requires a live database for every test, including ones that only exercise aggregate/state-machine logic with no persistence involved — slow, and it hides which failures are genuine domain-logic defects versus environment/wiring problems.

**Decided shape for this reference:** unit tier for the aggregate root and any state-machine/invariant logic with no kit or database involved; integration tier for command/query handlers exercised through the kit against a real schema; acceptance tier for one increment's full observable behavior end to end (HTTP in, database/audit/outbox rows out), mirroring the shape of the kit's own external-wheel acceptance check.

## 6. Project layout and dependency tooling

**What the kit decides:** nothing about consumer project structure — it ships as an installable package (`hdx-domain-kit==<version>`) with no project scaffolding tool or template of its own.

**What the consumer must decide:** the repository layout and dependency-management tooling for a new, independent service.

**Failure mode of skipping it:** inventing a project shape from generic FastAPI convention that conflicts with how `hdx-domain-kit` itself expects a consumer to be laid out (an installed dependency, not a subpackage of the kit) — see [the service skeleton](../assets/service-skeleton.md) for the decided shape, derived from the kit's own external-consumer test fixture (the only consumer-shaped, installable-package example in the reference repository; `examples/booking/` lives inside the kit's own repo and imports from it directly, so it is not a copyable service shape) plus the kit's own `pyproject.toml` tooling conventions (`uv`, `[dependency-groups]`, `mypy --strict` with the Pydantic plugin, `ruff`, `pytest-asyncio` in `auto` mode).

## Explicitly not decided here

These remain named, open decisions returned to the user rather than prescribed by this reference — each is a real choice with more than one reasonable answer, and none is settled by `hdx-domain-kit`'s own decisions:

- **Auth provider behind the actor header.** The kit trusts an `X-Actor-Id` header as given (its own router comments call this the seam a real application replaces); which identity provider populates that header, and how, is entirely a consumer decision.
- **Deployment and containerization.** The kit has no opinion on how the FastAPI process is packaged or run.
- **CI pipeline.** Not addressed by any kit decision; the consumer chooses its own.
- **Observability exporter (OpenTelemetry or otherwise).** The kit emits structured logs (`structlog`) and named composition-time log events; where those logs and any traces/metrics go is unspecified.

An increment that needs one of these decided is a stop, not an inferred default — route it back through the handoff's `return_on_conflict` rather than choosing on the user's behalf.
