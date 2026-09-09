# Discovery artifact contracts

These contracts are the discovery slice of the shared artifact design. They intentionally mirror the repository's common metadata and lifecycle rules while keeping this package self-contained.

## Common metadata

Each artifact begins with one H1 and a metadata table containing:

| Field | Allowed or required meaning |
| --- | --- |
| `artifact` | Stable type: `assessment`, `domain-vision`, or `ubiquitous-language`. |
| `status` | `draft`, `active`, `superseded`, or `archived`. |
| `validation` | `unvalidated`, `partially-validated`, `validated`, or `stale`. |
| `owner` | `ddd-discover` or a named project owner. |
| `scope` | Domain, project, capability, or language scope. |
| `provenance` | Sources, contributors, and dates sufficient to trace claims. |
| `assumptions` | Explicit assumptions or `none recorded`. |
| `open_questions` | Unresolved questions or `none recorded`. |
| `last_updated` | Date of the latest substantive update. |

Body sections distinguish facts, current behavior, desired policy/meaning, obligations, interpretations, proposals, and assumptions. A claim without provenance is not an established fact.

## Safe updates

1. Inspect whether the artifact exists and whether it is user-authored.
2. Create only missing files under `docs/ddd/`.
3. Preserve existing content, metadata, links, and ownership by default.
4. Add or update only discovery-owned sections.
5. Ask before deleting, replacing, renaming, or restructuring ambiguous existing content.
6. Record conflicts as separate claims and mark affected artifacts `stale` when needed.
7. Never edit product source, tests, configuration, generated output, or deployment files.
8. Stop and report the exact path and decision when the requested change exceeds this boundary.

## Minimum sections

### Assessment

Include desired outcomes; scope and mode; complexity and change-risk signals; DDD-fit decision; evidence table; constraints; assumptions; open questions; simpler alternative when `not-fit`; and next-stage recommendation.

### Domain vision

Include domain purpose and scope; users and stakeholders; outcomes; major policies and events; strategic-importance hypotheses; excluded scope; facts versus proposals; and validation record.

### Ubiquitous language

Include term; scope/context; definition; examples and non-examples; source; status (`proposed`, `accepted`, `conflicted`, or `retired`); owner; and conflict/translation notes. Same spelling does not imply same meaning.
