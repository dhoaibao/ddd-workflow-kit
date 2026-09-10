# Skill portability

The suite has two package classes, recorded in the release-root `PACKAGES` manifest (`name<TAB>class<TAB>label`). The six `document`-class packages are portable documentation skills: they do not require a programming language, framework, vendor, database, host, model, deployment topology, or runtime API. `implementation`-class packages (currently `ddd-impl-fastapi-hdx`) declare a specific target stack and write target-project code for one ratified increment; they stay host/vendor-neutral and package-local like every other package, but they are not runtime-neutral in the document-package sense — the stack they implement against is exactly what the package name declares.

## Package contract

Each package has a root `SKILL.md`, package-local references/assets/evals, and only relative links inside its own package. A package can be copied independently regardless of class. The validator checks simple frontmatter, links, one-level references, one H1 per Markdown file, required assets, evaluation shape, forbidden host/machine/runtime-specific references, the `PACKAGES` manifest's exact 1:1 correspondence with `skills/` directories, and that every implementation-class package's `SKILL.md` states its write boundary and approval gates.

## Transport and activation

`ddd-routing-v1` remains the compatibility transport. The explicitly versioned `ddd-implementation-gate-v1` extension carries one increment ID, target/runtime, baseline, owner, acceptance, containment, dual readiness, ratification, and authority revisions from adoption through review and orchestration. A host without named activation receives the exact manual stage name and unchanged request bundle; no package claims that an unavailable stage ran.

## File and artifact boundary

- `ddd` owns only `docs/ddd/README.md` routing/status markers and the authorized `docs/ddd/implementation-handoff.md`.
- discovery conditionally owns assessment/vision/language decision records;
- strategic owns one selected context and only triggered maps/glossary/additional contexts;
- tactical owns one model and evidence-backed additive tactical notes;
- adoption owns one adoption plan;
- review owns one exception-based review and decision queue;
- an installed implementation-class package owns one `docs/ddd/implementation/<increment-id>.md` record per increment in the target project, plus the domain code/tests for that ratified increment; it never edits `docs/ddd/implementation-handoff.md`.

Every stage preserves existing files, reads legacy metadata, uses additive owned sections, and returns stale/conflict routes instead of rewriting another stage's authority.

## Validation scope

`python3 scripts/validate-skills.py` is deterministic repository-convention coverage. It validates package isolation, links, H1 counts, runtime neutrality, lean contract markers, evaluation cases, handoff/ratification markers, the local sanitized fixture, and the `PACKAGES` manifest/class contract. It does not establish live host/model behavior or external-project effectiveness, and it does not evaluate an implementation package's target-repository output. No external BonVoye repository is accessed by this redesign.
