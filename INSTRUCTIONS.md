# Instructions For LLMs And Agents

Goal: preserve checkable research progress. Do not write essays, transcripts,
or unsupported claims.

## Start

1. Read `README.md`, `CONTRIBUTING.md`, and `docs/pr-guard.md`.
2. Resolve the requested problem to the exact catalog `id` under `catalog/`.
   Use that ID in paths: `problems/<catalog-id>/...`.
   Example: TOPP Problem 55 is `problems/topp-problem-55/`, not `problems/55/`.
3. Read the existing problem workspace if it exists.
4. Use the closest template under `templates/`.

## Scope

- One research PR must stay within one problem.
- Do as much checkable work as you can justify for that problem.
- Multiple connected claims, routes, attempts, failures, reviews, or tasks are
  allowed when each object is reviewable.
- Write under `problems/<problem-id>/proposals/`, `review/`, or `refuted/`.
- Do not edit `canonical/` unless a human maintainer explicitly asks.

If no checkable contribution is justified, say:

```text
No repository contribution is justified.
```

Then state the single best next task.

## Required Shape

Each research object must include:

- precise statement or objective
- dependencies
- sources or reproducible reasoning
- gap, weakness, or review risk
- next step
- AI assistance disclosure when applicable

State claims only as strongly as the derivation supports.

## Do Not Submit

- raw chat transcripts
- filler or broad essays
- unsupported claims
- duplicate background
- cross-problem research PRs
- unverified work marked as verified
- `llm_reviewed: true`, `human_reviewed: true`, or `formal_reviewed: true` on
  your own contribution

## Pull Requests

Use `PR type: research` for research-state changes and `PR type: technical`
for tooling, docs, templates, catalog imports, CI, or policy.

If a checkable research contribution is produced and GitHub access is
available, you must publish it as a literal draft GitHub pull request:

1. create a branch,
2. add the problem-scoped object or objects,
3. commit,
4. run the PR guard,
5. push,
6. open a draft PR.

A local file is not a PR. Do not say the guard passed unless you actually ran
it and it exited successfully. If you cannot open a PR, say exactly why.
