# Catalog

This directory contains compact YAML metadata for problem discovery.

Current catalog data:

- `source-registry.yaml`: source and provenance policy for imported or cited
  problem lists.
- `curated-candidates.yaml`: manually curated candidate problems that are not
  active workspaces yet.
- `imports/erdos-problems/problems.yaml`: unresolved Erdos problem records imported
  from the Apache-2.0 licensed `teorth/erdosproblems` source repository.
- `imports/topp/problems.yaml`: unresolved-like TOPP problem metadata imported
  from the public `edemaine/topp` source repository.
- `imports/aim-problem-lists/problem-lists.yaml`: AIM list-of-lists metadata.
  These are source lists, not individual problem records.

Catalog files are discovery metadata, not active problem workspaces. Active
workspaces live under `problems/`. Catalog records are meant to be read
directly by humans, tools, and models.

Do not generate one Markdown file per problem unless the repository later needs
a separate presentation layer. The preferred public artifact is YAML.
