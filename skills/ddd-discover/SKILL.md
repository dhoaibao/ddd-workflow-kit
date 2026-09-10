---
name: ddd-discover
description: Decide the smallest evidence-backed DDD fit for one bounded capability, preserve material current-versus-desired conflicts, and stop or hand off without generating downstream artifacts by default.
---

# DDD discovery

Establish whether DDD is useful for one bounded capability and record only evidence that changes the next decision.

## Scope and entry

Require a target scope, permitted evidence boundary, and desired outcome. Read existing artifacts and legacy metadata without destructive migration. Discovery owns fit, scope, current-system evidence, material terminology, and the non-fit stop. It never designs contexts, tactical patterns, adoption execution, or product code.

## Evidence discipline

Classify material claims as current behavior, desired policy/meaning, required obligation, fact, interpretation, proposal, or assumption. Keep current behavior separate from desired behavior when the difference affects the selected increment. Cite evidence beside disputed claims; do not infer facts from generic DDD guidance or code shape.

## Lean workflow

1. Frame one outcome, in/out scope, mode, stakeholders, constraints, and evidence boundary.
2. Prefer concrete examples, exceptions, decisions, terms, and observed behavior over explanatory prose.
3. Assess `fit`, `limited-fit`, or `not-fit` with a simpler path and revisit signal.
4. Persist only material current-versus-desired conflicts and questions that can change the next action.
5. Create `assessment.md`, `domain-vision.md`, or `ubiquitous-language.md` only when their conditional trigger is recorded. A normal one-context flow may keep the fit decision in `README.md`.
6. Route one bounded strategic request only when outcome, terms, evidence, owner, and scope are sufficient. A non-fit flow stops without downstream artifacts.

## Conditional artifacts

- `assessment.md`: disputed/evidence-heavy/limited fit or a durable decision record.
- `domain-vision.md`: absent or materially disputed outcome, stakeholders, or strategic intent.
- `ubiquitous-language.md`: reused, overloaded, or materially conflicting terms.

Omit empty sections and generic teaching. Do not create artifacts merely to satisfy a template.

## Safe boundary and ownership

Create or update only discovery-owned sections under `docs/ddd/`. Preserve user-authored prose, links, legacy fields, and provenance. Record conflicts and stale impact instead of choosing silently. Refuse source, tests, configuration, schemas, migrations, deployment files, generated output, runtime behavior, and unrelated paths.

## Result

Return fit, scope, material evidence, changed paths, assumptions, questions with dispositions, validation gaps, and either one `ddd-strategic` request or a bounded simpler-path stop. State exact next human action. No discovery result authorizes implementation.

Read [the method](references/discovery-method.md), [the contract](references/artifact-contracts.md), and the conditional templates before writing.
