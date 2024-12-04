import numpy as np
from helper import time_wrapper


test_input = f"""
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

with open("inputs/input_04.txt", "r") as f:
    real_input = f.read()


def preprocess(some_input):
    input_list = [[element for element in line] for line in some_input.split("\n") if len(line.strip()) > 0]
    return input_list

@time_wrapper
def task1(some_input):
    some_input = preprocess(some_input)
    some_array = np.array(some_input)

    count_xmas = 0
    for a in [some_array, some_array.T]: #horizontal and vertical
        for aa in a:
            b = "".join(aa)
            count_xmas += b.count("XMAS")
            count_xmas += b.count("SAMX")

    h, w = a.shape
    max_dim = max(h, w)
    diagonals = [some_array.diagonal(i) for i in range(-max_dim, max_dim)] # \ -diagonals
    diagonals += [np.fliplr(some_array).diagonal(i) for i in range(-max_dim, max_dim)] # / -diagonals

    for aa in diagonals:
        b = "".join(aa)
        count_xmas += b.count("XMAS")
        count_xmas += b.count("SAMX")

    return count_xmas


def matches_pattern(some_part_matrix, pattern):
    if np.all(some_part_matrix[pattern != None] == pattern[pattern != None]):
        return True
    return False


@time_wrapper
def task2(some_input):
    some_input = preprocess(some_input)
    some_array = np.array(some_input)
    h, w = some_array.shape
    count_xmas = 0

    pattern = np.array([["M", None, "M"], [None, "A", None], ["S", None, "S"]])
    patterns = [pattern, np.flipud(pattern), pattern.T, np.flipud(pattern).T]

    for i in range(h - 2):
        for j in range(w - 2):
            part_array = some_array[i:i + 3, j:j + 3]
            # print(part_array)
            for pattern in patterns:
                if matches_pattern(part_array, pattern):
                    count_xmas += 1
    return count_xmas


if __name__ == "__main__":
    print("test")
    print(task1(test_input))
    print(task2(test_input))
    print()

    print("real")
    print(task1(real_input))
    print(task2(real_input))
