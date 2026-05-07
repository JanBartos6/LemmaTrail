# Review Template

Use this for an LLM triage note, human review note, source check, or gap
review. Reviews do not make a claim verified by themselves.

Copy the block below into:

```text
problems/<problem-id>/review/<review-kind>/<object-id>.md
```

```markdown
---
id: PROBLEM-REV0001
type: review
review_target: TARGET-ID
reviewer_type: llm
reviewer: unknown
status: needs-review
created: YYYY-MM-DD
authors:
  - name: unknown
    github: null
    role: reviewer
contributors: []
reviewers: []
curators: []
ai_assistance:
  used: false
  model: none
  role: none
---

# Review Summary

Short result of the review.

# Checks

- [ ] IDs and dependencies exist
- [ ] Terms match glossary
- [ ] Sources support the stated use
- [ ] Derivation is locally valid
- [ ] Gaps are explicit
- [ ] No duplicate found

# Findings

- Finding ID or concise finding

# Recommendation

Use one: pass-to-human, needs-revision, likely-duplicate, has-gap, reject.
```
