# Text Policy

Text is allowed only when it helps verification or continuation.

The repository should not be equations-only, because reviewers and future models need context, dependencies, gaps, and source notes. But prose must be structured and attached to a mathematical purpose.

## Allowed Text

- definitions
- source notes
- short context
- proof commentary
- dependency explanations
- gap descriptions
- failure reasons
- review notes
- next-step instructions
- edge-case notes

## Disallowed Text

- raw LLM transcripts
- long essays
- broad philosophy
- hype
- personal motivation inside problem files
- vague speculation
- duplicate explanations
- prose that does not attach to a statement, source, gap, or task

## Inline Comments

Inline comments are allowed when they justify a formal step.

Preferred style:

```text
1. Formal line.
   Short justification.

2. Formal line.
   Short justification.
```

Avoid free-floating paragraphs in mathematical files. If a paragraph does not fit under `Context`, `Source`, `Derivation`, `Gap`, `Review`, or `Next Step`, it probably does not belong.

## Length Guardrails

These are guardrails, not hard law:

- Context: at most 150 words
- Justification per formal step: at most 2 sentences
- Gap: at most 100 words
- Next step: at most 100 words

