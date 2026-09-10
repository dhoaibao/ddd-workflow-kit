# DDD skill-set design

**Status: lean decision-driven redesign implemented for candidate review.** The six packages remain independently copyable, documentation-only, and runtime-neutral. Their shared unit of progress is one bounded implementation increment; artifact generation is progressive and trigger-based.

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

The packages may create or update only owned target-project `docs/ddd/` artifacts and portable result bundles. They never edit product source, tests, configuration, schemas, migrations, deployment files, generated output, or runtime behavior. `ddd` owns the index routing/status and, only after explicit ratification, one `implementation-handoff-v1`.

## Evaluation record

The versioned local sanitized BonVoye-shaped report is [`lean-workflow-redesign-v1-report.json`](../evaluations/lean-workflow-redesign-v1-report.json), backed by its repository-local input and materialized-artifact fixture. It records deterministic fixture evidence only; it does not claim access to an external project, host/model success, or production authorization.

- [Implemented six packages](../../skills/ddd/SKILL.md)
- [Remaining implementation roadmap](../plans/README.md)
