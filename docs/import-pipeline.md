# Import Pipeline

Imports should discover candidate problems. They should not create trusted mathematical content.

## Rule

Importers may write to `catalog/`. They must not write directly to `problems/<problem-id>/canonical/`.

## Recommended Flow

```text
external source
  -> catalog/source-registry.yaml
  -> catalog/seed-problems.yaml
  -> human curation
  -> problems/<problem-id>/ problem workspace
  -> proposals/
  -> review/
  -> canonical/
```

## Why

Problem lists often mix statuses, levels of difficulty, outdated statements, and secondary descriptions. Bulk importing them into active problem folders would make the repository look more authoritative than it is.

## Future Scraper Contract

Any future scraper should output small records:

```yaml
id: candidate-problem-id
title: Problem title
area: unknown
status: open
source_ids:
  - source-id
primary_sources:
  - title: Source title
    url: https://example.org/problem
    type: official | survey | database | paper | wiki | unknown
imported_at: YYYY-MM-DD
workspace_status: not-created
curation_status: seed-only
```

The scraper should not import full pages, long prose, images, or generated explanations.

See [scraping-sources.md](scraping-sources.md) for source tiers and adapter order.
