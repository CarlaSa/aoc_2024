from collections import defaultdict
from helper import time_wrapper

test_input = """
1
10
100
2024
"""

other_test_input = """
1
2
3
2024
"""

with open("inputs/input_22.txt", "r") as f:
    real_input = f.read()


def preprocess(some_input):
    return [int(s) for s in some_input.strip().split("\n")]

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


@time_wrapper
def task1(some_input):
    start_numbers = preprocess(some_input)
    result = 0

    for number in start_numbers:
        temp = number
        for _ in range(2000):
            temp = next_number(temp)
        result += temp

    return result

def all_last_numbers(some_input):
    start_numbers = preprocess(some_input)

    all_last_numbers = []
    all_diff = []

    for number in start_numbers:
        temp = number
        this_last_number_temp = temp % 10
        this_last_number = [this_last_number_temp]
        this_diff = []
        # last_number_string = str(temp)[-1]
        for _ in range(2000):
            temp = next_number(temp)
            this_last_number_temp_next = temp % 10
            this_last_number.append(this_last_number_temp_next)
            this_diff.append(this_last_number_temp_next - this_last_number_temp)
            this_last_number_temp = this_last_number_temp_next
            # this_diff.append(th)
            # last_number_string += str(temp)[-1]
        all_last_numbers.append(this_last_number)
        all_diff.append(this_diff)
        # all_last_numbers.append(last_number_string)
    return all_last_numbers, all_diff

@time_wrapper
def task2(some_input):
    values, diffs = all_last_numbers(some_input)
    sum_by_diff = defaultdict(int)

    num_samples = len(values)
    for j in range(num_samples):
        sample_values = values[j]
        sample_diff = diffs[j]
        already_seen_windows = set()

        for i in range(4, 2001):

            window = ",".join(str(v) for v in (sample_diff[i-4:i]))
            if len(window) ==0:
                continue
            if window in already_seen_windows:
                continue
            value = sample_values[i]
            sum_by_diff[window] += value
            already_seen_windows.add(window)

    max_diff_window = max(sum_by_diff, key=sum_by_diff.get)
    print(max_diff_window)
    return sum_by_diff[max_diff_window]


if __name__ == "__main__":
    print("test")
    print(task1(test_input))
    print(task2(other_test_input))
    # print()

    print("real")
    print(task1(real_input))
    print(task2(real_input))