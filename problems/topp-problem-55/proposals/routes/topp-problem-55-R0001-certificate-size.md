---
id: topp-problem-55-R0001
type: route
status: proposed
depends_on:
  - topp-problem-55
source_ids:
  - topp-p55
review:
  llm_reviewed: false
  human_reviewed: false
  formal_reviewed: false
---

# Route

Certificate-size analysis for input encodings.

# Core Idea

The TOPP source highlights that NP membership is unclear because the input is
compact while an arbitrary packing may have many items. Separate the geometric
coordinate issue from the compactness issue by first proving NP membership
when `n` is unary, then ask what kind of compressed certificate would be
needed for binary `n`.

# Dependencies

- `topp-problem-55`
- `topp-p55`

# Candidate Claims

- `topp-problem-55-C0001`

# Known Obstructions

- An explicit coordinate certificate has one record per rectangle. This is
  `Theta(n)` certificate data before coordinate bit lengths are considered,
  so it is not automatically polynomial in the binary-encoded input length.

# Next Step

Look for a polynomial-size compressed certificate model for binary-encoded
instances, or construct a family that appears to force many distinct local
placement records.
