# Skill portability

The six packages are portable documentation skills. They do not require a programming language, framework, vendor, database, host, model, deployment topology, or runtime API.

## Package contract

Each package has a root `SKILL.md`, package-local references/assets/evals, and only relative links inside its own package. A package can be copied independently. The validator checks simple frontmatter, links, one-level references, one H1 per Markdown file, required assets, evaluation shape, and forbidden host/machine/runtime-specific references.

## Transport and activation

`ddd-routing-v1` remains the compatibility transport. The explicitly versioned `ddd-implementation-gate-v1` extension carries one increment ID, target/runtime, baseline, owner, acceptance, containment, dual readiness, ratification, and authority revisions from adoption through review and orchestration. A host without named activation receives the exact manual stage name and unchanged request bundle; no package claims that an unavailable stage ran.

## File and artifact boundary

- `ddd` owns only `docs/ddd/README.md` routing/status markers and the authorized `docs/ddd/implementation-handoff.md`.
- discovery conditionally owns assessment/vision/language decision records;
- strategic owns one selected context and only triggered maps/glossary/additional contexts;
- tactical owns one model and evidence-backed additive tactical notes;
- adoption owns one adoption plan;
- review owns one exception-based review and decision queue.

Every stage preserves existing files, reads legacy metadata, uses additive owned sections, and returns stale/conflict routes instead of rewriting another stage's authority.

## Validation scope

`python3 scripts/validate-skills.py` is deterministic repository-convention coverage. It validates package isolation, links, H1 counts, runtime neutrality, lean contract markers, evaluation cases, handoff/ratification markers, and the local sanitized fixture. It does not establish live host/model behavior or external-project effectiveness. No external BonVoye repository is accessed by this redesign.
