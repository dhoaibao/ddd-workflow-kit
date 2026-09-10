# Lean quality gates

Quality gates still run rigorously, but generated review output is exception-based. Passing checks are summarized in one sentence; only findings that can change the selected increment are emitted.

## Internal gate record

Each gate internally has a question, evidence, status (`pass`, `follow-up`, `blocked`, or `not-applicable`), owner, and revisit trigger. The review artifact need not repeat passing records.

## Gates

- **Fit and scope:** a simpler/non-fit result stops downstream artifacts; a fit has one bounded outcome and evidence.
- **Evidence and provenance:** current behavior, desired policy/meaning, obligations, interpretations, proposals, and assumptions remain distinct and sourced where material.
- **Lean utility:** every emitted field or paragraph supports decision, behavior/invariant, boundary/contract, acceptance, or material risk; empty/generic/duplicate content is omitted.
- **Conditional depth:** operational detail and optional artifacts exist only when a recorded data, async, privacy, external-contract, concurrency, brownfield, or pattern trigger exists.
- **Strategic-to-tactical:** one selected context has purpose, boundary, owner, language, relationships, scenarios, and invariants sufficient for the slice.
- **Tactical behavior:** examples, rules, transitions, failure semantics, and consistency are explicit; unused tactical patterns are absent.
- **Adoption safety:** one increment has stable ID, target/runtime, baseline, accountable implementation owner, outcome, in/out scope, dependencies, acceptance, and stop conditions; risk and containment are present when triggered.
- **Decision queue:** every unresolved item has impact, disposition, owner, smallest action, affected paths, and revisit trigger, and these fields survive gate/handoff transport. Blockers cannot be silently reclassified.
- **Dual readiness:** review records `documentation_readiness` separately from `increment_gate`; `ready` alone never authorizes work.
- **Ratification:** authorization names a human decision owner (its own field, may equal or differ from the accountable implementation owner), one increment, exact revisions, outcome/scope/return contract, acceptance, containment, and durable question dispositions.
- **Handoff authority:** `implementation-handoff-v1` exists only after ratification and references exact, current authoritative sections. Revision/staleness/conflict invalidates it.
- **Safe boundary:** only owned `docs/ddd/` artifacts are changed; legacy documents are preserved and readable.

## Review output

`ddd-review` reports the named increment and authority set, the two readiness states, blocking/invalidating/decision-required findings, materially relevant assumptions/deferred/out-of-scope items, earliest owner, and one next action. It says that passed gates were checked and does not print a full passing table.

## No approval leakage

Documentation readiness is not implementation, deployment, migration, release, architecture, or schema approval. A handoff is authorization for exactly one bounded increment only.
