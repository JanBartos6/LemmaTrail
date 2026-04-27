# Scraping Sources

This document lists candidate sources for building the problem catalog.

The first importer should collect metadata only. It should not copy long descriptions, PDF text, abstracts, or full problem statements into this repository.

## Import Tiers

### Tier 1: Best Starting Sources

These sources are useful enough to justify dedicated adapters.

- `clay-millennium`: official, small, manually curated
- `topp`: structured computational geometry list with a GitHub source repo
- `erdos-problems`: large database of Erdos problems with open-status pages
- `open-problem-garden`: broad open-problem wiki across many areas
- `aim-problem-lists`: list-of-lists maintained by the American Institute of Mathematics

### Tier 2: Discovery Sources

These sources are useful for finding candidates, but not for canonical imports.

- `wikipedia-unsolved-math`
- `wikipedia-unsolved-cs`
- `mathworld-unsolved`
- `oeis-open-problems`
- `west-graph-theory-combinatorics`
- `arxiv-open-problem-papers`

### Tier 3: Link-Only Sources

These sources may have copyright or maintenance issues. Use links and independently written metadata only.

- `openproblems-math-physics`

## Metadata-Only Record

Every scraper should output records shaped like this:

```yaml
id: stable-slug
title: Standard problem name
area: unknown
status: open
summary: Optional one-sentence original summary.
source_ids:
  - source-id
primary_sources:
  - title: Source title
    url: https://example.org/problem
    type: official | survey | database | paper | wiki | unknown
introduced:
  year: unknown
  by: []
prize:
  exists: false
workspace_status: not-created
curation_status: seed-only
```

## Scraper Rules

- Scrapers may write to `catalog/`.
- Scrapers must not write directly to `problems/<problem-id>/canonical/`.
- Scrapers should preserve source URLs.
- Scrapers should store source IDs, not copied source text.
- Scrapers should mark status as `unknown` when open status is not clear.
- Scrapers should prefer many small metadata records over a few large documents.
- Scrapers should include an `imported_at` date once automated imports exist.

## First Implementation Order

1. Clay manual seed
2. Erdos Problems metadata adapter
3. TOPP metadata adapter
4. Open Problem Garden metadata adapter
5. AIM list index adapter
6. Wikipedia discovery adapter

This order gives a mix of famous problems, structured specialist problems, and broad discovery without making the repository heavy.

## Existing Adapters

### Erdos Problems

Script: `tools/import_erdos_problems.py`

Source: `https://github.com/teorth/erdosproblems`

Output: `catalog/imports/erdos-problems/problems.yaml`

The adapter imports unresolved source records by default. It uses the Apache-2.0
licensed GitHub source repository instead of crawling `erdosproblems.com`
directly.

Resume behavior:

- source clone: `.cache/sources/erdosproblems/`
- checkpoints: `.cache/imports/erdos-problems/<scope>/records.jsonl`
- state: `.cache/imports/erdos-problems/<scope>/state.json`
- final output is written only after all selected records are transformed

## Source Review Checklist

Before adding an adapter:

- [ ] Check whether robots.txt allows access.
- [ ] Check license or terms.
- [ ] Identify whether pages are stable enough to cite.
- [ ] Decide which fields are allowed.
- [ ] Confirm that the adapter produces metadata only.
- [ ] Add the source to `catalog/source-registry.yaml`.
