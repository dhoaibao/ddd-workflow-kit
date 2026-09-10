# DDD Workflow Kit

A portable skill suite for evidence-backed Domain-Driven Design work. Six `document`-class packages are language-, framework-, and runtime-neutral and documentation-only: they create and review DDD planning artifacts under a target project's `docs/ddd/` directory and never edit product code, tests, configuration, or runtime behavior. One opt-in `implementation`-class package, `ddd-impl-fastapi-hdx`, implements one ratified increment as target-project code and tests for a declared stack.

The suite ships seven packages by default install and opt-in: the `ddd` orchestrator, which routes one document-workflow stage at a time; five focused document-workflow stages for discovery, strategic design, tactical modeling, adoption planning, and artifact review; and the opt-in `ddd-impl-fastapi-hdx` implementation package. See the release-root `PACKAGES` manifest for the exact class of each package.

## Install

Requires Linux or macOS with Bash 3.2 or newer. The installer downloads a checksum-verified release, installs a versioned cache at `~/.ddd-workflow-kit/skills`, and symlinks the packages into the selected agent skill directory. It never clones this repository, modifies shell profiles, or overwrites files it does not manage.

Interactive (use ↑/↓ and Space to choose targets, then Enter; scope is a single-select menu):

```bash
curl -fsSL https://raw.githubusercontent.com/dhoaibao/ddd-workflow-kit/main/install.sh | bash
```

Non-interactive, for automation. Supported targets: `shared`, `claude`, `codex`, `opencode`, `antigravity`, `pi`. `shared` registers the common `.agents/skills` directory (`~/.agents/skills` globally or `<project>/.agents/skills` locally).

```bash
# Register with one or more agents globally
curl -fsSL https://raw.githubusercontent.com/dhoaibao/ddd-workflow-kit/main/install.sh | \
  bash -s -- --agent shared,codex --global

# Register with one agent in a project (omit the path for the current directory)
curl -fsSL https://raw.githubusercontent.com/dhoaibao/ddd-workflow-kit/main/install.sh | \
  bash -s -- --agent pi --project /path/to/project
```

Use `--path /some/skills-directory` to register a single explicit destination. Document-class packages install by default; add `--skill NAME[,NAME...]` (or `--skill all`) to also opt into an implementation-class package such as `ddd-impl-fastapi-hdx`:

```bash
# Also install the opt-in FastAPI + hdx-domain-kit implementation package
curl -fsSL https://raw.githubusercontent.com/dhoaibao/ddd-workflow-kit/main/install.sh | \
  bash -s -- --agent pi --global --skill ddd-impl-fastapi-hdx
```

To refresh every registration later, preserving the prior package selection:

```bash
~/.ddd-workflow-kit/bin/ddd-workflow-kit update
```

The manager also accepts `install` for a new selection, `uninstall` for full or registration-scoped removal, and `version` to print the installed release. Uninstall prompts default to No; automation must pass `--yes`. Interactive Project uninstall lists all project and explicit-path registration rows (explicit rows are labelled `explicit path`) and selects registrations rather than physical destinations.

```bash
# Remove every managed registration and the local installer state
~/.ddd-workflow-kit/bin/ddd-workflow-kit uninstall --full --yes

# Remove one registration while preserving shared physical links when needed
~/.ddd-workflow-kit/bin/ddd-workflow-kit uninstall --partial --agent shared --global --yes
```

## How it works

Invoke the `ddd` orchestrator for a broad workflow request, or invoke a focused package directly when its entry criteria and evidence are already satisfied. The workflow now advances one bounded increment at a time: it writes only decision-, behavior-, boundary-, acceptance-, and risk-bearing content, preserves existing material, and stops with an explicit earliest-owner handoff when evidence or authority is missing.

The canonical flow:

```
ddd-discover → ddd-strategic → ddd-tactical → ddd-adoption → ddd-review
```

| Package | Purpose | Primary output in `docs/ddd/` |
| --- | --- | --- |
| [`ddd`](skills/ddd/SKILL.md) | Route requests and transition state across the workflow. | Routing and status sections of `README.md` |
| [`ddd-discover`](skills/ddd-discover/SKILL.md) | Establish the smallest evidence-backed fit decision and material conflicts. | Index decision by default; `assessment.md`, `domain-vision.md`, and language records only on triggers |
| [`ddd-strategic`](skills/ddd-strategic/SKILL.md) | Define one selected context, touched relationships, and material language/boundaries. | One `contexts/<safe-slug>.md`; maps, glossary, and additional contexts only on triggers |
| [`ddd-tactical`](skills/ddd-tactical/SKILL.md) | Model one slice's examples, rules, invariants, transitions, and relevant failure semantics. | One `models/<slice-slug>.md`; unused tactical patterns are omitted |
| [`ddd-adoption`](skills/ddd-adoption/SKILL.md) | Fully specify one candidate increment with target, baseline, implementation owner, outcome/scope, acceptance, and typed uncertainty routing; add containment only when triggered. | `adoption-plan.md` plus the gate extension |
| [`ddd-review`](skills/ddd-review/SKILL.md) | Run internal quality gates and emit exception findings plus one decision queue. | `review.md` and its README queue/review markers |
| **After ratification** | A separate human decision owner authorizes one exact increment; `ddd` preserves the accountable implementation owner and records the transport authorization. | `implementation-handoff.md` as the sole implementation entry point |
| [`ddd-impl-fastapi-hdx`](skills/ddd-impl-fastapi-hdx/SKILL.md) *(opt-in)* | Implement one ratified increment as target-project FastAPI/`hdx-domain-kit` code and tests, after verifying the handoff's authorization and authority revisions. | `docs/ddd/implementation/<increment-id>.md` |

## Guarantees and boundaries

- **Evidence and provenance:** claims distinguish current behavior, desired meaning, obligations, facts, interpretations, and assumptions; sources, validation state, and open questions stay visible.
- **Bounded stops:** missing evidence, conflicting claims, or unsafe paths stop the workflow with a handoff rather than inventing facts.
- **Additive ownership:** each stage owns only its documented artifact sections; nothing is silently rewritten.
- **Class-scoped write boundary:** the six `document`-class packages make no edits to product source, tests, schemas, configuration, migrations, or deployment files. The opt-in `implementation`-class package may write target-repository domain code and tests for the ratified increment only, with migrations, composition-root edits, and dependency/config changes approval-gated per run.
- **Scoped reviews:** `documentation_readiness: ready` is separate from `increment_gate: awaiting-ratification`; neither alone authorizes implementation.
- **Scoped ratification:** a named human decision owner may authorize one exact increment for the accountable implementation owner; only then can `ddd` create one revision-bound `implementation-handoff-v1`.
- **Legacy compatibility:** existing target artifacts remain readable and are never silently rewritten.

## Documentation

- [Changelog](CHANGELOG.md) — release history and notable changes.
- [DDD foundation](docs/foundation/README.md) — language-neutral concepts, evidence discipline, and adoption guidance.
- [Skill design](docs/skill-design/README.md) — package contracts, workflows, quality gates, and portability rules.
- [Implementation history and roadmap](docs/plans/README.md) — ordered implementation record and evaluation history.
- [Lean redesign evaluation report](docs/evaluations/lean-workflow-redesign-v1-report.json) — local sanitized BonVoye-shaped fixture and limitations.
- [Phase-4 evaluation report](docs/evaluations/phase-4-report.json) — historical live results, hashes, limitations, and residual risks.

## Development

Validate the repository's packages, links, and evaluation cases:

```bash
python3 scripts/validate-skills.py
```

The current deterministic suite validates the seven packages (six `document`-class, one `implementation`-class) plus the `PACKAGES` manifest, their shared contracts, 15 redesign acceptance cases, package links/H1s/runtime neutrality, and a local sanitized BonVoye-shaped fixture. Historical phase-0 and phase-4 records remain unchanged. Static validation covers repository conventions and fixture behavior only; it does not establish compatibility with every host/model or an external project, and it does not evaluate an implementation package's target-repository output.
