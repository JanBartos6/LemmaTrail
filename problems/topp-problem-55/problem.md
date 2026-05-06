---
id: topp-problem-55
title: Pallet Loading
status: proposed
area: packing
source_ids:
  - topp-p55
  - topp-source-p000055
ai_assistance:
  used: true
  model: GPT-5 Codex
  role: workspace-curation-and-derived-claim
review:
  llm_reviewed: false
  human_reviewed: false
  formal_reviewed: false
---

# Problem

Determine the complexity of the pallet loading decision problem: given finite
numeric inputs \(A,B,a,b,n\), decide whether \(n\) axis-parallel copies of an
\(a \times b\) rectangle, each allowed either orientation, can be packed without
overlap in an \(A \times B\) rectangle.

# Scope

This workspace is for the complexity of the compactly encoded rectangular
packing problem in TOPP Problem 55. Work here should keep separate:

- source-backed facts about the TOPP problem record;
- derived claims about variants such as unary \(n\), integer inputs, rational
  inputs, guillotine restrictions, or certificate formats;
- speculative routes toward the compact binary-\(n\) problem.

Out of scope unless used as a direct comparison: non-axis-parallel packing,
maximal unit-square packing in simple polygons, and implementation-only pallet
loading heuristics.

# Sources

- `topp-p55`: TOPP Problem 55 page, used for the title, statement, open status,
  compact-input warning, and listed related references.
- `topp-source-p000055`: source repository record for TOPP `Problems/P.000055`,
  used to cross-check the imported catalog entry.

# Known Equivalent Forms

- None curated yet.

# Initial Routes

- No route object is curated yet. See `topp-problem-55-c0001` and
  `topp-problem-55-a0001` for the initial explicit-certificate boundary.

# Notes

The TOPP page records the problem as open and says the original compact-input
version is not known to be in NP. Claims in this workspace should not treat
membership in NP, NP-hardness, or earlier appearance claims as established
without a checked source or a reproducible derivation.
