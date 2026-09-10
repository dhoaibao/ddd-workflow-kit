# Adoption artifact contract

`docs/ddd/adoption-plan.md` uses new lean metadata (`scope`, `state`, conditional `owner`) or remains readable with legacy metadata.

## Immediate increment contract

The plan contains stable `increment_id`; target repository/runtime and baseline revision; intended outcome/change; in/out behavior; accountable implementation owner; dependencies; observable acceptance; stop conditions; and typed question dispositions with impact, owner, action, affected paths, and revisit trigger. Add material risk/containment only when a trigger exists; later increments are hypotheses without exhaustive tables.

Adoption emits `ddd-implementation-gate-v1` as a result extension with target, baseline, implementation owner, outcome/scope/return contract, acceptance, conditional containment, question dispositions, readiness, gate, and authority revisions. `ddd` carries it and performs human ratification; it never authorizes execution here.

## Safe and legacy behavior

Adoption owns only its path. Inspect first, preserve existing prose/metadata/links, update additively, read legacy fields, and never silently rewrite or migrate. Refuse product/runtime mutations and unsafe paths.
