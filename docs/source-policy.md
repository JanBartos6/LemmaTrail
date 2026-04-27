# Source And Reproducibility Policy

This is a draft guardrail for `v0.1-alpha`, not final governance.

Every durable contribution must be checkable.

That means it must provide either:

1. precise sources, or
2. reproducible reasoning.

## Source-Backed Contributions

Use source-backed entries for known definitions, theorems, surveys, and problem statements.

Good source notes include:

- title
- author or institution
- year if known
- exact section, theorem, proposition, page, or URL
- what the source is being used for

Bad source notes:

- "well known"
- "from number theory"
- "Wikipedia says"
- "the model remembered this"

## Derivation-Backed Contributions

If no external source is available, write the reasoning so another reviewer can get to the same finding.

Current expected sections:

- statement
- dependencies
- derivation
- gap or weakness
- smallest next step

## Computation-Backed Contributions

Computation-backed claims must include enough detail to reproduce the result:

- code or algorithm reference
- exact inputs
- environment if relevant
- output summary
- limitations

Generated artifacts should not be committed unless they are necessary for review.
