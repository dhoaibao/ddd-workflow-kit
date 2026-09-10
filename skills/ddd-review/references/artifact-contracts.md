# Review artifact contract

`ddd-review` owns `docs/ddd/review.md` and only the `decision-queue`/`latest-review` markers in `docs/ddd/README.md`, with lean `scope`/`state` metadata and conditional `owner`; legacy metadata remains readable. `ddd` owns and preserves the other index markers.

## Exception output

The review records one named increment and authority set; `documentation_readiness`; `increment_gate`; one sentence of passed-gate summary; blocking/invalidating/decision-required findings; materially relevant accepted assumptions/deferred/out-of-scope items; earliest-owner routing; one next action; and explicit no-authorization language.

The consolidated decision queue fields are ID, issue, increment impact, disposition, owner/earliest stage, required decision/evidence, affected artifacts, and revisit trigger. The queue uses only the shared dispositions. Passed gates are not repeated as full tables.

## Safe ownership

Inspect and preserve existing review prose/legacy metadata. Update only review-owned sections additively, including the two named README markers. Mark source/dependent paths stale in findings but never rewrite them. Refuse product/runtime and unrelated paths. Review never creates `implementation-handoff.md`.
