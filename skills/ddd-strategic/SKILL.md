---
name: ddd-strategic
description: Define one evidence-backed bounded context and only the relationships, language, and conditional strategic artifacts needed by a selected increment; preserve boundaries without inferring deployment topology.
---

# DDD strategic design

Turn discovery evidence into one selected context hypothesis for one increment. Strategic work is slice-first, not a whole-domain catalogue.

## Entry and boundary

Require a fit/limited-fit result or explicit bounded strategic request, one meaningful outcome, usable terms/examples, ownership, evidence, and allowed paths. Own context purpose, boundary, decision ownership, touched relationships, material language, and strategic uncertainty. Do not design tactical patterns, deployment services, schemas, or product code.

## Lean workflow

1. Identify candidate boundaries and classification only when they change the selected increment.
2. Select exactly one context using explicit objective, evidence, and owner priority. Keep other contexts as short hypotheses.
3. Record only touched upstream/downstream relationships, direction, translation responsibility, and failure/consistency semantics required by the slice.
4. Preserve overloaded terms by context and record translation/conflict only when it affects behavior or the boundary.
5. Create one `contexts/<safe-slug>.md` by default. Create `domain-map.md`, `context-map.md`, a glossary, or additional context files only when the plan's conditional trigger is recorded.
6. Route exactly one tactical request when the selected context has sufficient purpose, boundary, language, scenarios, owner, and evidence. Otherwise return the earliest decision.

## Conditional artifacts

- `domain-map.md`: classification changes investment, sourcing, or ownership.
- `context-map.md`: two or more contexts and their direction/translation affect this increment.
- `ubiquitous-language.md`: terms are reused, overloaded, or materially conflicted.
- additional context file: selected or required by a current relationship.

Do not create exhaustive maps or generic stakeholder inventories merely because a template exists. A bounded context is not automatically a deployment service.

## Safe slugs and updates

Reuse a validated ASCII safe slug; do not normalize a new slug in tactical work. For a new context label, lowercase ASCII letters/digits, replace each run of non-alphanumeric separators with one hyphen, trim hyphens, and reject non-ASCII, empty, ambiguous, colliding, or traversal-like labels. Resolve `docs/ddd/contexts/<safe-slug>.md` and require its parent to be exactly `docs/ddd/contexts` before writing. Inspect existing paths, preserve user-authored prose/legacy metadata, update owned sections additively, and stop for filename collision, ambiguous ownership, unsafe traversal, or structural replacement. Mark tactical/adoption dependents stale when a boundary changes.

## Result

Return one selected context, purpose, in/out boundary, key terms, touched relationships, evidence, assumptions, decision queue items, changed paths, stale dependents, and one `ddd-tactical` request or bounded stop. No strategic result authorizes implementation.

Read [the method](references/strategic-method.md), [the contract](references/artifact-contracts.md), and the conditional assets before writing.
