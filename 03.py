import re
from helper import time_wrapper
test_input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
test_input2 = "xmul(2,4)&mul[3,7]!^don't()\n_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
with open("inputs/input_03.txt", "r") as f:
    real_input = f.read()

def find_mul(some_input):
    mul_pattern = r"mul\(\d{1,3},\d{1,3}\)"
    match = re.findall(mul_pattern, some_input)
    return match

def do_mul(some_mul_input):
    some_mul_pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    match = re.match(some_mul_pattern, some_mul_input)
    assert match is not None
    return int(match.groups()[0]) * int(match.groups()[1])

def remove_do_dont(some_input):
    some_input = some_input.replace("\n", "") # . does not match line breaks
    some_input = some_input + "do()" # catch last dont
    dont_do_pattern = r"don't\(\).*?do\(\)"
    removed = re.split(dont_do_pattern, some_input)
    return "_".join(removed) # dont create new mul by accident

@time_wrapper
def task1(some_input):
    muls = find_mul(test_input)
    return sum(do_mul(mul) for mul in muls)

@time_wrapper
def task2(some_input):
    remove_do = remove_do_dont(some_input)
    muls = find_mul(remove_do)
    return sum(do_mul(mul) for mul in muls)


if __name__ == "__main__":
    print("test")
    print(task1(test_input))
    print(task2(test_input))
    print()

    #print(task1(test_input2))
    #print(task2(test_input2))

    print("real")
    print(task1(real_input))
    print(task2(real_input))