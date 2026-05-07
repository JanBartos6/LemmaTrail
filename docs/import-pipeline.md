# Import Pipeline

Imports should discover candidate problems. They should not create trusted mathematical content.

## Rule

Importers may write to `catalog/`. They must not write directly to `problems/<problem-id>/canonical/`.

## Recommended Flow

```text
external source
  -> catalog/source-registry.yaml
  -> catalog/imports/<source-id>/
  -> human curation
  -> problems/<problem-id>/ problem workspace
  -> proposals/
  -> review/
  -> canonical/
```

## Why

Problem lists often mix statuses, levels of difficulty, outdated statements,
and secondary descriptions. `catalog/source-registry.yaml` records source and
provenance policy, and `catalog/imports/` stores imported metadata. Bulk
importing records into active problem folders would make the repository look
more authoritative than it is.

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

## Resume Behavior

Importers that process many records should checkpoint outside the committed
catalog, usually under `.cache/imports/<source-id>/`.

The final catalog file should be written atomically after the selected records
are complete. This keeps committed catalog files valid even when an import is
interrupted.
