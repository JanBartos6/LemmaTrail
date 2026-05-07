# Contributing

LemmaTrail is designed to stay readable for mathematicians and usable by
models. Human and AI-assisted contributions are welcome when they leave behind
a checkable object that helps the next contributor continue.

This is a `v0.1-alpha` project. The rules below are current guardrails, not final governance. They exist to keep the repository reviewable while the format evolves.

Durable repository changes happen through pull requests. Issues and comments
are welcome for proposals, questions, and feedback, but research state enters
the repository only after it is converted into a template-based file and merged
through a PR.

This applies to both humans and LLMs.

## Contribution Types

For a new problem workspace, copy `problems/_workspace-template/`.

For individual research objects, use the smallest matching template from
`templates/`:

- `claim.md` for a precise claim, lemma, or reduction
- `route.md` for a major approach
- `attempt.md` for distilled reasoning attempts
- `failure.md` for dead ends and obstructions
- `review.md` for LLM or human review notes

## Required Standard

Every mathematical contribution must include either:

1. a precise source, or
2. a derivation detailed enough that another reviewer can reproduce the reasoning.

If neither is present, the contribution should stay outside the repository.

## Canonical vs Proposal

Canonical files contain reviewed project state.

Proposal files contain unverified work.

Contributors should normally add or edit files under:

```text
problems/<problem-id>/proposals/
problems/<problem-id>/review/
problems/<problem-id>/refuted/
```

Do not move material into `canonical/` unless the PR is explicitly approved for that purpose.

## Continuing Or Branching

Continue an existing research object when the PR strengthens, corrects, or
extends the same line of reasoning.

Create a new research object when the PR starts an independent route, uses an
incompatible assumption, or branches from an earlier step while ignoring later
steps. In that case, list the original object in `depends_on` and state the
branch point in the body.

Use simple step anchors such as `Step A1`, `Step A2`, and `Step A3` when a
claim or attempt may need later continuation.

## AI-Assisted Contributions

AI assistance is allowed, but it must be disclosed in frontmatter:

```yaml
ai_assistance:
  used: true
  model: unknown
  role: proposed-derivation
```

Do not include raw model transcripts. Distill the useful mathematical state into the required template.

LLMs and agents should also follow [INSTRUCTIONS.md](INSTRUCTIONS.md).

## Credit And Recognition

Git history records commits. Research objects should also credit mathematical
authors, reviewers, source-finders, and curators in frontmatter when practical.

Maintainers may curate an issue, comment, or model output into template form,
but should preserve visible human credit for the useful contribution.

AI tools must be disclosed in `ai_assistance`, but they are tools, not authors.

Do not add reputation-seeking edits that do not improve research state.

## Text Policy

Text is allowed only when it serves verification or continuation. See [docs/text-policy.md](docs/text-policy.md).

Do not submit:

- raw LLM transcripts
- long essays
- vague intuition without a statement
- duplicate background
- reputation-seeking edits
- prose-only speculation
- rewrites that do not add mathematical state

## Pull Request Checklist

Before opening a PR, leave the `PR type:` marker in the pull request body.

- Use `PR type: research` for problem proposals, reviews, failures, claims, routes, and tasks.
- Use `PR type: technical` for tooling, documentation, templates, catalog imports, CI, or repository policy.

Research PRs are intentionally strict about scope: one PR must stay within one
problem workspace. It may include multiple connected, checkable research
objects when each one improves the review state. Technical PRs may edit
infrastructure, but they must not edit active problem workspaces.

Before opening a PR:

- [ ] The contribution has a stable ID.
- [ ] The status is one of the allowed statuses in [docs/status-levels.md](docs/status-levels.md).
- [ ] Dependencies are listed, or the object explicitly says there are none.
- [ ] Every source is listed, or the derivation is reproducible.
- [ ] AI assistance is disclosed in every research object.
- [ ] The gap, weakness, or limitation is stated when applicable.
- [ ] The next continuation point is concrete.

For agents with repository access, a PR is not complete until the branch is
committed, pushed, and opened on GitHub. Do not describe an untracked or
uncommitted local file as a pull request.
