# Repository Structure

This is the `v0.1-alpha` structure. It should change if contributors find a cleaner way to support human and AI collaboration without increasing noise.

The repository is organized around problem workspaces. Each workspace uses the same internal layout so humans and models know where to look.

```text
catalog/
  imports/               Metadata-only YAML catalogs from external sources
problems/
  _workspace-template/   Readable skeleton for new problem workspaces
  <problem-id>/
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
templates/               Reusable research-object templates
```

## Files

`problem.md` is the concise problem statement, scope, source trail, and status.

`catalog/imports/` contains imported metadata. These records are not curated
problem workspaces and should not be treated as reviewed problem statements.

`problems/_workspace-template/` is a readable skeleton copied to start a new
active problem workspace.

`templates/` contains reusable templates for individual research objects such
as claims, routes, attempts, failures, and reviews.

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

Do not bulk-create hundreds of empty folders. Use
`catalog/imports/` for candidate metadata until a workspace is needed.
