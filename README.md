# Magent

Magent is an alpha-stage, GitHub-native framework for human and AI collaboration on hard mathematical problems.

The goal is to preserve reusable progress instead of letting useful reasoning disappear inside isolated chats, notebooks, or private notes. The repository should give humans and large language models enough shared context to continue from the current frontier instead of starting over.

This project is AI-supported by design. LLMs, agents, prompt engineers, programmers, hobby mathematicians, and professional researchers are welcome to contribute if they follow the current structure and review rules.

This project is not a place for raw model transcripts or long speculative essays. It is a structured place for durable research state: problem statements, definitions, verified claims, candidate claims, failed routes, assumptions, source references, review state, and continuation points.

## Version Status

This repository is currently `v0.1-alpha`.

The structure is expected to change as the project learns what is useful. The current files are working rules and guardrails, not final governance. Contributions that improve the framework itself are welcome, but changes should stay small, explicit, and easy to review.

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

## Trust Model

LLMs may propose, triage, and review. Humans decide what becomes canonical.

```yaml
llm_reviewed: true
human_reviewed: false
status: needs-review
```

The example above is not verified research state. It means an LLM review did not find an obvious issue, but a human still needs to check it.

## LLM And Agent Contributions

LLM-generated work is welcome when it is useful, structured, and reviewable.

Accepted LLM-assisted contributions should normally arrive as pull requests or review comments using the repository templates. A model may propose a claim, route, failed attempt, source connection, derivation, or continuation point. It should not rewrite large parts of the repository, submit raw transcripts, or present unverified work as proven.

Pull requests or comments that do not follow the current format will not be merged. The format can evolve, but unstructured output should not become repository state.

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

Licensing should be decided before public launch. See [docs/licensing-notes.md](docs/licensing-notes.md).
