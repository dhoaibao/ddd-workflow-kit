# Tactical artifact contracts

These contracts define the tactical documentation slice without prescribing a programming language, framework, database, deployment topology, or implementation structure.

## Common metadata and claims

Each tactical artifact begins with one H1 and a metadata table containing a scoped `artifact` identifier such as `context-model:<context-slug>`, plus `status`, `validation`, `owner`, `scope`, `provenance`, `assumptions`, `open_questions`, and `last_updated`. Lifecycle values are `draft`, `active`, `superseded`, or `archived`; validation values are `unvalidated`, `partially-validated`, `validated`, or `stale`.

Distinguish current behavior, desired policy/meaning, required obligations, facts, interpretations, proposals, and assumptions. Maintain a claim-and-evidence ledger with `Claim ID`, claim type, statement, source/provenance, owner, scenario, validation, and references from invariants and decisions. Every invariant and model decision records its Claim IDs, evidence, owner, scenario, and validation state. A pattern name is not evidence.

## Safe ownership and paths

1. Accept one already validated strategic context and reuse its safe slug exactly; do not invent or normalize a new slug.
2. Create or update only `docs/ddd/models/<context-slug>.md`, additive tactical sections in `docs/ddd/contexts/<context-slug>.md`, and evidence-backed tactical language entries.
3. Resolve the model candidate and verify its parent is exactly `docs/ddd/models` before writing. Preserve existing content and ownership; ask before collision, ambiguity, structural, destructive, or ownership changes.
4. If evidence challenges the strategic boundary, language, owner, or relationship, preserve the conflict, mark affected work stale, include `invalidated_stages`, and return to `ddd-strategic` rather than rewriting strategic artifacts.
5. Never edit product source, tests, schemas, configuration, generated output, or deployment files.

## Minimum model schema

The model document includes the selected context and authority link; scope and outcome; commands/use cases; preconditions, outcomes, failures, counterexamples, and acceptance signals; invariants with immediate/eventual consistency and evidence; entities and value objects with identity/equality, responsibilities, and validation; aggregate/root decisions with in/out scope, protected invariant, references, transaction, and concurrency assumptions; repository contracts with failure semantics; domain/application service, specification, and factory decisions with named need or `not-needed`; past-tense events and delivery semantics; application flow; integration translation; optional CQRS and event-sourcing decisions with status, evidence, costs, and simpler alternative; examples/counterexamples; assumptions; open questions; and validation.

The materialized model must link back to the selected strategic context artifact and must not duplicate or silently revise context-map facts. It records tactical contributions separately from strategic ownership and preserves conflicting current, desired, and required claims as separate ledger entries.

## Transition contract

A successful result hands exactly one model to `ddd-adoption`. It includes the model path, context, commands/scenarios, invariants, tactical decisions, integration/persistence assumptions, risks, evidence, validation, owners, allowed paths, open questions, acceptance signals to define, and `return_to`. A host without named-stage activation returns the exact manual stage name and unchanged bundle. It does not claim that adoption ran.
