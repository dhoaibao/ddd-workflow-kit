# Strategic artifact contracts

New strategic output uses `scope` and `state` (`working`, `decision-needed`, `current`, `stale`, or `superseded`); include `owner` only when a named role must act. Existing legacy metadata remains readable.

## Conditional minimums

- A selected context records purpose/decision owner, in/out boundary, and key slice terms. It records touched relationships/translation only when material, and blocking boundary decisions only when unresolved decisions block this increment.
- `domain-map.md` appears only when classification affects investment, sourcing, or ownership.
- `context-map.md` appears only when at least two contexts and their direction/translation affect the increment; state explicitly that a bounded context is not a deployment service.
- `ubiquitous-language.md` appears only for reused/overloaded/conflicted terms.
- Additional context files appear only when selected or required by a current relationship.

Do not duplicate the full context map inside a context file. Evidence stays beside material claims; empty sections are omitted.

## Safe update

Inspect first and preserve existing prose and legacy fields. For a new context label, lowercase ASCII letters/digits, replace each run of non-alphanumeric separators with one hyphen, trim hyphens, and reject non-ASCII, empty, ambiguous, colliding, or traversal-like labels. Resolve the candidate and require its parent to be exactly `docs/ddd/contexts`; never follow a path that escapes that directory. Update only strategic-owned sections, mark downstream work stale on boundary change, and refuse destructive, collision, unsafe, or out-of-scope paths.
