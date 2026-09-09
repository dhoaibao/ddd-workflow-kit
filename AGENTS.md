<!-- b-init-managed:start -->
## Repository Purpose

This repository maintains a reusable, language- and framework-neutral Domain-Driven Design skill set: foundation and design guidance under `docs/`, plus portable executable skill packages under `skills/`.

## Project Operating Guide

### Architecture and change map

- Put stage-specific instructions, assets, references, and evaluation cases in the owning package under `skills/<skill-name>/`; each package is centered on `SKILL.md`.
- Use `docs/foundation/` for DDD foundations, `docs/skill-design/` for package contracts and workflows, and `docs/plans/` for implementation history and roadmap.
- The six packages currently shipped are `ddd`, `ddd-discover`, `ddd-strategic`, `ddd-tactical`, `ddd-adoption`, and `ddd-review`; keep package links and status synchronized with `README.md`.
- `scripts/validate-skills.py` is the repository's deterministic validation entry point.

### Canonical sources and required change flow

- `SKILL.md`, package-local `assets/`, `references/`, and `evals/evals.json` are the source documents for each portable skill; keep their relative links and evaluation inputs synchronized when changing a package.
- The implemented release is documentation-only: focused stages own their documented `docs/ddd/` artifacts, while `ddd` owns routing/status state and `ddd-review` owns review state. Use the package-local contracts and templates as the source of truth for ownership.
- Target-project modeling artifacts belong under a target project's `docs/ddd/` when a skill is run; this repository's package files describe that behavior and are not product source.
- Update `README.md` and relevant roadmap/evaluation records when package availability or documented status changes.

### Project-specific constraints and boundaries

- Keep the skill packages portable and runtime-neutral. The validator enforces package-local relative links, required assets and evals, and forbidden host- or machine-specific references.
- Preserve the documentation-only boundary for skill effects: implemented skills may update only owned target-project `docs/ddd/` artifacts and must not edit target-project product source, tests, deployment configuration, migrations, generated output, or runtime behavior.
- Preserve additive ownership and evidence/provenance boundaries; do not silently rewrite user-authored artifacts or treat a review result as implementation, deployment, migration, or release approval.
- Treat static validation as repository-convention coverage only; it does not establish host compatibility or live model/host evaluation.

## Verification

- `python3 scripts/validate-skills.py` — validates package frontmatter, links, assets, evaluation cases, tactical contracts, and runtime-neutral paths.
- Gap: no separate repository test, lint, format, type-check, or CI command is present in the repository evidence.
<!-- b-init-managed:end -->
