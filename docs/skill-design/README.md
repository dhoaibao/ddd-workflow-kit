# DDD skill-set design

**Status: lean decision-driven redesign implemented for candidate review.** The six `document`-class packages remain independently copyable, documentation-only, and runtime-neutral; their shared unit of progress is one bounded implementation increment, and artifact generation is progressive and trigger-based. One `implementation`-class package, `ddd-impl-fastapi-hdx`, is an explicit opt-in install that writes target-project code for a single ratified increment; see [Skills and routing](skills-and-routing.md#implementation-packages).

## Design goals

- Think rigorously while writing only decision-, behavior-, boundary-, acceptance-, and risk-bearing content.
- Preserve the DDD foundation without copying generic teaching into target artifacts.
- Make one selected increment the unit of adoption, review, ratification, and handoff.
- Keep legacy artifacts readable and preserve additive ownership.
- Separate documentation readiness from implementation authorization.

## Documents

- [Skills and routing](skills-and-routing.md)
- [Lean artifact contracts](artifact-contracts.md)
- [Lean workflows](workflows.md)
- [Quality gates](quality-gates.md)
- [Portability](portability.md)

## Release boundary

The release boundary is class-scoped. `document`-class packages may create or update only owned target-project `docs/ddd/` artifacts and portable result bundles; they never edit product source, tests, configuration, schemas, migrations, deployment files, generated output, or runtime behavior. `ddd` owns the index routing/status and, only after explicit ratification, one `implementation-handoff-v1`. The one `implementation`-class package writes target-project domain code and tests for a single ratified increment, with migrations, composition-root edits, and dependency/config changes approval-gated per run; it owns only its own `docs/ddd/implementation/<increment-id>.md` record and never touches the document-workflow artifacts.

## Evaluation record

The versioned local sanitized BonVoye-shaped report is [`lean-workflow-redesign-v1-report.json`](../evaluations/lean-workflow-redesign-v1-report.json), backed by its repository-local input and materialized-artifact fixture. It records deterministic fixture evidence only; it does not claim access to an external project, host/model success, or production authorization.

- [Implemented six packages](../../skills/ddd/SKILL.md)
- [Remaining implementation roadmap](../plans/README.md)
