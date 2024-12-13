from collections import defaultdict
import numpy as np

test_input = f"""
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

with open("inputs/input_12.txt", "r") as f:
    real_input = f.read()

def parse_input(some_input):
    some_input = [[c for c in line] for line in some_input.split("\n") if len(line.strip())>0]
    return np.array(some_input, dtype=object)


def neighbors(arr):
    # without oob
    neighbors_dict = defaultdict(list)
    for (i,j), val in np.ndenumerate(arr):
        for (i2, j2) in  [(i -1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if i2 >= 0 and j2 >= 0 and i2 < arr.shape[0] and j2 < arr.shape[1]:
                if arr[i2, j2] == val:
                    neighbors_dict[(i,j)].append((i2, j2))
    return neighbors_dict

def not_neighbors(arr):
    # does include oob
    not_neighbors_dict = defaultdict(list)
    for (i,j), val in np.ndenumerate(arr):
        for (i2, j2) in  [(i -1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if i2 >= 0 and j2 >= 0 and i2 < arr.shape[0] and j2 < arr.shape[1]:
                if arr[i2, j2] != val:
                    not_neighbors_dict[(i,j)].append((i2, j2))
            else:
                not_neighbors_dict[(i,j)].append((i2, j2))
    return not_neighbors_dict

def find_connected_components(arr, neighbors_dict):
    is_explored = np.zeros_like(arr, dtype=bool)
    label = np.zeros_like(arr, dtype=int)
    current_label = 1
    for (i,j), val in np.ndenumerate(arr):
        if is_explored[i,j]:
            continue
        assert label[i,j] == 0
        neighbor_queue = [(i,j)]
        while len(neighbor_queue) > 0:
            (this_i, this_j) = neighbor_queue.pop()
            is_explored[this_i,this_j] = True
            label[this_i,this_j] = current_label
            unexplored_neighbors = [(neigh_i, neigh_j) for (neigh_i, neigh_j) in neighbors_dict[(this_i,this_j)]
                                    if not is_explored[neigh_i,neigh_j]]
            neighbor_queue += unexplored_neighbors
        current_label += 1
    return label

def find_connected_components_alt(neighbors_dict):
    is_explored = {
        key: False for key in neighbors_dict.keys()
    }
    label = {
        key: 0 for key in neighbors_dict.keys()
    }
    current_label = 1
    for first_edge in neighbors_dict:
        if is_explored[first_edge]:
            continue
        assert label[first_edge] == 0

        neighbor_queue = [first_edge]
        while len(neighbor_queue) > 0:
            current_edge = neighbor_queue.pop()
            is_explored[current_edge] = True
            label[current_edge] = current_label
            unexplored_neighbors = [n for n in neighbors_dict[current_edge] if not is_explored[n]]
            neighbor_queue += unexplored_neighbors
        current_label += 1
    return label, current_label -1


def task1(some_input):
    some_input = parse_input(some_input)
    neighbors_dict = neighbors(some_input)
    labels = find_connected_components(some_input, neighbors_dict)
    cost = {
        label: {"area": 0, "perimeter": 0} for label in np.unique(labels)
    }

    for (i,j), val in np.ndenumerate(labels):
        cost[val]["area"] += 1
        cost[val]["perimeter"] += 4 - len(neighbors_dict[(i,j)])

    return sum(label_cost["area"] * label_cost["perimeter"] for label_cost in cost.values())

def task2(some_input):
    some_input = parse_input(some_input)
    neighbors_dict = neighbors(some_input)
    labels = find_connected_components(some_input, neighbors_dict)
    not_neighbors_dict = not_neighbors(labels)

    cost = {label: {"area": 0, "sides": dict()} for label in np.unique(labels)}

    # get all sides
    for (i,j), val in np.ndenumerate(labels):
        cost[val]["area"] += 1
        sides = []
        for not_neighbor in not_neighbors_dict[(i,j)]:
            side = ((i,j), not_neighbor)
            sides.append(side)
        cost[val]["sides"][(i,j)] = sides

    def border_dir(s):
        return (s[0][0] - s[1][0], s[0][1] - s[1][1])

    for key in cost:
        nodes = cost[key]["sides"]
        neighbor_edges_dict =  {
            edge: [] for node in nodes for edge in nodes[node]
        }

        for inner_val in nodes:
            dirs = [border_dir(side) for side in nodes[inner_val]]

            for some_neighbor in neighbors_dict[*inner_val]:
                some_neighbor_edges = nodes[some_neighbor]
                neighbor_dirs = [border_dir(side) for side in some_neighbor_edges]
                for k in range(len(nodes[inner_val])):
                    dir = dirs[k]
                    node = nodes[inner_val][k]
                    if dir in neighbor_dirs:
                         neighbor_edges_dict[tuple(node)].append(some_neighbor_edges[neighbor_dirs.index(dir)])

        labels_edges, num_labels = find_connected_components_alt(neighbor_edges_dict)
        cost[key]["num_sides"] = num_labels

    return sum(label_cost["area"] * label_cost["num_sides"] for label_cost in cost.values())


if __name__ == "__main__":

    print("test")
    print(task1(test_input))
    print(task2(test_input))
    print()

    print("real")
    print(task1(real_input))
    print(task2(real_input))
