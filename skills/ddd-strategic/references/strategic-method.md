# Strategic method

Use this method to turn discovery evidence into explicit strategic hypotheses. It does not require a particular workshop format or deployment architecture.

## Gate the input

Confirm:

- one meaningful outcome or capability is in scope;
- discovery says `fit` or `limited-fit`, or the user made an explicit bounded request;
- terms, examples, events, policies, and constraints are sufficient to compare boundaries;
- evidence distinguishes current behavior, desired meaning, and obligations;
- owners and allowed documentation paths are known.

If discovery says `not-fit`, preserve that result. Ask whether new evidence or an explicit decision should reopen it; do not model around the conflict silently.

## Classify subdomains

For each candidate capability, record:

- outcome and scope;
- core, supporting, generic, or unresolved hypothesis;
- rationale and evidence;
- owner and strategic importance;
- status and revisit signal.

A classification is a working hypothesis. A supporting or generic label does not mean the capability is unimportant, and a core label does not prove competitive advantage.

## Find bounded contexts

Look for consistent language, rules, lifecycle, decision ownership, and consistency needs. Record what is inside and outside each proposed context and challenge it with concrete scenarios. Different contexts may intentionally use different meanings for the same term.

Do not use module names, table names, team names, or service boundaries as proof. They can be evidence of current organization or implementation, but the domain boundary needs its own rationale.

## Map relationships

For each directional relationship, record upstream and downstream ownership, communication or contract, translation, consistency and failure assumptions, and evidence. Relationship labels such as shared kernel, customer-supplier, conformist, anti-corruption layer, open host service, or separate ways are optional shorthand. Describe the actual relationship even when no label fits.

## Validate and hand off

Challenge each boundary with:

- concrete scenarios and policy differences;
- change cadence and lifecycle;
- immediate versus eventual consistency;
- ownership and decision rights;
- security, privacy, and availability constraints;
- integration failure and translation behavior.

Tactical work is ready only when exactly one selected context has a purpose, vocabulary, scenarios, invariants to investigate, relationships, ownership, assumptions, and open questions. Otherwise return a bounded stop or request more discovery evidence.
