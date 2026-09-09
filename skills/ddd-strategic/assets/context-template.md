# Bounded context

| Field | Value |
| --- | --- |
| `artifact` | `context` |
| `status` | `draft` |
| `validation` | `unvalidated` |
| `owner` | `ddd-strategic` |
| `scope` | _domain, capability, or context_ |
| `provenance` | _sources, contributors, and dates_ |
| `assumptions` | _explicit assumptions or none recorded_ |
| `open_questions` | _unresolved questions or none recorded_ |
| `last_updated` | _YYYY-MM-DD_ |

This package template is subordinate to the [context-map contract](context-map-template.md). When materialized at `docs/ddd/contexts/<safe-slug>.md`, the emitted artifact must contain this Markdown link (shown as code): `[Context map](../context-map.md)`. That link is the artifact's authority and relationship facts must not be duplicated here.

## Identity and purpose

- **Name:** _context name and safe slug (lowercase ASCII letters/digits with single hyphens; reject ambiguous or unsafe labels)._
- **Purpose/outcome:** _what this model supports._
- **Decision owner:** _stakeholder or team responsible for domain decisions._
- **Boundary in:** _capabilities, terms, and workflows included._
- **Boundary out:** _explicit exclusions._

## Language and scenarios

- **Language:** _context-specific terms and meanings._
- **Key workflow/scenario:** _concrete scenario._
- **Policy difference:** _why this context's model differs._

## Invariants to investigate

- _Candidate invariant, evidence, and unresolved question._

## Relationships

| Direction | Other context | Ownership/contract | Translation | Consistency/failure assumption | Evidence |
| --- | --- | --- | --- | --- | --- |
| _upstream/downstream_ | _context_ | _who decides and how_ | _mapping_ | _assumption_ | _source_ |

## Validation and open questions

- **Validation:** _unvalidated, partially-validated, validated, or stale with evidence._
- **Open questions:** _owner and next evidence._
