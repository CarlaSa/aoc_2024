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


drawing_pipe =  '| '
drawing_end =   '└-'
drawing_blank = '  '

class Tree:
    def __init__(self, value = ""):
        self.value = value
        self.children = None

    def add_child(self, child):
        # assert isinstance(child, Tree)
        self.children.append(child)

    def _represent(self, before = None, last = True):
        if before is None:
            before = list()
        out = "".join(before) + str(self.value) + "\n"
        if len(before) > 0:
            if last:
                before[-1] = drawing_blank
            else:
                before[-1] = drawing_pipe
        before.append(drawing_end)
        for i, child in enumerate(self.children):
            if i == len(self.children) - 1:
                child_last = True
            else:
                child_last = False
            out += child._represent(before.copy(), child_last)
        return out


    def __repr__(self):
        return self._represent()

    def all_posibilities(self):
        all_posibilities = []
        if len(self.children) == 0:
            return [(self.value,)]
        for child in self.children:
            child_lists = child.all_posibilities()
            for child_set in child_lists:
                new_set = (self.value, *child_set)
                all_posibilities.append(new_set)
        return all_posibilities

class Solver:
    def __init__(self, some_input):
        rules, demands = preprocess(some_input)
        self.demands = demands
    # def __init__(self, rules):
        self.rules = set(rules)
        self.longest_rule = max(len(rule) for rule in rules)
        self.solution_exists_cache = defaultdict(bool)
        self.solution_cache = defaultdict(list)
        self.num_solution_cache = dict()

    def is_solvable(self, demand):
        if demand not in self.solution_exists_cache:
            for i in range(1, min(len(demand), self.longest_rule) + 1,):
                possible_rule = demand[:i]
                if possible_rule in self.rules:
                    if (possible_rule == demand or
                            self.is_solvable(demand[i:])):
                        self.solution_exists_cache[demand] = True
                        break
            if demand not in self.solution_exists_cache:
                self.solution_exists_cache[demand] = False
        return self.solution_exists_cache[demand]

    def get_all_solutions(self, wanted_coloring, value ="Start"):
        """ not used, but could be used to actually get all solutions (not just number) """
        if not self.is_solvable(wanted_coloring):
            return False
        solution_tree = Tree(value = value)

        if wanted_coloring in self.solution_cache:
            solution_tree.children = self.solution_cache[wanted_coloring]
            return solution_tree

        for i in range(1, min(len(wanted_coloring), self.longest_rule) + 1):

            possible_rule = wanted_coloring[:i]
            rest_wanted_coloring = wanted_coloring[i:]

            if possible_rule not in self.rules:
                continue
            elif len(rest_wanted_coloring) == 0:
                child_tree = Tree(value=possible_rule)
                solution_tree.add_child(child_tree)
            elif self.is_solvable(rest_wanted_coloring):
                child_tree = self.get_all_solutions(rest_wanted_coloring, value = possible_rule)
                solution_tree.add_child(child_tree)

        self.solution_cache[wanted_coloring] = solution_tree.children
        return solution_tree

    def number_solutions(self, wanted_coloring):
        if not self.is_solvable(wanted_coloring):
            return 0

        if wanted_coloring in self.num_solution_cache:
            return self.num_solution_cache[wanted_coloring]

        num_solutions = 0
        for i in range(1, min(len(wanted_coloring), self.longest_rule) + 1):

            possible_rule = wanted_coloring[:i]
            rest_wanted_coloring = wanted_coloring[i:]

            if possible_rule not in self.rules:
                continue
            elif len(rest_wanted_coloring) == 0:
                num_solutions += 1
            elif self.is_solvable(rest_wanted_coloring):
                num_solutions += self.number_solutions(rest_wanted_coloring)

        self.num_solution_cache[wanted_coloring] = num_solutions
        return num_solutions


    @time_wrapper
    def task1(self):
        doable = 0
        for i, demand in enumerate(self.demands):
            if self.is_solvable(demand):
                doable += 1
        return doable

    @time_wrapper
    def task2(self):
        num_solutions = dict()
        n = 0
        for demand in self.demands:
            num_solutions[demand] = self.number_solutions(demand)

        # print(num_solutions)
        return sum(num_solutions.values())


if __name__ == "__main__":
    test_solver = Solver(test_input)
    real_solver = Solver(real_input)
    print(test_solver.task1())
    print(real_solver.task1())

    print(test_solver.task2())
    print(real_solver.task2())
