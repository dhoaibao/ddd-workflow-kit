<!-- b-init-managed:start -->
## Repository Purpose

This repository maintains a reusable, language- and framework-neutral Domain-Driven Design skill set: foundation and design guidance under `docs/`, plus portable executable skill packages under `skills/`.

## Project Operating Guide

### Architecture and change map

- Put stage-specific instructions, assets, references, and evaluation cases in the owning package under `skills/<skill-name>/`; each package is centered on `SKILL.md`.
- Use `docs/foundation/` for DDD foundations, `docs/skill-design/` for package contracts and workflows, and `docs/plans/` for stages that are planned but not implemented.
- Update the repository `README.md` when package availability or documented status changes. `scripts/validate-skills.py` is the repository's deterministic validation entry point.

### Canonical sources and required change flow

- `SKILL.md`, package-local `assets/`, `references/`, and `evals/evals.json` are the source documents for each portable skill; keep their links and evaluation inputs synchronized when changing a package.
- The implemented release is documentation-only and currently covers `ddd-discover`, `ddd-strategic`, and `ddd-tactical`. The orchestrator, adoption, and review stages remain planned; do not claim them as implemented without their packages and validation.
- Target-project modeling artifacts belong under a target project's `docs/ddd/` when a skill is run; this repository's package files describe that behavior and are not product source.

### Project-specific constraints and boundaries

- Keep the skill packages portable and runtime-neutral. The validator enforces package-local relative links, required assets and evals, and forbidden host- or machine-specific references.
- Preserve the documentation-only boundary for skill effects: implemented skills may update only owned target-project `docs/ddd/` artifacts and must not edit target-project product source, tests, deployment configuration, or runtime behavior.
- Treat static validation as repository-convention coverage only; it does not establish host compatibility or live model/host evaluation.

## Verification

- `python3 scripts/validate-skills.py` — validates package frontmatter, links, assets, evaluation cases, tactical contracts, and runtime-neutral paths.
- Gap: no separate repository test, lint, format, type-check, or CI command is present in the repository evidence.
<!-- b-init-managed:end -->
