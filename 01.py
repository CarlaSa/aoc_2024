test_input = f"""
3   4
4   3
2   5
1   3
3   9
3   3
"""

with open("inputs/input_01_a.txt", "r") as f:
    real_input = f.read()

def preprocess(some_input):
    input_list = [[int(l) for l in line.split()] for line in some_input.split("\n") if len(line.strip()) > 0]
    first_list = [l[0] for l in input_list]
    second_list = [l[1] for l in input_list]
    return first_list, second_list

def task1(some_input):
    first_list, second_list = preprocess(some_input)

    first_list = sorted(first_list)
    second_list = sorted(second_list)

    d = 0
    for (a,b) in zip(first_list, second_list):
        d += abs(a - b)

    return d

def task2(some_input):
    first_list, second_list = preprocess(some_input)

    d = 0
    for n in first_list:
        count = second_list.count(n)
        d += n * count
    return d

if __name__ == "__main__":
    print("Test data")
    print(task1(test_input))
    print(task2(test_input))
    print()
    print("Real data")
    print(task1(real_input))
    print(task2(real_input))