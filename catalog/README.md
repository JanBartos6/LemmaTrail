# Catalog

This directory contains compact YAML metadata for problem discovery.

Current catalog data:

- `imports/erdos-problems/problems.yaml`: unresolved Erdős problem records imported from the Apache-2.0 licensed `teorth/erdosproblems` source repository.
- `imports/topp/problems.yaml`: TOPP problem metadata imported from the public `edemaine/topp` source repository.
- `imports/aim-problem-lists/problem-lists.yaml`: AIM list-of-lists metadata. These are source lists, not individual problem records.

Catalog files are discovery metadata, not active problem workspaces. Active workspaces live under `problems/`.

Imported catalog records are not reviewed problem statements. They are starting
points for creating or finding active workspaces.

Catalog records are meant to be read directly by humans, tools, and models. For the catalog layer, YAML is the preferred source format.

Do not generate one Markdown file per catalog problem unless the repository later needs a separate presentation layer.
