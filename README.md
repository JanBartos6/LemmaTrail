# Magent

Magent is a GitHub-native research ledger for hard mathematical problems.

The goal is to preserve reusable progress instead of letting useful reasoning disappear inside isolated chats, notebooks, or private notes. The repository tracks problem statements, definitions, verified claims, candidate claims, failed routes, assumptions, source references, review state, and continuation points.

This project is not a place for raw model transcripts or long speculative essays. It is a structured place for durable research state.

## Core Rule

Every contribution must make the next reviewer or model better positioned to continue.

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

## Repository Map

```text
catalog/                 Candidate problem sources and seed problem index
docs/                    Project rules, status model, source policy, text policy
problems/                Problem workspaces
  _template/             Copy this folder to start a new problem
templates/               Reusable contribution templates
.github/                 PR and issue templates
```

See [docs/repository-structure.md](docs/repository-structure.md) for the full structure.
See [docs/import-pipeline.md](docs/import-pipeline.md) before adding any scraper or source adapter.

## Current Scope

The first public version should stay intentionally small:

- no website yet
- no generated files
- no raw chat logs
- no automatic import into canonical problem files
- no LLM-authored canonical claims

Problem lists may be seeded from reliable public sources, but each actual problem folder should be curated manually before it becomes active.

Licensing should be decided before public launch. See [docs/licensing-notes.md](docs/licensing-notes.md).
