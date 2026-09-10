# DDD Workflow Kit

A portable, language-, framework-, and runtime-neutral skill suite for evidence-backed Domain-Driven Design work. The skills are documentation-only: they create and review DDD planning artifacts under a target project's `docs/ddd/` directory and never edit product code, tests, configuration, or runtime behavior.

The suite ships six packages: the `ddd` orchestrator, which routes one stage at a time, plus five focused stages for discovery, strategic design, tactical modeling, adoption planning, and artifact review.

## Install

Requires Linux or macOS with Bash 3.2 or newer. The installer downloads a checksum-verified release, installs a versioned cache at `~/.ddd-workflow-kit/skills`, and symlinks the packages into the selected agent skill directory. It never clones this repository, modifies shell profiles, or overwrites files it does not manage.

Interactive (prompts for agents and scope):

```bash
curl -fsSL https://raw.githubusercontent.com/dhoaibao/ddd-workflow-kit/main/install.sh | bash
```

Non-interactive, for automation. Supported agents: `claude`, `codex`, `opencode`, `antigravity`, `pi`.

```bash
# Register with one or more agents globally
curl -fsSL https://raw.githubusercontent.com/dhoaibao/ddd-workflow-kit/main/install.sh | \
  bash -s -- --agent claude,codex --global

# Register with one agent in a project (omit the path for the current directory)
curl -fsSL https://raw.githubusercontent.com/dhoaibao/ddd-workflow-kit/main/install.sh | \
  bash -s -- --agent pi --project /path/to/project
```

Use `--path /some/skills-directory` to register a single explicit destination. To refresh every registration later:

```bash
~/.ddd-workflow-kit/bin/ddd-workflow-kit update
```

The manager also accepts `install` for a new selection and `version` to print the installed release.

## How it works

Invoke the `ddd` orchestrator for a broad workflow request, or invoke a focused package directly when its entry criteria and evidence are already satisfied. Each stage writes only the artifact sections it owns, preserves existing material, and produces a bounded stop with an explicit handoff when evidence is missing or a boundary is unsafe.

The canonical flow:

```
ddd-discover → ddd-strategic → ddd-tactical → ddd-adoption → ddd-review
```

| Package | Purpose | Primary output in `docs/ddd/` |
| --- | --- | --- |
| [`ddd`](skills/ddd/SKILL.md) | Route requests and transition state across the workflow. | Routing and status sections of `README.md` |
| [`ddd-discover`](skills/ddd-discover/SKILL.md) | Establish scope, evidence, vocabulary, and DDD fit. | `assessment.md`, initial `domain-vision.md`, discovery contributions to `ubiquitous-language.md` |
| [`ddd-strategic`](skills/ddd-strategic/SKILL.md) | Define subdomains, bounded contexts, language, and ownership. | `domain-map.md`, `context-map.md`, `contexts/<safe-slug>.md`, `ubiquitous-language.md` |
| [`ddd-tactical`](skills/ddd-tactical/SKILL.md) | Model one context's behavior, invariants, and consistency. | `models/<context-slug>.md` and additive tactical sections |
| [`ddd-adoption`](skills/ddd-adoption/SKILL.md) | Plan a bounded, incremental, reversible adoption slice. | `adoption-plan.md` |
| [`ddd-review`](skills/ddd-review/SKILL.md) | Review artifacts for evidence, boundaries, and readiness. | `review.md` |

## Guarantees and boundaries

- **Evidence and provenance:** claims distinguish current behavior, desired meaning, obligations, facts, interpretations, and assumptions; sources, validation state, and open questions stay visible.
- **Bounded stops:** missing evidence, conflicting claims, or unsafe paths stop the workflow with a handoff rather than inventing facts.
- **Additive ownership:** each stage owns only its documented artifact sections; nothing is silently rewritten.
- **Documentation-only:** no edits to product source, tests, schemas, configuration, migrations, or deployment files.
- **Scoped reviews:** a `ready` review means documentation readiness for the stated scope only — not implementation, deployment, or release approval.

## Documentation

- [Changelog](CHANGELOG.md) — release history and notable changes.
- [DDD foundation](docs/foundation/README.md) — language-neutral concepts, evidence discipline, and adoption guidance.
- [Skill design](docs/skill-design/README.md) — package contracts, workflows, quality gates, and portability rules.
- [Implementation history and roadmap](docs/plans/README.md) — ordered implementation record and evaluation history.
- [Phase-4 evaluation report](docs/evaluations/phase-4-report.json) — live results, hashes, limitations, and residual risks.

## Development

Validate the repository's packages, links, and evaluation cases:

```bash
python3 scripts/validate-skills.py
```

The recorded suite evidence covers 59 cases: 29 phase-0 cases carried forward under matching package and evaluation hashes, plus 30 phase-4 live cases across adoption, review, and orchestration, all passing. Static validation covers repository conventions only and does not establish compatibility with every host; live results are model- and host-dependent. See the [phase-4 report](docs/evaluations/phase-4-report.json) for commands, hashes, and limitations.
