# LemmaTrail

LemmaTrail is an alpha-stage, GitHub-native framework for human and AI collaboration on hard mathematical problems.

The goal is to preserve reusable progress instead of letting useful reasoning disappear inside isolated chats, notebooks, or private notes. The repository should give humans and large language models enough shared context to continue from the current frontier instead of starting over.

This project is AI-supported by design. LLMs, agents, prompt engineers, programmers, hobby mathematicians, and professional researchers are welcome to contribute if they follow the current structure and review rules.

This project is not a place for raw model transcripts or long speculative essays. It is a structured place for durable research state: problem statements, definitions, verified claims, candidate claims, failed routes, assumptions, source references, review state, and continuation points.

## What You Can Contribute In 10 Minutes

- add one precise source connection
- record one failed route and its obstruction
- add one concrete next task for a problem
- review one claim for a gap
- convert one chat result into a checkable object

## For LLMs And Agents

If you are using a model or coding agent, start here:

- [MODEL_PROMPT.md](MODEL_PROMPT.md) for the copy-paste prompt to give a model.
- [INSTRUCTIONS.md](INSTRUCTIONS.md) for the required model-facing workflow.
- [AGENTS.md](AGENTS.md) for the repository entry point used by coding agents.

## Version Status

This repository is currently `v0.1-alpha`.

The structure is expected to change as the project learns what is useful. The current files are working rules and guardrails, not final governance. Contributions that improve the framework itself are welcome, but changes should stay small, explicit, and easy to review.

## License

Original LemmaTrail code, documentation, templates, and research objects are
licensed under the MIT License. See [LICENSE.md](LICENSE.md). External sources
and imported metadata keep their own terms; see
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Credit

Git history records commits, and research objects should preserve visible
credit for authors, reviewers, source-finders, and curators when practical.
AI tools must be disclosed, but they are not credited as authors. See
[CONTRIBUTORS.md](CONTRIBUTORS.md).

## Core Rule

Every contribution must make the next human, reviewer, or model better positioned to continue.

Accepted contributions should add at least one of:

- a precise problem statement
- a sourced definition or known result
- a candidate claim with derivation
- a verified claim with review evidence
- a refutation or counterexample
- a failed path with a clear obstruction
- a concrete next task
- a useful reference

See [docs/example-research-object.md](docs/example-research-object.md) for a
small mergeable contribution shape.

## Trust Model

LLMs may propose, triage, and review. Humans decide what becomes canonical.

```yaml
llm_reviewed: true
human_reviewed: false
status: needs-review
```

The example above is not verified research state. It means an LLM review did not find an obvious issue, but a human still needs to check it.

## How Contributions Become Repository State

Durable contributions enter LemmaTrail through pull requests.

Issues, comments, and external discussions are welcome for proposing ideas,
asking questions, reporting gaps, or giving feedback. But if something should
become part of the repository's research state, it must be converted into a
checkable research object using the repository templates and merged through a
pull request.

This applies to both human and LLM-assisted contributions.

Pull requests that do not follow the current format will not be merged. The
format can evolve, but unstructured output should not become repository state.

## LLM And Agent Contributions

LLM-assisted work is welcome when it is useful, structured, and reviewable.

A model may help propose a claim, route, failed attempt, source connection,
derivation, review note, or continuation point. It should not rewrite large
parts of the repository, submit raw transcripts, or present unverified work as
proven.

LLM-assisted contributions follow the same repository rules as human
contributions: durable work must become a templated research object and enter
through a pull request.

See [INSTRUCTIONS.md](INSTRUCTIONS.md) for the current model-facing workflow.
For a copy-paste prompt to give a model or agent, see [MODEL_PROMPT.md](MODEL_PROMPT.md).

Future versions may support richer agent workflows, benchmarks, automated triage, or a website. For now, the source of truth is the GitHub repository and its review history.

## Repository Map

```text
catalog/                 Candidate sources and imported YAML problem metadata
docs/                    Project rules, status model, source policy, text policy
problems/                Problem workspaces
  _template/             Copy this folder to start a new problem
templates/               Reusable contribution templates
.github/                 PR and issue templates
AGENTS.md                Entry point for coding agents
INSTRUCTIONS.md          Short workflow for LLMs and agents
MODEL_PROMPT.md          Copy-paste prompt for model-assisted contributions
CONTRIBUTORS.md          Credit and recognition policy
LICENSE.md              Project license summary
THIRD_PARTY_NOTICES.md   External source notice policy
```

See [docs/repository-structure.md](docs/repository-structure.md) for the full structure.
See [docs/import-pipeline.md](docs/import-pipeline.md) before adding any scraper or source adapter.
See [docs/pr-guard.md](docs/pr-guard.md) for pull request shape rules.

## Current Scope

The first public version should stay intentionally small:

- no website yet
- no generated files
- no raw chat logs
- no automatic import into canonical problem files
- no LLM-authored canonical claims
- no bulk-created empty problem folders

Problem lists may be seeded from reliable public sources, but each actual problem folder should be curated manually before it becomes active.

See [docs/licensing-notes.md](docs/licensing-notes.md) before copying external material.
