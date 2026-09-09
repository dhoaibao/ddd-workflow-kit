# 1. Fundamentals

## What DDD is for

Domain-Driven Design (DDD) focuses software design on the domain—the activity, rules, events, and language that matter to an organization and its users. It connects two kinds of work:

- **Strategic design** decides how to divide and relate areas of the problem.
- **Tactical design** shapes a model and its code within one deliberately bounded area.

The goal is not to reproduce every business detail. The goal is to make important decisions visible, testable, and understandable to the people who own or use the business capability.

DDD is especially useful where rules are complex, terminology is ambiguous, and the cost of changing business behavior is significant. A simple CRUD workflow may need little more than clear data validation and a well-chosen persistence model.

## Domain knowledge and ubiquitous language

A **model** is a purposeful representation of the domain for a particular context. It selects concepts and relationships that support decisions; it is not necessarily a complete picture of reality.

**Ubiquitous language** is the shared vocabulary used by domain experts and the delivery team in conversations, examples, documentation, tests, and code. It should be specific to a bounded context. If two groups use the same word differently, record the distinction rather than silently merging the meanings.

Useful discovery questions include:

- What outcome is the business trying to achieve?
- Which decisions or policies make this work difficult?
- What words, examples, and exceptions do experts use?
- Which events indicate that something meaningful happened?
- Where do definitions, ownership, or rules change?

## A collaborative feedback loop

A practical DDD loop is:

1. Explore a business scenario with domain experts.
2. Capture terms, rules, examples, commands, and domain events.
3. Propose a model and its boundaries.
4. Challenge the model with concrete examples and edge cases.
5. Implement a small slice and use tests or executable examples to expose rules.
6. Revisit the model as new evidence appears.

This loop makes disagreement useful: it can reveal a missing concept, an overloaded term, or a boundary that needs adjustment.

## Two levels of design

Strategic and tactical design answer different questions:

| Level | Main question | Typical outputs |
| --- | --- | --- |
| Strategic | How should the domain be understood and divided? | domain map, subdomains, bounded contexts, context map, integration priorities |
| Tactical | How should one context represent and enforce its rules? | entities, value objects, aggregates, services, repositories, events, specifications |

Do not use tactical patterns to avoid a strategic boundary decision, or use a context map as a substitute for modeling the rules inside a context.
