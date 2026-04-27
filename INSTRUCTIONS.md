# Instructions For LLMs And Agents

You are welcome to help with LemmaTrail if you can follow the repository rules.

Your goal is not to sound impressive or produce a long answer. Your goal is to improve the shared research state in a way that humans and future models can verify.

## Before Working

Read:

1. `README.md`
2. `CONTRIBUTING.md`
3. the relevant problem folder under `problems/`
4. the relevant template under `templates/`

If the problem folder does not exist yet, work from `catalog/seed-problems.yaml` and propose a curated workspace rather than creating a large unsourced folder.

## What You May Contribute

You may propose:

- a precise claim
- a possible route
- a failed route with a clear obstruction
- a source connection
- a reproducible derivation
- a counterexample
- a concrete continuation task
- an LLM triage review of an existing proposal

## Where To Write

Prefer proposal and review areas:

```text
problems/<problem-id>/proposals/
problems/<problem-id>/review/
problems/<problem-id>/refuted/
```

Do not write directly into:

```text
problems/<problem-id>/canonical/
```

unless a human maintainer explicitly asked for that change.

## Required Shape

Any proposed mathematical contribution must include:

- a precise statement or objective
- dependencies
- sources or reproducible reasoning
- the gap, weakness, or review risk
- the smallest useful next step
- AI assistance disclosure when applicable

If you cannot produce that, say that no repository contribution is justified.

## Pull Request Behavior

A useful PR should be small. It should add one checkable research object or one clear framework improvement.

Do not submit:

- raw chat transcripts
- broad essays
- unsupported claims
- large rewrites
- duplicate background
- unverified claims marked as verified

Use `llm_reviewed: true` only to mean that an LLM reviewed the item. It does not mean the mathematics is verified.

## Good Default Output

If you find something worth proposing, create or suggest one file using the closest template from `templates/`.

If you do not find something worth proposing, report the most useful next task instead.

