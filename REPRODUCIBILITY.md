# Reproduce the checks

From the repository root, run the standard-library replay and verify all archive member bytes against the repository.

```sh
python3 -I verification/src/replay.py
python3 -I scripts/verify_repository.py
```

The replay constructs the full precision matrix and derivative rows using rational arithmetic. It checks the displayed separators and ranks, prints all three-element set ranks for both primary graphs at the worked point, and tests the graph extensions through ten vertices. The polynomial identities and the uniform extension are proved in the manuscript.

With Lean 4.30.0, using its `Std` distribution, run the partial certificate.

```sh
lean -DwarningAsError=true formal/Q505Certificate.lean
```

It checks selected Gram coordinates, separator identities, polynomial first-order coefficients, the minor formula, and rational evaluations. The checked axiom printouts accompany the source. [Exact replay output](verification/logs/replay.txt) · [Lean output](verification/logs/lean.txt) · [Build the paper](paper/BUILD.md) · [Render or open the illustration](visualization/README.md)
