---
id: p-vs-np-r0001
type: route
status: proposed
depends_on:
  - p-vs-np-c0001
source_ids:
  - cook-2000-pvsnp
  - razborov-rudich-1997-natural-proofs
  - baker-gill-solovay-1975-relativization
  - aaronson-wigderson-2009-algebrization
authors:
  - name: Jan Bartos
    github: JanBartos6
    role: requester
contributors: []
reviewers: []
curators: []
ai_assistance:
  used: true
  model: GPT-5.5 Thinking
  role: proposed-route
review:
  llm_reviewed: false
  human_reviewed: false
  formal_reviewed: false
---

# Route

Subcube-cover orientation route for 3-UNSAT.

# Core Idea

Represent 3-UNSAT as the question whether selected codimension-3 subcubes cover
\(\{0,1\}^n\). Then try to prove that any small unrestricted circuit deciding
this cover predicate yields a small cover-search protocol that, given a cover
and an assignment, finds a selected clause falsified by that assignment. A lower
bound for the cover-search protocol, combined with such an orientation
transfer, would imply a circuit lower bound for the cover predicate and
therefore \(P\ne NP\).

# Dependencies

- `p-vs-np-c0001`: defines \(CCF_n\) and proves that a super-polynomial circuit
  lower bound for it implies \(P\ne NP\).

# Candidate Claims

- `p-vs-np-c0001`: 3-UNSAT is equivalent to codimension-3 subcube cover.

# Known Obstructions

- A monotone lower bound alone is not enough: some monotone functions in \(P\)
  have large monotone circuits, so any transfer from general circuits to
  monotone or cover-oriented protocols must use special structure of \(CCF_n\).
- A truth-table-large, efficiently checkable lower-bound property risks falling
  under the natural-proofs barrier.
- A purely oracle-style or black-box simulation argument risks relativization.
- A proof using only low-degree extensions risks algebrization.

# Gap

The missing lemma is the orientation transfer:

\[
\text{small unrestricted circuits for } CCF_n
\Rightarrow
\text{small cover-search protocols for } CCF_n.
\]

No proof of this transfer is currently known in this workspace.

# Next Step

Define the exact cover-search protocol model and test the orientation transfer
on restricted circuit classes first, such as monotone circuits, formulas,
AC\(^0\), or bounded-depth threshold circuits.
