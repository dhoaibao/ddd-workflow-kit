#!/usr/bin/env python3
"""Validate the repository's portable skill packages.

This is a deterministic stdlib-only subset validator. It checks the required
simple frontmatter fields and repository conventions; it does not implement
full YAML or host compatibility validation and ignores unknown optional fields.
"""

from __future__ import annotations

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
ORCHESTRATOR_ASSETS = {"request-result-template.md", "ddd-readme-template.md"}
PACKAGE_REQUIREMENTS = {
    "ddd-discover": {"assets": DISCOVERY_ASSETS, "minimum_evals": 6},
    "ddd-strategic": {"assets": STRATEGIC_ASSETS, "minimum_evals": 7},
    "ddd-tactical": {"assets": TACTICAL_ASSETS, "minimum_evals": 11},
    "ddd-adoption": {"assets": ADOPTION_ASSETS, "minimum_evals": 10},
    "ddd-review": {"assets": REVIEW_ASSETS, "minimum_evals": 10},
    "ddd": {"assets": ORCHESTRATOR_ASSETS, "minimum_evals": 10},
}
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
    "`adoption-plan`", "Mode and outcome", "First slice and ordered increments",
    "Dependencies/prerequisites", "Acceptance signal", "Ownership, dependencies, and decision points",
    "Brownfield baseline and safety", "Data, integration, privacy, and operational risks",
    "Rollback, recovery, or containment", "Forbidden actions", "`ddd-review`",
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
    "`review`", "Review scope and objective", "Artifact inventory and validation summary",
    "DDD fit and quality-gate results", "Findings by severity", "Stale and conflicting artifacts",
    "Chat summary", "documentation readiness", "implementation, deployment, migration",
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
ORCHESTRATOR_RESULT_STATUSES = {"complete", "partial", "blocked", "not-fit-conflict", "strategic-conflict", "invalidated", "protocol-error"}
ORCHESTRATOR_PRESERVED_FIELDS = {"evidence", "claims", "provenance", "assumptions", "open_questions", "artifacts", "allowed_paths"}
ORCHESTRATOR_ARTIFACT_FIELDS = {"path", "lifecycle", "validation", "availability"}
ORCHESTRATOR_LIFECYCLES = {"draft", "active", "superseded", "archived", "none"}
ORCHESTRATOR_VALIDATIONS = {"unvalidated", "partially-validated", "validated", "stale", "not-applicable"}
ORCHESTRATOR_AVAILABILITIES = {"available", "missing", "partial", "out-of-scope", "none"}
ORCHESTRATOR_INDEX_MARKERS = {
    "project-scope", "routing-status", "artifact-index", "active-contexts", "validation-summary",
    "open-questions", "provenance-policy", "safe-update-policy", "ddd-review-owned:latest-review",
}
ORCHESTRATOR_TEMPLATE_MARKERS = (
    "Request and result bundles", "ddd-routing-v1", "Manual fallback", "Normal transition",
    "DDD artifact index", "ddd-owned:routing-status:start", "ddd-review-owned:latest-review:start",
    "project/domain scope", "validation summary", "Safe-update policy",
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
    check_relative_links(skill_root, skill_file)

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
    if "docs/ddd/adoption-plan.md" not in text:
        fail(f"{template}: adoption plan must constrain the owned target artifact to docs/ddd/adoption-plan.md")


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
    if "docs/ddd/review.md" not in text:
        fail(f"{template}: review must constrain the owned target artifact to docs/ddd/review.md")
    if "Severity | Evidence | Provenance | Owner | Action | Status | Affected artifact | Earliest stage" not in text:
        fail(f"{template}: finding table must expose the complete finding schema")


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


def validate_orchestrator_result(path: Path, result: object, case_id: str) -> None:
    if not isinstance(result, dict):
        fail(f"{path}: case {case_id} result must be an object")
    missing = sorted(ORCHESTRATOR_RESULT_FIELDS - result.keys())
    if missing:
        fail(f"{path}: case {case_id} result missing fields: {', '.join(missing)}")
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


def validate_tactical_contract(skill_root: Path) -> None:
    template = skill_root / "assets" / "context-model-template.md"
    if skill_root.name != "ddd-tactical" or not template.is_file():
        return
    text = template.read_text(encoding="utf-8")
    missing = [marker for marker in TACTICAL_CLAIM_LINK_MARKERS if marker not in text]
    if missing:
        fail(f"{template}: every tactical decision section must expose Claim IDs; missing: {', '.join(missing)}")
    if "_C-001 or none needed_" in text:
        fail(f"{template}: Claim ID cells must require an actual ledger ID; 'none needed' is not a Claim ID")


def validate_forbidden_runtime_references() -> None:
    for path in sorted((ROOT / "skills").rglob("*")):
        if not path.is_file() or path.suffix not in {".md", ".json"}:
            continue
        text = path.read_text(encoding="utf-8")
        match = FORBIDDEN_RE.search(text)
        if match:
            fail(f"{path}: forbidden runtime-specific or machine-local reference: {match.group(0)!r}")


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
        validate_forbidden_runtime_references()
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"validated {len(skill_dirs)} skill package(s), evals, references, assets, and runtime-neutral paths")
    print("scope: required simple frontmatter and repository conventions; full YAML/host validation is not claimed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
