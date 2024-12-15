from collections import defaultdict
from math import floor, log10
from helper import time_wrapper
test_input = "125 17"
with open("inputs/input_11.txt", "r") as f:
    real_input = f.read()



def preprocess(some_input):
    some_input = tuple(int(s) for s in some_input.strip().split(" "))
    stones = defaultdict(int)
    for stone in some_input:
        stones[stone] += 1
    return stones

def change_stone(number):
    if number == 0:
        return 1,
    elif floor(log10(number)) % 2 != 0:
        num_digits = (floor(log10(number)) + 1) / 2
        first, second = number // (10 ** num_digits), number % (10 ** num_digits)
        return (int(first), int(second))
    else:
        return number * 2024,

def blink(stones):
    new_stones = defaultdict(int)
    for stone in stones:
        quantity = stones[stone]
        outputs = change_stone(stone)
        for output in outputs:
            new_stones[output] += quantity
    return new_stones

@time_wrapper
def task1(some_input):
    stones = preprocess(some_input)
    for _ in range(25):
        stones = blink(stones)
    return sum(stones.values())

@time_wrapper
def task2(some_input):
    stones = preprocess(some_input)
    for _ in range(75):
        stones = blink(stones)
    return sum(stones.values())


if __name__ == "__main__":
    print("test")
    print(task1(test_input))
    print(task2(test_input))
    print()

    print("real")
    print(task1(real_input))
    print(task2(real_input))