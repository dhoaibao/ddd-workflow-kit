# 5. Adoption playbook

Adoption works best as a sequence of learning and delivery loops rather than a large up-front modeling exercise. Adapt the depth to the risk and size of the domain.

## Greenfield workflow

1. **Frame the outcome.** State the business goal, users, constraints, and decisions the system must support.
2. **Explore with experts.** Use concrete scenarios, examples, events, and questions. EventStorming or Domain Storytelling can provide workshop formats; neither replaces judgment.
3. **Map the domain.** Identify candidate subdomains, core/supporting/generic hypotheses, bounded contexts, ownership, and context-map relationships.
4. **Choose a thin slice.** Select a valuable, high-learning use case rather than modeling every possible feature.
5. **Define the model.** Agree on ubiquitous language, invariants, aggregate boundaries, commands, events, and integration contracts for that slice.
6. **Implement and verify.** Keep domain rules testable, exercise examples, and verify persistence and integration behavior separately.
7. **Observe and revise.** Use delivery feedback, production behavior, and expert review to update the model and boundaries.

## Brownfield workflow

1. **Establish a safe baseline.** Inventory behavior, dependencies, data ownership, integrations, and current failure modes. Add characterization tests or observability where behavior is poorly understood.
2. **Find seams.** Look for workflows, terms, tables, modules, or teams that already form natural boundaries. Do not assume current code structure is the domain structure.
3. **Start with one bounded context or capability.** Protect the selected seam with an explicit interface, translation layer, or anti-corruption layer where needed.
4. **Strangle incrementally.** Route one use case or rule at a time to the new model while keeping compatibility at the boundary. Preserve rollback and data reconciliation plans.
5. **Migrate language and ownership.** Update documentation, tests, dashboards, and team agreements so the new vocabulary is used consistently.
6. **Measure the result.** Compare change lead time, defect patterns, operational cost, and user outcomes; stop or adjust if the boundary is not paying for its complexity.

## Team practices

- Keep domain experts involved throughout, not only at kickoff.
- Make modeling artifacts versioned and easy to challenge.
- Prefer examples over vague definitions.
- Record unresolved questions and assumptions.
- Treat translations and integration contracts as deliberate code, not incidental mapping.
- Revisit classifications and boundaries as strategy changes.

## Adoption checklist

- [ ] There is a named outcome and a feedback loop with domain experts.
- [ ] The first slice has explicit scope and success signals.
- [ ] Boundaries, ownership, and integration assumptions are documented.
- [ ] Existing behavior is protected before a brownfield migration.
- [ ] The team has a rollback or containment strategy for risky changes.
- [ ] The model is validated by examples, tests, and observed outcomes.
