# Contributing

LemmaTrail is designed to stay readable for mathematicians and usable by models. Human and AI-assisted contributions are welcome only when they improve the research state.

This is a `v0.1-alpha` project. The rules below are current guardrails, not final governance. They exist to keep the repository reviewable while the format evolves.

## Contribution Types

Use the smallest matching template from `templates/`:

- `problem.md` for a new problem workspace
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

Research PRs are intentionally strict: one PR should normally add or edit one
checkable research object. Technical PRs may edit infrastructure, but they must
not edit active problem workspaces.

Before opening a PR:

- [ ] The contribution has a stable ID.
- [ ] The status is one of the allowed statuses.
- [ ] Every dependency is listed.
- [ ] Every source is listed, or the derivation is reproducible.
- [ ] Any AI assistance is disclosed.
- [ ] The gap or weakness is stated.
- [ ] The next continuation point is concrete.
