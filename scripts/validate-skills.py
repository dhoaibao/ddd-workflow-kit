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

    required_assets = DISCOVERY_ASSETS if skill_root.name == "ddd-discover" else set()
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
    minimum = 6 if skill_root.name == "ddd-discover" else 1
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
        validate_forbidden_runtime_references()
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"validated {len(skill_dirs)} skill package(s), evals, references, assets, and runtime-neutral paths")
    print("scope: required simple frontmatter and repository conventions; full YAML/host validation is not claimed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
