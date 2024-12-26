test_input = """
1
10
100
2024
"""

with open("inputs/input_22.txt", "r") as f:
    real_input = f.read()


def preprocess(some_input):
    return [int(s) for s in some_input.strip().split("\n")]

def task2(some_input):
    pass

def prune(i):
    return i % 16777216

def mix(a,b):
    return a ^ b


def next_number(secret_number):
    secret_number = mix(secret_number * 64, secret_number)
    secret_number = prune(secret_number)
    secret_number = mix(secret_number // 32 , secret_number)
    secret_number = prune(secret_number)
    secret_number = mix(secret_number * 2048,  secret_number)
    secret_number = prune(secret_number)
    return secret_number



def task1(some_input):
    start_numbers = preprocess(some_input)
    result = 0

    for number in start_numbers:
        temp = number
        for _ in range(2000):
            temp = next_number(temp)
        result += temp

    return result



if __name__ == "__main__":
    print("test")
    print(task1(test_input))
    # print(task2(test_input))
    # print()

    print("real")
    print(task1(real_input))
    # print(task2(real_input))