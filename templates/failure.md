# Failure Template

Use this for a failed route, refuted claim, obstruction, counterexample, or
dead end that future contributors should not repeat.

Copy the block below into:

```text
problems/<problem-id>/refuted/<object-id>.md
```

```markdown
---
id: PROBLEM-F0001
type: failure
status: refuted
route_ids: []
depends_on: []
source_ids: []
authors:
  - name: unknown
    github: null
    role: proposer
contributors: []
reviewers: []
curators: []
ai_assistance:
  used: false
  model: none
  role: none
review:
  llm_reviewed: false
  human_reviewed: false
  formal_reviewed: false
---

# Failed Claim Or Route

State what failed.

# Known Obstructions

Explain the exact obstruction, counterexample, invalid inference, or hidden
assumption.

# Evidence

Give source, derivation, computation, or counterexample.

# Lesson

State what future attempts should avoid.

# Next Step

State the smallest useful continuation after this obstruction.
```
