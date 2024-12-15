from collections import defaultdict
import numpy as np
from helper import time_wrapper, memoized
from tqdm import tqdm
from functools import cache, partial

test_input = f"""
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""
#
with open("inputs/input_19.txt", "r") as f:
    real_input = f.read()

def preprocess(some_input):
    some_input = some_input.strip()
    rules, demands = some_input.split("\n\n")
    rules = [rule.strip() for rule in rules.split(",")]
    demands = [demand.strip() for demand in demands.split("\n")]
    rules = set(rules)
    return rules, demands


# def cached_is_solvable(demand, rules):
#     cache = defaultdict(int)
#     if demand in cache:
#         return cache[demand]
#     for rule in rules
#     rules, demands = preprocess(some_input)


@memoized(["demands"])
def is_solvable(demand, rules):
    for i in range(1, min(len(demand) + 1, 8)):
        possible_rule = demand[:i]
        if possible_rule in rules:
            if possible_rule == demand:
                return True
            else:
                if is_solvable(demand = demand[i:], rules = rules):
                    return True
    return False


class Solver:
    def __init__(self, rules):
        self.rules = set(rules)
        self.longest_rule = max(len(rule) for rule in rules)
        self.cache = defaultdict(bool)

    def is_solvable(self, demand):
        if demand not in self.cache:
            for i in range(1, min(len(demand), self.longest_rule) + 1):
                possible_rule = demand[:i]
                if possible_rule in self.rules:
                    if (possible_rule == demand or
                            self.is_solvable(demand[i:])):
                        self.cache[demand] = True
                        break
            if demand not in self.cache:
                self.cache[demand] = False
        return self.cache[demand]

        # if demand in self.cache:
        #     return self.cache[demand]
        # else:
        #     while
        #     for i in range(1, min(len(demand) + 1, self.longest_rule)):
        #         possible_rule = demand[:i]
        #         if possible_rule == demand:
        #             self.cache[demand] = True
        #             return True
        #
        #         elif self.is_solvable(demand=demand[i:]):
        #             self.cache[demand] = True
        #             return True
        #     self.cache[demand] = False
        #     return False





# def number_solvable(demand, rules):
#     num = 0
#     for rule in rules:
#         if demand == rule:
#             num = num + 1
#         elif demand.startswith(rule):
#             num = num + number_solvable(demand[len(rule):], rules)
#     return num

@time_wrapper
def task1(some_input):
    rules, demands = preprocess(some_input)
    # cached_is_solvable = cache(partial(is_solvable, rules = rules))
    solver = Solver(rules)
    doable = 0
    for n, demand in enumerate(demands):
        if solver.is_solvable(demand):
            doable = doable + 1
    return doable

if __name__ == "__main__":
    print(task1(test_input))
    print(task1(real_input))