# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/dhoaibao/ddd-workflow-kit/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/dhoaibao/ddd-workflow-kit/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/dhoaibao/ddd-workflow-kit/releases/tag/v0.1.0
