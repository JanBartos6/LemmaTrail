---
id: topp-problem-55-C0001
type: claim
status: proposed
evidence_type: derivation
route_ids:
  - topp-problem-55-R0001
depends_on:
  - topp-problem-55
source_ids:
  - topp-p55
ai_assistance:
  used: true
  model: OpenAI Codex GPT-5
  role: proposed-derivation
review:
  llm_reviewed: false
  human_reviewed: false
  formal_reviewed: false
---

# Statement

Assume `A`, `B`, `a`, and `b` are rational numbers encoded in binary and
`n` is encoded in unary. Under that encoding, the pallet-loading decision
problem is in NP.

This does not claim NP membership for the compact binary-encoded-`n` version
described by TOPP Problem 55.

# Dependencies

- `topp-p55`: source statement of the pallet-loading decision problem and its
  note that compact input leaves NP membership open.
- Standard rational-polytope fact: a nonempty bounded polyhedron described by
  rational linear inequalities has a rational feasible point whose bit length
  is polynomial in the coefficient bit length and the number of inequalities.

# Derivation

1. For a unary input value `n = N`, a certificate can list, for each rectangle
   `i = 1,...,N`, an orientation bit and rational lower-left coordinates
   `(x_i,y_i)`.

2. Given such a certificate, a verifier computes the rectangle dimensions
   `(w_i,h_i)`, where `(w_i,h_i)` is either `(a,b)` or `(b,a)`, and checks
   containment:

   ```text
   0 <= x_i, 0 <= y_i, x_i + w_i <= A, y_i + h_i <= B.
   ```

   For each pair `i != j`, it also checks that at least one of the four
   separating inequalities holds:

   ```text
   x_i + w_i <= x_j,
   x_j + w_j <= x_i,
   y_i + h_i <= y_j,
   y_j + h_j <= y_i.
   ```

   These are rational comparisons, and there are `O(N^2)` of them. Since `N`
   is unary, this verification count is polynomial in the input length and in
   the listed coordinate bit lengths.

3. It remains to justify that a yes instance has a polynomial-size rational
   coordinate certificate whenever it has any real-coordinate packing. Fix a
   feasible real packing. For each pair of rectangles, choose one separating
   inequality from the four displayed above that is true in that packing.
   Together with the containment inequalities and the fixed orientations,
   these choices form a finite rational linear inequality system in the
   coordinate variables.

4. The coordinate variables are bounded by the containment inequalities, so
   the feasible region of that chosen linear system is a nonempty bounded
   rational polyhedron. A vertex of this polyhedron is determined by a square
   subsystem of tight rational linear inequalities. By Cramer's rule, its
   coordinates have numerator and denominator bit length polynomial in the
   number of variables, the number of inequalities, and the bit lengths of
   `A`, `B`, `a`, and `b`.

5. Therefore every real yes instance under the unary-`n` encoding has a
   polynomial-size rational certificate, and the verifier in steps 1-2 places
   this encoded problem in NP.

# Gap

The argument uses an explicit coordinate record for every rectangle. It is
therefore polynomial only when `n` is unary, or otherwise bounded polynomially
by the input length. It does not address the source problem's compact encoding
obstruction, where binary `n` can be exponentially larger than the written
input.

# Next Step

Investigate whether binary-encoded yes instances always admit polynomial-size
compressed certificates, such as periodic pattern descriptions or other
run-length encodings, or whether there are families where all natural
certificates appear to require listing Theta(n) local placement data.
