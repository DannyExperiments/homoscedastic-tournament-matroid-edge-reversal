# Claims and evidence

| Claim | Evidence |
| --- | --- |
| Prior small labelled counterexamples | Wu’s dissertation §5.4.1, p. 63. [Literature audit](audits/public_safe_reports/LITERATURE_AUDIT.md) |
| Three-vertex rank two versus three | Selected coordinate formulas, separator and derivative minor in the [paper](paper/manuscript.pdf). [Exact rational replay](verification/logs/replay.txt) |
| Abstract nonisomorphism at size three | Both types of three-coordinate minors in the paper. The replay checks all twenty triples of each graph at the same parameter values. |
| Strongly connected labelled pair in each size at least four | Four-coordinate separator, generic minor and graph extension in the paper. Exact examples through size ten in the replay. |
| Partial formal verification | [Lean source](formal/Q505Certificate.lean) and its [axiom report](verification/logs/lean.txt). |
