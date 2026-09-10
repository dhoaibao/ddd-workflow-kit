# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- A new `implementation`-class package, `ddd-impl-fastapi-hdx`, the suite's first code-writing package: it consumes a ratified `docs/ddd/implementation-handoff.md`, verifies its authorization/authority revisions/required headings, implements one ratified increment as target-project FastAPI/`hdx-domain-kit` domain code and tests, gates migrations/composition-root edits/dependency changes on explicit per-run approval, and owns exactly one target-project artifact, `docs/ddd/implementation/<increment-id>.md`. It is opt-in; the six existing packages remain the default install.
- `ddd-impl-fastapi-hdx`'s approval-gated greenfield bootstrap path is now a named ordered procedure with an explicit stop before any file is created, backed by two new package-local files: `references/bootstrap.md` (the residue decisions `hdx-domain-kit` deliberately leaves to a consumer's composition root — settings/config layer, authorizer and access-label wiring including the unstated `AllowAll()` default and the `authorizer=`/`query_authorizer=` split, publisher choice, consumer Alembic history/ordering, test tiers, project layout/tooling — plus an explicitly-not-decided list for auth provider, deployment, CI, and observability exporter) and `assets/service-skeleton.md` (the greenfield repository layout, composition root, `migrations/env.py` precedence, migration run order, and `pyproject.toml` shape, derived from the kit's external-wheel test fixture and its own tooling conventions). Four new eval cases cover bootstrap-without-approval, the missing-authorizer decision, a literal-DSN anti-pattern, and consumer-before-kit migration ordering, bringing the package to 16 eval cases.
- A release-root `PACKAGES` manifest (`name<TAB>class<TAB>label`, class `document` or `implementation`) naming every shipped package's class; `scripts/build-release.sh` now copies it into the release archive.
- `install.sh --skill NAME[,NAME...]` (also accepts `--skill all`) plus an interactive multi-select prompt for optional implementation-class packages. Document-class packages always install; `--skill`/the prompt only add or remove optional implementation-class packages, an update with no `--skill` preserves the prior selection, and deselecting a package removes only its exact recorded link. `scripts/test-installer.sh` gains default/`--skill`/update/deselect/unknown-package/archive-listing cases for the new selection path.
- `scripts/validate-skills.py` now parses `PACKAGES`, requires its exact 1:1 correspondence with `skills/` directories, and asserts that every implementation-class package's `SKILL.md` states its write boundary and approval gates.
- Foundation tactical rules for aggregate design: reference other aggregates by identity, keep one aggregate per transaction, use a domain-question tie-breaker (whose job is it to keep data consistent) to choose transactional versus eventual consistency, resolve dependent aggregates from the application service rather than inside the aggregate, and name the accepted reasons to break the one-aggregate-per-transaction rule.
- A new `docs/foundation/03-tactical-design.md` "Coordinating across boundaries" section distinguishing domain events from integration events, and naming the transactional outbox and saga/process-manager patterns behind the existing "coordinated asynchronously or by a higher-level process" phrase.
- Foundation strategic rules: a bounded context's public interface (commands, queries, events) as the expensive-to-change contract neighboring contexts depend on; Partnership and Big ball of mud added to the context-map relationship list, and Published language split out of the combined Open host service bullet, aligning the list with the relationship patterns of the DDD Reference context-mapping chapter.
- Glossary entries for big ball of mud, integration event, partnership, and process manager (saga); references for Vaughn Vernon's Effective Aggregate Design, the microservices.io saga pattern, and the ddd-crew context-mapping and bounded-context-canvas references.

### Changed

- Made the suite's write-boundary and "documentation-only" claims class-scoped instead of suite-wide in `README.md`, `AGENTS.md`, `docs/skill-design/README.md`, `docs/skill-design/skills-and-routing.md`, `docs/skill-design/portability.md`, and `docs/skill-design/artifact-contracts.md`: the six `document`-class packages remain documentation-only and runtime-neutral, while the new opt-in `implementation`-class package may write target-repository code under its own approval-gated boundary.
- Closed two implementer-facing gaps in the tactical/adoption contracts: `ddd-tactical`'s context-model template names an explicit `Consistency boundary` for each invariant, and `ddd-adoption`'s adoption-plan template names a `Target placement` (module/package/path) plus a conditional architecture-fit note for a new boundary/deployable.
- Collapsed `implementation-handoff-v1`'s literal duplication: `authorization` now records only the human `decision`, `owner`, and `date`; every scope, target, and evidence field (including the new `target.placement`) is recorded exactly once at the top level instead of twice, shrinking the template from 102 to 67 lines with no loss of tamper-detection strength. Synced `docs/skill-design/artifact-contracts.md`, `skills/ddd/SKILL.md`, `skills/ddd/references/artifact-contracts.md`, and `scripts/validate-skills.py`'s materialized-fixture gate-binding checks; regenerated the BonVoye-shaped fixture's `adoption-plan.md`, `models/storytelling-experience.md`, `review.md`, and `implementation-handoff.md` (pre/post) with recomputed `sha256` authority revisions.

## [0.3.0] - 2026-09-10

### Added

- Lean decision-driven DDD workflow across all six packages: one bounded increment, conditional artifacts, lean metadata, exception-based review, a consolidated decision queue, explicit human ratification, and revision-bound `implementation-handoff-v1` authorization.
- Local sanitized BonVoye-shaped redesign evaluation report covering one Storytelling Experience context, seven deterministic fixture scenarios, pre/post-authorization artifact profiles, and static-validation limitations.

### Changed

- Moved the four implemented plan files (`ddd-adoption`, `ddd-review`, `ddd`, `lean-workflow-redesign`) from `docs/plans/active/` to `docs/plans/complete/`, updated `docs/plans/README.md` links accordingly, and widened `scripts/validate-skills.py`'s implementation-handoff guard to resolve the plan across both directories and fail loudly if neither exists.
- Preserved `ddd-routing-v1` compatibility while adding the `ddd-implementation-gate-v1` extension; legacy target artifacts remain readable and documentation-only/runtime-neutral boundaries remain enforced.
- Closed authorization-boundary gaps with exact gate schemas, normalized logical authority paths, typed uncertainty routing, separately fielded implementation/decision owners (consistent across adoption, review, gate, and handoff), durable declined-decision markers, immutable pre/post fixture transitions, and exact authorized-index next actions.

## [0.2.0] - 2026-09-10

### Added

- A first-class `shared` install target for the global or project-local `.agents/skills` directory, with physical-link deduplication when compatible named agents share that destination.
- Dependency-free Bash 3.2 interactive arrow selectors for agent targets and scope, including multi-select target toggles and terminal-state restoration.
- Full and registration-scoped uninstall flows with confirmation-by-default, shared-destination preservation, exact-link safety checks, and rollback protection.
- Changelog-backed release-note extraction for tag releases, preserving the matching version section as the complete GitHub release description.

### Fixed

- Interactive Project uninstall now lists all project and explicit-path registrations; partial uninstall preflights only links whose last registration is removed, preserves authoritative registration metadata across updates, normalizes explicit paths, refuses legacy relative records, and keeps an independent full-uninstall rollback snapshot.

## [0.1.2] - 2026-09-10

### Fixed

- Interactive project-scope selection in `install.sh` now assigns the scope before registering, instead of failing with `internal: invalid scope`; a new pseudo-TTY regression case in `scripts/test-installer.sh` covers the prompt flow end to end.

## [0.1.1] - 2026-09-10

### Added

- Project changelog in Keep a Changelog format, exposed through the README documentation list.
- Contributor working rule requiring a `CHANGELOG.md` update before any commit step, recording pending changes under `Unreleased`.

## [0.1.0] - 2026-09-10

### Added

- Six portable, documentation-only DDD skill packages — the `ddd` orchestrator plus the `ddd-discover`, `ddd-strategic`, `ddd-tactical`, `ddd-adoption`, and `ddd-review` stages — routed one stage at a time along the canonical `ddd-discover → ddd-strategic → ddd-tactical → ddd-adoption → ddd-review` flow, each writing only its owned sections of `docs/ddd/` artifacts and never touching product code.
- Domain-Driven Design foundation and skill-design documentation under `docs/`, including language-neutral concepts and evidence discipline, per-package contracts and workflows, quality gates, portability rules, and artifact templates with additive ownership boundaries.
- Deterministic package validation via `scripts/validate-skills.py` and a recorded suite of 59 evaluation cases (29 phase-0 carried forward, 30 phase-4 live), with documented limitations: static validation covers repository conventions only and live results are model- and host-dependent.
- A checksum-verified `curl` installer that downloads a release into a versioned cache at `~/.ddd-workflow-kit/skills` and symlinks packages into agent skill directories, a `ddd-workflow-kit` manager with `install`, `update`, and `version` commands, and tag-triggered release automation.

[Unreleased]: https://github.com/dhoaibao/ddd-workflow-kit/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/dhoaibao/ddd-workflow-kit/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/dhoaibao/ddd-workflow-kit/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/dhoaibao/ddd-workflow-kit/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/dhoaibao/ddd-workflow-kit/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/dhoaibao/ddd-workflow-kit/releases/tag/v0.1.0
