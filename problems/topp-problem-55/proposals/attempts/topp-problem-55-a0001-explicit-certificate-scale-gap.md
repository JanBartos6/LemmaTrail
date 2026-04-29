---
id: topp-problem-55-a0001
type: attempt
status: blocked
route_ids: []
depends_on:
  - topp-problem-55-c0001
source_ids:
  - topp-p55
ai_assistance:
  used: true
  model: GPT-5 Codex
  role: obstruction-analysis
review:
  llm_reviewed: false
  human_reviewed: false
  formal_reviewed: false
---

# Objective

Test whether the explicit certificate used for the unary-\(n\) variant in
`topp-problem-55-c0001` also proves NP membership for the compact binary-\(n\)
TOPP problem.

# Distilled Attempt

1. Use the certificate from `topp-problem-55-c0001`: list every rectangle's
   orientation and coordinates, and list one separation relation for every
   pair of rectangles.
   This gives a direct polynomial verifier once the list is present.

2. Let the original input use binary integer encodings. Then the input length is
   \(O(\log A+\log B+\log a+\log b+\log n)\), up to encoding constants.

3. The explicit certificate has at least one orientation bit for each rectangle,
   hence length \(\Omega(n)\), before coordinates or pairwise relations are
   counted.

4. For an input with \(n=2^k\), the contribution of \(n\) to the input length is
   \(O(k)\), but the explicit orientation list already has length
   \(\Omega(2^k)\).

# Result

The explicit-placement certificate route is polynomial for unary \(n\), but by
itself it does not prove NP membership for the compact binary-\(n\) version
recorded in TOPP Problem 55.

# Gap Or Failure Point

This only rules out the uncompressed explicit-certificate argument. It does not
rule out a polynomial-size compressed certificate, a structural normal form, or
a different complexity classification.

# Next Step

Search for, or derive, a compressed certificate format whose size is polynomial
in the binary input length. The source-listed guillotine-pattern result and the
Nelissen report should be checked first because TOPP lists them under related
results and appearances for this problem.
