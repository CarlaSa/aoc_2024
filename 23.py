from collections import defaultdict
from helper import time_wrapper

test_input = f"""
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""

with open("inputs/input_23.txt", "r") as f:
    real_input = f.read()


def preprocess(some_input):
    neighbors = defaultdict(list)
    for line in some_input.splitlines():
        line = line.strip()
        if "-" in line:
            a, b = line.split("-")
            neighbors[a].append(b)
            neighbors[b].append(a)
    return neighbors

@time_wrapper
def task1(some_input):
    neighbors = preprocess(some_input)
    triples = []
    already_looked_at = set()
    for node in neighbors:
        for j in range(len(neighbors[node])):
            other_node = neighbors[node][j]
            if other_node in already_looked_at:
                continue
            for i in range(j+1, len(neighbors[node])):
                other_other_node = neighbors[node][i]
                if neighbors[node][i] in already_looked_at:
                    continue
                if other_other_node in neighbors[other_node]:
                    if node[0] == "t" or other_node[0] == "t" or other_other_node[0] == "t":
                        triples.append((node, other_node, other_other_node))
        already_looked_at.add(node)
    return len(triples)

@time_wrapper
def task2(some_input):
    neighbors = preprocess(some_input)
    list_nodes = list(neighbors.keys())

    def recursive_select(candidates) -> list:
        clusters = []
        candidates = set(candidates.copy())
        while len(candidates) > 0:
            candidate = candidates.pop()
            new_candidates = set(neighbors[candidate]) &  candidates
            if len(new_candidates) == 0:
                all_connected_neighbors = [[candidate]]
            else:
                all_connected_neighbors = recursive_select(new_candidates)
                all_connected_neighbors = [[candidate] + connected_neighbors for connected_neighbors in (
                    all_connected_neighbors)]
            clusters += all_connected_neighbors
        return clusters

    candidates = recursive_select(list_nodes)
    max_len = max(len(c) for c in candidates)
    max_candidates = [c for c in candidates if len(c) == max_len]
    assert len(max_candidates) == 1
    password = ",".join(sorted(max_candidates[0]))

    return password


if __name__ == "__main__":
    print("test")
    print(task1(test_input))
    print(task2(test_input))
    print()

    print("real")
    print(task1(real_input))
    print(task2(real_input))