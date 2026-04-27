# Problem Import Sources

Problem lists should be used carefully. A list can help discover candidate workspaces, but it should not automatically create canonical mathematical content.

## Recommended Seed Sources

### Clay Mathematics Institute

- URL: https://www.claymath.org/millennium-problems/
- Role: canonical source for Millennium Prize problem names, summaries, and official problem pages
- Import mode: manual curated seed

### TOPP: The Open Problems Project

- URL: https://topp.openproblem.net/
- Source repository: https://github.com/edemaine/topp
- Role: open problem list in discrete and computational geometry
- Import mode: curated adapter later

TOPP is especially relevant because it already accepts updates through GitHub pull requests.

### Wikipedia: List Of Unsolved Problems In Mathematics

- URL: https://en.wikipedia.org/wiki/List_of_unsolved_problems_in_mathematics
- Role: discovery index only
- Import mode: do not treat as canonical

Wikipedia is useful for finding candidate problems and references, but each problem should be traced to better primary or survey sources before a workspace becomes active.

## Import Rule

Do not bulk-download problem text into `problems/`.

Use `catalog/seed-problems.yaml` to track candidates. Create a problem folder only after someone is ready to curate sources, notation, and scope.

