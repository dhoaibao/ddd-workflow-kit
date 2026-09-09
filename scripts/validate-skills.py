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
PACKAGE_REQUIREMENTS = {
    "ddd-discover": {"assets": DISCOVERY_ASSETS, "minimum_evals": 6},
    "ddd-strategic": {"assets": STRATEGIC_ASSETS, "minimum_evals": 7},
    "ddd-tactical": {"assets": TACTICAL_ASSETS, "minimum_evals": 11},
}
TACTICAL_PREREQUISITE_STOP_CASES = {"missing-strategic-prerequisites", "select-one-context"}
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
        validate_forbidden_runtime_references()
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"validated {len(skill_dirs)} skill package(s), evals, references, assets, and runtime-neutral paths")
    print("scope: required simple frontmatter and repository conventions; full YAML/host validation is not claimed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
