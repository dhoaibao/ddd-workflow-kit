# Context map

| Field | Value |
| --- | --- |
| `artifact` | `context-map` |
| `status` | `draft` |
| `validation` | `unvalidated` |
| `owner` | `ddd-strategic` |
| `scope` | _domain, project, or capability_ |
| `provenance` | _sources, contributors, and dates_ |
| `assumptions` | _explicit assumptions or none recorded_ |
| `open_questions` | _unresolved questions or none recorded_ |
| `last_updated` | _YYYY-MM-DD_ |

A bounded context is a model and language boundary; it is not automatically a deployment service, database, team, or repository.

## Context inventory

| Context | Purpose/outcome | Boundary in/out | Owner | Language/lifecycle | Status/evidence |
| --- | --- | --- | --- | --- | --- |
| _name and link_ | _purpose_ | _in/out_ | _decision owner_ | _key meaning/lifecycle_ | _status and source_ |

## Relationships

| From/upstream | To/downstream | Direction/ownership | Contract/communication | Translation | Consistency/failure assumptions | Evidence/uncertainty |
| --- | --- | --- | --- | --- | --- | --- |
| _context_ | _context_ | _who owns what_ | _mechanism_ | _mapping or none_ | _assumptions_ | _source_ |

Relationship labels are optional shorthand. Describe the observed or proposed relationship rather than applying a catalog mechanically.

## Boundary validation

- **Scenario checks:** _concrete examples._
- **Change/lifecycle:** _different rates or lifecycles._
- **Security/availability:** _constraints._
- **Open questions:** _decision owner and next evidence._
