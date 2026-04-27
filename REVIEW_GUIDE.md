# Review Guide

Reviewers protect the repository from plausible-looking noise.

## Review Layers

1. Format review
   - IDs are present.
   - Status values are valid.
   - Dependencies are listed.
   - Required sections are present.

2. Relevance review
   - The contribution changes the research state.
   - It is not a duplicate.
   - It belongs in this problem workspace.

3. LLM triage
   - An LLM may check for obvious gaps, undefined terms, broken dependencies, and duplicated claims.
   - LLM triage can recommend pass, fail, or needs-human.
   - LLM triage cannot mark anything verified.

4. Human review
   - A human checks the argument, source, or computation.
   - Only human review can move ordinary mathematical content into canonical state.

## Review Labels

Recommended GitHub labels:

```text
type/problem
type/claim
type/route
type/failure
type/reference
status/needs-review
status/needs-revision
status/refuted
status/verified
llm-triage/pass
llm-triage/has-gap
llm-triage/likely-duplicate
human-review/requested
human-review/approved
```

## Reviewer Rule

If the contribution cannot be independently checked from its sources or derivation, do not merge it into canonical state.

