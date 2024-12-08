from collections import defaultdict

import numpy as np


from helper import time_wrapper, simcmap, np_repr

test_input = f"""
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


with open("inputs/input_08.txt", "r") as f:
    real_input = f.read()

class Line(object):
    def __init__(self, vec1: np.ndarray[2], vec2: np.ndarray[2]):
        self.vec1 = vec1
        self.vec2 = vec2

    def on_line(self, coord):
        pass

class SparseMap(object):
    def __init__(self, some_input):
        given_map = [[elem for elem in line] for line in some_input.splitlines() if len(line.strip()) > 0]
        given_map = np.array(given_map)

        fields_not_empty = np.argwhere(given_map != ".")

        location_antennas = defaultdict(list)
        for coordinate in fields_not_empty:
            value = given_map[*coordinate]
            location_antennas[value].append(coordinate)

        self.location_antennas = location_antennas
        self.location_antennas_lookup = {
                tuple(v): key for key in self.location_antennas.keys() for v in self.location_antennas[key]
                }
        self.location_antinodes = set()

        self.height = len(given_map)
        self.width = len(given_map[0])

    def is_out_of_bounds(self, coord):
        y, x = coord
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return False

    def number_antinodes(self):
        i = 0
        for coord in self.location_antinodes:
            if not self.is_out_of_bounds(coord):
                i += 1
        return i

    def __repr__(self):
        build_map = np.full((self.height, self.width), fill_value= ".", dtype=object)

        for antenna in self.location_antennas_lookup:
            build_map[*antenna] = self.location_antennas_lookup[antenna]

        for antinode in self.location_antinodes:
            if self.is_out_of_bounds(antinode):
                continue
            if build_map[*antinode] == ".":
                build_map[*antinode] = simcmap("#", "red")
            else:
                build_map[*antinode] = simcmap(build_map[*antinode], "red")

        return np_repr(build_map)


@time_wrapper
def task1(some_input):
    lmap = SparseMap(some_input)
    antinodes = set()
    antinodes_2 = set()
    for antenna_name in lmap.location_antennas:
        coords = lmap.location_antennas[antenna_name]
        coord_pairs = [
                (coords[i], coords[j]) for i in range(len(coords)) for j in range(len(coords)) if i != j
                ]
        for (antenna1, antenna2) in coord_pairs:
            coord1 = antenna1 + antenna1 - antenna2
            antinodes.add(tuple(coord1))
            antinodes_2.add(tuple(coord1))
            coord2 = antenna2 + antenna2 - antenna1
            antinodes.add(tuple(coord2))
            antinodes_2.add(tuple(coord2))
            coord3 = antenna1 + (antenna2 - antenna1) / 3
            if np.all(coord3 % 1 == 0):
                antinodes.add(tuple(coord3))
            coord4 = antenna1 + 2 * (antenna2 - antenna1) / 3
            if np.all(coord4 % 1 == 0):
                antinodes.add(tuple(coord4))
    lmap.location_antinodes = antinodes

    return lmap.number_antinodes()

@time_wrapper
def task2(some_input):
    lmap = SparseMap(some_input)
    antinodes = set()

    for antenna_name in lmap.location_antennas:
        coords = lmap.location_antennas[antenna_name]
        pairs = [
                (coords[i], coords[j]) for i in range(len(coords)) for j in range(len(coords)) if i != j
                ]

        for pair in pairs:
            antenna1, antenna2 = pair

            for t in range(-50, 51, 1):
                coord = antenna1 + t * (antenna2 - antenna1)
                if np.all(coord % 1 == 0):
                    antinodes.add(tuple(coord))

    lmap.location_antinodes = antinodes

    return lmap.number_antinodes()


if __name__ == "__main__":
    #
    # print("test")
    # print(task1(test_input))
    # print(task2(test_input))
    # print()
    #
    # print("real")
    # print(task1(real_input))
    # print(task2(real_input))

    vec1 = np.array([11,13])
    vec2 = np.array([17,1])
    diff = vec1 - vec2


    map = np.full((20,30), fill_value= ".", dtype=object)
    map[*vec1] = simcmap("#", "red")
    map[*vec2] = simcmap("#", "red")

    def maybe_add(vec, color):
        if np.all(vec % 1 == 0):
            vec = tuple(int(v) for v in vec)
            map[*vec] = simcmap("#", color)
    vec3 = vec2 + (vec1 - vec2) / 2
    maybe_add(vec3, "green")

    vec4 = vec2 + (vec1 - vec2) / 3
    maybe_add(vec4, "blue")

    print(np_repr(map))
