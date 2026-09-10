# Greenfield service skeleton

The repository shape for a brand-new consumer service that installs `hdx-domain-kit` as a dependency, derived from the kit's own external-wheel test fixture (`tests/fixtures/external_consumer/` — the only consumer-shaped, independently installable example in the reference repository) for everything outside a domain package, and from [the domain skeleton](domain-skeleton.md) (itself derived from `examples/booking/`, the kit's canonical worked example) for the domain package's own internal layout. Confirm this shape against the installed kit version during target preflight; treat a mismatch as a stop per [the bootstrap reference](../references/bootstrap.md).

Use only when bootstrapping is approval-gated and approved for this run — never create these files speculatively.

## Repository layout

`uv init`'s default **application** template places source under `src/<service_name>/` with a `uv_build` backend — the same shape `hdx-domain-kit` itself uses (`src/hdx_domain_kit/`) — rather than the flat, backend-less layout the kit's own `tests/fixtures/external_consumer/` fixture uses only because it is a test fixture, not an installable service. Use the `src/` shape below; do not mix it with the fixture's flat-plus-absolute-import shape (see "Dependency and tooling shape").

```
<service_repo>/
  pyproject.toml            # see "Dependency and tooling shape" below
  alembic.ini                # script_location = migrations; sqlalchemy.url left
                              # empty/placeholder — never a literal connection
                              # string (see bootstrap reference, item 4).
  migrations/
    env.py                    # HDX_DATABASE_URL-first precedence (below);
                               # version_table set to a name scoped to this
                               # service, distinct from the kit's own
                               # hdx_kit.alembic_version.
    script.py.mako
    versions/
      0001_<initial>.py
  src/
    <service_name>/
      __init__.py
      settings.py               # one BaseSettings subclass (bootstrap
                                 # reference, item 1); env_prefix scoped to
                                 # this service; read once at process start.
      auth.py                    # builds the authorizer (bootstrap reference,
                                  # item 2); an AccessPolicyAuthorizer instance
                                  # or an explicit, recorded AllowAll() choice.
      publishing.py               # builds the publisher (bootstrap reference,
                                   # item 3): NoopPublisher() or a real one.
      app.py                    # composition root: builds settings, the
                                 # authorizer, the publisher, and every domain
                                 # definition, then HdxApplication(...).fastapi().
      <domain_package>/          # one or more; see domain-skeleton.md for the
                                  # internal layout (builder.py, handlers.py,
                                  # domain.py, router.py, model/,
                                  # infrastructure/).
  tests/
    unit/                      # no database; aggregate/state-machine logic.
    integration/                # live database; handler/router behavior
                                 # through the kit.
    acceptance/                  # one increment's full observable behavior,
                                  # end to end.
```

## Composition root (`src/<service_name>/app.py`)

Every decision the bootstrap reference names is explicit here, by construction — there is no default that silently fills a gap. Imports are relative to the installed `<service_name>` package — the `src/` layout above and the `uv_build` backend below are what make a relative import like `from .settings import Settings` resolve at a top-level entry point; a flat, backend-less layout does not, and fails with "attempted relative import with no known parent package" instead:

```python
from hdx_domain_kit import HdxApplication

from .settings import Settings
from .auth import authorizer            # or an AccessPolicyAuthorizer instance
from .publishing import publisher        # NoopPublisher() if nothing to deliver yet
from .<domain_package>.domain import definition

settings = Settings()

app = HdxApplication(
    database_url=settings.database_url,
    domains=(definition,),
    authorizer=authorizer,
    query_authorizer=authorizer,   # same instance, both sides, when using
                                    # AccessPolicyAuthorizer for both — see
                                    # bootstrap reference item 2.
    publisher=publisher,
).fastapi()
```

`authorizer=`/`query_authorizer=` are shown explicitly on purpose: never omit `authorizer=` and rely on the kit's `AllowAll()` default without that choice being a deliberate, recorded line in the technical-plan record. Confirm this exact keyword set against the installed kit version first — see [the bootstrap reference](../references/bootstrap.md) item 1 for the full current parameter list.

## `migrations/env.py` — the precedence that matters

The one load-bearing pattern to copy: resolve the database URL from the environment before falling back to the static ini value, and never let ini carry a real connection string.

```python
import os
from alembic import context

config = context.config
database_url = os.environ.get("HDX_DATABASE_URL") or config.get_main_option("sqlalchemy.url")
if not database_url:
    raise RuntimeError("Alembic requires sqlalchemy.url or HDX_DATABASE_URL")
config.set_main_option("sqlalchemy.url", database_url)
```

Use `if not database_url:`, not `if database_url is None:` — with `sqlalchemy.url =` present but left empty as this skeleton instructs, `config.get_main_option("sqlalchemy.url")` returns `""`, not `None`; an `is None` check never fires, `set_main_option("")` still succeeds, and the failure this guard exists to name surfaces later as an opaque engine/DSN error instead. The kit's own fixture can use `is None` only because its `alembic.ini` carries a real URL, so the branch never has to matter there — do not copy that detail along with the precedence pattern.

Pair every `context.configure(...)` call in this file with an explicit `version_table="<service>_alembic_version"` (or similar), distinct from the kit's own `hdx_kit.alembic_version` — this service's migration history must never be mistaken for, or collide with, the kit's.

## Migration run order

Always the kit's infrastructure history first, then this service's own — see [the bootstrap reference](../references/bootstrap.md) item 4 for why:

```bash
export HDX_DATABASE_URL=<resolved-by-settings-or-deployment-environment>
python -m hdx_domain_kit.migrations upgrade   # kit infrastructure
alembic upgrade head                          # this service's own history
```

## Dependency and tooling shape

`pyproject.toml`, mirroring the kit's own conventions (not generic FastAPI convention where the two differ). `hdx-domain-kit` pulls in `sqlalchemy[asyncio]`/`asyncpg`/`alembic` transitively, but this service imports SQLAlchemy directly in its own `infrastructure/models.py` (per [the domain skeleton](domain-skeleton.md)) and invokes the `alembic` CLI directly (see "Migration run order" above) — declare them explicitly rather than relying on a 0.1.0 library's transitive graph for a direct import and a direct CLI entry point:

```toml
[project]
name = "<service-name>"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "hdx-domain-kit==<installed-version>",
    "fastapi>=0.115",
    "sqlalchemy[asyncio]>=2.0.36",
    "asyncpg>=0.30",
    "alembic>=1.14",
    "pydantic-settings",     # version floor: verify against the installed
                              # kit's own pydantic floor at bootstrap time.
    "uvicorn",                # version floor: verify at bootstrap time; not
                               # a kit dependency, so the kit's pyproject.toml
                               # gives no floor to copy.
]

[dependency-groups]
dev = [
    "pytest>=8.3",
    "pytest-asyncio>=0.24",
    "httpx>=0.28",
    "mypy>=1.13",
    "ruff>=0.8",
]

[build-system]
requires = ["uv_build>=0.11.7,<0.12.0"]
build-backend = "uv_build"

[tool.mypy]
python_version = "3.12"
strict = true
plugins = ["pydantic.mypy"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.ruff]
line-length = 100
target-version = "py312"
```

Every floor above except `pydantic-settings` and `uvicorn` is copied from the kit's own `pyproject.toml` (`fastapi>=0.115`, `sqlalchemy[asyncio]>=2.0.36`, `asyncpg>=0.30`, `alembic>=1.14`, and the whole `dev` group); those two have no kit floor to copy from because the kit does not depend on either, so treat them as unverified and confirm current minimums before bootstrapping rather than trusting the number shown here.

Initialize and manage this with `uv` (`uv init`, which produces exactly the `src/` layout and `uv_build` backend above; `uv add <dep>`; `uv add --dev <dep>` or `uv add --group dev <dep>`), matching how the kit manages its own dependencies — do not introduce a second, unrelated dependency manager into a kit-based service without an explicit reason recorded in the technical-plan record.

## Non-negotiable rules

- Source lives under `src/<service_name>/`, matching this skeleton's own composition-root imports and `uv init`'s default; do not flatten it to match `tests/fixtures/external_consumer/`'s layout while keeping this skeleton's relative imports — the two are mutually exclusive, pick one and keep every file consistent with it.
- `alembic.ini`'s `sqlalchemy.url` is never a literal connection string in a committed file — resolved at runtime from the environment only, and the `env.py` guard that enforces this must check falsiness (`if not database_url:`), not `is None`.
- `sqlalchemy[asyncio]`, `asyncpg`, and `alembic` are declared dependencies, not left to arrive transitively through `hdx-domain-kit`, wherever the service imports or invokes them directly.
- `authorizer=` is always passed explicitly; never rely on the unstated `AllowAll()` default.
- `publisher=` is the kit's own `NoopPublisher` when there is genuinely nothing to deliver yet, not a hand-written equivalent — see bootstrap reference item 3 for why the distinction is load-bearing.
- This service's Alembic `version_table` is named distinctly from the kit's own; its migrations never run before the kit's own infrastructure migrations.
- Domain-internal code follows [the domain skeleton](domain-skeleton.md), not this fixture's older hand-written pattern — the kit's own decision records (0016, 0018) name `DomainBuilder` and `domain_runtime_dep` as the intended form for new code, and keep the external-consumer fixture on the older primitive deliberately, to keep exercising it directly rather than only through the ergonomic layer above it.
