# DDD Workflow Kit

A portable skill suite for evidence-backed Domain-Driven Design work: it creates and reviews DDD planning artifacts under a target project's `docs/ddd/` directory, then can implement one ratified increment as target-repository code. Six `document`-class packages are documentation-only and framework-neutral; one opt-in `implementation`-class package, [`ddd-impl-fastapi-hdx`](skills/ddd-impl-fastapi-hdx/SKILL.md), writes code for a declared stack under its own approval-gated boundary. See the release-root `PACKAGES` manifest for every package's class.

## Install

Requires Linux or macOS with Bash 3.2+; installs a checksum-verified release into a versioned cache and symlinks packages into agent skill directories, never cloning this repository or touching shell profiles.

```bash
curl -fsSL https://raw.githubusercontent.com/dhoaibao/ddd-workflow-kit/main/install.sh | bash
```

Non-interactively, pass `--agent NAME[,NAME...]` (`shared`, `claude`, `codex`, `opencode`, `antigravity`, `pi`), `--global` or `--project [path]` for scope, `--path DIR` for one explicit destination, and `--skill NAME[,NAME...]` (or `--skill all`) to also opt into an implementation-class package — document-class packages always install — e.g. `--agent pi --global --skill ddd-impl-fastapi-hdx`. See [`docs/installer.md`](docs/installer.md) for manager commands, uninstall, and how package selection is recorded and inherited.

## How it works

`ddd-discover → ddd-strategic → ddd-tactical → ddd-adoption → ddd-review`

| Package | Purpose | Primary output in `docs/ddd/` |
| --- | --- | --- |
| [`ddd`](skills/ddd/SKILL.md) | Route requests and transition state across the workflow. | Routing and status sections of `README.md` |
| [`ddd-discover`](skills/ddd-discover/SKILL.md) | Establish the smallest evidence-backed fit decision and material conflicts. | Index decision by default; `assessment.md`, `domain-vision.md`, and language records added when needed |
| [`ddd-strategic`](skills/ddd-strategic/SKILL.md) | Define one selected context, its relationships, and key terms/boundaries. | One `contexts/<safe-slug>.md`; maps, glossary, and additional contexts when needed |
| [`ddd-tactical`](skills/ddd-tactical/SKILL.md) | Model one slice's examples, rules, invariants, transitions, and relevant failure semantics. | One `models/<slice-slug>.md`; unused tactical patterns are omitted |
| [`ddd-adoption`](skills/ddd-adoption/SKILL.md) | Fully specify one candidate increment: target, baseline, owner, scope, acceptance. | `adoption-plan.md` plus the gate extension |
| [`ddd-review`](skills/ddd-review/SKILL.md) | Run internal quality gates and emit exception findings plus one decision queue. | `review.md` and its README queue/review markers |
| **After ratification** | A separate human decision owner authorizes one exact increment; `ddd` preserves the accountable implementation owner and records the transport authorization. | `implementation-handoff.md` as the sole implementation entry point |
| [`ddd-impl-fastapi-hdx`](skills/ddd-impl-fastapi-hdx/SKILL.md) *(opt-in)* | Implement one ratified increment as target-project FastAPI/`hdx-domain-kit` code and tests. | `docs/ddd/implementation/<increment-id>.md` |

## Guarantees and boundaries

- **Evidence and provenance:** claims distinguish current behavior, desired meaning, obligations, facts, interpretations, and assumptions; sources, validation state, and open questions stay visible.
- **Bounded stops:** missing evidence, conflicting claims, or unsafe paths stop the workflow with a handoff rather than inventing facts.
- **Additive ownership:** each stage owns only its documented artifact sections; nothing — including artifacts predating this contract — is silently rewritten.
- **Class-scoped write boundary:** the six `document`-class packages make no edits to product source, tests, schemas, configuration, migrations, or deployment files. The opt-in `implementation`-class package may write target-repository domain code and tests for the ratified increment only, with migrations, composition-root edits, and dependency/config changes approval-gated per run.
- **Ratification is not authorization:** `documentation_readiness: ready` and `increment_gate: awaiting-ratification` do not by themselves authorize implementation; only a named human decision owner authorizing one exact increment lets `ddd` create one revision-bound `implementation-handoff-v1`.

## Documentation

- [Changelog](CHANGELOG.md) — release history and notable changes.
- [DDD foundation](docs/foundation/README.md) — language-neutral concepts, evidence discipline, and adoption guidance.
- [Skill design](docs/skill-design/README.md) — package contracts, workflows, quality gates, and portability rules.
- [Implementation history and roadmap](docs/plans/README.md) — ordered implementation record and evaluation history.
- [Lean redesign evaluation report](docs/evaluations/lean-workflow-redesign-v1-report.json) — local sanitized BonVoye-shaped fixture and limitations.
- [Phase-4 evaluation report](docs/evaluations/phase-4-report.json) — historical live results, hashes, limitations, and residual risks.

## Development

```bash
python3 scripts/validate-skills.py
```

Validates the repository's packages, links, and evaluation cases; static validation covers repository conventions and fixture behavior only, as the command's own output states.
