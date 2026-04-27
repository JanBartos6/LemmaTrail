# Status Levels

Use only these statuses unless the project governance changes.

```text
idea
proposed
triaged
needs-review
verified
formally-verified
refuted
blocked
superseded
```

## Meanings

`idea` means the object is a direction or hunch, not yet a precise claim.

`proposed` means the object is precise enough to discuss but has not passed structural review.

`triaged` means basic relevance, formatting, and dependency checks passed.

`needs-review` means the object may be mathematically useful but still needs human review.

`verified` means a human reviewer accepted the claim for this repository.

`formally-verified` means a formal proof assistant, certified computation, or equivalent formal method verified it.

`refuted` means the object is false or invalid.

`blocked` means progress depends on a named unresolved gap.

`superseded` means a stronger or cleaner object replaced it.

## Review Fields

Use review fields separately from status:

```yaml
review:
  llm_reviewed: true
  human_reviewed: false
  formal_reviewed: false
```

LLM review does not imply mathematical verification.

