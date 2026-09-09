# DDD Workflow Kit

DDD Workflow Kit is a portable, language-, framework-, and runtime-neutral skill suite for evidence-backed Domain-Driven Design work. It is documentation-only: the skills create and review DDD planning artifacts under a target project's `docs/ddd/` boundary, and do not edit product code or approve runtime, deployment, migration, or implementation changes.

## Workflow

The canonical flow is:

`ddd-discover → ddd-strategic → ddd-tactical → ddd-adoption → ddd-review`

Each stage can also be invoked directly when its entry criteria and evidence are satisfied. The `ddd` package routes one stage at a time, preserves request and result records, and returns an exact manual fallback when a host cannot activate the named stage.

| Package | Purpose | Owned output or contribution |
| --- | --- | --- |
| [`ddd`](skills/ddd/SKILL.md) | Route requests and transition state across the workflow without performing focused-stage work. | Routing and status sections of `docs/ddd/README.md` |
| [`ddd-discover`](skills/ddd-discover/SKILL.md) | Establish scope, evidence, vocabulary, DDD fit, and discovery questions. | `docs/ddd/assessment.md`, initial `domain-vision.md`, and discovery contributions to `ubiquitous-language.md` |
| [`ddd-strategic`](skills/ddd-strategic/SKILL.md) | Define evidence-backed subdomains, bounded contexts, language, ownership, and relationships. | `docs/ddd/domain-map.md`, `context-map.md`, `contexts/<safe-slug>.md`, `ubiquitous-language.md`, and strategic sections |
| [`ddd-tactical`](skills/ddd-tactical/SKILL.md) | Model one validated context's behavior, invariants, consistency, integration, and tactical elements. | `docs/ddd/models/<context-slug>.md` and additive tactical sections |
| [`ddd-adoption`](skills/ddd-adoption/SKILL.md) | Plan one bounded, incremental, reversible greenfield or brownfield adoption slice. | `docs/ddd/adoption-plan.md` |
| [`ddd-review`](skills/ddd-review/SKILL.md) | Review DDD artifacts for evidence, lifecycle, boundaries, consistency, safety, and documentation readiness. | `docs/ddd/review.md` |

## Guarantees and boundaries

- **Evidence and provenance:** claims distinguish current behavior, desired meaning, required obligations, facts, interpretations, proposals, decisions, and assumptions. Sources, owners, validation state, open questions, and revisit conditions remain visible.
- **Bounded stops:** missing evidence, unsafe paths, conflicting claims, unclear ownership, invalidated boundaries, and unavailable stages produce a bounded stop or an earliest-owner handoff rather than invented facts.
- **Additive ownership:** each focused stage owns only its documented artifact sections; existing material is preserved, and the orchestrator does not take ownership from focused stages.
- **Documentation-only operation:** the suite does not edit product source, tests, schemas, configuration, generated output, deployment files, migrations, or runtime behavior.
- **Review scope:** a `ready` review means documentation readiness for the stated scope only. It is not implementation, deployment, migration, data-cutover, or release approval.

## Install with curl

The first-phase installer supports Linux and macOS with Bash 3.2 or newer. It installs a versioned shared cache at `~/.ddd-workflow-kit/skills` and creates symlinks in the selected agent skill directory; it does not clone this repository or modify shell profiles.

Interactive installation (prompts through `/dev/tty`):

```bash
curl -fsSL https://raw.githubusercontent.com/dhoaibao/ddd-workflow-kit/main/install.sh | bash
```

For automation, provide one or more agents and a scope. The supported agent names are `claude`, `codex`, `opencode`, `antigravity`, and `pi`:

```bash
curl -fsSL https://raw.githubusercontent.com/dhoaibao/ddd-workflow-kit/main/install.sh | \\
  bash -s -- --agent claude,codex --global
curl -fsSL https://raw.githubusercontent.com/dhoaibao/ddd-workflow-kit/main/install.sh | \\
  bash -s -- --agent pi --project "/path/to/project"
# Omit the project argument to use the current directory.
curl -fsSL https://raw.githubusercontent.com/dhoaibao/ddd-workflow-kit/main/install.sh | \\
  bash -s -- --agent pi --project
```

`--path /some/skills-directory` registers one explicit destination. `--project` defaults to the current directory when its path is omitted. Existing unmanaged files and repointed symlinks are never overwritten. Every release archive is checksum-verified before extraction.

After installation, use the local manager to refresh every registered global, project, or explicit destination:

```bash
~/.ddd-workflow-kit/bin/ddd-workflow-kit update
```

The manager also accepts `install` for a new selection. Release assets are stable names: `ddd-workflow-kit.tar.gz` and `ddd-workflow-kit.tar.gz.sha256`.

## Use a package

Read or copy the package directory according to the host's skill-loading mechanism. Start with its `SKILL.md`; package-local references and assets use relative links and are intended to travel with that package. Invoke the canonical `ddd` orchestrator for a broad workflow request, or invoke a focused package directly when its entry criteria are already met. Do not assume an installation command, host integration, or compatibility guarantee that the host does not provide.

## Repository navigation

- [DDD foundation](docs/foundation/README.md) — language-neutral concepts, evidence discipline, and adoption guidance.
- [Skill design](docs/skill-design/README.md) — package contracts, workflows, quality gates, and portability rules.
- [Implementation history and roadmap](docs/plans/README.md) — ordered implementation record, completed phase gates, and evaluation history.
- [Evaluation report](docs/evaluations/phase-4-report.json) — phase-4 live results, phase-0 carry-forward evidence, transition coverage, and residual risks.
- [Validation script](scripts/validate-skills.py) — deterministic repository and package checks.

All six packages are implemented and independently reviewed: `ddd`, `ddd-discover`, `ddd-strategic`, `ddd-tactical`, `ddd-adoption`, and `ddd-review`.

## Verification and evaluation evidence

Run the repository validator:

```bash
python3 scripts/validate-skills.py
```

The recorded suite evidence covers **59 cases**: **29 phase-0 cases carried forward** only after the package and evaluation hashes matched (not rerun in phase 4), plus **30 phase-4 live cases** across adoption, review, and orchestration. The phase-4 live sessions recorded 30/30 process and semantic passes, while the phase-0 report records the carried-forward semantic results.

The optional `skills-ref` executable and Python module were unavailable, so that check is explicitly deferred and was not installed. Static validation does not establish compatibility with every host; live results are model- and host-dependent, used an isolated text-only wrapper, and did not exercise target-project artifact materialization. See the [phase-4 report](docs/evaluations/phase-4-report.json) for commands, hashes, limitations, and residual risks.
