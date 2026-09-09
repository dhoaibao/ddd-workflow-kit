# Review method

Review is an evidence and lifecycle check over named artifacts. It is not a modeling stage and cannot make missing facts appear.

## Scope and inventory

Record one objective, one domain/context/slice scope, requested acceptance criteria, requested paths, available paths, and the review depth. Inspect exact paths first. Classify each artifact as available, missing, partial, stale, superseded, archived, or out of scope. A missing artifact produces a finding with its expected path, owner, action, and earliest stage; never infer contents from neighboring documents.

## Gate record

For each gate record the question, evidence, status (`pass`, `follow-up`, `blocked`, or `not-applicable`), owner, and revisit trigger:

1. fit and scope;
2. evidence and provenance;
3. lifecycle and minimum schema;
4. vocabulary and translation;
5. strategic-to-tactical prerequisites;
6. adoption safety;
7. cross-artifact consistency and stale routing.

A gate result is scoped to the supplied evidence. Generic guidance can identify a question but cannot pass a target-project gate.

## Evidence and claims

For every material claim, preserve claim type, source/provenance, owner, scenario or impact, and validation. Current behavior belongs to executable behavior, tests, operations, or observed integrations; desired meaning belongs to users/domain experts; required obligations belong to explicit contracts, regulations, or security/privacy constraints. If sources disagree, record both claims and the decision needed. Do not turn a proposal or assumption into a fact.

## Finding classification

Use `info` for a bounded observation that does not invalidate the scope, `follow-up` for an owner action needed before broader confidence, `blocked` for a prerequisite or safety issue that prevents the stated review, and `invalidated` when new evidence makes an artifact or dependent assumption stale. Every finding carries observable evidence and provenance, not a generic label.

The earliest-stage rule is:

- discovery owns missing fit, scope, current-system, terminology evidence, and baseline observations;
- strategic owns context purpose, language, ownership, relationship direction, and boundaries;
- tactical owns behavior, commands, scenarios, invariants, model elements, and consistency;
- adoption owns sequencing, compatibility, observability, data reconciliation, and rollback/containment;
- review owns review scope, gate aggregation, finding completeness, and the review artifact.

## Cross-artifact and stale routing

Compare claims rather than headings. When a strategic boundary changes tactical assumptions, mark the model and adoption plan stale and route to strategic. When adoption safety invalidates a tactical choice, route to adoption or the earliest modeling owner supported by evidence. When vocabulary conflicts, preserve context-specific meanings and route to strategic. List all affected dependents and the evidence that makes them stale. Do not rewrite either source to remove the conflict.

A stale-routing record contains affected artifact paths, the earliest stage, accountable owner, required action, evidence/provenance, and revisit trigger. If the earliest owner is disputed, use `blocked` and ask for ownership clarification rather than choosing silently.

## Ready and bounded stops

`ready` means the named documentation set is coherent for its stated scope, gate results are qualified, and the review artifact is complete. It does not mean implementation, deployment, migration, data cutover, or release approval. A `follow-up`, `blocked`, or `invalidated` result names the exact next stage and preserves the review evidence.

If review scope is missing, return a bounded stop. If an artifact is missing, report it. If a request asks for product or deployment changes, refuse those paths and retain only a documentation-only review recommendation when it can be isolated safely.
