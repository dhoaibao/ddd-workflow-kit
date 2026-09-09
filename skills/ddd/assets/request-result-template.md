# Request and result bundles

These examples show the portable `ddd-routing-v1` shape. They contain no target-project facts.

## Request

```json
{
  "version": "ddd-routing-v1",
  "stage": "ddd-discover",
  "objective": "state one bounded objective",
  "scope": "named project/domain/context/slice",
  "artifacts": [{"path": "docs/ddd/assessment.md", "lifecycle": "draft", "validation": "unvalidated", "availability": "available"}],
  "evidence": [],
  "claims": [],
  "provenance": [],
  "assumptions": [],
  "open_questions": [],
  "allowed_paths": ["docs/ddd/"],
  "return_to": "ddd"
}
```

## Result

```json
{
  "version": "ddd-routing-v1",
  "stage": "ddd-discover",
  "status": "partial",
  "changed_artifacts": [{"path": "docs/ddd/assessment.md", "lifecycle": "draft", "validation": "unvalidated", "availability": "available"}],
  "findings": [],
  "handoff": "none",
  "stop": {"reason": "bounded evidence gap", "owner": "ddd-discover", "action": "collect evidence"},
  "invalidated_stages": [],
  "evidence": [],
  "claims": [],
  "provenance": [],
  "assumptions": [],
  "open_questions": [],
  "allowed_paths": ["docs/ddd/"],
  "return_to": "ddd"
}
```

## Transition rules

### Manual fallback

- Named-stage fallback returns the request object exactly unchanged and states the exact stage did not run.
### Normal transition

- A normal transition consumes a valid result and constructs one next request while preserving evidence, claims, provenance, assumptions, open questions, artifact paths, and allowed paths.
- A malformed result returns a bounded protocol stop; it is not repaired.
- `ready` or `complete` from a focused stage never means implementation or deployment approval.
