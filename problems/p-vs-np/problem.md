---
id: p-vs-np
title: P versus NP
status: proposed
area: computational-complexity
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
  role: research-dossier-distillation
review:
  llm_reviewed: false
  human_reviewed: false
  formal_reviewed: false
---

# Problem

Determine whether every language decidable by a nondeterministic Turing machine
in polynomial time is also decidable by a deterministic Turing machine in
polynomial time. Equivalently, determine whether \(P = NP\).

# Scope

This workspace is for checkable research state related to the P versus NP
problem, especially:

- NP-complete decision problems such as SAT and 3-SAT;
- circuit lower-bound routes to \(P \ne NP\);
- proof-complexity, communication-complexity, algebraic, descriptive,
  bounded-arithmetic, derandomization, and meta-complexity routes;
- failed routes and precise obstructions that future contributors should not
  repeat.

Claims here must separate established theorems, proposed lemmas, failed
approaches, and speculative routes. No contribution should present a full
solution unless the proof object contains reproducible dependencies, explicit
gaps if any, and independent review.

# Sources

- `cook-2000-pvsnp`: used for the standard definitions of \(P\), \(NP\),
  NP-completeness, SAT/3-SAT, and the circuit lower-bound implication.

# Known Equivalent Forms

- A polynomial-time algorithm for any NP-complete language, such as SAT or
  3-SAT, implies \(P = NP\).
- A super-polynomial Boolean circuit lower bound for an NP-complete language
  implies \(P \ne NP\), in fact \(NP \nsubseteq P/poly\).

# Initial Routes

- `p-vs-np-r0001`: subcube-cover orientation route for 3-UNSAT.

# Notes

The initial route in this workspace does not prove \(P \ne NP\). It identifies
a concrete monotone cover predicate equivalent to 3-UNSAT and isolates the
nonmonotone-to-cover-search transfer lemma as the main missing step.
