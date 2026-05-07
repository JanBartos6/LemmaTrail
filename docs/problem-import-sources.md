# Problem Import Sources

Problem lists should be used carefully. A list can help discover candidate workspaces, but it should not automatically create canonical mathematical content.

## Recommended Seed Sources

See [scraping-sources.md](scraping-sources.md) for the current source tiers and scraper rules.

### Clay Mathematics Institute

- URL: https://www.claymath.org/millennium-problems/
- Role: canonical source for Millennium Prize problem names, summaries, and official problem pages
- Import mode: manual curated seed

### TOPP: The Open Problems Project

- URL: https://topp.openproblem.net/
- Source repository: https://github.com/edemaine/topp
- Role: open problem list in discrete and computational geometry
- Import mode: metadata adapter

TOPP is especially relevant because it already accepts updates through GitHub pull requests.

### Erdos Problems

- URL: https://www.erdosproblems.com/
- Role: large source of open problems associated with Paul Erdos
- Import mode: metadata adapter

This is likely one of the most useful benchmark-style sources. Use the Apache-2.0
GitHub source repository for imports, and recheck open status during curation.

### Open Problem Garden

- URL: https://www.openproblemgarden.org/
- Role: broad discovery source across many mathematical areas
- Import mode: metadata adapter later

Treat as discovery until individual problems are traced to stronger sources.

### American Institute of Mathematics Problem Lists

- URL: https://aimath.org/problemlists/
- Role: index of problem lists across many mathematical areas
- Import mode: list metadata adapter

Many entries point to PDFs or external pages, so the first adapter should collect list metadata and links only.

### Wikipedia: List Of Unsolved Problems In Mathematics

- URL: https://en.wikipedia.org/wiki/List_of_unsolved_problems_in_mathematics
- Role: discovery index only
- Import mode: do not treat as canonical

Wikipedia is useful for finding candidate problems and references, but each problem should be traced to better primary or survey sources before a workspace becomes active.

## Import Rule

Do not bulk-download problem text into `problems/`.

Use `catalog/curated-candidates.yaml` to track manually curated candidates.
Create a problem folder only after someone is ready to curate sources,
notation, and scope.
