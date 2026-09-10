# hdx-domain-kit mapping reference

`hdx-domain-kit` is unpublished and moving (0.1.0). This reference names the decided shape for each DDD concept; it does not hardcode a specific kit API surface. Always confirm the installed kit version's actual API during target preflight before writing code, and treat a mismatch as a stop, not a silent adaptation.

| DDD concept | hdx-domain-kit shape |
| --- | --- |
| Bounded context | A domain package with its own DB schema and a `DomainBuilder`/`DomainDefinition`. |
| Consistency boundary | An aggregate. One aggregate is written per transaction. |
| Command | A `Command` class registered with `@domain.command`. |
| Query | A `Query` or `ListQuery` plus a DTO and explicit filter/sort bindings. |
| Domain event | A `DomainEvent` recorded through `ctx.audit.record_all`. |
| Cross-context effect | An `IntegrationEvent` (versioned with `schema_version`, a stable name) appended through `ctx.outbox.append` — never a second aggregate write in the same transaction. |
| State transition | A `StateMachine` behind a private status property; callers never set status directly. |
| Failure semantics | An error subclass of the kernel error taxonomy; no per-route `try/except` translating errors ad hoc. |
| Concurrency | `Versioned` plus `optimistic_update`; `get_for_update` only when the increment's acceptance signals require pessimistic locking. |
| Idempotency | An `IdempotencyPolicy` `ClassVar` declared on the `Command` class itself. |
| Authorization | An `access` label declared on the `Command`/`Query` class itself. |
| Eventual consistency | A consumer domain with an `EventConsumerDefinition` reacting to the producer's integration event. |
| Acceptance signal tiering | Unit (no DB), integration (real DB/kit), and acceptance (end-to-end behavior) tiers, chosen by what the increment's acceptance signals actually require. |
| `target.placement` | The domain package path the handoff names; code lands there, not in an invented location. |

## Non-negotiable invariants

- One aggregate per transaction. A cross-aggregate effect is an integration event through the outbox, never a second aggregate write in the same transaction.
- The kit owns the transaction boundary. Handlers never call `session.commit()`, `session.rollback()`, or otherwise manage the transaction directly.
- A protected invariant lives on the aggregate that owns it, not in the handler or a service method.
- An undecided mapping (for example, which aggregate owns a disputed invariant) is a stop routed to the handoff's `return_on_conflict`, not a default guess.
