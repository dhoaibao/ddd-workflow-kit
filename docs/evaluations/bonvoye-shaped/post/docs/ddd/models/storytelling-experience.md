# Storytelling Experience tactical slice
- scope: storytelling-characterization-v1
- state: current


## Outcome and examples

The outcome is a deterministic characterization of one storytelling slice. Evidence: local sanitized BonVoye-shaped fixture, `docs/evaluations/bonvoye-shaped-lean-fixture.json`. Entitled in-range online start succeeds; entitlement/readiness/duplicate cases reject; explicit completion completes; duplicate completion rejects.

| Case | Given | When | Then |
| --- | --- | --- | --- |
| `entitled-in-range-online-start` | `{"channel":"online","entitled":true,"proximity":"in-range","readiness":"ready","state":"not-started"}` | apply the selected start/complete rule | `{"decision":"start","state":"started"}` |
| `entitlement-rejection` | `{"channel":"online","entitled":false,"proximity":"in-range","readiness":"ready","state":"not-started"}` | apply the selected start/complete rule | `{"decision":"reject","reason":"entitlement"}` |
| `readiness-rejection` | `{"channel":"online","entitled":true,"proximity":"in-range","readiness":"not-ready","state":"not-started"}` | apply the selected start/complete rule | `{"decision":"reject","reason":"readiness"}` |
| `duplicate-start` | `{"channel":"online","entitled":true,"proximity":"in-range","readiness":"ready","state":"started"}` | apply the selected start/complete rule | `{"decision":"reject","reason":"duplicate-start"}` |
| `explicit-completion` | `{"channel":"online","completion":"explicit","entitled":true,"proximity":"in-range","readiness":"ready","state":"started"}` | apply the selected start/complete rule | `{"decision":"complete","state":"completed"}` |
| `duplicate-completion` | `{"channel":"online","completion":"explicit","entitled":true,"proximity":"in-range","readiness":"ready","state":"completed"}` | apply the selected start/complete rule | `{"decision":"reject","reason":"duplicate-completion"}` |
| `executable-proximity-profiles` | `{"channel":"online","entitled":true,"profiles":["in-range-online","out-of-range-online"],"readiness":"ready","state":"not-started"}` | apply the selected start/complete rule | `{"in-range-online":"start","out-of-range-online":"reject-proximity"}` |

## Commands, rules, and transitions

The selected commands are start and complete. The seven fixture inputs and expected outputs are the executable examples.

## Invariants and current-versus-desired delta

A story starts only when entitled, ready, in range, online, and not already started. Completion is explicit and occurs only once. This fixture records desired characterization behavior without changing product code.
