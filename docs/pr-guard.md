# PR Guard

The PR guard checks repository shape. It does not decide whether mathematics is
correct.

## PR Types

Every pull request is treated as one of these types:

- `research`: mathematical or research-state contribution
- `technical`: tooling, documentation, templates, catalog import, CI, or policy

The default is `research`.

Set the pull request type in the PR body:

```text
PR type: research
```

or:

```text
PR type: technical
```

Maintainers can bypass the guard with the `maintainer-override` or
`pr-guard: override` label.

## Research PR Rules

A research PR may touch only one active problem workspace.

It may add or edit one or more research objects for that problem:

- `problems/<problem-id>/problem.md`
- `problems/<problem-id>/tasks.md`
- `problems/<problem-id>/proposals/**/*.md`
- `problems/<problem-id>/review/**/*.md`
- `problems/<problem-id>/refuted/**/*.md`

It may also update support files for the same problem:

- `problems/<problem-id>/graph.yaml`
- `problems/<problem-id>/references.bib`

Research PRs may not edit:

- `problems/<problem-id>/canonical/**`
- `tools/**`
- `docs/**`
- `templates/**`
- `.github/**`
- `catalog/**`

## Technical PR Rules

A technical PR may edit infrastructure paths:

- `.github/**`
- `tools/**`
- `docs/**`
- `templates/**`
- `catalog/**`
- root policy files such as `README.md`, `CONTRIBUTING.md`, and `INSTRUCTIONS.md`
- root prompt files such as `MODEL_PROMPT.md`
- `problems/_template/**`

Technical PRs may not edit active problem workspaces under
`problems/<problem-id>/`.

## Global Blocks

Unless a maintainer override label is present, the guard blocks:

- binary/blob files such as PDFs, images, videos, archives, Word files, and spreadsheets
- raw chat transcript markers such as `User:` or `Assistant:`
- added `llm_reviewed: true`, `human_reviewed: true`, or `formal_reviewed: true`
- research objects missing `ai_assistance:` frontmatter
- research objects using statuses outside `docs/status-levels.md`
- oversized files

These checks are intentionally conservative. If a valid PR needs an exception,
ask a maintainer to split the PR or apply an override label.
