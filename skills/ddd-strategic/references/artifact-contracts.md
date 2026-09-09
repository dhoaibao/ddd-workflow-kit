# Strategic artifact contracts

These contracts are the strategic slice of the common artifact design. They keep metadata, lifecycle, claims, and safe updates consistent without requiring another package at runtime.

## Common metadata and claims

Each artifact begins with one H1 and a metadata table containing `artifact`, `status`, `validation`, `owner`, `scope`, `provenance`, `assumptions`, `open_questions`, and `last_updated`. Lifecycle values are `draft`, `active`, `superseded`, or `archived`; validation values are `unvalidated`, `partially-validated`, `validated`, or `stale`.

The body distinguishes current behavior, desired policy/meaning, required obligations, facts, interpretations, proposals, and assumptions. Subdomain classifications, boundaries, relationships, and ownership are proposals until named evidence supports them.

## Safe updates

1. Inspect existing paths and ownership before writing.
2. Create only missing strategic artifacts under `docs/ddd/`.
3. Preserve existing prose, metadata, links, and user ownership by default.
4. Update only strategic-owned sections and use additive revisions.
5. Ask before destructive, ambiguous, structural changes, or filename collisions.
6. Record conflicting claims separately; mark affected downstream artifacts stale through `invalidated_stages`.
7. Use a deterministic safe slug for context filenames: lowercase an ASCII label, replace each run of non-alphanumeric separators with one hyphen, trim hyphens, and require only lowercase ASCII letters, digits, and single hyphens. Reject or ask when input is non-ASCII, normalization is empty or ambiguous, distinct labels normalize to the same slug, or the target collides. Resolve the candidate and verify its parent is exactly `docs/ddd/contexts` before writing; never overwrite a collision silently or escape that directory.
8. Never edit product source, tests, configuration, generated output, or deployment files.

## Minimum schemas

### Domain map

Include domain/scope; candidate subdomains; core/supporting/generic/unresolved classification; rationale; evidence; owner; status; capabilities/outcomes; revisit signals; unresolved questions; links to contexts.

### Context map

Include context inventory; purpose, owner, language, lifecycle, and boundary for each context; directional relationships; upstream/downstream ownership; communication or contract; translation; consistency and failure assumptions; evidence; uncertainty; and explicit statement that a bounded context is not automatically a deployment service.

### Context file

Include identity and purpose; boundary in/out; stakeholders and decision owner; language; key workflows/scenarios; invariants to investigate; upstream/downstream relationships; data/consistency/security/availability assumptions; evidence; validation; and open questions. The materialized artifact must contain `[Context map](../context-map.md)` as the authority instead of duplicating the map.

### Ubiquitous language

Include term; context; definition; examples/non-examples; source; status (`proposed`, `accepted`, `conflicted`, or `retired`); owner; and conflict/translation notes. Preserve distinct meanings instead of forcing one global definition.
