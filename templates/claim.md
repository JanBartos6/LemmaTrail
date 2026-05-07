# Claim Template

Use this for a precise candidate claim, lemma, reduction, equivalence, or
checkable mathematical statement.

Copy the block below into:

```text
problems/<problem-id>/proposals/claims/<object-id>.md
```

```markdown
---
id: PROBLEM-C0001
type: claim
status: proposed
evidence_type: derivation
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

# Statement

Write one precise mathematical statement.

# Dependencies

- ID or source used here

# Derivation

## Step C1

Formal line. Short justification.

## Step C2

Formal line. Short justification.

# Branch Point

If this claim continues from an earlier object, state the exact object and
step. If not applicable, write `none`.

# Gap

State the exact weakness, missing proof step, or unchecked assumption.

# Next Step

State the smallest useful continuation.
```
