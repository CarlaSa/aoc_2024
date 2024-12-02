from helper import time_wrapper

test_input = f"""
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

with open("inputs/input_02.txt", "r") as f:
    real_input = f.read()

def preprocess(some_input):
    input_list = [[int(l) for l in line.split()] for line in some_input.split("\n") if len(line.strip()) > 0]
    return input_list

def is_safe(line):
    diff = [line[i] - line[i+1] for i in range(len(line)-1)]
    bed1 = all(d > 0 for d in diff) or all(d < 0 for d in diff)
    bed2 = all(abs(d) < 4 for d in diff)
    return bed1 and bed2

def is_safe_with_damper(line):
    if is_safe(line):
        return True
    for i in range(len(line)):
        mod_line = [line[j] for j in range(len(line)) if j != i]
        if is_safe(mod_line):
            return True
    return False

@time_wrapper
def task1(some_input):
    c = 0
    for line in preprocess(some_input):
        if is_safe(line):
            c += 1
    return c

@time_wrapper
def task2(some_input):
    c = 0
    for line in preprocess(some_input):
        if is_safe_with_damper(line):
            c += 1
    return c


if __name__ == "__main__":
    print("Test data")
    print(task1(test_input))
    print(task2(test_input))
    print()
    print("Real data")
    print(task1(real_input))
    print(task2(real_input))

