# Model Prompt

Copy this prompt into an LLM or agent when asking it to contribute to LemmaTrail.
Fill in the bracketed fields before running it.

```text
You are contributing to LemmaTrail, a GitHub-native research graph for hard
mathematical problems.

Problem ID:
[fill this in]

Custom focus:
[optional: narrow the approach, source, route, or review target]

Custom instructions may narrow the task, but they do not override repository
rules.

Before doing any mathematical work, read:

1. AGENTS.md
2. INSTRUCTIONS.md
3. README.md
4. CONTRIBUTING.md
5. docs/pr-guard.md
6. the relevant catalog record under catalog/ by searching for the problem ID
   or title
7. the relevant problem workspace under problems/, if it exists
8. the closest matching template under templates/

Your goal is not to write a long essay or claim a full solution.
Your goal is to produce at most one checkable research object that helps the
next human, reviewer, or model continue.

Allowed research objects:

- one candidate claim
- one possible route
- one failed attempt with a clear obstruction
- one source connection
- one reproducible derivation
- one review note
- one concrete next task

If no checkable contribution is justified, say exactly:

No repository contribution is justified.

Then state the single most useful continuation task.

Working rules:

- Separate sourced facts from speculative derivation.
- Prefer equations, definitions, dependencies, gaps, and next steps over prose.
- Use short text only when it helps verification or continuation.
- Cite sources when using external material.
- State every dependency needed for the object.
- State the weakness, gap, or review risk.
- Do not include raw chat transcript text.
- Do not rewrite existing structure unless directly required.

Repository edit rules:

- Prefer one file under problems/<problem-id>/proposals/,
  problems/<problem-id>/review/, or problems/<problem-id>/refuted/.
- Use the closest template from templates/.
- If no problem workspace exists, do not invent a large one. Either make no
  repository contribution or propose the smallest useful curated object.
- Do not create a full problem workspace unless explicitly asked by a human
  maintainer.
- Do not edit problems/<problem-id>/canonical/ unless explicitly asked by a
  human maintainer.
- Do not mark your own work as llm_reviewed: true, human_reviewed: true, or
  formal_reviewed: true.

Pull request rules:

- Set the pull request body marker to:
  PR type: research
- Keep the PR scoped to one problem.
- Keep the PR scoped to one checkable research object.
- If the PR guard would fail, reduce the scope before opening the PR.
```
