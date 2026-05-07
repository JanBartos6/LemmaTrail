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

Use GitHub labels sparingly. The current project labels are:

```text
research
technical
needs-review
superseded
```

Put detailed review state in review comments or research-object frontmatter,
not in a large label taxonomy. For example, `verified`, `refuted`, and
`needs-revision` are statuses or review outcomes, not labels maintainers need
to create on day one.

## Reviewer Rule

If the contribution cannot be independently checked from its sources or derivation, do not merge it into canonical state.
