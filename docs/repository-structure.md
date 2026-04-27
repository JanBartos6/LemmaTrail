# Repository Structure

This is the `v0.1-alpha` structure. It should change if contributors find a cleaner way to support human and AI collaboration without increasing noise.

The repository is organized around problem workspaces. Each workspace uses the same internal layout so humans and models know where to look.

```text
problems/<problem-id>/
  problem.md
  glossary.md
  graph.yaml
  references.bib
  canonical/
    definitions.md
    known-results.md
    verified-claims/
  proposals/
    claims/
    routes/
    attempts/
  review/
    llm-triage/
    human-review/
  refuted/
  tasks.md
```

## Files

`problem.md` is the concise problem statement, scope, source trail, and status.

`glossary.md` defines local notation. Avoid redefining notation inside claims unless the claim needs local temporary notation.

`graph.yaml` stores IDs and dependency edges. It should stay small and machine-readable.

`references.bib` stores bibliographic references used by the problem workspace.

`canonical/` stores reviewed definitions, known results, and verified claims.

`proposals/` stores unverified work. Most PRs should start here.

`review/` stores LLM triage and human review notes.

`refuted/` stores false claims, counterexamples, invalid routes, and useful dead ends.

`tasks.md` stores concrete continuation points.

## When To Create A New Problem Folder

Create a problem folder only when at least one contributor is ready to curate it.

Do not bulk-create hundreds of empty folders. Use `catalog/seed-problems.yaml` for candidate problems until a workspace is needed.
