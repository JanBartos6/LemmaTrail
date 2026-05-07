# Model Prompt

Copy this into an LLM or agent. Fill in the bracketed fields.

```text
You are contributing to LemmaTrail.

Problem:
[problem id, title, or source number]

Custom focus:
[optional]

First read:
- AGENTS.md
- INSTRUCTIONS.md
- README.md
- CONTRIBUTING.md
- docs/pr-guard.md

Before editing, resolve the problem to an existing problems/<problem-id>/
workspace or an imported catalog record under catalog/imports/**. Use that
stable id for paths. Example: TOPP Problem 55 uses
problems/topp-problem-55/, not problems/55/.

Goal:
Preserve checkable progress for one problem. Do as much useful work as you can
justify, but every claim, route, attempt, failure, review, or task must be
checkable.

Rules:
- Stay within one problem per research PR.
- Use templates/ for new research objects.
- Prefer proposals/, review/, or refuted/.
- Do not edit canonical/ unless a human maintainer explicitly asks.
- Separate sourced facts from speculative derivation.
- Cite sources or give reproducible reasoning.
- State dependencies, gap or weakness, and next step.
- State claims only as strongly as the derivation supports.
- Do not include raw chat transcripts or filler.
- Do not set llm_reviewed, human_reviewed, or formal_reviewed to true on your
  own contribution.

If no checkable contribution is justified, say exactly:
No repository contribution is justified.
Then state the best next task.

If a checkable research contribution is produced and GitHub access is
available, you must publish it as a literal draft GitHub pull request:
- create a branch
- add the problem-scoped object or objects
- commit
- run the PR guard
- push
- open a draft PR with PR type: research

A local file is not a PR. Do not claim the guard passed unless you ran it and
it exited successfully. If you cannot open a PR, say exactly why.
```
