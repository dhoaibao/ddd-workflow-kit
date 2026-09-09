# Skill portability

This document records the portability decisions for the first executable MVP. The package follows the public Agent Skills shape while keeping behavior and outputs platform-neutral.

## Package contract

The executable package is `skills/ddd-discover/` with a required root `SKILL.md`, optional `references/` and `assets/` directories, and an evaluation file under `evals/`. The skill name is lowercase, uses letters, numbers, and hyphens, and matches its directory name. Its description states both what the skill does and when to use it.

The skill's instructions do not depend on a particular host, command runner, language framework, model vendor, or activation mechanism. Relative links resolve from the package root. Reference documents remain one level below `references/` so a host can discover them without recursive package conventions.

## Activation and transitions

A host may activate `ddd-discover` directly when its trigger matches. The skill receives a user goal, target scope, evidence boundary, permitted paths, and existing artifact context. It returns repository artifact changes plus a portable result bundle containing:

- `stage`: `ddd-discover`;
- `status`: `complete`, `partial`, `blocked`, or `not-fit`;
- `scope` and `changed_artifacts`;
- evidence, assumptions, open questions, and fit rationale;
- a `handoff` with exact next stage and request bundle, or a bounded stop;
- `invalidated_stages` when later work is stale.

The future orchestrator owns routing/state and may pass the unchanged bundle to `ddd-strategic`. A host without named-stage activation returns the exact manual invocation `ddd-strategic` and the bundle; it does not emulate the next skill or claim it ran. This package remains independently useful when no orchestrator exists.

## File and artifact boundary

The first executable release may create or update only `docs/ddd/assessment.md`, `domain-vision.md`, and `ubiquitous-language.md`. It preserves existing files, uses additive owned sections, records provenance and validation state, and asks before destructive or ambiguous updates. It never edits product source, tests, configuration, generated output, or deployment files.

## Source and validation scope

The package shape and description requirements are based on the [Agent Skills specification](https://agentskills.io/specification). Instruction-writing guidance is informed by [skill creation best practices](https://agentskills.io/skill-creation/best-practices), and evaluation design by [evaluating skills](https://agentskills.io/skill-creation/evaluating-skills).

The repository validator checks a deterministic subset of those requirements: frontmatter delimiters and simple required scalars, name/directory and length rules, description length, the recommended instruction length, relative-file containment, one-level references, required assets/evals, evaluation structure, and forbidden runtime-specific or machine-local paths. It intentionally does not claim full YAML or host compatibility validation and does not reject unknown optional fields merely because it does not interpret them.

The optional official `skills-ref` validator was unavailable in this environment and was not installed. That is a validation gap, not a reason to invent compatibility fields or claim full conformance.
