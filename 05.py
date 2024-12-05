from helper import time_wrapper

test_input = f"""
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


with open("inputs/input_05.txt", "r") as f:
    real_input = f.read()


def preprocess(some_input):
    ordering_rules, pages_to_be_printed = some_input.split("\n\n")
    ordering_rules = [[int(element) for element in line.split("|")] for line in ordering_rules.split("\n") if len(
            line.strip()) > 0]
    pages_to_be_printed =  [[int(element) for element in line.split(",")] for line in pages_to_be_printed.split("\n")
                            if len(line.strip()) > 0]
    return ordering_rules, pages_to_be_printed

def satisfies_rule(line, rule):
    if rule[0] in line and rule[1] in line:
        return line.index(rule[0]) < line.index(rule[1])
    return True

@time_wrapper
def task1(some_input):
    ordering_rules, pages_to_be_printed = preprocess(some_input)

    result_sum = 0
    for line in pages_to_be_printed:
        if all(satisfies_rule(line, rule) for rule in ordering_rules):
            middle_element = line[len(line) // 2]
            result_sum += middle_element
    return result_sum


def sort_with_ruleset(line, ordering_rules):
    relevant_rules = []
    for rule in ordering_rules:
        if rule[0] in line and rule[1] in line:
            relevant_rules.append(rule)

    def recursive_sort_with_ruleset(current_ruleset, beginning_line):
        if len(current_ruleset) == 1:
            last_rule = current_ruleset[0]
            return beginning_line + last_rule
        find_first = set(rule[0] for rule in current_ruleset) - set(rule[1] for rule in current_ruleset)
        assert len(find_first) == 1
        first_elem = find_first.pop()
        beginning_line.append(first_elem)
        ruleset_without_first = [rule for rule in current_ruleset if rule[0] != first_elem]
        return recursive_sort_with_ruleset(ruleset_without_first, beginning_line)

    return recursive_sort_with_ruleset(relevant_rules, [])

@time_wrapper
def task2(some_input):
    ordering_rules, pages_to_be_printed = preprocess(some_input)

    result_sum = 0
    for line in pages_to_be_printed:
        if all(satisfies_rule(line, rule) for rule in ordering_rules):
            pass
        else:
            sorted_line = sort_with_ruleset(line, ordering_rules)
            middle_element = sorted_line[len(line) // 2]
            result_sum += middle_element
    return result_sum



if __name__ == "__main__":
    print("test")
    print(task1(test_input))
    print(task2(test_input))
    print()

    print("real")
    print(task1(real_input))
    print(task2(real_input))