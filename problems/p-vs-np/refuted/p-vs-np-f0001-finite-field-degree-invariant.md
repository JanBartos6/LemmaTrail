---
id: p-vs-np-f0001
type: failure
status: refuted
route_ids:
  - p-vs-np-r0001
depends_on:
  - p-vs-np-c0001
source_ids: []
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
  role: obstruction-analysis
review:
  llm_reviewed: false
  human_reviewed: false
  formal_reviewed: false
---

# Failed Claim Or Route

Use high algebraic degree over \(\mathbb F_2\) as a standalone invariant to
prove super-polynomial unrestricted Boolean circuit lower bounds for \(CCF_n\).

# Known Obstructions

Algebraic degree over \(\mathbb F_2\) does not by itself imply large
unrestricted Boolean circuits. The function

\[
AND_N(x_1,\ldots,x_N)=x_1x_2\cdots x_N
\]

has full \(\mathbb F_2\)-degree \(N\), but it has linear-size Boolean circuits.
Therefore, even if \(CCF_n\) has high or full \(\mathbb F_2\)-degree, that fact
alone cannot prove a super-polynomial unrestricted circuit lower bound.

# Evidence

The algebraic normal form of \(AND_N\) over \(\mathbb F_2\) is the single
monomial \(x_1x_2\cdots x_N\), so its degree is \(N\). A Boolean circuit
computes \(AND_N\) by a binary tree or fan-in-2 chain of AND gates using \(N-1\)
AND gates. Thus full algebraic degree is compatible with linear circuit size.

# Lesson

Finite-field degree may still help inside a more refined argument, but it is
not a sufficient lower-bound measure for unrestricted Boolean circuits. Future
attempts should use a more syntax-sensitive, communication-theoretic,
proof-complexity, or cover-search invariant.

# Next Step

Test whether a refined invariant, such as cover-search protocol complexity or a
restricted proof-complexity measure for subcube-cover tautologies, avoids this
counterexample.
