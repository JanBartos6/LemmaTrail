# Erdos Problems Import

This directory contains metadata imported from the Apache-2.0 licensed
`teorth/erdosproblems` source repository.

The import is metadata-only. Problem statements are not copied here.

Run:

```bash
python -m pip install -r requirements.txt
python tools/import_erdos_problems.py
```

The importer checkpoints progress under `.cache/imports/erdos-problems/`, so an
interrupted run can resume without restarting the transform.
