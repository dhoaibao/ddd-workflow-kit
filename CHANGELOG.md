# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/dhoaibao/ddd-workflow-kit/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/dhoaibao/ddd-workflow-kit/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/dhoaibao/ddd-workflow-kit/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/dhoaibao/ddd-workflow-kit/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/dhoaibao/ddd-workflow-kit/releases/tag/v0.1.0
