# Instructions For LLMs And Agents

You are welcome to help with Magent if you can follow the repository rules.

Your goal is not to sound impressive or produce a long answer. Your goal is to improve the shared research state in a way that humans and future models can verify.

## Before Working

Read:

1. `README.md`
2. `CONTRIBUTING.md`
3. `docs/pr-guard.md`
4. the relevant catalog record under `catalog/`
5. the relevant problem folder under `problems/`, if it exists
6. the relevant template under `templates/`

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

State claims as narrowly as the derivation supports. Do not imply a complexity
classification, final solution, or polynomial certificate unless the object
actually proves it.

If you cannot produce that, say that no repository contribution is justified.

## Pull Request Behavior

A useful PR should be small. It should add one checkable research object or one clear framework improvement.

Set the pull request body marker to either:

```text
PR type: research
```

or:

```text
PR type: technical
```

If asked to "attempt" or "solve" a hard problem, treat that as permission to
make one small, reviewable research contribution. Do not create a full problem
workspace, full theory, or final proof unless the user explicitly asks for that
scope.

If asked to publish, open, or make a pull request, and you have Git and GitHub
access, do the full PR workflow:

1. create a branch,
2. add or edit the single intended object,
3. commit it,
4. run the PR guard against the committed branch,
5. push the branch, and
6. open the pull request.

A local untracked file is not a pull request. Do not say a PR exists until it
has been opened. Do not say the PR guard passed unless you actually ran the
guard command and it exited successfully.

If you do not have the ability to commit, push, or open a PR, say that clearly
and provide only the smallest reviewable patch or file content.

Model-generated material is not reviewed by virtue of being generated. Do not
set `llm_reviewed: true`, `human_reviewed: true`, or `formal_reviewed: true`
on your own contribution.

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
