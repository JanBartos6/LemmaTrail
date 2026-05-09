---
id: p-vs-np-c0001
type: claim
status: proposed
evidence_type: derivation
route_ids:
  - p-vs-np-r0001
depends_on:
  - p-vs-np
source_ids:
  - cook-2000-pvsnp
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
  role: proposed-derivation
review:
  llm_reviewed: false
  human_reviewed: false
  formal_reviewed: false
---

# Statement

For each \(n\), let \(\mathcal C_n\) be the set of all signed 3-clauses on
three distinct variables from \(x_1,\ldots,x_n\). For
\(z \in \{0,1\}^{\mathcal C_n}\), define

\[
F_z = \bigwedge_{C : z_C = 1} C.
\]

For each clause \(C\), let \(Q_C \subseteq \{0,1\}^n\) be the codimension-3
subcube of assignments that falsify \(C\). Then

\[
F_z \text{ is unsatisfiable}
\quad\Longleftrightarrow\quad
\bigcup_{C:z_C=1} Q_C = \{0,1\}^n.
\]

Consequently, the Boolean function

\[
CCF_n(z)=1 \iff F_z \text{ is unsatisfiable}
\]

is monotone. If the family \(CCF_n\) requires super-polynomial-size
unrestricted Boolean circuits as a function of
\(N = |\mathcal C_n| = 8\binom n3\), then \(P \ne NP\).

# Dependencies

- `cook-2000-pvsnp`: standard NP-completeness of 3-SAT and the fact that
  polynomial-time decidability gives polynomial-size circuit families.

# Derivation

## Step C1

Each signed 3-clause \(C\) is falsified by exactly one assignment to its three
variables.

Short justification: a disjunction of three literals is false exactly when all
three literals are false.

## Step C2

The set of global assignments falsifying \(C\) is a codimension-3 subcube
\(Q_C\subseteq\{0,1\}^n\).

Short justification: the three variables of \(C\) are fixed to their unique
falsifying values, while the remaining \(n-3\) variables are free.

## Step C3

An assignment \(\alpha\in\{0,1\}^n\) satisfies \(F_z\) iff
\(\alpha\notin\bigcup_{C:z_C=1}Q_C\).

Short justification: \(\alpha\) satisfies the conjunction iff it falsifies none
of the selected clauses.

## Step C4

Therefore \(F_z\) is unsatisfiable iff the selected subcubes cover
\(\{0,1\}^n\).

Short justification: unsatisfiability means there is no assignment outside the
union of falsifying subcubes.

## Step C5

The function \(CCF_n\) is monotone in the selected-clause bits.

Short justification: adding clauses can only add falsifying subcubes to the
union, so a cover remains a cover.

## Step C6

If \(P=NP\), then 3-UNSAT is decidable in polynomial time.

Short justification: 3-SAT is NP-complete, and 3-UNSAT is the complement of
3-SAT. If \(P=NP\), then \(P=coP\) and the complement is also polynomial-time
decidable.

## Step C7

If \(P=NP\), then \(CCF_n\) has polynomial-size Boolean circuits.

Short justification: an input \(z\) can be decoded as a 3-CNF formula of size
polynomial in \(N\). A polynomial-time decision algorithm for 3-UNSAT gives a
polynomial-time algorithm for \(CCF_n\), and every polynomial-time language has
polynomial-size nonuniform circuit families.

## Step C8

Thus a super-polynomial unrestricted circuit lower bound for \(CCF_n\) implies
\(P\ne NP\).

Short justification: it contradicts Step C7.

# Branch Point

none

# Gap

This claim only identifies a concrete lower-bound target. It does not prove any
super-polynomial circuit lower bound for \(CCF_n\).

# Next Step

Formalize the cover-search relation associated with \(CCF_n\): given a selected
cover \(S\subseteq\mathcal C_n\) and an assignment \(\alpha\), output a clause
\(C\in S\) falsified by \(\alpha\). Then test whether lower bounds for this
relation can be connected to unrestricted circuits for \(CCF_n\).
