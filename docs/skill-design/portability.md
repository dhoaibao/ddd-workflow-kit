# Skill portability

This document records portability decisions for the executable focused slices. Each package follows the public Agent Skills shape while keeping behavior and outputs platform-neutral.

## Package contract

Each executable package, currently `skills/ddd-discover/`, `skills/ddd-strategic/`, `skills/ddd-tactical/`, and `skills/ddd-adoption/`, has a required root `SKILL.md`, optional `references/` and `assets/` directories, and a package-local evaluation file under `evals/`. The skill name is lowercase, uses letters, numbers, and hyphens, and matches its directory name. Its description states both what the skill does and when to use it.

The skill instructions do not depend on a particular host, command runner, language framework, model vendor, or activation mechanism. Relative links resolve from the package root. Reference documents remain one level below `references/` so a host can discover them without recursive package conventions.

## Activation and transitions

A host may activate `ddd-discover`, `ddd-strategic`, `ddd-tactical`, or `ddd-adoption` directly when its trigger matches. Each skill receives a user goal or stage request, target scope, evidence boundary, permitted paths, and existing artifact context. It returns repository artifact changes plus a portable result bundle containing:

- `stage`: the exact package name;
- `status`: a stage-specific bounded result such as `complete`, `partial`, `blocked`, `not-fit-conflict`, or `strategic-conflict`;
- `scope` and `changed_artifacts`;
- evidence, assumptions, open questions, and validation state;
- a `handoff` with exact next stage and request bundle, or a bounded stop;
- `invalidated_stages` when later work is stale.

The future `ddd` orchestrator owns routing/state and may pass unchanged bundles between focused stages. A host without named-stage activation returns the exact manual stage name and unchanged bundle; it does not emulate the next skill or claim it ran. Each package remains independently useful when no orchestrator exists.

## File and artifact boundary

The focused slices create or update only their owned strategic, tactical, or discovery documents under `docs/ddd/`:

- discovery owns `assessment.md`, `domain-vision.md`, and initial language sections;
- strategic owns `domain-map.md`, `context-map.md`, `contexts/<safe-slug>.md`, and strategic language/vision sections;
- tactical owns `models/<validated-context-slug>.md` plus additive tactical sections in the selected context and language documents;
- adoption owns `adoption-plan.md` and only its adoption-owned sections.

Each preserves existing files, uses additive owned sections, records provenance and validation state, and asks before destructive or ambiguous updates. Tactical work does not alter context maps or strategic boundaries; boundary conflicts return to strategic design. No focused slice edits product source, tests, configuration, generated output, schemas, or deployment files.

## Source and validation scope

The package shape and description requirements are based on the [Agent Skills specification](https://agentskills.io/specification). Instruction-writing guidance is informed by [skill creation best practices](https://agentskills.io/skill-creation/best-practices), and evaluation design by [evaluating skills](https://agentskills.io/skill-creation/evaluating-skills).

The repository validator checks a deterministic subset of those requirements per package: frontmatter delimiters and simple required scalars, name/directory and length rules, description length, the recommended instruction length, relative-file containment, one-level references, package-specific assets/evals, evaluation structure, and forbidden runtime-specific or machine-local paths. It intentionally does not claim full YAML or host compatibility validation and does not reject unknown optional fields merely because it does not interpret them.

The optional official `skills-ref` validator was unavailable in this environment and was not installed. That is a validation gap, not a reason to invent compatibility fields or claim full conformance.
