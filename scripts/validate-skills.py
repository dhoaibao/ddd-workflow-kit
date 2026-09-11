#!/usr/bin/env python3
"""Validate the repository's portable skill packages.

This is a deterministic stdlib-only subset validator. It checks the required
simple frontmatter fields and repository conventions; it does not implement
full YAML or host compatibility validation and ignores unknown optional fields.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FORBIDDEN_RE = re.compile(
    r"(?:\bPi\b|\bClaude\b|\bOpenAI\b|\bAnthropic\b|\bMCP\b|\brtk\b|"
    + r"/" + r"(?:home|Users)/|[A-Za-z]" + ":" + r"\\\\)"
)
DISCOVERY_ASSETS = {
    "assessment-template.md",
    "domain-vision-template.md",
    "ubiquitous-language-template.md",
}
STRATEGIC_ASSETS = {
    "domain-map-template.md",
    "context-map-template.md",
    "context-template.md",
    "ubiquitous-language-template.md",
}
TACTICAL_ASSETS = {"context-model-template.md"}
ADOPTION_ASSETS = {"adoption-plan-template.md"}
REVIEW_ASSETS = {"review-template.md"}
ORCHESTRATOR_ASSETS = {"request-result-template.md", "ddd-readme-template.md", "implementation-handoff-template.md"}
IMPLEMENTATION_FASTAPI_HDX_ASSETS = {
    "implementation-record-template.md",
    "domain-skeleton.md",
    "service-skeleton.md",
}
PACKAGE_REQUIREMENTS = {
    "ddd-discover": {"assets": DISCOVERY_ASSETS, "minimum_evals": 6},
    "ddd-strategic": {"assets": STRATEGIC_ASSETS, "minimum_evals": 7},
    "ddd-tactical": {"assets": TACTICAL_ASSETS, "minimum_evals": 11},
    "ddd-adoption": {"assets": ADOPTION_ASSETS, "minimum_evals": 10},
    "ddd-review": {"assets": REVIEW_ASSETS, "minimum_evals": 10},
    "ddd": {"assets": ORCHESTRATOR_ASSETS, "minimum_evals": 10},
    "ddd-impl-fastapi-hdx": {"assets": IMPLEMENTATION_FASTAPI_HDX_ASSETS, "minimum_evals": 10},
}
PACKAGE_MANIFEST_CLASSES = {"document", "implementation"}
IMPLEMENTATION_BOUNDARY_MARKERS = ("write boundary", "approval-gated", "migration")
TACTICAL_PREREQUISITE_STOP_CASES = {"missing-strategic-prerequisites", "select-one-context"}
ADOPTION_CASE_CATEGORIES = {
    "greenfield slice", "brownfield baseline", "missing rollback", "ownership gap",
    "unsafe migration", "claim conflict", "partial modeling", "existing artifact",
    "docs-only boundary", "review handoff",
}
ADOPTION_COMPLETE_FIELDS = {
    "mode", "outcome", "first_slice", "artifacts", "evidence", "assumptions",
    "open_questions", "owners", "dependencies", "allowed_paths", "return_to",
}
ADOPTION_NONEMPTY_LIST_FIELDS = {
    "artifacts", "evidence", "assumptions", "open_questions", "owners", "dependencies", "allowed_paths",
}
ADOPTION_BROWNFIELD_FIELDS = {
    "baseline", "seam", "characterization", "compatibility", "observability",
    "data_reconciliation", "rollback_containment",
}
ADOPTION_TEMPLATE_MARKERS = (
    "# Candidate implementation increment", "increment_id", "Target repository/runtime",
    "Baseline revision", "Observable acceptance signals", "Conditional fragment",
    "Decision queue", "Accountable implementation owner",
)
REVIEW_CASE_CATEGORIES = {
    "fit", "provenance", "lifecycle/schema", "vocabulary", "strategic-to-tactical",
    "adoption safety", "cross-artifact conflict/stale routing", "missing artifact", "ready", "docs-only",
}
REVIEW_SCOPE_FIELDS = {"review_scope", "requested_artifacts", "available_artifacts", "evidence", "acceptance_criteria", "allowed_paths", "return_to"}
REVIEW_COMPLETE_FIELDS = REVIEW_SCOPE_FIELDS | {"artifact_summaries", "gate_results", "findings"}
REVIEW_ARTIFACT_FIELDS = {"path", "status", "validation", "owner", "provenance"}
REVIEW_FINDING_FIELDS = {"severity", "evidence", "provenance", "owner", "action", "status", "affected_artifact", "earliest_stage"}
REVIEW_SEVERITIES = {"info", "follow-up", "blocked", "invalidated"}
REVIEW_FINDING_STATUSES = {"open", "routed", "accepted", "resolved"}
REVIEW_EARLIEST_STAGES = {"ddd-discover", "ddd-strategic", "ddd-tactical", "ddd-adoption", "ddd-review"}
REVIEW_GATE_NAMES = {"fit", "provenance", "lifecycle_schema", "vocabulary", "strategic_tactical", "adoption_safety", "cross_artifact"}
REVIEW_GATE_STATUSES = {"pass", "follow-up", "blocked", "not-applicable"}
REVIEW_TEMPLATE_MARKERS = (
    "# Increment review", "Increment and authority set", "documentation_readiness",
    "increment_gate", "passed gates", "Findings and decision queue", "Next action",
    "Accountable implementation owner", "docs/ddd/review.md",
)
ORCHESTRATOR_CASE_CATEGORIES = {
    "normal flow", "direct invocation", "manual fallback", "normal transition", "missing evidence",
    "non-fit", "invalidation loop", "malformed result", "index ownership", "docs-only",
}
ORCHESTRATOR_STAGES = {"ddd-discover", "ddd-strategic", "ddd-tactical", "ddd-adoption", "ddd-review"}
ORCHESTRATOR_REQUEST_FIELDS = {
    "version", "stage", "objective", "scope", "artifacts", "evidence", "claims", "provenance",
    "assumptions", "open_questions", "allowed_paths", "return_to",
}
ORCHESTRATOR_RESULT_FIELDS = {
    "version", "stage", "status", "changed_artifacts", "findings", "handoff", "stop",
    "invalidated_stages", "evidence", "claims", "provenance", "assumptions", "open_questions",
    "allowed_paths", "return_to",
}
ORCHESTRATOR_RESULT_ECHO_FIELDS = {"objective", "scope", "artifacts"}
ORCHESTRATOR_RESULT_STATUSES = {"complete", "partial", "blocked", "ready", "not-fit-conflict", "strategic-conflict", "invalidated", "protocol-error"}
ORCHESTRATOR_PRESERVED_FIELDS = {"evidence", "claims", "provenance", "assumptions", "open_questions", "artifacts", "allowed_paths"}
ORCHESTRATOR_ARTIFACT_FIELDS = {"path", "lifecycle", "validation", "availability"}
ORCHESTRATOR_LIFECYCLES = {"draft", "active", "superseded", "archived", "none"}
ORCHESTRATOR_VALIDATIONS = {"unvalidated", "partially-validated", "validated", "stale", "not-applicable"}
ORCHESTRATOR_AVAILABILITIES = {"available", "missing", "partial", "out-of-scope", "none"}
ORCHESTRATOR_STATES = {"working", "decision-needed", "current", "stale", "superseded"}
ORCHESTRATOR_STATE_MAPPING = {
    "working": ("draft", "unvalidated"),
    "decision-needed": ("draft", "unvalidated"),
    "current": ("active", "validated"),
    "stale": ("preserve", "stale"),
    "superseded": ("superseded", "stale"),
}
IMPLEMENTATION_GATE_KEYS = {
    "version", "increment_id", "target", "owner", "outcome", "in_scope", "out_of_scope",
    "return_on_conflict", "acceptance_signals", "containment", "accepted_assumptions",
    "deferred_questions", "out_of_scope_questions", "question_dispositions",
    "documentation_readiness", "increment_gate", "ratification", "authoritative_revisions",
}
IMPLEMENTATION_GATE_TARGET_KEYS = {"repository", "runtime", "baseline_revision"}
IMPLEMENTATION_GATE_AUTHORITY_KEYS = {"path", "sections", "revision", "role"}
IMPLEMENTATION_GATE_DISPOSITION_KEYS = {"id", "disposition", "status", "issue", "impact", "owner", "action", "affected_artifacts", "revisit_trigger"}
IMPLEMENTATION_GATE_DISPOSITION_STATUS_MATRIX = {
    "blocking": {"open", "resolved"},
    "invalidating": {"open", "resolved"},
    "decision-required": {"open", "resolved"},
    "accepted-assumption": {"resolved"},
    "deferred": {"deferred"},
    "out-of-scope": {"closed"},
    "resolved": {"resolved"},
}
IMPLEMENTATION_GATE_RATIFICATION_RECORD_KEYS = {
    "decision", "owner", "date", "increment_id", "target_repository", "target_runtime", "baseline_revision",
    "accepted_revisions", "accepted_assumptions", "deferred_questions", "out_of_scope_questions",
    "question_dispositions", "acceptance_signals", "containment_limitations", "outcome", "in_scope",
    "out_of_scope", "return_on_conflict",
}
IMPLEMENTATION_GATE_RATIFICATION_KEYS = {
    "not-yet-requested": {"state"},
    "pending": {"state"},
    "authorized": {"state", "record"},
    "declined": {"state", "record"},
}
IMPLEMENTATION_GATE_RETURN_TARGETS = {"ddd", *ORCHESTRATOR_STAGES}
ORCHESTRATOR_INDEX_MARKERS = {
    "project-scope", "routing-status", "artifact-index", "active-contexts", "validation-summary",
    "open-questions", "provenance-policy", "safe-update-policy", "ddd-review-owned:latest-review",
}
ORCHESTRATOR_TEMPLATE_MARKERS = (
    "Request and result bundles", "ddd-routing-v1", "Manual fallback", "Normal transition",
    "DDD artifact index", "ddd-owned:routing-status:start", "ddd-review-owned:latest-review:start",
    "docs/ddd/README.md", "documentation_readiness", "increment_gate", "extensions", "declined decision", "target/baseline identity", "reason",
)
TACTICAL_REQUIRED_INPUT_FIELDS = {
    "purpose", "outcome", "vocabulary", "commands", "scenarios", "relationships",
    "decision_owner", "evidence", "provenance", "assumptions", "open_questions",
    "candidate_invariants", "allowed_paths", "artifact_ownership", "return_to",
}
TACTICAL_CONTEXT_FIELDS = {"name", "safe_slug", "path", "validation"}
TACTICAL_NONEMPTY_LIST_FIELDS = {"vocabulary", "commands", "scenarios", "evidence", "provenance", "candidate_invariants", "allowed_paths"}
TACTICAL_OPTIONAL_LIST_FIELDS = {"relationships", "assumptions", "open_questions"}
TACTICAL_CLAIM_LINK_MARKERS = (
    "| Command/use case | Claim IDs |",
    "| Entity | Claim IDs |",
    "| Value object | Claim IDs |",
    "| Aggregate/root | Protected immediate invariant | Claim IDs |",
    "| Contract | Claim IDs |",
    "| Element | Claim IDs |",
    "| Past-tense event | Claim IDs |",
    "| Decision area | Claim IDs |",
    "| Pattern | Claim IDs |",
)
REQUIRED_EVAL_FIELDS = {"id", "title", "prompt", "input", "expected_outcomes", "forbidden_outcomes"}
LEAN_CASE_IDS = {
    "non-fit-stop", "one-context-slice", "conditional-artifacts", "omit-optional-patterns",
    "review-exception-summary", "documentation-ready-gate-blocked", "deferred-out-of-scope",
    "blocking-not-reclassified", "consolidated-decision-queue", "handoff-preconditions",
    "ratification-one-handoff", "stale-handoff-invalidation", "coding-agent-reading-order",
    "legacy-preserved", "docs-only-boundary",
}
AUTHORITY_REVISION_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
IMPLEMENTATION_GATE_REQUIRED = {
    "version", "increment_id", "target", "owner", "acceptance_signals", "containment",
    "accepted_assumptions", "deferred_questions", "out_of_scope_questions", "question_dispositions",
    "outcome", "in_scope", "out_of_scope", "return_on_conflict",
    "documentation_readiness", "increment_gate", "ratification", "authoritative_revisions",
}
IMPLEMENTATION_GATE_DISPOSITIONS = {
    "blocking", "invalidating", "decision-required", "accepted-assumption", "deferred", "out-of-scope", "resolved",
}


class ValidationError(Exception):
    """A deterministic validation failure."""


def fail(message: str) -> None:
    raise ValidationError(message)


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        fail(f"{path}: missing opening frontmatter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError:
        fail(f"{path}: missing closing frontmatter delimiter")
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):[ \t]*(.*)$", line)
        if not match:
            # Unknown complex YAML is intentionally outside this subset.
            continue
        key, value = match.groups()
        values[key] = value.strip().strip('"\'')
    for key in ("name", "description"):
        if key not in values or not values[key]:
            fail(f"{path}: required simple scalar {key} is missing or empty")
    return values


def check_relative_links(skill_root: Path, skill_file: Path) -> None:
    text = skill_file.read_text(encoding="utf-8")
    for raw_target in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", text):
        if raw_target.startswith(("http://", "https://", "mailto:")):
            continue
        target = (skill_file.parent / raw_target).resolve()
        if skill_root.resolve() not in target.parents and target != skill_root.resolve():
            fail(f"{skill_file}: relative link escapes package: {raw_target}")
        if not target.exists():
            fail(f"{skill_file}: referenced relative file does not exist: {raw_target}")


def validate_skill(skill_root: Path) -> None:
    skill_file = skill_root / "SKILL.md"
    if not skill_file.is_file():
        fail(f"{skill_root}: missing SKILL.md")
    metadata = parse_frontmatter(skill_file)
    name = metadata["name"]
    description = metadata["description"]
    if not NAME_RE.fullmatch(name):
        fail(f"{skill_file}: name must be lowercase alphanumeric words joined by hyphens: {name!r}")
    if name != skill_root.name:
        fail(f"{skill_file}: name {name!r} does not match directory {skill_root.name!r}")
    if len(name) > 64:
        fail(f"{skill_file}: name exceeds 64 characters")
    if not 1 <= len(description) <= 1024:
        fail(f"{skill_file}: description must be 1-1024 characters")
    line_count = len(skill_file.read_text(encoding="utf-8").splitlines())
    if line_count >= 500:
        fail(f"{skill_file}: instruction length is {line_count} lines; keep it under 500")
    for markdown in sorted(skill_root.rglob("*.md")):
        check_relative_links(skill_root, markdown)

    references = skill_root / "references"
    if references.exists():
        if any(path.is_dir() for path in references.iterdir()):
            fail(f"{references}: references must remain one level deep")
        if not any(references.glob("*")):
            fail(f"{references}: directory is empty")

    requirements = PACKAGE_REQUIREMENTS.get(skill_root.name, {"assets": set(), "minimum_evals": 1})
    required_assets = requirements["assets"]
    assets = skill_root / "assets"
    missing_assets = sorted(name for name in required_assets if not (assets / name).is_file())
    if missing_assets:
        fail(f"{skill_root}: missing required assets: {', '.join(missing_assets)}")


def validate_evals(skill_root: Path) -> None:
    path = skill_root / "evals" / "evals.json"
    if not path.is_file():
        fail(f"{path}: required package-local eval file is missing")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path}: invalid JSON: {exc}")
    if not isinstance(payload, dict) or payload.get("skill") != skill_root.name:
        fail(f"{path}: payload skill must match package directory {skill_root.name!r}")
    cases = payload.get("cases")
    requirements = PACKAGE_REQUIREMENTS.get(skill_root.name, {"minimum_evals": 1})
    minimum = requirements["minimum_evals"]
    if not isinstance(cases, list) or len(cases) < minimum:
        fail(f"{path}: expected at least {minimum} evaluation case(s)")
    ids: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            fail(f"{path}: case {index} is not an object")
        missing = sorted(REQUIRED_EVAL_FIELDS - case.keys())
        if missing:
            fail(f"{path}: case {index} missing fields: {', '.join(missing)}")
        for field in ("id", "title", "prompt"):
            if not isinstance(case[field], str) or not case[field].strip():
                fail(f"{path}: case {index} field {field} must be a nonempty string")
        if not isinstance(case["input"], dict):
            fail(f"{path}: case {case['id']} input must be an object")
        case_id = case["id"]
        if case_id in ids:
            fail(f"{path}: duplicate case id: {case_id}")
        ids.add(case_id)
        for field in ("expected_outcomes", "forbidden_outcomes"):
            values = case[field]
            if not isinstance(values, list) or not values or not all(isinstance(item, str) and item.strip() for item in values):
                fail(f"{path}: case {case_id} field {field} must be a nonempty string list")


def validate_tactical_eval_inputs(skill_root: Path, cases: list[dict]) -> None:
    if skill_root.name != "ddd-tactical":
        return
    for case in cases:
        if case["id"] in TACTICAL_PREREQUISITE_STOP_CASES:
            continue
        payload = case["input"]
        missing = sorted(TACTICAL_REQUIRED_INPUT_FIELDS - payload.keys())
        if missing:
            fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} missing tactical entry fields: {', '.join(missing)}")
        context = payload.get("selected_context")
        if not isinstance(context, dict):
            fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} must have one selected_context")
        missing_context = sorted(TACTICAL_CONTEXT_FIELDS - context.keys())
        if missing_context:
            fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} missing context fields: {', '.join(missing_context)}")
        for field in sorted(TACTICAL_CONTEXT_FIELDS):
            value = context[field]
            if not isinstance(value, str) or not value.strip():
                fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} context field {field} must be a nonempty string")
        if context["validation"] != "validated":
            fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} selected context must be validated")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", context["safe_slug"]):
            fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} has an unsafe context slug")
        expected_context_path = f"docs/ddd/contexts/{context['safe_slug']}.md"
        expected_model_path = f"docs/ddd/models/{context['safe_slug']}.md"
        if context["path"] != expected_context_path:
            fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} context path must reuse its safe slug")
        for field in ("purpose", "outcome", "decision_owner", "return_to"):
            if not isinstance(payload[field], str) or not payload[field].strip():
                fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} field {field} must be a nonempty string")
        for field in sorted(TACTICAL_NONEMPTY_LIST_FIELDS):
            values = payload[field]
            if not isinstance(values, list) or not values or not all(isinstance(item, str) and item.strip() for item in values):
                fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} field {field} must be a nonempty string list")
        for field in sorted(TACTICAL_OPTIONAL_LIST_FIELDS):
            values = payload[field]
            if not isinstance(values, list) or not all(isinstance(item, str) and item.strip() for item in values):
                fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} field {field} must be a string list, possibly empty")
        allowed_paths = set(payload["allowed_paths"])
        permitted_paths = {expected_model_path, expected_context_path, "docs/ddd/ubiquitous-language.md"}
        if not {expected_model_path, expected_context_path}.issubset(allowed_paths) or not allowed_paths.issubset(permitted_paths):
            fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} allowed_paths must contain only the derived model/context paths and optional language path")
        ownership = payload["artifact_ownership"]
        if not isinstance(ownership, dict) or not all(isinstance(ownership.get(key), str) and ownership[key].strip() for key in ("model", "context", "language")):
            fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} artifact_ownership must name model, context, and language owners")


def validate_adoption_eval_inputs(skill_root: Path, cases: list[dict]) -> None:
    if skill_root.name != "ddd-adoption":
        return
    categories = {case.get("category") for case in cases}
    missing_categories = sorted(ADOPTION_CASE_CATEGORIES - categories)
    if missing_categories:
        fail(f"{skill_root / 'evals' / 'evals.json'}: missing adoption evaluation categories: {', '.join(missing_categories)}")
    for case in cases:
        category = case.get("category")
        payload = case["input"]
        if not isinstance(category, str) or not category.strip():
            fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} must name an adoption category")
        entry_status = payload.get("entry_status")
        if entry_status not in {"complete", "incomplete"}:
            fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} entry_status must be complete or incomplete")
        if entry_status == "complete":
            missing = sorted(ADOPTION_COMPLETE_FIELDS - payload.keys())
            if missing:
                fail(f"{skill_root / 'evals' / 'evals.json'}: complete case {case['id']} missing entry fields: {', '.join(missing)}")
            if payload["mode"] not in {"greenfield", "brownfield"}:
                fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} mode must be greenfield or brownfield")
            for field in sorted(ADOPTION_NONEMPTY_LIST_FIELDS):
                values = payload[field]
                if not isinstance(values, list) or not values or not all(isinstance(item, str) and item.strip() for item in values):
                    fail(f"{skill_root / 'evals' / 'evals.json'}: complete case {case['id']} field {field} must be a nonempty string list")
            if payload["allowed_paths"] != ["docs/ddd/adoption-plan.md"]:
                fail(f"{skill_root / 'evals' / 'evals.json'}: complete case {case['id']} allowed_paths must contain only docs/ddd/adoption-plan.md")
            if payload["return_to"] not in {"ddd-tactical", "ddd-adoption"}:
                fail(f"{skill_root / 'evals' / 'evals.json'}: complete case {case['id']} return_to must identify the prior stage or ddd-adoption")
            if payload["mode"] == "brownfield":
                brownfield = payload.get("brownfield")
                if not isinstance(brownfield, dict):
                    fail(f"{skill_root / 'evals' / 'evals.json'}: complete brownfield case {case['id']} must include brownfield safety fields")
                missing_brownfield = sorted(ADOPTION_BROWNFIELD_FIELDS - brownfield.keys())
                if missing_brownfield:
                    fail(f"{skill_root / 'evals' / 'evals.json'}: brownfield case {case['id']} missing safety fields: {', '.join(missing_brownfield)}")
                if not all(isinstance(brownfield[field], str) and brownfield[field].strip() for field in ADOPTION_BROWNFIELD_FIELDS):
                    fail(f"{skill_root / 'evals' / 'evals.json'}: brownfield case {case['id']} safety fields must be nonempty strings")
        else:
            missing_fields = payload.get("missing_fields")
            if not isinstance(missing_fields, list) or not missing_fields or not all(isinstance(item, str) and item.strip() for item in missing_fields):
                fail(f"{skill_root / 'evals' / 'evals.json'}: incomplete case {case['id']} must name missing_fields")
    review_cases = [case for case in cases if case.get("category") == "review handoff"]
    if len(review_cases) != 1:
        fail(f"{skill_root / 'evals' / 'evals.json'}: expected exactly one review handoff case")
    review = review_cases[0]
    if review["input"].get("entry_status") != "complete":
        fail(f"{skill_root / 'evals' / 'evals.json'}: review handoff case must have complete entry fields")
    if not any("exactly one" in outcome.lower() and "ddd-review" in outcome for outcome in review["expected_outcomes"]):
        fail(f"{skill_root / 'evals' / 'evals.json'}: review handoff case must require exactly one ddd-review request")


def validate_adoption_contract(skill_root: Path) -> None:
    if skill_root.name != "ddd-adoption":
        return
    template = skill_root / "assets" / "adoption-plan-template.md"
    text = template.read_text(encoding="utf-8")
    missing = [marker for marker in ADOPTION_TEMPLATE_MARKERS if marker not in text]
    if missing:
        fail(f"{template}: adoption contract markers missing: {', '.join(missing)}")
    if "## Review handoff and boundary" in text or "ddd-implementation-gate-v1" in text:
        fail(f"{template}: adoption output template must omit transport/boundary teaching")
    if re.search(r"Accountable owner:", text):
        fail(f"{template}: adoption template must use the unambiguous label 'Accountable implementation owner', not the bare 'Accountable owner'")


def validate_review_eval_inputs(skill_root: Path, cases: list[dict]) -> None:
    if skill_root.name != "ddd-review":
        return
    categories = {case.get("category") for case in cases}
    missing_categories = sorted(REVIEW_CASE_CATEGORIES - categories)
    if missing_categories:
        fail(f"{skill_root / 'evals' / 'evals.json'}: missing review evaluation categories: {', '.join(missing_categories)}")
    for case in cases:
        category = case.get("category")
        payload = case["input"]
        if not isinstance(category, str) or not category.strip():
            fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} must name a review category")
        missing_scope = sorted(REVIEW_SCOPE_FIELDS - payload.keys())
        if missing_scope:
            fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} missing review scope fields: {', '.join(missing_scope)}")
        if not isinstance(payload["review_scope"], str) or not payload["review_scope"].strip():
            fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} review_scope must be nonempty")
        for field in ("requested_artifacts", "available_artifacts", "evidence", "acceptance_criteria", "allowed_paths"):
            values = payload[field]
            if not isinstance(values, list) or not all(isinstance(item, str) and item.strip() for item in values):
                fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} field {field} must be a string list")
        if payload["allowed_paths"] != ["docs/ddd/review.md"]:
            fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} allowed_paths must contain only docs/ddd/review.md")
        if payload.get("entry_status") not in {"complete", "incomplete"}:
            fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} entry_status must be complete or incomplete")
        if payload["entry_status"] == "complete":
            missing = sorted(REVIEW_COMPLETE_FIELDS - payload.keys())
            if missing:
                fail(f"{skill_root / 'evals' / 'evals.json'}: complete case {case['id']} missing review fields: {', '.join(missing)}")
            summaries = payload["artifact_summaries"]
            if not isinstance(summaries, list) or not summaries:
                fail(f"{skill_root / 'evals' / 'evals.json'}: complete case {case['id']} must include artifact_summaries")
            for summary in summaries:
                if not isinstance(summary, dict):
                    fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} artifact summary must be an object")
                missing_summary = sorted(REVIEW_ARTIFACT_FIELDS - summary.keys())
                if missing_summary:
                    fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} artifact summary missing: {', '.join(missing_summary)}")
                if not all(isinstance(summary[field], str) and summary[field].strip() for field in REVIEW_ARTIFACT_FIELDS):
                    fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} artifact summary fields must be nonempty strings")
            gates = payload["gate_results"]
            if not isinstance(gates, dict) or set(gates) != REVIEW_GATE_NAMES:
                fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} gate_results must contain exactly the review gate names")
            if not all(gates[name] in REVIEW_GATE_STATUSES for name in REVIEW_GATE_NAMES):
                fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} gate_results contain an invalid status")
        else:
            missing_fields = payload.get("missing_fields")
            if not isinstance(missing_fields, list) or not missing_fields or not all(isinstance(item, str) and item.strip() for item in missing_fields):
                fail(f"{skill_root / 'evals' / 'evals.json'}: incomplete case {case['id']} must name missing_fields")
        findings = payload.get("findings", [])
        if not isinstance(findings, list):
            fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} findings must be a list")
        for finding in findings:
            if not isinstance(finding, dict):
                fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} finding must be an object")
            missing_finding = sorted(REVIEW_FINDING_FIELDS - finding.keys())
            if missing_finding:
                fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} finding missing: {', '.join(missing_finding)}")
            for field in REVIEW_FINDING_FIELDS - {"severity", "status", "earliest_stage"}:
                if not isinstance(finding[field], str) or not finding[field].strip():
                    fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} finding field {field} must be nonempty")
            if finding["severity"] not in REVIEW_SEVERITIES:
                fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} finding has invalid severity")
            if finding["status"] not in REVIEW_FINDING_STATUSES:
                fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} finding has invalid status")
            if finding["earliest_stage"] not in REVIEW_EARLIEST_STAGES:
                fail(f"{skill_root / 'evals' / 'evals.json'}: case {case['id']} finding has invalid earliest stage")
    ready_cases = [case for case in cases if case.get("category") == "ready"]
    if len(ready_cases) != 1:
        fail(f"{skill_root / 'evals' / 'evals.json'}: expected exactly one ready case")
    ready = ready_cases[0]
    if ready["input"].get("entry_status") != "complete" or ready["input"].get("findings") != []:
        fail(f"{skill_root / 'evals' / 'evals.json'}: ready case must have complete entry fields and no findings")
    if not all(ready["input"]["gate_results"][name] == "pass" for name in REVIEW_GATE_NAMES):
        fail(f"{skill_root / 'evals' / 'evals.json'}: ready case must pass every review gate")
    stale_cases = [case for case in cases if case.get("category") == "cross-artifact conflict/stale routing"]
    if len(stale_cases) != 1 or not isinstance(stale_cases[0]["input"].get("stale_routing"), dict):
        fail(f"{skill_root / 'evals' / 'evals.json'}: stale-routing case must include stale_routing")
    stale = stale_cases[0]["input"]["stale_routing"]
    required_stale = {"affected_artifacts", "earliest_stage", "owner", "action", "evidence", "revisit_trigger"}
    if required_stale - stale.keys() or stale["earliest_stage"] not in REVIEW_EARLIEST_STAGES or not isinstance(stale["affected_artifacts"], list) or not stale["affected_artifacts"]:
        fail(f"{skill_root / 'evals' / 'evals.json'}: stale-routing case has incomplete earliest-stage routing")


def validate_review_contract(skill_root: Path) -> None:
    if skill_root.name != "ddd-review":
        return
    template = skill_root / "assets" / "review-template.md"
    text = template.read_text(encoding="utf-8")
    missing = [marker for marker in REVIEW_TEMPLATE_MARKERS if marker not in text]
    if missing:
        fail(f"{template}: review contract markers missing: {', '.join(missing)}")
    if "docs/ddd/review.md" not in text or "decision-queue" not in text or "latest-review" not in text:
        fail(f"{template}: review must expose the visible owned artifact and README marker contract")
    if "Disposition" not in text or "Affected artifacts" not in text or "Revisit trigger" not in text:
        fail(f"{template}: decision queue must expose impact, disposition, affected paths, and revisit trigger")
    rendered = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    if "## Boundary" in rendered or "| _DQ-001_ |" in rendered or "**Stale/invalidated authorities:**" in rendered:
        fail(f"{template}: review output must omit unconditional boundary/finding/stale-authority filler")
    if "## Next action" not in text:
        fail(f"{template}: default rendered heading must be Next action, not a stale-routing heading")
    if "Conditional fragment: only when a stale or invalidated authority exists for this increment" not in text or "Stale/invalidated authorities:" not in text.split("Conditional fragment: only when a stale or invalidated authority exists for this increment", 1)[1].split("-->", 1)[0]:
        fail(f"{template}: stale/invalidated authorities line must live only inside a non-rendering conditional fragment")


def validate_orchestrator_artifacts(path: Path, values: object, case_id: str, field: str) -> None:
    if not isinstance(values, list):
        fail(f"{path}: case {case_id} field {field} must be an artifact-record list")
    for record in values:
        if not isinstance(record, dict):
            fail(f"{path}: case {case_id} field {field} must reject bare-string artifact records")
        missing = sorted(ORCHESTRATOR_ARTIFACT_FIELDS - record.keys())
        if missing:
            fail(f"{path}: case {case_id} artifact record in {field} missing: {', '.join(missing)}")
        if not isinstance(record["path"], str) or not record["path"].strip():
            fail(f"{path}: case {case_id} artifact record path must be nonempty")
        if record["lifecycle"] not in ORCHESTRATOR_LIFECYCLES:
            fail(f"{path}: case {case_id} artifact record has invalid lifecycle")
        if record["validation"] not in ORCHESTRATOR_VALIDATIONS:
            fail(f"{path}: case {case_id} artifact record has invalid validation")
        if record["availability"] not in ORCHESTRATOR_AVAILABILITIES:
            fail(f"{path}: case {case_id} artifact record has invalid availability")
        if "state" in record:
            state = record["state"]
            if state not in ORCHESTRATOR_STATES:
                fail(f"{path}: case {case_id} artifact record has invalid lean state")
            lifecycle, validation = ORCHESTRATOR_STATE_MAPPING[state]
            if lifecycle == "preserve":
                if record["validation"] != validation or record["lifecycle"] not in {"draft", "active", "superseded", "archived"}:
                    fail(f"{path}: case {case_id} stale artifact must preserve a valid prior lifecycle and use stale validation")
            elif (record["lifecycle"], record["validation"]) != (lifecycle, validation):
                fail(f"{path}: case {case_id} artifact record state/lifecycle/validation mapping is inconsistent")


def validate_authority_revision(path: Path, value: object, case_id: str, field: str) -> None:
    if not isinstance(value, str) or not AUTHORITY_REVISION_RE.fullmatch(value):
        fail(f"{path}: case {case_id} {field} must be authority-revision-v1 sha256:<64 lowercase hex digits>")


def validate_implementation_gate(path: Path, extension: object, case_id: str) -> None:
    if extension is None:
        return
    if not isinstance(extension, dict):
        fail(f"{path}: case {case_id} implementation gate extension must be an object")
    unknown = set(extension) - IMPLEMENTATION_GATE_KEYS
    if unknown:
        fail(f"{path}: case {case_id} implementation gate has unknown fields: {sorted(unknown)}")
    missing = sorted(IMPLEMENTATION_GATE_REQUIRED - extension.keys())
    if missing:
        fail(f"{path}: case {case_id} implementation gate missing: {', '.join(missing)}")
    if extension.get("version") != "ddd-implementation-gate-v1":
        fail(f"{path}: case {case_id} implementation gate version is invalid")
    if not isinstance(extension.get("increment_id"), str) or not extension["increment_id"].strip():
        fail(f"{path}: case {case_id} implementation gate increment_id must be nonempty")
    target = extension.get("target")
    if not isinstance(target, dict) or set(target) != IMPLEMENTATION_GATE_TARGET_KEYS or not all(isinstance(target.get(key), str) and target[key].strip() for key in IMPLEMENTATION_GATE_TARGET_KEYS):
        fail(f"{path}: case {case_id} implementation gate target must contain exactly repository, runtime, and baseline_revision")
    if not isinstance(extension.get("owner"), str) or not extension["owner"].strip():
        fail(f"{path}: case {case_id} implementation gate owner must be named")
    for field in ("acceptance_signals", "containment", "accepted_assumptions", "deferred_questions", "out_of_scope_questions", "question_dispositions", "authoritative_revisions", "in_scope", "out_of_scope"):
        if not isinstance(extension[field], list):
            fail(f"{path}: case {case_id} implementation gate {field} must be a list")
    for field in ("acceptance_signals", "containment", "accepted_assumptions", "deferred_questions", "out_of_scope_questions", "in_scope", "out_of_scope"):
        if not all(isinstance(item, str) and item.strip() for item in extension[field]):
            fail(f"{path}: case {case_id} implementation gate {field} must contain nonempty strings")
    if not isinstance(extension["outcome"], str) or not extension["outcome"].strip() or extension["return_on_conflict"] not in IMPLEMENTATION_GATE_RETURN_TARGETS:
        fail(f"{path}: case {case_id} implementation gate outcome and return_on_conflict must use a focused DDD return target")
    if not extension["in_scope"]:
        fail(f"{path}: case {case_id} implementation gate in_scope must name at least one executable behavior")
    seen_disposition_ids = set()
    for disposition in extension["question_dispositions"]:
        if not isinstance(disposition, dict) or set(disposition) != IMPLEMENTATION_GATE_DISPOSITION_KEYS:
            fail(f"{path}: case {case_id} question dispositions must contain exactly the typed uncertainty-routing fields")
        if not isinstance(disposition["id"], str) or not disposition["id"].strip() or disposition["disposition"] not in IMPLEMENTATION_GATE_DISPOSITIONS or disposition["status"] not in {"open", "resolved", "deferred", "closed"}:
            fail(f"{path}: case {case_id} question disposition identity/status is invalid")
        if disposition["id"] in seen_disposition_ids:
            fail(f"{path}: case {case_id} question disposition ids must be unique")
        seen_disposition_ids.add(disposition["id"])
        if disposition["status"] not in IMPLEMENTATION_GATE_DISPOSITION_STATUS_MATRIX.get(disposition["disposition"], set()):
            fail(f"{path}: case {case_id} question disposition status {disposition['status']} is not legal for disposition {disposition['disposition']}")
        if not isinstance(disposition.get("issue"), str) or not disposition["issue"].strip():
            fail(f"{path}: case {case_id} question disposition issue must be nonempty")
        if not isinstance(disposition["impact"], str) or not disposition["impact"].strip() or not isinstance(disposition["owner"], str) or not disposition["owner"].strip() or not isinstance(disposition["action"], str) or not disposition["action"].strip() or not isinstance(disposition["revisit_trigger"], str) or not disposition["revisit_trigger"].strip() or not isinstance(disposition["affected_artifacts"], list) or not all(isinstance(item, str) and item.strip() for item in disposition["affected_artifacts"]):
            fail(f"{path}: case {case_id} question disposition routing fields are invalid")
    deferred_issues = [d["issue"] for d in extension["question_dispositions"] if d.get("disposition") == "deferred"]
    out_of_scope_issues = [d["issue"] for d in extension["question_dispositions"] if d.get("disposition") == "out-of-scope"]
    accepted_assumption_issues = [d["issue"] for d in extension["question_dispositions"] if d.get("disposition") == "accepted-assumption"]
    if sorted(deferred_issues) != sorted(extension["deferred_questions"]):
        fail(f"{path}: case {case_id} deferred_questions must equal exactly the deferred disposition issues, with no orphans")
    if sorted(out_of_scope_issues) != sorted(extension["out_of_scope_questions"]):
        fail(f"{path}: case {case_id} out_of_scope_questions must equal exactly the out-of-scope disposition issues, with no orphans")
    if sorted(accepted_assumption_issues) != sorted(extension["accepted_assumptions"]):
        fail(f"{path}: case {case_id} accepted_assumptions must equal exactly the accepted-assumption disposition issues, with no orphans")
    if extension.get("documentation_readiness") not in {"ready", "follow-up", "blocked", "invalidated"}:
        fail(f"{path}: case {case_id} implementation gate documentation_readiness is invalid")
    if extension.get("increment_gate") not in {"blocked", "awaiting-ratification", "authorized"}:
        fail(f"{path}: case {case_id} implementation gate increment_gate is invalid")
    ratification = extension.get("ratification")
    if not isinstance(ratification, dict) or ratification.get("state") not in IMPLEMENTATION_GATE_RATIFICATION_KEYS:
        fail(f"{path}: case {case_id} ratification must contain a valid state")
    if set(ratification) != IMPLEMENTATION_GATE_RATIFICATION_KEYS[ratification["state"]]:
        fail(f"{path}: case {case_id} ratification fields are invalid for state {ratification['state']}")
    if ratification["state"] in {"not-yet-requested", "pending"} and "record" in ratification:
        fail(f"{path}: case {case_id} pending/not-yet-requested ratification cannot carry a decision record")
    for disposition in extension["question_dispositions"]:
        if not isinstance(disposition, dict) or disposition.get("disposition") not in IMPLEMENTATION_GATE_DISPOSITIONS:
            fail(f"{path}: case {case_id} question disposition is invalid")
        if disposition.get("status") not in {"open", "resolved", "deferred", "closed"}:
            fail(f"{path}: case {case_id} question disposition status is invalid")
        if disposition.get("disposition") == "decision-required" and disposition.get("status") != "resolved":
            fail(f"{path}: case {case_id} unresolved decision-required item blocks ratification")
        if disposition.get("disposition") in {"blocking", "invalidating"} and disposition.get("status") != "resolved":
            fail(f"{path}: case {case_id} open blocking/invalidating item blocks the gate")
    authorities_by_path = {}
    for authority in extension["authoritative_revisions"]:
        if not isinstance(authority, dict) or set(authority) != IMPLEMENTATION_GATE_AUTHORITY_KEYS:
            fail(f"{path}: case {case_id} authority revision must contain exactly path, sections, revision, and role")
        authority_parts = authority["path"].split("/") if isinstance(authority.get("path"), str) else []
        if not isinstance(authority["path"], str) or not re.fullmatch(r"docs/ddd(?:/[A-Za-z0-9._-]+)+\.md", authority["path"]) or any(part in {"", ".", ".."} for part in authority_parts):
            fail(f"{path}: case {case_id} authority path must be a normalized relative Markdown path under docs/ddd")
        if authority["path"] in authorities_by_path:
            fail(f"{path}: case {case_id} authority paths must be unique")
        authorities_by_path[authority["path"]] = authority
        if not isinstance(authority["sections"], list) or not authority["sections"] or not all(isinstance(section, str) and section.strip() for section in authority["sections"]):
            fail(f"{path}: case {case_id} authority sections must be nonempty exact headings")
        validate_authority_revision(path, authority["revision"], case_id, "authority revision")
        if not isinstance(authority["role"], str) or not authority["role"].strip():
            fail(f"{path}: case {case_id} authority role must be nonempty")
    if extension["increment_gate"] == "awaiting-ratification":
        if extension["documentation_readiness"] != "ready":
            fail(f"{path}: case {case_id} awaiting-ratification requires documentation_readiness ready")
        if ratification["state"] != "pending":
            fail(f"{path}: case {case_id} awaiting-ratification requires pending ratification")
        if not extension["acceptance_signals"] or not extension["containment"] or not authorities_by_path:
            fail(f"{path}: case {case_id} awaiting-ratification requires acceptance, containment, and authorities")
    if extension["increment_gate"] == "authorized" and not authorities_by_path:
        fail(f"{path}: case {case_id} authorized gate requires at least one authority")
    if extension["increment_gate"] == "blocked" and ratification["state"] not in {"not-yet-requested", "declined"}:
        fail(f"{path}: case {case_id} blocked gate requires not-yet-requested or declined ratification")
    if extension["increment_gate"] in {"awaiting-ratification", "authorized"} and any(item.get("disposition") in {"blocking", "invalidating"} and item.get("status") != "resolved" for item in extension["question_dispositions"]):
        fail(f"{path}: case {case_id} blocked or invalidating findings cannot cross the gate")
    if ratification["state"] == "authorized":
        record = ratification.get("record")
        if not isinstance(record, dict) or set(record) != IMPLEMENTATION_GATE_RATIFICATION_RECORD_KEYS:
            fail(f"{path}: case {case_id} authorized ratification requires exactly the complete record fields")
        if record.get("decision") != "authorized" or record.get("increment_id") != extension["increment_id"] or not isinstance(record.get("owner"), str) or not record["owner"].strip() or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(record.get("date"))):
            fail(f"{path}: case {case_id} ratification record identity is invalid")
        if record.get("target_repository") != extension["target"].get("repository") or record.get("target_runtime") != extension["target"].get("runtime") or record.get("baseline_revision") != extension["target"].get("baseline_revision"):
            fail(f"{path}: case {case_id} ratification target/runtime/baseline does not match gate target")
        for field in ("accepted_assumptions", "deferred_questions", "out_of_scope_questions", "question_dispositions", "acceptance_signals", "containment_limitations"):
            if not isinstance(record.get(field), list):
                fail(f"{path}: case {case_id} ratification {field} must be a list")
        for field in ("accepted_assumptions", "deferred_questions", "out_of_scope_questions", "acceptance_signals", "containment_limitations", "in_scope", "out_of_scope"):
            if not all(isinstance(item, str) and item.strip() for item in record[field]):
                fail(f"{path}: case {case_id} ratification {field} must contain nonempty strings")
        for field in ("outcome", "return_on_conflict"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                fail(f"{path}: case {case_id} ratification {field} must be a nonempty string")
        for disposition in record["question_dispositions"]:
            if not isinstance(disposition, dict) or set(disposition) != IMPLEMENTATION_GATE_DISPOSITION_KEYS or not isinstance(disposition.get("id"), str) or not disposition["id"].strip() or disposition.get("disposition") not in IMPLEMENTATION_GATE_DISPOSITIONS or disposition.get("status") not in {"open", "resolved", "deferred", "closed"} or not isinstance(disposition.get("impact"), str) or not disposition["impact"].strip() or not isinstance(disposition.get("owner"), str) or not disposition["owner"].strip() or not isinstance(disposition.get("action"), str) or not disposition["action"].strip() or not isinstance(disposition.get("revisit_trigger"), str) or not disposition["revisit_trigger"].strip() or not isinstance(disposition.get("affected_artifacts"), list) or not all(isinstance(item, str) and item.strip() for item in disposition["affected_artifacts"]):
                fail(f"{path}: case {case_id} ratification question dispositions are not typed/routed")
        if any(record[field] != extension[field] for field in ("accepted_assumptions", "deferred_questions", "out_of_scope_questions", "question_dispositions", "acceptance_signals", "in_scope", "out_of_scope")) or record["containment_limitations"] != extension["containment"] or record["outcome"] != extension["outcome"] or record["return_on_conflict"] != extension["return_on_conflict"]:
            fail(f"{path}: case {case_id} ratification contract fields must equal the gate")
        accepted = record.get("accepted_revisions")
        if not isinstance(accepted, list) or not accepted or any(not isinstance(item, dict) or set(item) != IMPLEMENTATION_GATE_AUTHORITY_KEYS or not isinstance(item.get("path"), str) or not re.fullmatch(r"docs/ddd(?:/[A-Za-z0-9._-]+)+\.md", item["path"]) or any(part in {"", ".", ".."} for part in item["path"].split("/")) or not isinstance(item.get("revision"), str) or not isinstance(item.get("sections"), list) or not item["sections"] or not all(isinstance(section, str) and section.strip() for section in item["sections"]) or not isinstance(item.get("role"), str) or not item["role"].strip() for item in accepted):
            fail(f"{path}: case {case_id} ratification accepted_revisions must carry the complete path/sections/revision/role authority record")
        accepted_by_path = {item["path"]: item for item in accepted}
        if len(accepted_by_path) != len(accepted):
            fail(f"{path}: case {case_id} ratification accepted_revisions paths must be unique")
        if accepted_by_path != authorities_by_path:
            fail(f"{path}: case {case_id} ratified revision set must equal the authoritative set exactly, including sections and role")
        for item in accepted:
            validate_authority_revision(path, item["revision"], case_id, "ratified revision")
        if not record["acceptance_signals"] or not record["containment_limitations"]:
            fail(f"{path}: case {case_id} ratification record requires acceptance and containment")
    if ratification["state"] == "declined":
        record = ratification.get("record")
        required_declined = {"decision", "owner", "date", "increment_id", "target_repository", "target_runtime", "baseline_revision", "reason"}
        if not isinstance(record, dict) or set(record) != required_declined or record.get("decision") != "declined" or record.get("increment_id") != extension["increment_id"]:
            fail(f"{path}: case {case_id} declined ratification requires exactly a complete decision record")
        if not isinstance(record.get("owner"), str) or not record["owner"].strip() or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(record.get("date"))) or not isinstance(record.get("reason"), str) or not record["reason"].strip():
            fail(f"{path}: case {case_id} declined ratification record identity/reason is invalid")
        if record.get("target_repository") != extension["target"].get("repository") or record.get("target_runtime") != extension["target"].get("runtime") or record.get("baseline_revision") != extension["target"].get("baseline_revision"):
            fail(f"{path}: case {case_id} declined ratification target/runtime/baseline does not match gate")
    if ratification["state"] == "authorized" and extension["increment_gate"] != "authorized":
        fail(f"{path}: case {case_id} authorized ratification requires the authorized gate")
    if extension["increment_gate"] == "authorized" and ratification["state"] != "authorized":
        fail(f"{path}: case {case_id} authorized gate requires authorized ratification")
    if extension["increment_gate"] == "authorized" and extension["documentation_readiness"] != "ready":
        fail(f"{path}: case {case_id} authorized gate requires documentation_readiness ready")


def validate_orchestrator_request(path: Path, request: object, case_id: str, allow_empty: bool = False) -> None:
    if not isinstance(request, dict):
        fail(f"{path}: case {case_id} request must be an object")
    missing = sorted(ORCHESTRATOR_REQUEST_FIELDS - request.keys())
    if missing:
        fail(f"{path}: case {case_id} request missing fields: {', '.join(missing)}")
    if request.get("version") != "ddd-routing-v1":
        fail(f"{path}: case {case_id} request version must be ddd-routing-v1")
    if request.get("stage") not in ORCHESTRATOR_STAGES:
        fail(f"{path}: case {case_id} request has an unknown stage")
    for field in ("objective", "scope", "return_to"):
        if not isinstance(request[field], str) or (not allow_empty and not request[field].strip()):
            fail(f"{path}: case {case_id} request field {field} must be a nonempty string")
    if request["return_to"] not in ({"ddd"} | ORCHESTRATOR_STAGES):
        fail(f"{path}: case {case_id} request return_to is not a known stage or ddd")
    validate_orchestrator_artifacts(path, request["artifacts"], case_id, "request.artifacts")
    for field in ("evidence", "claims", "provenance", "assumptions", "open_questions", "allowed_paths"):
        values = request[field]
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            fail(f"{path}: case {case_id} request field {field} must be a string list")
    extensions = request.get("extensions", {})
    if not isinstance(extensions, dict):
        fail(f"{path}: case {case_id} request extensions must be an object")
    unknown = set(extensions) - {"ddd-implementation-gate-v1"}
    if unknown:
        fail(f"{path}: case {case_id} request has unknown extensions: {sorted(unknown)}")
    validate_implementation_gate(path, extensions.get("ddd-implementation-gate-v1"), case_id)


def validate_orchestrator_result(path: Path, result: object, case_id: str) -> None:
    if not isinstance(result, dict):
        fail(f"{path}: case {case_id} result must be an object")
    missing = sorted(ORCHESTRATOR_RESULT_FIELDS - result.keys())
    if missing:
        fail(f"{path}: case {case_id} result missing fields: {', '.join(missing)}")
    present_echoes = ORCHESTRATOR_RESULT_ECHO_FIELDS & result.keys()
    if present_echoes and present_echoes != ORCHESTRATOR_RESULT_ECHO_FIELDS:
        fail(f"{path}: case {case_id} result objective/scope/artifacts echoes must be complete")
    if "objective" in result and (not isinstance(result["objective"], str) or not result["objective"].strip() or not isinstance(result["scope"], str) or not result["scope"].strip()):
        fail(f"{path}: case {case_id} result objective and scope echoes must be nonempty strings")
    if "artifacts" in result:
        validate_orchestrator_artifacts(path, result["artifacts"], case_id, "result.artifacts")
    if result.get("version") != "ddd-routing-v1" or result.get("stage") not in ORCHESTRATOR_STAGES:
        fail(f"{path}: case {case_id} result has an invalid version or stage")
    if result.get("status") not in ORCHESTRATOR_RESULT_STATUSES:
        fail(f"{path}: case {case_id} result has an invalid status")
    validate_orchestrator_artifacts(path, result["changed_artifacts"], case_id, "result.changed_artifacts")
    for field in ("findings", "invalidated_stages", "evidence", "claims", "provenance", "assumptions", "open_questions", "allowed_paths"):
        values = result[field]
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            fail(f"{path}: case {case_id} result field {field} must be a string list")
    if result["return_to"] not in ({"ddd"} | ORCHESTRATOR_STAGES):
        fail(f"{path}: case {case_id} result return_to is not a known stage or ddd")
    if result["handoff"] != "none":
        validate_orchestrator_request(path, result["handoff"], case_id)
    if result["stop"] != "none" and not isinstance(result["stop"], (str, dict)):
        fail(f"{path}: case {case_id} result stop must be none, a string, or an object")
    extensions = result.get("extensions", {})
    if not isinstance(extensions, dict):
        fail(f"{path}: case {case_id} result extensions must be an object")
    unknown = set(extensions) - {"ddd-implementation-gate-v1"}
    if unknown:
        fail(f"{path}: case {case_id} result has unknown extensions: {sorted(unknown)}")
    validate_implementation_gate(path, extensions.get("ddd-implementation-gate-v1"), case_id)
    if not all(stage in ORCHESTRATOR_STAGES for stage in result["invalidated_stages"]):
        fail(f"{path}: case {case_id} result contains an unknown invalidated stage")


def validate_orchestrator_eval_inputs(skill_root: Path, cases: list[dict]) -> None:
    if skill_root.name != "ddd":
        return
    path = skill_root / "evals" / "evals.json"
    categories = {case.get("category") for case in cases}
    missing_categories = sorted(ORCHESTRATOR_CASE_CATEGORIES - categories)
    if missing_categories:
        fail(f"{path}: missing orchestrator evaluation categories: {', '.join(missing_categories)}")
    order = {stage: index for index, stage in enumerate(("ddd-discover", "ddd-strategic", "ddd-tactical", "ddd-adoption", "ddd-review"))}
    for case in cases:
        category = case.get("category")
        payload = case["input"]
        if not isinstance(category, str) or not category.strip():
            fail(f"{path}: case {case['id']} must name an orchestrator category")
        if payload.get("entry_status") not in {"complete", "incomplete"}:
            fail(f"{path}: case {case['id']} entry_status must be complete or incomplete")
        validate_orchestrator_request(path, payload.get("request"), case["id"], allow_empty=payload["entry_status"] == "incomplete")
        if payload["entry_status"] == "incomplete":
            missing_fields = payload.get("missing_fields")
            if not isinstance(missing_fields, list) or not missing_fields or not all(isinstance(item, str) and item.strip() for item in missing_fields):
                fail(f"{path}: incomplete case {case['id']} must name missing_fields")
        if "result" in payload:
            if payload.get("result_valid", True):
                validate_orchestrator_result(path, payload["result"], case["id"])
                result_echo = ORCHESTRATOR_RESULT_ECHO_FIELDS & payload["result"].keys()
                if result_echo and payload["result"].get("handoff") == "none":
                    if result_echo != ORCHESTRATOR_RESULT_ECHO_FIELDS or any(payload["result"].get(field) != payload["request"].get(field) for field in ORCHESTRATOR_RESULT_ECHO_FIELDS):
                        fail(f"{path}: terminal result echoes must preserve the prior request inventory/objective/scope")
            else:
                malformed = payload.get("malformed_fields")
                if not isinstance(malformed, list) or not malformed or not all(isinstance(item, str) and item.strip() for item in malformed):
                    fail(f"{path}: malformed case {case['id']} must name malformed_fields")
        if category == "normal flow":
            if payload.get("route_sequence") != ["ddd-discover", "ddd-strategic", "ddd-tactical", "ddd-adoption", "ddd-review"] or payload.get("expected_one_at_a_time") is not True:
                fail(f"{path}: normal flow case must specify canonical one-at-a-time routing")
        if category == "direct invocation" and payload.get("direct_entry_validated") is not True:
            fail(f"{path}: direct invocation case must validate focused entry")
        if category == "manual fallback":
            if payload.get("manual_fallback_exact") is not True or payload.get("request") != payload.get("fallback_request"):
                fail(f"{path}: manual fallback case must preserve the request object exactly")
            if payload.get("manual_stage") not in ORCHESTRATOR_STAGES:
                fail(f"{path}: manual fallback case must name an exact stage")
        if category == "normal transition":
            if not isinstance(payload.get("next_request"), dict):
                fail(f"{path}: normal transition case must include next_request")
            validate_orchestrator_request(path, payload["next_request"], case["id"])
            if set(payload.get("preserved_fields", [])) != ORCHESTRATOR_PRESERVED_FIELDS:
                fail(f"{path}: normal transition must preserve every required field")
            assertions = payload.get("preservation_assertions")
            if not isinstance(assertions, dict) or set(assertions) != ORCHESTRATOR_PRESERVED_FIELDS:
                fail(f"{path}: normal transition preservation assertions are incomplete")
            handoff = payload["result"].get("handoff")
            for field in ORCHESTRATOR_PRESERVED_FIELDS:
                if assertions[field] != handoff.get(field) or assertions[field] != payload["next_request"].get(field):
                    fail(f"{path}: normal transition changed preserved field {field}")
            validate_orchestrator_artifacts(path, assertions["artifacts"], case["id"], "preservation_assertions.artifacts")
            prior_by_path = {record["path"]: record for record in payload["request"]["artifacts"]}
            for record in payload["result"]["changed_artifacts"]:
                prior_by_path[record["path"]] = record
            if payload["next_request"]["artifacts"] != list(prior_by_path.values()):
                fail(f"{path}: normal transition must merge changed_artifacts by path into the exact next inventory")
            if "objective" in payload["result"] and (payload["result"].get("objective") != payload["next_request"]["objective"] or payload["result"].get("scope") != payload["next_request"]["scope"]):
                fail(f"{path}: modern result echoes must bind objective and scope to the next request")
            if "artifacts" in payload["result"] and payload["result"].get("artifacts") != payload["next_request"]["artifacts"]:
                fail(f"{path}: modern result artifact echo must bind the exact next inventory")
        if category == "invalidation loop":
            result = payload.get("result", {})
            invalidated = result.get("invalidated_stages", [])
            earliest = payload.get("earliest_invalidated_stage")
            if not invalidated or earliest not in invalidated or earliest != min(invalidated, key=order.get):
                fail(f"{path}: invalidation case must route to the earliest invalidated stage")
            if not isinstance(payload.get("stale_artifacts"), list) or not payload["stale_artifacts"]:
                fail(f"{path}: invalidation case must name stale artifacts")
            if payload.get("next_request", {}).get("stage") != earliest:
                fail(f"{path}: invalidation case next request must target earliest stage")
            original_by_path = {record["path"]: record for record in payload["request"]["artifacts"]}
            for record in payload["next_request"]["artifacts"]:
                original = original_by_path.get(record["path"])
                if original is None or record["lifecycle"] != original["lifecycle"] or record["validation"] != "stale":
                    fail(f"{path}: invalidation case must preserve lifecycle and mark only validation stale")
        if category == "malformed result":
            if payload.get("result_valid") is not False or not isinstance(payload.get("stop"), dict):
                fail(f"{path}: malformed result case must produce a bounded stop")
        if category == "non-fit":
            if payload.get("result", {}).get("status") != "not-fit-conflict" or payload.get("result", {}).get("handoff") != "none":
                fail(f"{path}: non-fit case must stop without a handoff")
        if category == "index ownership":
            if set(payload.get("index_markers", [])) != ORCHESTRATOR_INDEX_MARKERS or payload.get("review_stewardship") is not True or payload.get("preserve_user_prose") is not True:
                fail(f"{path}: index ownership case must cover canonical markers and review stewardship")
        if category == "docs-only":
            requested_paths = payload.get("requested_paths", [])
            if not any(path_value.startswith(("src/", "deploy/", "tests/")) for path_value in requested_paths):
                fail(f"{path}: docs-only case must include an outside-scope path")
            if not isinstance(payload.get("stop"), dict):
                fail(f"{path}: docs-only case must produce a bounded stop")


def validate_orchestrator_contract(skill_root: Path) -> None:
    if skill_root.name != "ddd":
        return
    request_template = skill_root / "assets" / "request-result-template.md"
    index_template = skill_root / "assets" / "ddd-readme-template.md"
    request_text = request_template.read_text(encoding="utf-8")
    index_text = index_template.read_text(encoding="utf-8")
    missing_request = [marker for marker in ORCHESTRATOR_TEMPLATE_MARKERS if marker not in request_text + index_text]
    if missing_request:
        fail(f"{request_template}: orchestrator contract markers missing: {', '.join(missing_request)}")
    if "docs/ddd/README.md" not in index_text:
        fail(f"{index_template}: index template must name docs/ddd/README.md")
    if "ddd-owned:routing-status:start" not in index_text or "ddd-review-owned:latest-review:start" not in index_text:
        fail(f"{index_template}: index ownership markers are incomplete")
    if "ddd-routing-v1" not in request_text:
        fail(f"{request_template}: request/result template must name ddd-routing-v1")
    if "Conditional fragment: only when the increment has an unresolved finding or decision, replace the line above" not in index_text or "No open decisions for the selected increment." not in index_text:
        fail(f"{index_template}: decision-queue table must be marked conditional and omissible when empty")
    if "Conditional fragment: only when the ratification state is declined, add these two lines" not in index_text:
        fail(f"{index_template}: declined-decision lines must be marked conditional on a declined ratification state")
    index_rendered = re.sub(r"<!--.*?-->", "", index_text, flags=re.DOTALL)
    if "| DQ-001 |" in index_rendered or "**Declined decision:**" in index_rendered or "**declined decision persisted record:**" in index_rendered:
        fail(f"{index_template}: decision-queue rows and declined-decision lines must live only inside non-rendering conditional fragments, not the default rendered skeleton")


def validate_tactical_contract(skill_root: Path) -> None:
    template = skill_root / "assets" / "context-model-template.md"
    if skill_root.name != "ddd-tactical" or not template.is_file():
        return
    text = template.read_text(encoding="utf-8")
    for marker in ("Claim and evidence ledger", "Outcome and examples", "Commands, rules, and transitions", "Invariants and current-versus-desired delta", "Conditional fragment"):
        if marker not in text:
            fail(f"{template}: visible lean tactical contract marker missing: {marker}")
    if "Do not emit empty or `not-needed` pattern rows." not in text:
        fail(f"{template}: tactical pattern omission rule is missing")


def validate_phase4_transition_matrix() -> None:
    path = ROOT / "docs" / "evaluations" / "phase-4-transition-matrix.json"
    if not path.is_file():
        return
    payload = json.loads(path.read_text(encoding="utf-8"))
    required_categories = {
        "focused direct invocation", "discover→strategic", "strategic→tactical", "tactical→adoption",
        "adoption→review", "review-ready terminal result", "non-fit stop", "malformed result stop",
        "manual fallback request identity", "review invalidation to earliest affected stage",
    }
    if payload.get("schema_version") != 1 or payload.get("kind") != "phase-4-transition-matrix":
        fail(f"{path}: invalid phase-4 transition matrix identity")
    expected_order = ["ddd-discover", "ddd-strategic", "ddd-tactical", "ddd-adoption", "ddd-review"]
    if payload.get("canonical_stage_order") != expected_order:
        fail(f"{path}: canonical stage order is invalid")
    if set(payload.get("preserved_fields", [])) != ORCHESTRATOR_PRESERVED_FIELDS:
        fail(f"{path}: preserved field contract is incomplete")
    schema = payload.get("artifact_record_schema", {})
    if set(schema.get("required_fields", [])) != ORCHESTRATOR_ARTIFACT_FIELDS:
        fail(f"{path}: artifact record schema fields are incomplete")
    if set(schema.get("lifecycles", [])) != ORCHESTRATOR_LIFECYCLES or set(schema.get("validations", [])) != ORCHESTRATOR_VALIDATIONS or set(schema.get("availabilities", [])) != ORCHESTRATOR_AVAILABILITIES:
        fail(f"{path}: artifact record allowed values do not match the orchestrator contract")
    fixtures = payload.get("fixtures")
    if not isinstance(fixtures, list) or len({fixture.get("category") for fixture in fixtures}) != len(fixtures):
        fail(f"{path}: transition fixtures must have unique categories")
    categories = {fixture.get("category") for fixture in fixtures}
    missing = sorted(required_categories - categories)
    if missing:
        fail(f"{path}: transition matrix missing categories: {', '.join(missing)}")
    order = {stage: index for index, stage in enumerate(expected_order)}
    for fixture in fixtures:
        case_id = fixture.get("id", "phase-4")
        category = fixture.get("category")
        if category == "focused direct invocation":
            validate_orchestrator_request(path, fixture.get("request"), case_id)
            if fixture.get("entry_validated") is not True or fixture["request"]["stage"] != "ddd-tactical":
                fail(f"{path}: {case_id} must prove a validated direct tactical entry")
        elif category in {"discover→strategic", "strategic→tactical", "tactical→adoption", "adoption→review"}:
            validate_orchestrator_request(path, fixture.get("request"), case_id)
            validate_orchestrator_result(path, fixture.get("result"), case_id)
            validate_orchestrator_request(path, fixture.get("next_request"), case_id)
            if fixture["result"]["handoff"] != fixture["next_request"]:
                fail(f"{path}: {case_id} handoff and next request differ")
            if fixture["result"]["stage"] != fixture["request"]["stage"] or fixture["next_request"]["stage"] not in ORCHESTRATOR_STAGES:
                fail(f"{path}: {case_id} stage identity is invalid")
            if set(fixture.get("preserved_fields", [])) != ORCHESTRATOR_PRESERVED_FIELDS:
                fail(f"{path}: {case_id} preserved field list is incomplete")
            assertions = fixture.get("preservation_assertions", {})
            for field in ORCHESTRATOR_PRESERVED_FIELDS - {"artifacts"}:
                if (fixture["result"].get(field) != fixture["result"]["handoff"].get(field)
                        or assertions.get(field) != fixture["result"]["handoff"].get(field)
                        or assertions.get(field) != fixture["next_request"].get(field)):
                    fail(f"{path}: {case_id} failed exact preservation for {field}")
            if assertions.get("artifacts") != fixture["result"]["handoff"].get("artifacts") or assertions.get("artifacts") != fixture["next_request"].get("artifacts"):
                fail(f"{path}: {case_id} failed exact preservation for artifacts")
            if not fixture["result"]["changed_artifacts"] and fixture["request"]["artifacts"] != fixture["result"]["handoff"]["artifacts"]:
                fail(f"{path}: {case_id} changed artifact records despite an empty changed_artifacts result")
            if not fixture["result"]["changed_artifacts"] and fixture["request"]["artifacts"] != fixture["next_request"]["artifacts"]:
                fail(f"{path}: {case_id} did not preserve request artifact records")
            validate_orchestrator_artifacts(path, assertions.get("artifacts"), case_id, "preservation_assertions.artifacts")
        elif category == "review-ready terminal result":
            validate_orchestrator_request(path, fixture.get("request"), case_id)
            validate_orchestrator_result(path, fixture.get("result"), case_id)
            if fixture["result"]["status"] != "ready" or fixture["result"]["handoff"] != "none" or fixture.get("terminal") is not True:
                fail(f"{path}: {case_id} must be a ready terminal result")
        elif category == "non-fit stop":
            validate_orchestrator_request(path, fixture.get("request"), case_id)
            validate_orchestrator_result(path, fixture.get("result"), case_id)
            if fixture["result"]["status"] != "not-fit-conflict" or fixture["result"]["handoff"] != "none":
                fail(f"{path}: {case_id} must stop without a handoff")
        elif category == "malformed result stop":
            validate_orchestrator_request(path, fixture.get("request"), case_id)
            if fixture.get("result_valid") is not False or not fixture.get("malformed_fields"):
                fail(f"{path}: {case_id} must retain malformed fields and reject repair")
        elif category == "manual fallback request identity":
            validate_orchestrator_request(path, fixture.get("request"), case_id)
            serialized = fixture.get("request_serialized")
            returned_serialized = fixture.get("returned_request_serialized")
            if (fixture.get("exact_identity") is not True or fixture.get("request") != fixture.get("returned_request")
                    or not isinstance(serialized, str) or serialized != returned_serialized
                    or hashlib.sha256(serialized.encode("utf-8")).hexdigest() != fixture.get("serialization_sha256")
                    or fixture.get("manual_stage") not in ORCHESTRATOR_STAGES):
                fail(f"{path}: {case_id} must preserve the manual request byte representation exactly")
        elif category == "review invalidation to earliest affected stage":
            validate_orchestrator_request(path, fixture.get("request"), case_id)
            validate_orchestrator_result(path, fixture.get("result"), case_id)
            validate_orchestrator_request(path, fixture.get("next_request"), case_id)
            invalidated = fixture["result"]["invalidated_stages"]
            earliest = fixture.get("earliest_invalidated_stage")
            if not invalidated or earliest != min(invalidated, key=order.get) or fixture["next_request"]["stage"] != earliest:
                fail(f"{path}: {case_id} does not route to the earliest invalidated stage")
            original = {record["path"]: record for record in fixture["request"]["artifacts"]}
            for record in fixture["next_request"]["artifacts"]:
                if record["path"] not in original or record["lifecycle"] != original[record["path"]]["lifecycle"] or record["validation"] != "stale":
                    fail(f"{path}: {case_id} does not preserve lifecycle while marking validation stale")


def markdown_h1_count(text: str) -> int:
    in_fence = False
    count = 0
    for line in text.splitlines():
        if line.strip().startswith(("```", "~~~")):
            in_fence = not in_fence
        elif not in_fence and re.match(r"^#\s+", line):
            count += 1
    return count


def validate_repository_markdown() -> None:
    candidates = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md")), *sorted((ROOT / "skills").rglob("*.md"))]
    for path in candidates:
        if markdown_h1_count(path.read_text(encoding="utf-8")) != 1:
            fail(f"{path}: expected exactly one H1 outside code fences")
        for raw in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", path.read_text(encoding="utf-8")):
            if raw.startswith(("http://", "https://", "mailto:")) or "<" in raw or "{" in raw:
                continue
            target = (path.parent / raw).resolve()
            if not target.exists():
                fail(f"{path}: broken repository link: {raw}")


def validate_lean_eval_suite() -> None:
    seen: set[str] = set()
    for path in sorted(SKILLS_ROOT.glob("*/evals/evals.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for case in payload.get("cases", []):
            seen.add(case["id"])
    missing = sorted(LEAN_CASE_IDS - seen)
    if missing:
        fail(f"lean redesign evals missing required cases: {', '.join(missing)}")
    if len(seen) < 15:
        fail("lean redesign evals must retain at least 15 required cases")


def validate_lean_case_semantics() -> None:
    cases = {}
    for path in sorted(SKILLS_ROOT.glob("*/evals/evals.json")):
        for case in json.loads(path.read_text(encoding="utf-8")).get("cases", []):
            cases[case["id"]] = case
    def require(case_id: str) -> dict:
        if case_id not in cases:
            fail(f"lean case missing during semantic validation: {case_id}")
        return cases[case_id]["input"]
    ratification_case = require("ratification-one-handoff")
    gate = ratification_case.get("request", {}).get("extensions", {}).get("ddd-implementation-gate-v1")
    if not isinstance(gate, dict) or gate.get("version") != "ddd-implementation-gate-v1" or gate.get("increment_gate") != "authorized" or gate.get("ratification", {}).get("state") != "authorized":
        fail("ratification-one-handoff must carry an authorized implementation-gate envelope")
    for authority in gate.get("authoritative_revisions", []):
        validate_authority_revision(ROOT / "skills/ddd/evals/evals.json", authority.get("revision"), "ratification-one-handoff", "authority revision")
        if not authority.get("sections"):
            fail("ratification-one-handoff authority must list exact headings")
    if ratification_case.get("pre_ratification") != {"documentation_readiness": "ready", "increment_gate": "awaiting-ratification"}:
        fail("ratification-one-handoff pre_ratification must show ready documentation still awaiting explicit ratification")
    human_decision = ratification_case.get("human_decision")
    if not isinstance(human_decision, dict) or human_decision.get("decision") != "authorized" or not isinstance(human_decision.get("owner"), str) or not human_decision["owner"].strip() or not human_decision.get("accepted_revisions"):
        fail("ratification-one-handoff human_decision must record an authorized decision with a named owner and accepted revisions")
    record = gate["ratification"]["record"]
    if record["decision"] != human_decision["decision"] or record["owner"] != human_decision["owner"] or record["date"] != human_decision["date"]:
        fail("ratification-one-handoff post-decision request must reflect the exact same human decision, owner, and date")
    if sorted(human_decision["accepted_revisions"], key=lambda item: item["path"]) != sorted(record["accepted_revisions"], key=lambda item: item["path"]):
        fail("ratification-one-handoff human_decision accepted_revisions must exactly match the post-decision request's accepted revisions, including sections and role")
    negative_input = require("gate-negative-combinations")
    negative = negative_input.get("invalid_gate_cases", [])
    if set(negative) != {"blocked-with-authorized", "awaiting-with-blocked-readiness", "empty-acceptance", "empty-authority", "unresolved-decision", "pending-blocked", "blocking-authorized", "empty-in-scope", "duplicate-disposition-id", "deferred-wrong-status", "orphan-deferred-question", "orphan-accepted-assumption", "unbound-accepted-assumption-disposition"}:
        fail("gate-negative-combinations must cover every invalid authorization combination")
    import copy
    declined = negative_input.get("declined_case")
    if not isinstance(declined, dict) or declined.get("increment_gate") != "blocked" or declined.get("ratification", {}).get("state") != "declined":
        fail("gate-negative-combinations must include a blocked declined decision case")
    validate_implementation_gate(ROOT / "skills/ddd/evals/evals.json", declined, "gate-negative-combinations-declined")
    persisted_decline = negative_input.get("declined_persisted_authorization")
    declined_record = declined.get("ratification", {}).get("record", {})
    if not isinstance(persisted_decline, dict) or set(persisted_decline) != {"path", "marker", "decision", "owner", "date", "increment_id", "target_repository", "target_runtime", "baseline_revision", "reason"} or persisted_decline.get("path") != "docs/ddd/README.md" or persisted_decline.get("marker") != "ddd-owned:authorization" or any(persisted_decline.get(field) != declined_record.get(field) for field in ("decision", "owner", "date", "increment_id", "target_repository", "target_runtime", "baseline_revision", "reason")):
        fail("gate-negative-combinations must persist the exact declined decision in the owned README authorization marker")
    declined_missing_record = copy.deepcopy(declined)
    declined_missing_record["ratification"].pop("record", None)
    try:
        validate_implementation_gate(ROOT / "skills/ddd/evals/evals.json", declined_missing_record, "gate-negative-combinations-declined-mutation")
    except ValidationError:
        pass
    else:
        fail("gate-negative-combinations declined mutation unexpectedly passed")
    for name in negative:
        candidate = copy.deepcopy(gate)
        if name == "blocked-with-authorized": candidate["increment_gate"] = "blocked"
        elif name == "awaiting-with-blocked-readiness": candidate["documentation_readiness"] = "blocked"
        elif name == "empty-acceptance":
            candidate["acceptance_signals"] = []
            candidate["ratification"]["record"]["acceptance_signals"] = []
        elif name == "empty-authority":
            candidate["authoritative_revisions"] = []
            candidate["ratification"]["record"]["accepted_revisions"] = []
        elif name == "unresolved-decision":
            mutant = {"id": "Q-decision", "disposition": "decision-required", "status": "open", "issue": "unresolved decision", "impact": "blocks ratification", "owner": "owner", "action": "action", "affected_artifacts": [], "revisit_trigger": "trigger"}
            candidate["question_dispositions"] = [mutant]
            candidate["ratification"]["record"]["question_dispositions"] = list(candidate["question_dispositions"])
        elif name == "pending-blocked": candidate["increment_gate"] = "blocked"; candidate["ratification"] = {"state":"pending"}
        elif name == "blocking-authorized":
            mutant = {"id": "Q-blocking", "disposition": "blocking", "status": "open", "issue": "blocking finding", "impact": "blocks the gate", "owner": "owner", "action": "action", "affected_artifacts": [], "revisit_trigger": "trigger"}
            candidate["question_dispositions"] = [mutant]
            candidate["ratification"]["record"]["question_dispositions"] = list(candidate["question_dispositions"])
        elif name == "empty-in-scope":
            candidate["in_scope"] = []
            candidate["ratification"]["record"]["in_scope"] = []
        elif name == "duplicate-disposition-id":
            candidate["question_dispositions"] = candidate["question_dispositions"] * 2
            candidate["ratification"]["record"]["question_dispositions"] = list(candidate["question_dispositions"])
        elif name == "deferred-wrong-status":
            mutant_disposition = {"id": "Q-mutant", "disposition": "deferred", "status": "resolved", "issue": "mutant deferred issue", "impact": "n/a", "owner": "owner", "action": "action", "affected_artifacts": [], "revisit_trigger": "trigger"}
            candidate["question_dispositions"] = candidate["question_dispositions"] + [mutant_disposition]
            candidate["deferred_questions"] = candidate["deferred_questions"] + ["mutant deferred issue"]
            candidate["ratification"]["record"]["question_dispositions"] = list(candidate["question_dispositions"])
            candidate["ratification"]["record"]["deferred_questions"] = list(candidate["deferred_questions"])
        elif name == "orphan-deferred-question":
            candidate["deferred_questions"] = candidate["deferred_questions"] + ["unbound issue text"]
            candidate["ratification"]["record"]["deferred_questions"] = list(candidate["deferred_questions"])
        elif name == "orphan-accepted-assumption":
            candidate["accepted_assumptions"] = candidate["accepted_assumptions"] + ["unbound assumption text"]
            candidate["ratification"]["record"]["accepted_assumptions"] = list(candidate["accepted_assumptions"])
        elif name == "unbound-accepted-assumption-disposition":
            mutant_disposition = {"id": "Q-assumption", "disposition": "accepted-assumption", "status": "resolved", "issue": "assumed but unlisted", "impact": "n/a", "owner": "owner", "action": "action", "affected_artifacts": [], "revisit_trigger": "trigger"}
            candidate["question_dispositions"] = candidate["question_dispositions"] + [mutant_disposition]
            candidate["ratification"]["record"]["question_dispositions"] = list(candidate["question_dispositions"])
        try:
            validate_implementation_gate(ROOT / "skills/ddd/evals/evals.json", candidate, "gate-negative-combinations")
        except ValidationError:
            continue
        fail(f"gate-negative-combinations mutation {name} unexpectedly passed")
    def _mutate_scalar_in_scope(candidate):
        candidate.update({"in_scope": "one behavior"})
        candidate["ratification"]["record"].update({"in_scope": "one behavior"})
    def _mutate_invalid_return_target(candidate):
        candidate.update({"return_on_conflict": "ship-now"})
        candidate["ratification"]["record"].update({"return_on_conflict": "ship-now"})
    def _mutate_authority_traversal(candidate):
        candidate["authoritative_revisions"][0].update({"path": "docs/ddd/../src/app.py"})
        candidate["ratification"]["record"]["accepted_revisions"][0].update({"path": "docs/ddd/../src/app.py"})
    def _mutate_authority_section_unaccepted(candidate):
        candidate["authoritative_revisions"][0]["sections"] = ["Some other H2"]
    def _mutate_authority_role_unaccepted(candidate):
        candidate["authoritative_revisions"][0]["role"] = "release-approval"
    strict_mutations = {
        "unknown-gate-key": lambda candidate: candidate.update({"authorized_for_deployment": True}),
        "scalar-in-scope": _mutate_scalar_in_scope,
        "invalid-return-target": _mutate_invalid_return_target,
        "authority-traversal": _mutate_authority_traversal,
        "authority-section-unaccepted": _mutate_authority_section_unaccepted,
        "authority-role-unaccepted": _mutate_authority_role_unaccepted,
        "pending-record": lambda candidate: candidate.update({"increment_gate": "awaiting-ratification", "ratification": {"state": "pending", "record": {}}}),
        "unknown-ratification-key": lambda candidate: candidate["ratification"]["record"].update({"release_approved": True}),
    }
    if set(negative_input.get("strict_schema_mutations", [])) != set(strict_mutations):
        fail("gate-negative-combinations must name all strict authorization/schema mutation probes")
    for name, mutate in strict_mutations.items():
        candidate = copy.deepcopy(gate)
        mutate(candidate)
        try:
            validate_implementation_gate(ROOT / "skills/ddd/evals/evals.json", candidate, "gate-strict-schema")
        except ValidationError:
            continue
        fail(f"gate-strict-schema mutation {name} unexpectedly passed")
    stale = require("stale-handoff-invalidation")
    if stale.get("authority_revision") == stale.get("current_revision"):
        fail("stale-handoff-invalidation must prove a revision mismatch")
    state_records = require("lean-state-transport").get("request", {}).get("artifacts", [])
    if {record.get("state") for record in state_records} != {"working", "decision-needed", "current", "stale", "superseded"}:
        fail("lean-state-transport must cover every lean state")
    if not any(record.get("state") == "stale" and record.get("lifecycle") == "draft" for record in state_records):
        fail("lean-state-transport must cover working/decision-needed invalidation preserving draft lifecycle")
    if not {"target", "baseline", "owner", "acceptance", "containment"}.issubset(set(require("handoff-preconditions").get("missing", []))):
        fail("handoff-preconditions must cover target, baseline, owner, acceptance, and containment")
    if require("one-context-slice").get("selected_context") != "storytelling-experience":
        fail("one-context-slice must name exactly one selected context")
    conditional = require("conditional-artifacts")
    if conditional.get("trigger") != "vision and language" or require("conditional-strategic-artifacts").get("conditional_triggers") != ["context-map", "ubiquitous-language"]:
        fail("conditional-artifacts must record explicit triggers")
    if require("omit-optional-patterns").get("pattern_triggers") != []:
        fail("omit-optional-patterns must have no optional pattern trigger")
    if require("review-exception-summary").get("finding") != "acceptance signal missing":
        fail("review-exception-summary must retain its material exception")
    dual = require("documentation-ready-gate-blocked")
    if dual.get("documentation_readiness") != "ready" or dual.get("increment_gate") != "blocked":
        fail("documentation-ready-gate-blocked must preserve the dual readiness distinction")
    queue = require("consolidated-decision-queue")
    if not queue.get("findings") or not queue.get("owners"):
        fail("consolidated-decision-queue must retain findings and earliest owners")
    deferred = require("deferred-out-of-scope")
    if not deferred.get("owner") or not deferred.get("revisit_trigger"):
        fail("deferred-out-of-scope must name an owner and revisit trigger")
    blocked = require("blocking-not-reclassified")
    if blocked.get("human_confirmation") is not False:
        fail("blocking-not-reclassified must cover absent human confirmation")
    if not require("coding-agent-reading-order").get("authority_set"):
        fail("coding-agent-reading-order must name the exact authority set")
    legacy_inputs = []
    for path in sorted(SKILLS_ROOT.glob("*/evals/evals.json")):
        legacy_inputs.extend(case["input"] for case in json.loads(path.read_text(encoding="utf-8")).get("cases", []) if case["id"] == "legacy-preserved")
    if not any(item.get("legacy_metadata") or item.get("legacy_fields") for item in legacy_inputs):
        fail("legacy-preserved must exercise legacy metadata")
    if not any(path.startswith("src/") for path in require("docs-only-boundary").get("requested_paths", [])):
        fail("docs-only-boundary must include an outside product path")


def validate_lean_contracts() -> None:
    shared = (ROOT / "docs/skill-design/artifact-contracts.md").read_text(encoding="utf-8")
    for marker in ("Lean metadata contract", "Default and conditional artifact profile", "Decision queue", "documentation_readiness", "increment_gate", "Coding-agent consumption"):
        if marker not in shared:
            fail(f"shared lean contract marker missing: {marker}")
    if "increment_gate: blocked | awaiting-ratification | authorized" in shared:
        fail("shared review contract must not claim authorized as a review output")
    ddd_text = "\n".join(path.read_text(encoding="utf-8") for path in (SKILLS_ROOT / "ddd").glob("**/*.md"))
    for marker in ("ddd-routing-v1", "ddd-implementation-gate-v1", "extensions.ddd-implementation-gate-v1", "authority-revision-v1", "awaiting-ratification", "implementation-handoff-v1"):
        if marker not in ddd_text:
            fail(f"ddd extension contract marker missing: {marker}")
    handoff = (SKILLS_ROOT / "ddd/assets/implementation-handoff-template.md").read_text(encoding="utf-8")
    request_result = (SKILLS_ROOT / "ddd/assets/request-result-template.md").read_text(encoding="utf-8")
    if "when any modern result echo is present, all three are required and must equal the next request" in request_result:
        fail("result schema must distinguish terminal prior-request echoes from nonterminal next-request echoes")
    for marker in ("version: implementation-handoff-v1", "decision: authorized", "authoritative_artifacts", "exact revision", "return_on_conflict"):
        if marker not in handoff:
            fail(f"handoff marker missing: {marker}")
    if "acceptance_signals: []" in handoff or "containment: []" in handoff or "containment_limitations: []" in handoff:
        fail("handoff template must show nonempty required acceptance and containment fields")
    review = (SKILLS_ROOT / "ddd-review/assets/review-template.md").read_text(encoding="utf-8")
    for marker in ("documentation_readiness", "increment_gate", "decision queue", "passed gates"):
        if marker not in review:
            fail(f"review lean marker missing: {marker}")
    if "## Boundary" in review or "| _DQ-001_ |" in review:
        fail("review template must omit unconditional boundary/finding filler")
    adoption_template = (SKILLS_ROOT / "ddd-adoption/assets/adoption-plan-template.md").read_text(encoding="utf-8")
    context_template = (SKILLS_ROOT / "ddd-strategic/assets/context-template.md").read_text(encoding="utf-8")
    if "Conditional fragment" not in adoption_template or "emit the following section only when" not in adoption_template or "Transport gate boundary" in adoption_template or "ddd-implementation-gate-v1" in adoption_template:
        fail("adoption template must make risk/queue sections conditional and omit transport protocol teaching")
    if "emit `## Touched relationships` only when" not in context_template or "Blocking boundary decisions" not in context_template:
        fail("context template must make relationships and blocking decisions conditional")
    if "This context file is created only when selected" in context_template:
        fail("context template must omit generic output-only protocol guidance")
    for name in ("ddd-discover", "ddd-strategic", "ddd-tactical", "ddd-adoption", "ddd-review"):
        for path in (SKILLS_ROOT / name / "assets").glob("*.md"):
            text = path.read_text(encoding="utf-8")
            before_h2 = text.split("\n## ", 1)[0]
            if re.search(r"^\|\s*`?owner`?\s*\|", before_h2, flags=re.MULTILINE):
                fail(f"{path}: default metadata must omit conditional owner")


def validate_sanitized_fixture() -> None:
    fixture_path = ROOT / "docs/evaluations/bonvoye-shaped-lean-fixture.json"
    report_path = ROOT / "docs/evaluations/lean-workflow-redesign-v1-report.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    report = json.loads(report_path.read_text(encoding="utf-8"))
    expected_ids = ["entitled-in-range-online-start", "entitlement-rejection", "readiness-rejection", "duplicate-start", "explicit-completion", "duplicate-completion", "executable-proximity-profiles"]
    if fixture.get("external_access") is not False or fixture.get("selected_context") != "storytelling-experience" or fixture.get("increment_id") != "storytelling-characterization-v1":
        fail(f"{fixture_path}: fixture identity or external-access flag is invalid")
    cases = fixture.get("cases")
    if [case.get("id") for case in cases or []] != expected_ids:
        fail(f"{fixture_path}: characterization case order does not match the agreed seven cases")
    proximity = cases[-1]
    if proximity.get("profiles") != ["in-range-online", "out-of-range-online"]:
        fail(f"{fixture_path}: both executable proximity profiles are required")
    if report.get("fixture_path") != "docs/evaluations/bonvoye-shaped-lean-fixture.json" or report.get("external_access") is not False:
        fail(f"{report_path}: report must be generated from the local fixture without external access")
    report_fixture = report.get("bonvoye_shaped_fixture", {})
    if report_fixture.get("characterization_cases") != expected_ids or report_fixture.get("executable_proximity_profiles") != proximity["profiles"]:
        fail(f"{report_path}: report does not name the agreed characterization cases/profiles")
    runs = {run.get("id"): run for run in report.get("runs", [])}
    if set(runs) != set(expected_ids):
        fail(f"{report_path}: report must contain one observed output per fixture case")
    for case in cases:
        if runs[case["id"]].get("status") != "pass" or runs[case["id"]].get("observed_output") != case["expected_output"]:
            fail(f"{report_path}: observed output does not match fixture expectation for {case['id']}")
    if report_fixture.get("pre_authorization_artifacts") != ["docs/ddd/README.md", "docs/ddd/contexts/storytelling-experience.md", "docs/ddd/models/storytelling-experience.md", "docs/ddd/adoption-plan.md", "docs/ddd/review.md"]:
        fail(f"{report_path}: default artifact profile is incorrect")
    if report_fixture.get("post_authorization_artifacts", [])[-1:] != ["docs/ddd/implementation-handoff.md"]:
        fail(f"{report_path}: handoff must be the sole post-authorization addition")
    ddd_cases = json.loads((SKILLS_ROOT / "ddd/evals/evals.json").read_text(encoding="utf-8"))["cases"]
    declined_case = next((case for case in ddd_cases if case["id"] == "gate-negative-combinations"), {})
    declined_gate = declined_case.get("input", {}).get("declined_case", {})
    declined_record = declined_gate.get("ratification", {}).get("record", {})
    declined_persisted = declined_case.get("input", {}).get("declined_persisted_authorization", {})
    expected_checks = {
        "fixture_inputs_present": len(cases) == 7 and set(runs) == set(expected_ids),
        "seven_characterization_cases": len(cases) == 7,
        "both_executable_proximity_profiles": proximity.get("profiles") == ["in-range-online", "out-of-range-online"],
        "observed_outputs_match_expected": all(runs[case["id"]].get("observed_output") == case["expected_output"] for case in cases),
        "materialized_artifacts": all((ROOT / path).is_file() for path in fixture.get("materialized_post_authorization", [])),
        "authority_revisions_real": all("sha256:" + hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == item.get("revision") for path, item in ((item["path"], item) for item in report_fixture.get("authority_revisions", []))),
        "queue_and_gate_materialized": all((ROOT / path).is_file() for path in fixture.get("materialized_pre_authorization", [])),
        "handoff_materialized": (ROOT / fixture.get("materialized_post_authorization", [])[-1]).is_file() if fixture.get("materialized_post_authorization") else False,
        "index_present": "docs/ddd/README.md" in report_fixture.get("pre_authorization_artifacts", []),
        "one_selected_context": report_fixture.get("selected_context") == "storytelling-experience",
        "unrelated_contexts_omitted": len([path for path in report_fixture.get("pre_authorization_artifacts", []) if path.startswith("docs/ddd/contexts/")]) == 1,
        "one_candidate_increment": bool(report_fixture.get("increment_id")),
        "exception_queue": "docs/ddd/review.md" in report_fixture.get("pre_authorization_artifacts", []),
        "dual_readiness": report_fixture.get("gate_before_authorization", {}).get("documentation_readiness") == "ready" and report_fixture.get("gate_before_authorization", {}).get("increment_gate") == "awaiting-ratification" and report_fixture.get("gate_before_authorization", {}).get("implementation_handoff") is False,
        "no_handoff_before_authorization": "docs/ddd/implementation-handoff.md" not in report_fixture.get("pre_authorization_artifacts", []),
        "one_handoff_after_authorization": report_fixture.get("post_authorization_artifacts", []).count("docs/ddd/implementation-handoff.md") == 1,
        "post_index_authorized": report_fixture.get("gate_after_authorization", {}).get("increment_gate") == "authorized" and report_fixture.get("gate_after_authorization", {}).get("implementation_handoff") is True,
        "handoff_structured": (ROOT / fixture.get("materialized_post_authorization", [])[-1]).read_text(encoding="utf-8").count("implementation-handoff-v1") == 1 if fixture.get("materialized_post_authorization") else False,
        "review_owned_state_preserved": (ROOT / fixture["materialized_pre_authorization"][-1]).read_bytes() == (ROOT / fixture["materialized_post_authorization"][-2]).read_bytes(),
        "logical_handoff_paths": True,
        "examples_materialized": True,
        "pre_review_contract_complete": True,
        "gate_envelope_bound": fixture.get("gate_before_envelope", {}).get("ratification", {}).get("state") == "pending" and fixture.get("gate_after_envelope", {}).get("ratification", {}).get("state") == "authorized",
        "no_trigger_sections_absent": True,
        "provenance_citations": True,
        "declined_decision_recorded": declined_gate.get("increment_gate") == "blocked" and declined_gate.get("ratification", {}).get("state") == "declined" and declined_record.get("decision") == "declined" and bool(declined_record.get("reason")) and declined_persisted.get("path") == "docs/ddd/README.md" and declined_persisted.get("marker") == "ddd-owned:authorization" and all(declined_persisted.get(field) == declined_record.get(field) for field in ("decision", "owner", "date", "increment_id", "target_repository", "target_runtime", "baseline_revision", "reason")),
        "documentation_only": not any(path.startswith(("src/", "tests/", "deploy/")) for path in report_fixture.get("pre_authorization_artifacts", []) + report_fixture.get("post_authorization_artifacts", [])),
        "no_external_project_access": report.get("external_access") is False and fixture.get("external_access") is False,
    }
    if report.get("checks") != expected_checks or not all(expected_checks.values()):
        fail(f"{report_path}: report checks do not match deterministic fixture assertions")


def validate_materialized_fixture() -> None:
    fixture_path = ROOT / "docs/evaluations/bonvoye-shaped-lean-fixture.json"
    report_path = ROOT / "docs/evaluations/lean-workflow-redesign-v1-report.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report_fixture = report["bonvoye_shaped_fixture"]
    pre = fixture["materialized_pre_authorization"]
    post = fixture["materialized_post_authorization"]
    if not all((ROOT / path).is_file() for path in pre + post):
        fail(f"{fixture_path}: materialized pre/post artifact set is incomplete")
    expected_post_prefix = [path.replace("/pre/", "/post/") for path in pre]
    if post[:-1] != expected_post_prefix or not post[-1].endswith("implementation-handoff.md"):
        fail(f"{fixture_path}: post-authorization profile must materialize the same five authorities plus one handoff")
    authorities = {item["path"]: item for item in report_fixture["authority_revisions"]}
    if set(authorities) != set(fixture["authority_sections"]):
        fail(f"{report_path}: authority set does not match materialized fixture authorities")
    for path, sections in fixture["authority_sections"].items():
        materialized = ROOT / path
        digest = "sha256:" + hashlib.sha256(materialized.read_bytes()).hexdigest()
        authority = authorities[path]
        if authority["revision"] != digest or authority["sections"] != sections:
            fail(f"{report_path}: authority revision/sections do not match {path}")
        headings = set(re.findall(r"^##\s+(.+)$", materialized.read_text(encoding="utf-8"), flags=re.MULTILINE))
        if not set(sections).issubset(headings):
            fail(f"{materialized}: authority section list contains a missing H2")
    pre_index = (ROOT / pre[0]).read_text(encoding="utf-8")
    post_index = (ROOT / post[0]).read_text(encoding="utf-8")
    pre_review = (ROOT / pre[-1]).read_text(encoding="utf-8")
    post_review = (ROOT / post[-2]).read_text(encoding="utf-8")
    adoption_path = next(path for path in authorities if path.endswith("/adoption-plan.md"))
    adoption = (ROOT / adoption_path).read_text(encoding="utf-8")
    handoff_path = post[-1]
    handoff = (ROOT / handoff_path).read_text(encoding="utf-8")
    if "documentation_readiness: ready" not in pre_index or "increment_gate: awaiting-ratification" not in pre_index or "Decision queue" not in pre_index or "not authorized" not in pre_index:
        fail(f"{ROOT / pre[0]}: pre-authorization index lacks queue/readiness gate")
    if "documentation_readiness: ready" not in post_index or "increment_gate: authorized" not in post_index or "implementation-handoff.md" not in post_index or "not authorized" in post_index:
        fail(f"{ROOT / post[0]}: post-authorization index is not authorized and linked")
    expected_post_index = pre_index.replace("**What's happening:** Documentation is ready; review is waiting for a human to ratify or decline this increment.", "**What's happening:** This increment is authorized; the implementation handoff is ready to start a coding-agent run.", 1).replace("**Next action:** Ratify this increment or decline it.", "**Next action:** Start a coding-agent run from `docs/ddd/implementation-handoff.md` and create a repository-specific technical plan before editing.", 1).replace("- **Current stage:** ddd-review.", "- **Current stage:** ddd (authorized handoff).", 1).replace("increment_gate: awaiting-ratification", "increment_gate: authorized", 1).replace("- **Exact next human action:** ratify this increment or decline it.", "- **Exact next human action:** start a coding-agent run from `docs/ddd/implementation-handoff.md` and create a repository-specific technical plan before editing.", 1).replace("| `docs/ddd/review.md` | ddd-review | current | readiness evidence |\n", "| `docs/ddd/review.md` | ddd-review | current | readiness evidence |\n| `docs/ddd/implementation-handoff.md` | ddd | current | authorized entry point |\n", 1).replace("- **Ratification:** pending for one increment.\n- **Implementation handoff:** `not authorized`.", "- **Ratification:** authorized for one increment.\n- **Implementation handoff:** `docs/ddd/implementation-handoff.md`.", 1)
    if post_index != expected_post_index:
        fail(f"{ROOT / post[0]}: authorization changed README content beyond the expected gate/ratification/handoff transition")
    if pre_review != post_review:
        fail(f"{ROOT / pre[-1]}: review-owned review.md must remain byte-identical through authorization")
    if "documentation_readiness: ready" not in pre_review or "increment_gate: awaiting-ratification" not in pre_review or "Decision queue" not in pre_review or "Owner:" not in pre_review or "Revisit trigger:" not in pre_review:
        fail(f"{ROOT / pre[-1]}: pre-authorization review lacks queue/readiness fields")
    if "passed gates:" not in pre_review or "provenance (local sanitized fixture cited" not in pre_review or "acceptance signals:" not in pre_review or "containment:" not in pre_review or "business-decision owner:" not in pre_review:
        fail(f"{ROOT / pre[-1]}: pre-authorization review lacks contract-complete gate/provenance summary")
    fixture_owner = fixture["gate_before_envelope"]["owner"]
    if f"accountable implementation owner: {fixture_owner}" not in adoption or f"accountable implementation owner: {fixture_owner}" not in pre_review:
        fail(f"{ROOT / adoption_path}: adoption and review must both name the identical accountable implementation owner: {fixture_owner}")
    for field, prefix in (("outcome", "- outcome: "), ("return_on_conflict", "- return on conflict: ")):
        if prefix + str(fixture["gate_before_envelope"][field]) not in pre_review:
            fail(f"{ROOT / pre[-1]}: pre-review {field} is not the pending gate value")
    if "- in scope: " + "; ".join(fixture["gate_before_envelope"]["in_scope"]) not in pre_review or "- out of scope: " + " and ".join(fixture["gate_before_envelope"]["out_of_scope"]) not in pre_review:
        fail(f"{ROOT / pre[-1]}: pre-review scope contract is not exact")
    for authority in report_fixture["authority_revisions"]:
        if f"`{authority['target_path']}`" not in pre_review or authority["revision"] not in pre_review:
            fail(f"{ROOT / pre[-1]}: pre-review authority set is not exact for {authority['target_path']}")
    context_pre = (ROOT / next(path for path in pre if path.endswith("/contexts/storytelling-experience.md"))).read_text(encoding="utf-8")
    adoption_pre = (ROOT / next(path for path in pre if path.endswith("/adoption-plan.md"))).read_text(encoding="utf-8")
    if "business-decision owner:" not in context_pre or "stop condition:" not in adoption_pre:
        fail(f"{ROOT / pre[-1]}: pre-authorized context/adoption contracts lack owner or stop condition")
    queue_pattern = r"<!-- ddd-review-owned:decision-queue:start -->(.*?)<!-- ddd-review-owned:decision-queue:end -->"
    pre_queue = re.search(queue_pattern, pre_index, flags=re.DOTALL)
    post_queue = re.search(queue_pattern, post_index, flags=re.DOTALL)
    if not pre_queue or not post_queue or pre_queue.group(1) != post_queue.group(1):
        fail(f"{ROOT / pre[0]}: review-owned decision queue body was rewritten during authorization")
    latest_pattern = r"<!-- ddd-review-owned:latest-review:start -->(.*?)<!-- ddd-review-owned:latest-review:end -->"
    pre_latest = re.search(latest_pattern, pre_index, flags=re.DOTALL)
    post_latest = re.search(latest_pattern, post_index, flags=re.DOTALL)
    if not pre_latest or not post_latest or pre_latest.group(1) != post_latest.group(1):
        fail(f"{ROOT / pre[0]}: review-owned latest-review body was rewritten during authorization")
    if "increment_gate: awaiting-ratification" not in post_review:
        fail(f"{ROOT / post[-2]}: review result must remain awaiting-ratification while ddd transport gate authorizes")
    context_path = next(path for path in authorities if path.endswith("/contexts/storytelling-experience.md"))
    context_text = (ROOT / context_path).read_text(encoding="utf-8")
    model_path = next(path for path in authorities if path.endswith("/models/storytelling-experience.md"))
    model_text = (ROOT / model_path).read_text(encoding="utf-8")
    adoption_pre = (ROOT / next(path for path in pre if path.endswith("/adoption-plan.md"))).read_text(encoding="utf-8")
    context_pre = (ROOT / next(path for path in pre if path.endswith("/contexts/storytelling-experience.md"))).read_text(encoding="utf-8")
    model_pre = (ROOT / next(path for path in pre if path.endswith("/models/storytelling-experience.md"))).read_text(encoding="utf-8")
    if any(marker in text for text in (adoption, adoption_pre) for marker in ("## Material risk and containment", "No product or external data risk")) or any(marker in text for text in (context_text, context_pre) for marker in ("## Touched relationships", "No unrelated relationship")):
        fail(f"{fixture_path}: no-trigger conditional sections must be absent from materialized authorities")
    if any("Evidence: local sanitized BonVoye-shaped fixture" not in text for text in (context_text, context_pre, model_text, model_pre)):
        fail(f"{fixture_path}: provenance-pass authorities must cite the local fixture")
    if "increment_id: storytelling-characterization-v1" not in adoption or "Increment identity and outcome" not in adoption:
        fail(f"{ROOT / adoption_path}: materialized adoption increment is incomplete")
    match = re.search(r"```json\s*(\{.*?\})\s*```", handoff, flags=re.DOTALL)
    if not match:
        fail(f"{ROOT / handoff_path}: materialized handoff lacks a structured JSON payload")
    handoff_payload = json.loads(match.group(1))
    required_handoff = {"version", "authorization", "implementation_owner", "increment", "target", "authoritative_artifacts", "in_scope", "out_of_scope", "accepted_assumptions", "deferred_questions", "out_of_scope_questions", "question_dispositions", "acceptance_signals", "containment", "return_on_conflict", "characterization_cases"}
    if set(handoff_payload) != required_handoff or handoff_payload["version"] != "implementation-handoff-v1":
        fail(f"{ROOT / handoff_path}: structured handoff fields are incomplete")
    auth = handoff_payload["authorization"]
    if not isinstance(auth, dict) or set(auth) != {"decision", "owner", "date"}:
        fail(f"{ROOT / handoff_path}: authorization must contain exactly decision, owner, and date, with no second copy of the ratified target/scope/evidence")
    if auth.get("decision") != "authorized" or not isinstance(auth.get("owner"), str) or not auth["owner"].strip() or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(auth.get("date"))):
        fail(f"{ROOT / handoff_path}: authorization decision/owner/date is invalid")
    if not isinstance(handoff_payload.get("increment"), dict) or set(handoff_payload["increment"]) != {"id", "outcome"}:
        fail(f"{ROOT / handoff_path}: increment must contain exactly id and outcome")
    for artifact in handoff_payload.get("authoritative_artifacts", []):
        if not isinstance(artifact, dict) or set(artifact) != IMPLEMENTATION_GATE_AUTHORITY_KEYS:
            fail(f"{ROOT / handoff_path}: authoritative_artifacts entries must contain exactly path, sections, revision, and role")
    if not isinstance(handoff_payload.get("implementation_owner"), str) or not handoff_payload["implementation_owner"].strip():
        fail(f"{ROOT / handoff_path}: implementation_owner must be a named accountable implementation owner")
    handoff_target = handoff_payload.get("target")
    if not isinstance(handoff_target, dict) or set(handoff_target) != {"repository", "runtime", "baseline_revision", "placement"} or not all(isinstance(handoff_target.get(key), str) and handoff_target[key].strip() for key in ("repository", "runtime", "baseline_revision", "placement")):
        fail(f"{ROOT / handoff_path}: target must contain exactly repository, runtime, baseline_revision, and placement")
    if handoff_target["placement"] != fixture.get("target_placement"):
        fail(f"{ROOT / handoff_path}: target placement is not bound to the ratified adoption plan")
    gate_before = fixture.get("gate_before_envelope")
    gate_after = fixture.get("gate_after_envelope")
    if not isinstance(gate_before, dict) or not isinstance(gate_after, dict) or gate_before.get("increment_gate") != "awaiting-ratification" or gate_before.get("ratification", {}).get("state") != "pending" or gate_after.get("increment_gate") != "authorized" or gate_after.get("ratification", {}).get("state") != "authorized":
        fail(f"{fixture_path}: materialized pre/post gate envelopes are incomplete")
    validate_implementation_gate(fixture_path, gate_before, "materialized-pre-authorization")
    validate_implementation_gate(fixture_path, gate_after, "materialized-post-authorization")
    for disposition in gate_before["question_dispositions"]:
        required_routing = (f"Disposition: {disposition['disposition']}", f"Status: {disposition['status']}", f"Increment impact: {disposition['impact']}", f"Owner: {disposition['owner']}", f"Required action: {disposition['action']}", f"Affected artifacts: {disposition['affected_artifacts']}", f"Revisit trigger: {disposition['revisit_trigger']}")
        if any(marker not in pre_review for marker in required_routing):
            fail(f"{ROOT / pre[-1]}: review queue does not preserve typed uncertainty routing for {disposition['id']}")
    if report_fixture.get("gate_before_envelope") != gate_before or report_fixture.get("gate_after_envelope") != gate_after or fixture.get("authority_revisions") != report_fixture.get("authority_revisions"):
        fail(f"{report_path}: report gate/authority copies must equal the materialized fixture declarations")
    if fixture.get("gate_before_authorization") != {"documentation_readiness": gate_before["documentation_readiness"], "increment_gate": gate_before["increment_gate"], "implementation_handoff": False} or fixture.get("gate_after_authorization") != {"documentation_readiness": gate_after["documentation_readiness"], "increment_gate": gate_after["increment_gate"], "implementation_handoff": True}:
        fail(f"{fixture_path}: summary gate states must equal the detailed pre/post envelopes")
    def check_immutable_transition(before: dict, after: dict) -> bool:
        immutable_fields = set(before) - {"increment_gate", "ratification"}
        return not any(before[field] != after.get(field) for field in immutable_fields) and set(after) == set(before)
    if not check_immutable_transition(gate_before, gate_after):
        fail(f"{fixture_path}: authorization changed an immutable candidate gate field")
    for field in ("target", "increment_id", "owner", "outcome", "in_scope"):
        mutated_after = copy.deepcopy(gate_after)
        if field == "target":
            mutated_after["target"] = {**mutated_after["target"], "runtime": "rogue-runtime"}
        elif isinstance(mutated_after[field], list):
            mutated_after[field] = mutated_after[field] + ["rogue addition"]
        else:
            mutated_after[field] = "rogue-" + str(mutated_after[field])
        if check_immutable_transition(gate_before, mutated_after):
            fail(f"{fixture_path}: immutable pre/post transition mutation on {field} unexpectedly passed")
    pre_authority_paths = [path for path in pre if "/contexts/" in path or "/models/" in path or path.endswith("/adoption-plan.md")]
    for pre_path in pre_authority_paths:
        post_path = pre_path.replace("/pre/", "/post/")
        if (ROOT / pre_path).read_bytes() != (ROOT / post_path).read_bytes():
            fail(f"{fixture_path}: focused authority changed during authorization: {pre_path}")
    expected_authority_set = {item["target_path"]: item["revision"] for item in report_fixture["authority_revisions"]}
    if {item["path"]: item["revision"] for item in gate_before["authoritative_revisions"]} != expected_authority_set or {item["path"]: item["revision"] for item in gate_after["authoritative_revisions"]} != expected_authority_set:
        fail(f"{fixture_path}: pending/authorized gate authority revisions do not match the report authority set")
    for mutation_name, mutate in (
        ("changed-outcome", lambda candidate: candidate.update({"outcome": "unratified outcome"})),
        ("changed-authority", lambda candidate: candidate["authoritative_revisions"][0].update({"revision": "sha256:" + "0" * 64})),
        ("authorized-with-pending-ratification", lambda candidate: candidate.update({"ratification": {"state": "pending"}})),
    ):
        candidate = copy.deepcopy(gate_after)
        mutate(candidate)
        try:
            validate_implementation_gate(fixture_path, candidate, f"materialized-transition-{mutation_name}")
        except ValidationError:
            continue
        fail(f"{fixture_path}: transition mutation {mutation_name} unexpectedly passed")
    if handoff_payload["increment"]["id"] != fixture["increment_id"]:
        fail(f"{ROOT / handoff_path}: handoff increment id is not bound to the fixture")
    if gate_after["target"] != {key: handoff_target[key] for key in ("repository", "runtime", "baseline_revision")} or gate_after["increment_id"] != handoff_payload["increment"]["id"] or gate_after["owner"] != handoff_payload.get("implementation_owner") or auth.get("owner") != gate_after["ratification"].get("record", {}).get("owner"):
        fail(f"{ROOT / handoff_path}: target, increment, implementation owner, or decision owner is not bound to the ratified gate")
    record = gate_after["ratification"].get("record", {})
    if auth.get("decision") != record.get("decision") or auth.get("owner") != record.get("owner") or auth.get("date") != record.get("date"):
        fail(f"{ROOT / handoff_path}: authorization decision/owner/date must equal the ratified gate's decision record exactly")
    for field in ("outcome", "in_scope", "out_of_scope", "return_on_conflict", "accepted_assumptions", "deferred_questions", "out_of_scope_questions", "question_dispositions", "acceptance_signals"):
        handoff_value = handoff_payload["increment"]["outcome"] if field == "outcome" else handoff_payload[field]
        if handoff_value != gate_after[field]:
            fail(f"{ROOT / handoff_path}: {field} is not bound to the ratified gate")
    if handoff_payload["containment"] != gate_after["containment"]:
        fail(f"{ROOT / handoff_path}: containment is not bound to the ratified gate")
    if handoff_payload["increment"]["outcome"] != gate_after["outcome"]:
        fail(f"{ROOT / handoff_path}: increment outcome is not bound to the ratified gate")
    def bound_to_gate(payload: dict, gate: dict) -> bool:
        return (payload["increment"]["outcome"] == gate["outcome"] and payload["in_scope"] == gate["in_scope"] and payload["out_of_scope"] == gate["out_of_scope"] and payload["return_on_conflict"] == gate["return_on_conflict"] and payload["acceptance_signals"] == gate["acceptance_signals"] and payload["containment"] == gate["containment"] and payload["authoritative_artifacts"] == gate["authoritative_revisions"])
    if not bound_to_gate(handoff_payload, gate_after):
        fail(f"{ROOT / handoff_path}: executable handoff is not fully bound to the ratified gate")
    for field, value in (("outcome", "broadened outcome"), ("in_scope", gate_after["in_scope"] + ["unratified behavior"]), ("return_on_conflict", "ddd-adoption")):
        candidate = copy.deepcopy(handoff_payload)
        if field == "outcome": candidate["increment"]["outcome"] = value
        else: candidate[field] = value
        if bound_to_gate(candidate, gate_after):
            fail(f"{ROOT / handoff_path}: handoff mutation {field} was not rejected by gate binding")
    handoff_authority_paths = [item.get("path") for item in handoff_payload["authoritative_artifacts"]]
    if any(not isinstance(path, str) or not path.startswith("docs/ddd/") or ".." in path for path in handoff_authority_paths) or len(set(handoff_authority_paths)) != len(handoff_authority_paths):
        fail(f"{ROOT / handoff_path}: logical authority paths must be unique and contained under docs/ddd")
    expected_handoff_authorities = [{"path": item["target_path"], "sections": item["sections"], "revision": item["revision"], "role": item["role"]} for item in report_fixture["authority_revisions"]]
    if handoff_payload["authoritative_artifacts"] != expected_handoff_authorities or gate_after["authoritative_revisions"] != expected_handoff_authorities:
        fail(f"{ROOT / handoff_path}: logical authoritative artifact set is not exact or not bound to the gate")
    if set(handoff_payload["characterization_cases"]) != {case["id"] for case in fixture["cases"]}:
        fail(f"{ROOT / handoff_path}: handoff does not name all seven characterization cases")
    model_path = next(path for path in authorities if path.endswith("/models/storytelling-experience.md"))
    model_text = (ROOT / model_path).read_text(encoding="utf-8")
    if "| Case | Given | When | Then |" not in model_text:
        fail(f"{ROOT / model_path}: tactical authority lacks the executable Given/When/Then table")

    def decide(data: dict) -> dict:
        if data.get("entitled") is not True:
            return {"decision": "reject", "reason": "entitlement"}
        if data.get("readiness") != "ready":
            return {"decision": "reject", "reason": "readiness"}
        if data.get("channel") != "online":
            return {"decision": "reject", "reason": "channel"}
        if data.get("proximity") != "in-range":
            return {"decision": "reject", "reason": "proximity"}
        if data.get("state") == "completed":
            return {"decision": "reject", "reason": "duplicate-completion"}
        if data.get("state") == "started":
            if data.get("completion") == "explicit":
                return {"decision": "complete", "state": "completed"}
            return {"decision": "reject", "reason": "duplicate-start"}
        return {"decision": "start", "state": "started"}

    def oracle(case: dict) -> dict:
        if case["id"] == "executable-proximity-profiles":
            outputs = {}
            for profile in case["profiles"]:
                data = dict(case["input"])
                data["proximity"] = "in-range" if profile == "in-range-online" else "out-of-range"
                outputs[profile] = "start" if decide(data)["decision"] == "start" else "reject-proximity"
            return outputs
        return decide(case["input"])
    runs = {run["id"]: run for run in report["runs"]}
    for case in fixture["cases"]:
        expected = oracle(case)
        data = dict(case["input"])
        if "profiles" in case:
            data["profiles"] = case["profiles"]
        given = json.dumps(data, sort_keys=True, separators=(",", ":"))
        rendered = json.dumps(expected, sort_keys=True, separators=(",", ":"))
        if given not in model_text or rendered not in model_text or f"`{case['id']}`" not in model_text:
            fail(f"{ROOT / model_path}: rendered authority omits executable input/output for {case['id']}")
        if expected != case["expected_output"] or runs[case["id"]]["observed_output"] != expected:
            fail(f"{report_path}: deterministic oracle mismatch for {case['id']}")


HANDOFF_TEMPLATE_SECTION_TARGETS = (
    (re.compile(r"/adoption-plan\.md$"), ("ddd-adoption", "adoption-plan-template.md")),
    (re.compile(r"/models/[^/]+\.md$"), ("ddd-tactical", "context-model-template.md")),
    (re.compile(r"/contexts/[^/]+\.md$"), ("ddd-strategic", "context-template.md")),
)


def validate_handoff_template_sections() -> None:
    """Regression gate for F-B2: the implementation-handoff-v1 template's own
    illustrative ``sections`` YAML, not only a materialized fixture, must
    list real H2 headings of the stage template each authoritative artifact
    corresponds to. A prior version used an unquoted flow-list whose
    comma-bearing heading silently mis-split under a YAML parser and was
    never checked against real content because coverage only ever validated
    a pre-fixed fixture -- this closes that gap by checking the template
    itself, the artifact a real run actually copies."""
    template_path = SKILLS_ROOT / "ddd" / "assets" / "implementation-handoff-template.md"
    text = template_path.read_text(encoding="utf-8")
    artifact_count = len(re.findall(r"^  - path: \S+", text, flags=re.MULTILINE))
    entries = re.findall(r"- path: (\S+)\s*\n\s*sections: \[(.*?)\]", text)
    if not entries:
        fail(f"{template_path}: no authoritative_artifacts sections entries found to validate")
        return
    if len(entries) != artifact_count:
        fail(f"{template_path}: found {artifact_count} authoritative_artifacts entries but only matched {len(entries)} single-line sections values (a multi-line or reformatted sections list would be silently skipped)")
        return
    for path_value, raw_sections in entries:
        target = next(
            (
                SKILLS_ROOT / skill_name / "assets" / asset_name
                for pattern, (skill_name, asset_name) in HANDOFF_TEMPLATE_SECTION_TARGETS
                if pattern.search(path_value)
            ),
            None,
        )
        if target is None:
            fail(f"{template_path}: unrecognized authoritative artifact path pattern: {path_value}")
            continue
        quoted_sections = re.findall(r'"([^"]*)"', raw_sections)
        unquoted_remainder = re.sub(r'"[^"]*"', "", raw_sections).replace(",", "").strip()
        if not quoted_sections or unquoted_remainder:
            fail(f"{template_path}: sections for {path_value} must be double-quoted YAML flow-list entries, not {raw_sections!r}")
            continue
        headings = set(re.findall(r"^##\s+(.+)$", target.read_text(encoding="utf-8"), flags=re.MULTILINE))
        missing = [section for section in quoted_sections if section not in headings]
        if missing:
            fail(f"{template_path}: sections for {path_value} are not real H2 headings of {target}: {missing}")


def validate_forbidden_runtime_references() -> None:
    for path in sorted((ROOT / "skills").rglob("*")):
        if not path.is_file() or path.suffix not in {".md", ".json"}:
            continue
        text = path.read_text(encoding="utf-8")
        match = FORBIDDEN_RE.search(text)
        if match:
            fail(f"{path}: forbidden runtime-specific or machine-local reference: {match.group(0)!r}")


def validate_packages_manifest(skill_dirs: list[Path]) -> dict[str, str]:
    path = ROOT / "PACKAGES"
    if not path.is_file():
        fail(f"{path}: repository PACKAGES manifest is missing")
    skill_names = {skill_root.name for skill_root in skill_dirs}
    classes: dict[str, str] = {}
    for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip("\n")
        if not line.strip():
            continue
        fields = line.split("\t")
        if len(fields) != 3:
            fail(f"{path}:{lineno}: expected exactly name<TAB>class<TAB>label")
        name, package_class, label = fields
        if not NAME_RE.fullmatch(name):
            fail(f"{path}:{lineno}: package name must be lowercase alphanumeric words joined by hyphens: {name!r}")
        if name in classes:
            fail(f"{path}:{lineno}: duplicate package name: {name}")
        if package_class not in PACKAGE_MANIFEST_CLASSES:
            fail(f"{path}:{lineno}: unknown package class {package_class!r} for {name}")
        if not label.strip():
            fail(f"{path}:{lineno}: package {name} has an empty label")
        classes[name] = package_class
    missing_from_manifest = sorted(skill_names - classes.keys())
    if missing_from_manifest:
        fail(f"{path}: missing manifest row(s) for skill package(s): {', '.join(missing_from_manifest)}")
    extra_in_manifest = sorted(classes.keys() - skill_names)
    if extra_in_manifest:
        fail(f"{path}: manifest names package(s) with no matching skills/ directory: {', '.join(extra_in_manifest)}")
    return classes


def validate_implementation_write_boundary(skill_root: Path) -> None:
    text = (skill_root / "SKILL.md").read_text(encoding="utf-8").lower()
    missing = [marker for marker in IMPLEMENTATION_BOUNDARY_MARKERS if marker not in text]
    if missing:
        fail(f"{skill_root / 'SKILL.md'}: implementation package must state its write boundary and approval gates; missing: {', '.join(missing)}")


def validate_active_plan_handoff_reference() -> None:
    candidates = [
        ROOT / "docs/plans/active/lean-workflow-redesign.md",
        ROOT / "docs/plans/complete/lean-workflow-redesign.md",
    ]
    plan_path = next((path for path in candidates if path.is_file()), None)
    if plan_path is None:
        fail(f"{candidates[0]}: lean-workflow-redesign plan not found under docs/plans/active/ or docs/plans/complete/")
        return
    text = plan_path.read_text(encoding="utf-8")
    if "version: implementation-handoff-v1" in text:
        fail(f"{plan_path}: must not duplicate the implementation-handoff-v1 schema; link to skills/ddd/assets/implementation-handoff-template.md instead")
    if "skills/ddd/assets/implementation-handoff-template.md" not in text:
        fail(f"{plan_path}: must reference the canonical implementation-handoff-v1 template")


def main() -> int:
    try:
        if not SKILLS_ROOT.is_dir():
            fail(f"{SKILLS_ROOT}: skills root is missing")
        skill_dirs = sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir())
        if not skill_dirs:
            fail(f"{SKILLS_ROOT}: no skill packages found")
        for skill_root in skill_dirs:
            validate_skill(skill_root)
            validate_evals(skill_root)
        package_classes = validate_packages_manifest(skill_dirs)
        for skill_root in skill_dirs:
            if package_classes[skill_root.name] == "implementation":
                validate_implementation_write_boundary(skill_root)
        tactical_eval_path = SKILLS_ROOT / "ddd-tactical" / "evals" / "evals.json"
        if tactical_eval_path.is_file():
            tactical_root = SKILLS_ROOT / "ddd-tactical"
            tactical_payload = json.loads(tactical_eval_path.read_text(encoding="utf-8"))
            validate_tactical_eval_inputs(tactical_root, tactical_payload["cases"])
            validate_tactical_contract(tactical_root)
        adoption_eval_path = SKILLS_ROOT / "ddd-adoption" / "evals" / "evals.json"
        if adoption_eval_path.is_file():
            adoption_root = SKILLS_ROOT / "ddd-adoption"
            adoption_payload = json.loads(adoption_eval_path.read_text(encoding="utf-8"))
            validate_adoption_eval_inputs(adoption_root, adoption_payload["cases"])
            validate_adoption_contract(adoption_root)
        review_eval_path = SKILLS_ROOT / "ddd-review" / "evals" / "evals.json"
        if review_eval_path.is_file():
            review_root = SKILLS_ROOT / "ddd-review"
            review_payload = json.loads(review_eval_path.read_text(encoding="utf-8"))
            validate_review_eval_inputs(review_root, review_payload["cases"])
            validate_review_contract(review_root)
        orchestrator_eval_path = SKILLS_ROOT / "ddd" / "evals" / "evals.json"
        if orchestrator_eval_path.is_file():
            orchestrator_root = SKILLS_ROOT / "ddd"
            orchestrator_payload = json.loads(orchestrator_eval_path.read_text(encoding="utf-8"))
            validate_orchestrator_eval_inputs(orchestrator_root, orchestrator_payload["cases"])
            validate_orchestrator_contract(orchestrator_root)
        validate_phase4_transition_matrix()
        validate_lean_eval_suite()
        validate_lean_case_semantics()
        validate_lean_contracts()
        validate_sanitized_fixture()
        validate_materialized_fixture()
        validate_handoff_template_sections()
        validate_active_plan_handoff_reference()
        validate_repository_markdown()
        validate_forbidden_runtime_references()
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"validated {len(skill_dirs)} skill package(s) plus the PACKAGES manifest, historical and lean evals, contracts, references, assets, fixture, links, H1s, and runtime-neutral paths")
    print("scope: deterministic repository/fixture/schema coverage; live host/model compatibility and external-project effectiveness are not claimed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
