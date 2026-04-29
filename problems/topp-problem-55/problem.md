---
id: topp-problem-55
title: Pallet Loading
status: active
area: packing
source_ids:
  - topp-p55
  - edemaine-topp-p000055
review:
  llm_reviewed: false
  human_reviewed: false
  formal_reviewed: false
---

# Problem

Given dimensions `(A,B)` and `(a,b)`, and a target number `n`, decide
whether `n` congruent small rectangles of size `a x b` can be packed into a
large rectangle of size `A x B`. Each small rectangle may be placed in either
axis-parallel orientation, so an item may occupy either an `a x b` box or a
`b x a` box.

# Scope

This workspace concerns the decision and complexity question for packing
identical axis-parallel rectangles with optional 90-degree rotation into one
axis-parallel container. Restricted encodings, certificate size, guillotine
patterns, exact algorithms for special cases, and obstructions to NP
membership belong here.

This workspace does not cover arbitrary non-identical rectangle packing except
as a comparison problem or as part of a sourced reduction.

# Sources

- `topp-p55`: TOPP Problem 55 page,
  `https://topp.openproblem.net/P55.html`. Used for the problem statement,
  open status, motivation, and the note that the compactly encoded problem is
  not known to be in NP.
- `edemaine-topp-p000055`: `edemaine/topp` source record `Problems/P.000055`,
  `https://github.com/edemaine/topp/blob/main/Problems/P.000055`. Used as the
  source repository record mirrored by the TOPP page.

# Known Equivalent Forms

- None added yet.

# Initial Routes

- `topp-problem-55-R0001`: isolate certificate size as a route into the
  compact-input complexity question.

# Notes

The catalog entry resolving this workspace is
`catalog/imports/topp/problems.yaml` entry `topp-problem-55`.
