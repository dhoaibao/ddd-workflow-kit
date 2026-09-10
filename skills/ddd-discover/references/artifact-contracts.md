# Discovery artifact contracts

New discovery output uses the lean metadata contract: `scope` and `state` are required; `owner` appears when a named person/role must act. Legacy `artifact`, `status`, `validation`, `provenance`, `assumptions`, `open_questions`, and `last_updated` fields remain readable.

## Conditional minimums

- `assessment.md` records outcome, scope/mode, fit decision, evidence, constraints, simpler alternative when non-fit, and next action only when fit is disputed/evidence-heavy/limited or a durable record is needed.
- `domain-vision.md` records purpose, stakeholders, outcome, material policies/events, excluded scope, facts/proposals, and validation only when intent is absent or materially disputed.
- `ubiquitous-language.md` records context-specific term, definition, examples, source, status, owner, and translation/conflict only when terms are reused, overloaded, or materially conflicted.

All claims keep type and evidence beside the claim. Empty sections and `not applicable` rows are omitted.

## Safe updates

Inspect first; preserve legacy/user prose; update only discovery-owned sections; mark dependents stale when evidence changes; refuse destructive or out-of-bound paths. A non-fit result can live in the mandatory index alone.
