# Domain skeleton (canonical layout)

A minimal, host-neutral layout for one bounded-context domain package under an existing `HdxApplication` composition root, matching `examples/booking/` (the kit's canonical worked example) and its acyclic-import decision for the builder — not the human-facing folder-name table in `docs/ARCHITECTURE.md` §5 (`entities/`, `value_objects/`, `commands/`, `queries/`, `events/`, `policies/`, `states/`, `handlers/`), which names a different, equally valid convention the kit does not mechanically enforce either way. Following the worked example is the better default because it is the shape the kit's own decision records (0016, 0018) were written against; do not diff this skeleton against §5 and treat a difference as a defect. Names other than the fixed module names below are illustrative placeholders, not literal requirements. Always confirm the installed kit version's actual layout/API during target preflight; treat a mismatch as a stop, not a silent adaptation.

## A domain with commands/queries (handler domain)

```
<domain_package>/
  __init__.py
  builder.py               # DomainBuilder("<domain-name>") instance ONLY — a
                            # leaf module of its own, so handlers.py and
                            # domain.py stay acyclic (decorating with the
                            # builder must not require importing domain.py).
  handlers.py               # @domain.command / @domain.query handlers;
                             # each: load aggregate, apply one write, drain
                             # events via ctx.audit.record_all, append any
                             # cross-context effect via ctx.outbox.append.
  domain.py                  # imports .handlers (load-bearing: runs the
                              # registrations), builds domain.manifest(),
                              # and assembles the DomainDefinition
                              # (manifest, router, service factories,
                              # optional event_consumers).
  router.py                   # APIRouter; routes depend on
                               # Depends(domain_runtime_dep(domain)); no
                               # per-route try/except — every failure is a
                               # DomainError subclass the kit's mapper
                               # resolves.
  model/
    aggregate.py               # aggregate root (AggregateRoot); plain
                                # Python + typed fields, no persistence
                                # import; protected invariants enforced here.
    commands.py                 # Command subclasses; ClassVar idempotency
                                 # (IdempotencyPolicy) and access label live
                                 # here, on the Command class.
    queries.py                   # Query/ListQuery subclasses + filter/sort
                                  # bindings.
    dtos.py                       # read-side DTOs returned by query handlers.
    events.py                      # DomainEvent subclasses (internal record).
    integration_events.py           # IntegrationEvent subclasses
                                     # (schema_version, stable event_name);
                                     # hand-mapped from domain events, never
                                     # auto-derived.
    status.py                        # StateMachine + the enum it drives,
                                      # behind a private status property on
                                      # the aggregate.
    errors.py                         # error subclasses of the kernel
                                       # taxonomy (e.g. NotFoundError,
                                       # ConflictError subclasses).
    repository.py                     # Protocol(s) for the aggregate/query
                                       # repositories (ports).
  infrastructure/
    models.py                          # SQLAlchemy models for this domain's
                                        # own schema.
    repository.py                      # concrete repository satisfying the
                                        # model/repository.py Protocol(s).
    publisher.py                       # adapter wiring for outbox delivery,
                                        # if the domain needs one beyond the
                                        # kit's default.
```

## A consumer-only domain (eventual consistency)

A domain with no commands/queries of its own has no builder and no router; it declares only an `EventConsumerDefinition` on its `DomainDefinition`:

```
<consumer_domain_package>/
  __init__.py
  consumer.py    # the handler function the kit's idempotent receiver calls
                 # at-least-once; write only through the consumer's own
                 # storage, guarded on (aggregate_version, event_ordinal)
                 # when the write is a re-projection rather than a plain
                 # insert of a new row.
  domain.py       # DomainDefinition(manifest=DomainManifest(name=...),
                  # event_consumers=(EventConsumerDefinition(...),)); imports
                  # the producer's IntegrationEvent class by name, never a
                  # string event-name literal.
  infrastructure/
    models.py       # SQLAlchemy model(s) for this consumer's own projection
                     # table(s) — a consumer domain still owns its schema even
                     # though it has no commands/queries/router of its own.
```

## Non-negotiable structural rules

- `builder.py` is a leaf module containing only the `DomainBuilder(...)` instance — never merge it into `domain.py` or `handlers.py`; doing so reintroduces the import cycle the kit's decision record explicitly avoids.
- The kit owns the transaction boundary; nothing in `handlers.py` or `router.py` calls `session.commit()`/`session.rollback()` directly.
- `router.py` routes depend on the builder object (`Depends(domain_runtime_dep(domain))`), not on a hand-rolled per-router lookup wrapper.
- The domain never imports its own or another domain's `infrastructure/` SQLAlchemy models from `model/`; `model/` stays persistence-free.
- A cross-context effect is an `IntegrationEvent` through `ctx.outbox.append` in the same transaction as the aggregate write, consumed by another domain's `EventConsumerDefinition` — never a synchronous cross-domain aggregate write.

Tests mirror this layout: unit tests exercise `model/aggregate.py` and `model/status.py` with no DB; integration tests exercise `handlers.py`/`router.py` against the kit and a real schema; acceptance tests exercise one full increment's observable behavior end to end.
