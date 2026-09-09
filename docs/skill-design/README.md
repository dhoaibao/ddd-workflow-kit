# DDD skill-set design

**Status: first executable MVP.** `ddd-discover` is implemented as the first portable skill slice; the remaining orchestrator and focused stages are still unimplemented. The MVP produces repository documentation under `docs/ddd/` and a concise chat summary; it must not edit product code.

## Design goals

- Assess whether DDD fits the problem instead of assuming it does.
- Keep domain facts grounded in supplied evidence and clearly label assumptions.
- Separate discovery, strategic design, tactical design, adoption, and review responsibilities.
- Support a guided end-to-end flow through a portable transition protocol while keeping each stage independently invocable.
- Make artifacts versionable, provenance-aware, incrementally validated, and safe to update.
- Remain language- and framework-neutral.

## Documents

- [Skills and routing](skills-and-routing.md): responsibilities, triggers, flow, and handoffs.
- [Artifact contracts](artifact-contracts.md): target-project documents, schemas, lifecycle, validation, and ownership.
- [Workflows](workflows.md): greenfield, brownfield, evidence, questions, and feedback loops.
- [Quality gates](quality-gates.md): fit, modeling, architecture, migration, and completeness checks.

## Non-goals

This design does not choose a programming language, framework, deployment platform, database, or team topology. It does not prescribe microservices, aggregates, CQRS, event sourcing, or any other pattern. It also does not define product behavior or invent facts about a target project.

## First-release boundary

The `ddd-discover` MVP creates or updates only the discovery-owned modeling documents under `docs/ddd/`, preserving existing content and marking uncertainty. The future `ddd` orchestrator owns routing/state only and passes exact stage names plus request/result bundles through the portable transition protocol; it never duplicates focused-stage work. A host that cannot activate a named stage returns the exact manual invocation and unchanged bundle. It must stop for material user decisions, missing evidence, conflicts, or unsafe file changes. Product source, tests, deployment configuration, and runtime behavior are outside this release.

- [Implemented MVP portability notes](portability.md)
- [Implemented skill package](../../skills/ddd-discover/SKILL.md)
