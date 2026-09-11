# Getting started with DDD Workflow Kit

A newcomer walkthrough of the one command you run and the two moments you decide something. No prior DDD knowledge assumed.

## 1. What this does — and does not do

It turns one bounded piece of work (an "increment") into evidence-backed planning documents under a target project's `docs/ddd/`, then pauses for you to approve exactly that one increment before anything gets built. It does not model your whole domain, does not write product code by default, and does not guess facts it wasn't given — see [Guarantees and boundaries](../README.md#guarantees-and-boundaries) for the full list.

## 2. Install

One command, from [the README](../README.md#install):

```bash
curl -fsSL https://raw.githubusercontent.com/dhoaibao/ddd-workflow-kit/main/install.sh | bash
```

It prompts for your agent(s) and scope. Details, uninstall, and the opt-in `--skill` flag are in [the installer reference](installer.md).

## 3. The only thing you type: `ddd`

Everything in this suite routes through one package: [`ddd`](../skills/ddd/SKILL.md). You describe the outcome you want; `ddd` figures out the rest. You never need to name `ddd-discover`, `ddd-strategic`, `ddd-tactical`, `ddd-adoption`, or `ddd-review` yourself — those are internal stages `ddd` routes through on its own, in that order, inside one run (its [Guided run](../skills/ddd/SKILL.md#guided-run) section).

## 4. Your first run, narrated

1. You ask your agent to run `ddd` for a bounded piece of work — for example, "use ddd to plan how approvals should work for expense claims."
2. `ddd` looks for `docs/ddd/README.md`. On a first run there isn't one, so it creates it and starts at the earliest stage.
3. It routes through the internal stages one at a time, writing only the files each stage owns, until it either:
   - stops because it's missing something it can't guess (a scope, a decision, a target), or
   - reaches review with a documented "ready" result and asks you to ratify.
4. Each time it stops, `docs/ddd/README.md`'s **Status** section names what's happening and the one next thing to do — see step 9.
5. You keep answering what it asks; you don't restart or re-invoke separate packages.

## 5. What each generated file is for

| File | Created by | What it's for |
| --- | --- | --- |
| `docs/ddd/README.md` | `ddd` | The index: target outcome, current status, artifact list, decision queue, and authorization state. Read this first, every time. |
| `docs/ddd/assessment.md`, `domain-vision.md`, `ubiquitous-language.md` | discovery stage | Only created when there's a real fit question, disputed intent, or terminology conflict to record. |
| `docs/ddd/contexts/<slug>.md` | strategic stage | The one selected context's boundary, key terms, and relationships. |
| `docs/ddd/models/<slug>.md` | tactical stage | One slice's examples, rules, invariants, and state transitions. |
| `docs/ddd/adoption-plan.md` | adoption stage | The one candidate increment: target, baseline, owner, scope, acceptance signals. |
| `docs/ddd/review.md` | review stage | The exception-based quality check and the decision queue behind it. |
| `docs/ddd/implementation-handoff.md` | `ddd`, after you ratify | The sole entry point for building the increment. Created once, never before authorization. |
| `docs/ddd/implementation/<increment-id>.md` | opt-in implementation package | Only if you also install an implementation package (see step 7). |

## 6. The two moments you must decide

Nothing else in this workflow needs you to make a call — these two moments do:

1. **Answer questions.** Any stage may stop with a small, grouped set of questions about scope, ownership, behavior, or boundaries it can't infer from evidence. Answer them; the run continues from there.
2. **Approve — or decline — one increment.** When review reports `documentation_readiness: ready` and `increment_gate: awaiting-ratification`, `ddd` asks you, a named human, to ratify that exact increment. "Ready" is not the same as authorized — nothing is built until you explicitly say so. You can also decline, with a reason; that's recorded too, and no handoff is created.

## 7. Building an increment (opt-in)

Planning artifacts alone don't write product code. If you want that, install the opt-in implementation package for your stack — currently [`ddd-impl-fastapi-hdx`](../skills/ddd-impl-fastapi-hdx/SKILL.md) for Python/FastAPI on `hdx-domain-kit` — with `--skill ddd-impl-fastapi-hdx` at install time (see [the installer reference](installer.md)). It only starts from your ratified `docs/ddd/implementation-handoff.md`, and it still gates migrations, composition-root edits, and dependency changes on your explicit per-run approval.

## 8. Doing the next one

An increment is deliberately small — "one bounded piece of work," not your whole domain. Once one is ratified (and, if you chose to, implemented), run `ddd` again for the next increment. Later increments start as one-line hypotheses and only get fully specified when their turn comes; you don't need to plan them all up front.

## 9. When it stops, and what to do

Open `docs/ddd/README.md` and read **Status**. Its **What's happening** line explains where the run is; its **Next action** line is the one thing to do — answer a question, provide missing evidence, or ratify/decline an increment. A collapsed "Machine state" block under the same section carries the same information in a stricter form for tooling; you don't need to read it.

## 10. The six words that matter

- **ready** — `documentation_readiness: ready` means the documentation is internally consistent and complete for this increment. It is not permission to build.
- **authorized** — `increment_gate: authorized` is set only after your explicit ratification. This is the only value that unlocks a handoff.
- **current** — an artifact's normal, up-to-date state. Also not permission to build; "current or ready never means authorized."
- **stale** — what happens to downstream artifacts when something upstream changes; they get marked stale and re-routed, never silently rewritten.
- **blocking** — a decision disposition that must be resolved before review can call the increment ready.
- **deferred** — a decision disposition that's explicitly postponed to a later increment, with an owner and a trigger to revisit it — not silently dropped.

## 11. Don't do this

- **Don't ask for a whole-project model.** The workflow's unit of progress is one bounded increment, not a complete domain catalogue; asking for "the whole domain modeled" just produces a stop or an oversized, ungrounded artifact set.
- **Don't hand-edit a `sha256`-pinned section.** Once an artifact's exact bytes are referenced by a `sha256:` authority revision (used from adoption through the handoff), editing that section outside the workflow invalidates the authorization rather than updating it quietly. Let the workflow regenerate it instead.

## Where to go next

- DDD concepts and vocabulary (not covered here): [DDD foundation](foundation/README.md).
- The exact artifact fields and ownership rules each stage follows: [Artifact contracts](skill-design/artifact-contracts.md).
- Everything this guide summarizes, in full: [`skills/ddd/SKILL.md`](../skills/ddd/SKILL.md).
