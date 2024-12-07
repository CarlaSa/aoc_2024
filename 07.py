from itertools import product
from helper import time_wrapper
from math import log10, floor

test_input = f"""
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

with open("inputs/input_07.txt", "r") as f:
    real_input = f.read()

def preprocess(some_input):
    data = []
    for line in some_input.splitlines():
        if ':' in line:
            value, inputs = line.split(":")
            inputs = inputs.strip().split(" ")
            value = int(value)
            inputs = [int(input) for input in inputs]
            data.append((value, inputs))
    return data

def try_backwards(value, inputs):
    if len(inputs) == 1:
        return value == inputs[0]
    last_input, rest = inputs[-1], inputs[:-1]
    if value % last_input == 0:
        if try_backwards(value/last_input, rest):
            return True
    if try_backwards(value - last_input, rest):
        return True
    return False

def try_backwards2(value, inputs):
    if len(inputs) == 1:
        return value == inputs[0]
    last_input, rest = inputs[-1], inputs[:-1]
    if value % last_input == 0:
        if try_backwards2(value/last_input, rest):
            return True
    if try_backwards2(value - last_input, rest):
        return True
    magn_last = floor(log10(last_input)) + 1
    if value % 10**magn_last == last_input:
        if try_backwards2(value // 10 ** magn_last, rest):
            return True
    return False

@time_wrapper
def task1(some_input):
    data = preprocess(some_input)
    sum_possible = 0
    for value, inputs in data:
        success = try_backwards(value, inputs)
        if success:
            sum_possible += value
    return sum_possible

@time_wrapper
def task2(some_input):
    data = preprocess(some_input)
    sum_possible = 0
    for value, inputs in data:
        success = try_backwards2(value, inputs)
        if success:
            sum_possible += value
    return sum_possible

if __name__ == "__main__":
    print("test")
    print(task1(test_input))
    print(task2(test_input))
    print()

    print("real")
    print(task1(real_input))
    print(task2(real_input))

