# Example Research Object

Good research contributions are small enough to review and precise enough to
continue.

```yaml
---
id: topp-problem-55-c0001
type: claim
status: proposed
evidence_type: derivation
route_ids: []
depends_on:
  - topp-problem-55
source_ids:
  - topp-p55
authors:
  - name: Jan Bartos
    github: JanBartos6
    role: proposer
contributors: []
reviewers: []
curators: []
ai_assistance:
  used: true
  model: unknown
  role: proposed-derivation
review:
  llm_reviewed: false
  human_reviewed: false
  formal_reviewed: false
---
```

Why this is reviewable:

- the object has a stable ID
- the claim has dependencies and sources
- AI assistance is disclosed
- review flags are not self-certified
- the body must state a gap and next step

Likely rejected:

- a raw model transcript
- a broad essay with no checkable statement
- a claim marked verified by its own author
- a duplicate summary that adds no source, gap, route, or task
