# Skill portability

This document records the portability decisions for the first executable focused slices. Each package follows the public Agent Skills shape while keeping behavior and outputs platform-neutral.

## Package contract

Each executable package, currently `skills/ddd-discover/` and `skills/ddd-strategic/`, has a required root `SKILL.md`, optional `references/` and `assets/` directories, and a package-local evaluation file under `evals/`. The skill name is lowercase, uses letters, numbers, and hyphens, and matches its directory name. Its description states both what the skill does and when to use it.

The skill's instructions do not depend on a particular host, command runner, language framework, model vendor, or activation mechanism. Relative links resolve from the package root. Reference documents remain one level below `references/` so a host can discover them without recursive package conventions.

## Activation and transitions

A host may activate `ddd-discover` or `ddd-strategic` directly when its trigger matches. Each skill receives a user goal or stage request, target scope, evidence boundary, permitted paths, and existing artifact context. It returns repository artifact changes plus a portable result bundle containing:

- `stage`: the exact package name, such as `ddd-discover` or `ddd-strategic`;
- `status`: a stage-specific bounded result such as `complete`, `partial`, `blocked`, or `not-fit`;
- `scope` and `changed_artifacts`;
- evidence, assumptions, open questions, and fit rationale;
- a `handoff` with exact next stage and request bundle, or a bounded stop;
- `invalidated_stages` when later work is stale.

The future orchestrator owns routing/state and may pass the unchanged bundle to `ddd-strategic`. A host without named-stage activation returns the exact manual invocation `ddd-strategic` and the bundle; it does not emulate the next skill or claim it ran. This package remains independently useful when no orchestrator exists.

## File and artifact boundary

The focused slices create or update only their owned strategic or discovery documents under `docs/ddd/`: discovery owns `assessment.md`, `domain-vision.md`, and initial language sections; strategic owns `domain-map.md`, `context-map.md`, `contexts/<safe-slug>.md`, and strategic language/vision sections. Each preserves existing files, uses additive owned sections, records provenance and validation state, and asks before destructive or ambiguous updates. Neither edits product source, tests, configuration, generated output, or deployment files.

## Source and validation scope

The package shape and description requirements are based on the [Agent Skills specification](https://agentskills.io/specification). Instruction-writing guidance is informed by [skill creation best practices](https://agentskills.io/skill-creation/best-practices), and evaluation design by [evaluating skills](https://agentskills.io/skill-creation/evaluating-skills).

The repository validator checks a deterministic subset of those requirements per package: frontmatter delimiters and simple required scalars, name/directory and length rules, description length, the recommended instruction length, relative-file containment, one-level references, package-specific assets/evals, evaluation structure, and forbidden runtime-specific or machine-local paths. It intentionally does not claim full YAML or host compatibility validation and does not reject unknown optional fields merely because it does not interpret them.

The optional official `skills-ref` validator was unavailable in this environment and was not installed. That is a validation gap, not a reason to invent compatibility fields or claim full conformance.
