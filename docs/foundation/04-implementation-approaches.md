# 4. Implementation approaches

DDD describes modeling and collaboration. It does not require a particular deployment style, programming language, database, or framework. Select architecture from domain boundaries, operational constraints, team ownership, and expected change.

## Modular monolith

A modular monolith deploys as one unit while keeping contexts or modules separated by code-level boundaries, contracts, and ownership. It can make transactions and local calls simple while allowing gradual extraction later. It still requires discipline: shared tables, unrestricted imports, and a common model can recreate coupling inside one process.

## Separately deployed services

A service boundary can align with a bounded context when independent deployment, scaling, ownership, security, or failure isolation justifies the operational cost. Services require explicit contracts, observability, resilience, versioning, and data ownership. Splitting early can turn ordinary calls and transactions into distributed coordination problems, so a context map should precede a deployment decision.

## Layered, hexagonal, and clean arrangements

These arrangements organize dependencies differently but commonly keep domain policy independent from infrastructure details:

- **Layered:** presentation/application, domain, and infrastructure layers with agreed dependency direction. It is straightforward, but layers can become passive bags of data and procedural services if boundaries are not enforced.
- **Hexagonal (ports and adapters):** the domain/application core exposes ports and external systems implement adapters. This supports substituting persistence or messaging, but adds interfaces that should earn their cost.
- **Clean or dependency-rule arrangements:** concentric or similarly separated boundaries keep policy from depending on mechanisms. Naming and exact layers vary; the useful constraint is controlled dependency direction.

None of these arrangements automatically creates a good domain model. Collaboration, language, boundaries, and explicit rules remain necessary.

## CQRS

**Command Query Responsibility Segregation (CQRS)** separates models or paths for changing state and reading state. It can help when read and write concerns have substantially different shapes, performance needs, or evolution rates. It also introduces synchronization, duplication, and operational complexity. A single model is often sufficient until a concrete pressure appears.

## Event sourcing

**Event sourcing** stores a sequence of domain facts as the primary record from which state is rebuilt. It can support auditability, temporal reconstruction, and event-driven workflows, but requires careful event evolution, replay behavior, snapshots, privacy handling, and operational tooling. Publishing ordinary domain events or using messaging does not by itself mean the system is event-sourced.

## Choosing deliberately

Evaluate an approach against:

- required consistency and transaction scope;
- data ownership and integration contracts;
- deployment and team autonomy needs;
- latency, throughput, and failure isolation;
- audit, retention, privacy, and recovery requirements;
- operational maturity and total cost;
- reversibility of the decision.

Start with the simplest architecture that preserves the important boundaries, and record what evidence would justify a later change.
