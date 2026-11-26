#!/usr/bin/env python3
"""Exact rational checks from the full precision parametrization."""
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement

CORE3 = {(2, 1), (1, 3), (2, 3)}
CORE4 = {(2, 1), (3, 1), (1, 4), (3, 2), (4, 2), (4, 3)}
SELECT3 = ((1, 1), (1, 3), (3, 3))
SELECT4 = ((1, 1), (1, 4), (2, 2), (1, 2))


def reverse(edges, edge):
    assert edge in edges and edge[::-1] not in edges
    return (edges - {edge}) | {edge[::-1]}


def elimination(rows):
    """Return rank and pivot product including row-exchange sign."""
    matrix = [[Q(x) for x in row] for row in rows]
    rank = 0
    product = Q(1)
    for col in range(len(matrix[0])):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][col]), None)
        if pivot is None:
            continue
        if rank != pivot:
            matrix[pivot], matrix[rank] = matrix[rank], matrix[pivot]
            product = -product
        lead = matrix[rank][col]
        product *= lead
        for i in range(rank + 1, len(matrix)):
            mul = matrix[i][col] / lead
            for j in range(col, len(matrix[i])):
                matrix[i][j] -= mul * matrix[rank][j]
        rank += 1
        if rank == len(matrix):
            break
    return rank, product


def determinant(rows):
    assert len(rows) == len(rows[0])
    rank, product = elimination(rows)
    return product if rank == len(rows) else Q(0)


def full_model(n, edges, weights, s=Q(1)):
    """Return A = I − Λ, all K coordinates, and their parameter gradients."""
    vertices = range(1, n + 1)
    assert set(weights) <= edges
    assert {tuple(sorted(edge)) for edge in edges} == set(combinations(vertices, 2))
    assert len(edges) == n * (n - 1) // 2
    a = {(i, j): Q(i == j) - weights.get((i, j), 0) for i in vertices for j in vertices}
    coordinates = tuple(combinations_with_replacement(vertices, 2))
    gram = {(i, j): sum(a[i, k] * a[j, k] for k in vertices) for i, j in coordinates}
    k = {ij: s * g for ij, g in gram.items()}
    gradients = {
        (i, j): {
            "s": gram[i, j],
            **{
                (u, v): -s * ((i == u) * a[j, v] + (j == u) * a[i, v])
                for u, v in edges
            },
        }
        for i, j in coordinates
    }
    return [[a[i, j] for j in vertices] for i in vertices], k, gradients


def rows(jacobian, coordinates, parameters=None):
    if parameters is None:
        parameters = tuple(next(iter(jacobian.values())))
    return [[jacobian[ij][parameter] for parameter in parameters] for ij in coordinates]


def separator3(triple):
    u, v, w = triple
    return u * w - v * v - w * w


def separator4(quadruple):
    x, u, y, v = quadruple
    d = u * u - v * v
    return d * d - x * d * (x - y) + u * u * (x - y) ** 2


def check_three():
    graphs = (CORE3, reverse(CORE3, (2, 3)))
    for label, edges, varying, rank in zip("GH", graphs, ((2, 3), (3, 2)), (2, 3)):
        a, k, j = full_model(3, edges, {(2, 1): Q(1, 4), (1, 3): Q(1, 4), varying: Q(1, 2)})
        value = tuple(k[ij] for ij in SELECT3)
        assert value == (Q(17, 16), Q(-1, 4), Q(1) if label == "G" else Q(5, 4))
        assert determinant(a) == (Q(1) if label == "G" else Q(31, 32))
        residual = separator3(value)
        assert residual == (0 if label == "G" else Q(-19, 64))
        assert elimination(rows(j, SELECT3))[0] == rank
        if label == "G":
            assert determinant(rows(j, SELECT3[1:], ("s", (1, 3)))) == 1
        else:
            assert determinant(rows(j, SELECT3, ("s", (1, 3), (3, 2)))) == Q(-15, 16)
        print(f"{label} coordinates {', '.join(map(str, value))}; det(A)={determinant(a)}; P={residual}")
        triples = {triple: elimination(rows(j, triple))[0] for triple in combinations(k, 3)}
        assert {triple for triple, value in triples.items() if value < 3} == ({SELECT3} if label == "G" else set())
        print(f"{label} triple ranks in lexicographic coordinate order:")
        for triple, value in triples.items():
            print(f"  {' '.join(f'K{i}{j}' for i, j in triple)}: {value}")

    old = {(2, 1), (3, 1), (2, 3)}
    for label, edges, varying, rank in zip("GH", (old, reverse(old, (2, 3))), ((2, 3), (3, 2)), (2, 3)):
        a, k, j = full_model(3, edges, {(2, 1): Q(1, 4), (3, 1): Q(1, 4), varying: Q(1, 2)})
        u, v, w = (k[ij] for ij in SELECT3)
        assert determinant(a) == 1
        assert u * w - u * u - v * v == (0 if label == "G" else Q(1, 4))
        assert elimination(rows(j, SELECT3))[0] == rank
    for edge in ((1, 2), (2, 1)):
        _, _, j = full_model(2, {edge}, {edge: Q(1, 2)})
        assert all(elimination(rows(j, pair))[0] == 2 for pair in combinations(j, 2))
    print("PASS: both three-vertex witnesses, all triples, and both two-vertex orientations")


def strongly_connected(n, edges):
    for vertex in range(1, n + 1):
        reached = {vertex}
        for _ in range(n - 1):
            reached |= {v for u, v in edges if u in reached}
        if len(reached) != n:
            return False
    return True


def check_extensions():
    for n in range(3, 11):
        new = range(4, n + 1)
        base = CORE3 | {(w, i) for w in new for i in range(1, 4)} | set(combinations(new, 2))
        for label, edges, varying, rank in zip("GH", (base, reverse(base, (2, 3))), ((2, 3), (3, 2)), (2, 3)):
            a, k, j = full_model(n, edges, {(2, 1): Q(1, 4), (1, 3): Q(1, 4), varying: Q(1, 2)})
            assert determinant(a) == (Q(1) if label == "G" else Q(31, 32))
            assert separator3(tuple(k[ij] for ij in SELECT3)) == (Q(0) if label == "G" else Q(-19, 64))
            assert elimination(rows(j, SELECT3))[0] == rank
    for n in range(4, 11):
        new = range(5, n + 1)
        for new_edges in (set(combinations(new, 2)), {(j, i) for i, j in combinations(new, 2)}):
            base = CORE4 | {(4, w) for w in new} | {(w, i) for w in new for i in (1, 2, 3)} | new_edges
            cycle = reverse(base, (3, 2))
            assert strongly_connected(n, base) and strongly_connected(n, cycle)
            _, _, jg = full_model(n, base, {})
            assert elimination(rows(jg, SELECT4))[0] == 3
            assert determinant(rows(jg, (SELECT4[0], SELECT4[1], SELECT4[3]), ("s", (1, 4), (2, 1)))) == 1
            det_model, _, jh = full_model(n, cycle, {(2, 3): Q(1, 2)})
            assert determinant(det_model) == 1
            assert determinant(rows(jh, SELECT4, ("s", (1, 4), (2, 1), (2, 3)))) == -1
            for edges, expect in ((base, Q(0)), (cycle, Q(1, 16))):
                weights = {(1, 4): Q(1, 2)}
                if edges == cycle:
                    weights[2, 3] = Q(1, 2)
                det_model, k, _ = full_model(n, edges, weights)
                assert determinant(det_model) == 1
                assert separator4(tuple(k[ij] for ij in SELECT4)) == expect
    print("PASS: three-coordinate lifts through 10 and strongly connected certificates for 4–10")


if __name__ == "__main__":
    check_three()
    check_extensions()
