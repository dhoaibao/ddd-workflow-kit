# Context relationships

| Field | Value |
| --- | --- |
| `scope` | _only contexts/relationships touching the selected increment_ |
| `state` | _working, decision-needed, current, stale, or superseded_ |

Generate this artifact only when two or more contexts and their direction or translation affect the slice. A bounded context is a model/language boundary, not automatically a deployment service.

## Touched context inventory

| Context | Purpose/boundary | Decision owner | Key language/lifecycle | Evidence |
| --- | --- | --- | --- | --- |
| _selected context_ | _in/out scope_ | _owner_ | _terms_ | _source_ |

## Touched relationships

Upstream/downstream convention: upstream supplies the capability and defines the contract; downstream consumes it and absorbs the translation cost (Evans Customer/Supplier; see `references/strategic-method.md`).

| Upstream | Downstream | Direction/contract | Translation | Consistency/failure | Evidence/uncertainty |
| --- | --- | --- | --- | --- | --- |
| _context_ | _context_ | _ownership and communication_ | _mapping_ | _only material semantics_ | _source_ |

## Boundary decision

- **Selected increment consequence:** _why this relationship is needed now._
- **Unresolved decision:** _only if it blocks the increment._
