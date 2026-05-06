---
id: topp-problem-55-c0001
type: claim
status: proposed
evidence_type: derivation
route_ids: []
depends_on: []
source_ids:
  - topp-p55
ai_assistance:
  used: true
  model: GPT-5 Codex
  role: proposed-derivation
review:
  llm_reviewed: false
  human_reviewed: false
  formal_reviewed: false
---

# Statement

Assume \(A,B,a,b\) are positive rational numbers encoded in binary and \(n\) is
encoded in unary. The corresponding axis-parallel pallet loading decision
problem is in NP.

# Dependencies

- `topp-p55`: source for the pallet loading problem and the compact-input
  difficulty in the original version.
- The rational linear-feasibility certificate bound derived below.

# Derivation

1. For each rectangle \(i\in\{1,\ldots,n\}\), a certificate may list an
   orientation \(o_i\in\{(a,b),(b,a)\}\) and rational lower-left coordinates
   \((x_i,y_i)\).
   This fixes the width \(w_i\) and height \(h_i\) of each rectangle.

2. For each unordered pair \(i<j\), the certificate may also list one selected
   separation relation from:
   \(x_i+w_i\le x_j\), \(x_j+w_j\le x_i\), \(y_i+h_i\le y_j\), or
   \(y_j+h_j\le y_i\).
   Two closed axis-parallel rectangles with disjoint interiors satisfy at least
   one of these four weak separations.

3. The verifier checks the boundary inequalities
   \(0\le x_i\), \(0\le y_i\), \(x_i+w_i\le A\), \(y_i+h_i\le B\), and the
   selected pairwise separation inequalities.
   These checks are polynomial in the certificate bit length.

4. Conversely, any valid packing determines orientations, coordinates, and at
   least one true separation relation for each pair, so the certificate format
   is complete for explicit \(n\)-rectangle packings.

5. Fix any orientation and pairwise-separation choices. The remaining
   coordinate conditions form a bounded rational polyhedron in \(2n\) variables.
   If it is nonempty, it has a rational vertex. After clearing denominators in
   the input coefficients, Cramer's rule expresses each vertex coordinate as a
   quotient of determinants of integer matrices of dimension at most \(2n\).
   Hadamard's determinant bound gives numerator and denominator bit lengths
   polynomial in \(n\) and in the input numeric bit length.

6. The certificate therefore has \(O(n)\) orientation bits, \(O(n^2)\) pairwise
   relation choices, and \(O(n)\) rational coordinates of polynomial bit length.
   Because \(n\) is unary, this certificate length is polynomial in the input
   length, and verification is polynomial.

# Gap

This does not address the TOPP problem with compact binary \(n\). With binary
\(n\), the explicit orientation, coordinate, and pairwise-relation lists can be
exponential in the input length.

# Next Step

Look for a source-backed or derived normal form that compresses valid packings
to size polynomial in \(\log n\), or prove such a form for a restricted subclass
such as guillotine patterns.
