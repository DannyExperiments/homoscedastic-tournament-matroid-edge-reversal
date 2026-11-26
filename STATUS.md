# Review and verification status

**Internally reviewed, not peer reviewed.**

OpenAI Codex independently checked the graph convention, rational point, selected minors, all-triples argument, and general strongly connected extension. The finite replay derives the matrices and derivatives from their edge data. The [literature audit](audits/public_safe_reports/LITERATURE_AUDIT.md) identifies earlier computations with direct overlap.

The partial Lean 4.30.0 certificate checks selected Gram coordinates, polynomial separator identities, exact polynomial linearization, the selected minor formula and rational evaluations. It evaluates the scalar expression for the rational determinant value. The full matrix invertibility argument, Jacobian matroid criterion, all-triples claim and strongly connected extension are in the analytic proof.
