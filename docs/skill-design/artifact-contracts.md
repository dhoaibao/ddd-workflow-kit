# Artifact contracts

A future implementation writes modeling artifacts under `docs/ddd/`. These are repository documents for shared understanding, not generated source code. The contracts below define the minimum shape and safe lifecycle.

## Common metadata contract

Every artifact begins with a human-readable title followed by a metadata table containing, at minimum:

| Field | Requirement |
| --- | --- |
| `artifact` | Stable artifact type and, for scoped artifacts, context/model identifier. |
| `status` | Lifecycle status: `draft`, `active`, `superseded`, or `archived`. |
| `validation` | Validation status: `unvalidated`, `partially-validated`, `validated`, or `stale`. |
| `owner` | Skill/stage or named project owner responsible for the next update. |
| `scope` | Domain, context, model, or adoption slice covered. |
| `provenance` | Evidence sources, contributors, and dates sufficient to trace claims. |
| `assumptions` | Explicit assumptions; use `none recorded` when empty. |
| `open_questions` | Unresolved questions or `none recorded`. |
| `last_updated` | Date of the latest substantive update. |

The body must distinguish **facts**, **interpretations**, **proposals**, and **decisions**. A claim without provenance is an assumption or proposal, never an established fact. Validation records should name the evidence or reviewers and may be partial.

## Lifecycle and validation

- `draft` means the document is being shaped and may be incomplete.
- `active` means it is the current working agreement for its scope; it may still contain open questions.
- `superseded` means a newer artifact replaces it; retain a link to the replacement and the reason.
- `archived` means it is retained for historical context and must not guide new decisions.
- `unvalidated` means no relevant expert or behavioral check has occurred.
- `partially-validated` means some claims or scenarios have been checked.
- `validated` means the stated scope has been checked against the named evidence; it does not mean universally true.
- `stale` means new evidence may invalidate the artifact; downstream users must not treat it as current until reviewed.

A strategic change that affects tactical assumptions marks affected tactical and adoption artifacts `stale`. A changed fact does not silently rewrite historical provenance.

## Artifact inventory and minimum schemas

### `docs/ddd/README.md`

**Owner:** `ddd` with `ddd-review` stewardship. **Purpose:** index the artifact set and explain scope. **Minimum sections:** project/domain scope; current status; artifact index; active contexts; validation summary; open questions; provenance policy; safe-update policy; link to the latest `review.md`.

### `docs/ddd/assessment.md`

**Owner:** `ddd-discover`. **Minimum sections:** desired outcomes; complexity/change-risk signals; DDD-fit decision (`fit`, `limited-fit`, or `not-fit`); evidence table; current-system mode (`greenfield`, `brownfield`, or `mixed`); constraints; assumptions; open questions; next-stage recommendation. A `not-fit` result should explain the simpler approach to prefer.

### `docs/ddd/domain-vision.md`

**Owner:** `ddd-discover`, with strategic updates by `ddd-strategic`. **Minimum sections:** domain purpose and scope; users/stakeholders; outcomes; major policies/events; strategic importance hypotheses; excluded scope; facts versus proposals; validation record.

### `docs/ddd/ubiquitous-language.md`

**Owner:** `ddd-strategic`, informed by discovery and reviewed by `ddd-review`. **Minimum sections:** term; context; definition; examples/non-examples; source; status (`proposed`, `accepted`, `conflicted`, or `retired`); owner; conflict/translation notes. Same spelling does not imply same meaning across contexts.

### `docs/ddd/domain-map.md`

**Owner:** `ddd-strategic`. **Minimum sections:** domain and subdomains; core/supporting/generic classification with rationale; capabilities/outcomes; ownership; evidence; unresolved classifications; links to contexts. Classifications remain hypotheses until validated.

### `docs/ddd/context-map.md`

**Owner:** `ddd-strategic`. **Minimum sections:** context inventory; each context's purpose, owner, language, and lifecycle; relationship direction; relationship type or description; contracts and translation; consistency/failure assumptions; evidence; unresolved boundaries. It must state that a bounded context is not automatically a deployment service.

### `docs/ddd/contexts/`

**Owner:** `ddd-strategic`, with review by `ddd-review`. **One document per context. Minimum sections:** context identity and purpose; boundary in/out; stakeholders/owner; language; key workflows; invariants to protect; upstream/downstream relationships; data/consistency assumptions; validation and open questions. Context files must link to the context map rather than duplicate it as an authority.

### `docs/ddd/models/`

**Owner:** `ddd-tactical`. **One document per modeled context or slice. Minimum sections:** scope; commands/use cases; entities; value objects; aggregate roots and invariants; repositories; domain/application services; specifications; factories; domain events; integration translations; examples; optional CQRS/event-sourcing decision and rationale; assumptions; validation gaps. Patterns may be marked `not-needed` with evidence.

### `docs/ddd/adoption-plan.md`

**Owner:** `ddd-adoption`. **Minimum sections:** mode; target outcome; first slice; ordered increments; dependencies; acceptance signals; ownership; risks; rollback/containment; data/integration/privacy considerations; decision points; explicit product-code boundary. It must distinguish recommendation from execution.

### `docs/ddd/review.md`

**Owner:** `ddd-review`. **Minimum sections:** review scope/date; artifact and validation summary; DDD-fit result; quality-gate results; findings by severity; stale/conflicting artifacts; required owner/action; earliest stage to revisit; next step; chat-summary text. A ready result means documentation is coherent for its stated scope, not that implementation is approved.

## Safe create and update behavior

1. Inspect whether the target path and its scope already exist.
2. Create only missing artifacts within the agreed `docs/ddd/` boundary.
3. Preserve existing prose, metadata, links, and user ownership by default.
4. Update only sections owned by the active skill, using additive or explicitly labeled revisions.
5. Never delete, rename, or replace a user-authored artifact without explicit approval.
6. If existing facts conflict with new evidence, record the conflict, provenance, and `stale` status; do not choose silently.
7. Keep a replacement link and reason when an artifact is superseded.
8. Do not edit product source, tests, configuration, generated files, or deployment artifacts.
9. If the requested change exceeds the boundary or cannot be made safely, stop and report the exact path and decision needed.

## Ownership matrix

| Artifact | Discover | Strategic | Tactical | Adoption | Review |
| --- | --- | --- | --- | --- | --- |
| `README.md` | consult | consult | consult | consult | steward |
| `assessment.md` | own | consult | consult | consult | validate |
| `domain-vision.md` | own initial | update | consult | consult | validate |
| `ubiquitous-language.md` | contribute | own | contribute | consult | validate |
| `domain-map.md` | consult | own | consult | consult | validate |
| `context-map.md` | consult | own | consult | consult | validate |
| `contexts/` | consult | own | contribute | consult | validate |
| `models/` | consult | consult | own | consult | validate |
| `adoption-plan.md` | consult | consult | contribute | own | validate |
| `review.md` | consult | consult | consult | consult | own |

`ddd` coordinates but does not silently take ownership from a focused stage. Review may annotate any artifact with findings but does not rewrite the domain model.
