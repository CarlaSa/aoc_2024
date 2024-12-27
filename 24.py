from collections import defaultdict
from helper import time_wrapper
from copy import deepcopy
from random import randint

test_input = f"""
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
"""

test_input_2 = f"""
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""

with open("inputs/input_24.txt", "r") as f:
    real_input = f.read()


def preprocess(some_input):
    start_values_, instructions_ = some_input.split("\n\n")
    start_values_dict = dict()
    for line in start_values_.split("\n"):
        if len(line) > 0:
            node, value = line.split(": ")
            assert value in "01"
            start_values_dict[node] = int(value)

    instructions = []
    for line in instructions_.split("\n"):
        line_split = line.split(" ")
        if len(line_split) == 5:
            assert line_split[3] == "->"
            parse_dict = {
                    "input1"   : line_split[0],
                    "input2"   : line_split[2],
                    "operation": line_split[1],
                    "output"   : line_split[4],
                    }
            instructions.append(parse_dict)

    return start_values_dict, instructions


def do_operation(input1, input2, operation):
    if operation == "AND":
        return input1 & input2
    elif operation == "OR":
        return input1 | input2
    elif operation == "XOR":
        return input1 ^ input2
    else:
        raise ValueError("Invalid operation")


def do_connections(inputs, instructions):
    outstanding = [True] * len(instructions)

    # inputs = deepcopy(inputs)
    outputs = inputs.copy()
    i = 0
    for _ in range(len(instructions)):
        if not any(outstanding):
            break
    # while any(outstanding):
        for idx, instruction in enumerate(instructions):
            if not outstanding[idx]:
                continue

            input1, input2, operation, output = (instruction["input1"], instruction["input2"],
                                                 instruction["operation"], instruction["output"])

            if input1 in outputs and input2 in outputs:
                outputs[output] = do_operation(outputs[input1], outputs[input2], operation)
                outstanding[idx] = False

            else:
                continue
        # if i
        # i = i + 1
    if any(outstanding):
        return False

    return outputs


def decode_binary(values, key="z"):
    solution = "".join([str(values[k]) for k in sorted(values.keys()) if k[0] == key][::-1])
    solution = int(solution, 2)
    return solution


def do_operation_literal(input1, input2, operation, output):
    return f"[{output}]({input1} {operation} {input2})"


def get_instructions_of_solution(some_input):
    inputs, instructions = preprocess(some_input)
    outstanding = [True] * len(instructions)

    set_values = {
            v: v for v in inputs.keys()
            }

    while any(outstanding):
        for idx, instruction in enumerate(instructions):
            if not outstanding[idx]:
                continue

            input1, input2, operation, output = (instruction["input1"], instruction["input2"],
                                                 instruction["operation"], instruction["output"])

            if input1 in set_values and input2 in set_values:
                set_values[output] = do_operation_literal(set_values[input1], set_values[input2], operation, output)
                outstanding[idx] = False

            else:
                continue

    return set_values


def swap_instructions(instructions, idx):
    new_inst = deepcopy(instructions)

    for i in range(len(idx) // 2):
        idx1 = idx[2 * i]
        idx2 = idx[2 * i + 1]
        new_inst[idx1]["output"], new_inst[idx2]["output"] = (new_inst[idx2]["output"],
                                                              new_inst[idx1]["output"])
    return new_inst


@time_wrapper
def task1(some_input):
    inputs, instructions = preprocess(some_input)

    values = do_connections(inputs, instructions)
    solution = decode_binary(values)

    return solution


def task2(some_input):
    inputs, instructions = preprocess(some_input)
    for i in range(len(instructions)):
        instructions[i]["idx"] = i

    decoded_x = decode_binary(inputs, key="x")
    decoded_y = decode_binary(inputs, key="y")

    z_prime = decoded_x + decoded_y

    z_operations = [
            instr for instr in instructions if "z" in instr["output"]
            ]

    z_operations_wrong = [
            instr for instr in z_operations if instr["operation"] != "XOR" and instr["output"] != "z45"
            ]

    swaps = list()

    for operation in z_operations_wrong:
        # ZNN is always (Something) XOR (XNN XOR YNN)
        num_z = operation["output"][1:]
        x, y = f"x{num_z}", f"y{num_z}"
        # get (XNN XOR YNN)
        first_component = [instr for instr in instructions
                           if instr["input1"] in (x, y) and instr["input2"] in (x, y)
                           and instr["operation"] == "XOR"]
        assert len(first_component) == 1
        first_component = first_component[0]
        # get key of (XNN XOR YNN)
        output_of_first_component = first_component["output"]

        # find instruction that XORS with that key
        z_candidates = [
                instr for instr in instructions
                if (instr["input1"] == output_of_first_component
                    or instr["input2"] == output_of_first_component)
                   and instr["operation"] == "XOR"
                ]
        assert len(z_candidates) == 1
        z_candidate = z_candidates[0]

        swaps.append(operation["idx"])
        swaps.append(z_candidate["idx"])

    # this gives me 6 outputs, brute force the last swap

    # original_solution = decode_binary(do_connections(inputs, instructions))
    swap_candidates_second_round = []
    try_swap_history = []

    i = 0
    for j1 in range(len(instructions)):
        for j2 in range(j1+1, len(instructions)):
            instr1 = instructions[j1]
            instr2 = instructions[j2]

            try_swap = swaps.copy()
            try_swap.append(instr1["idx"])
            try_swap.append(instr2["idx"])
            try_swap_history.append(try_swap)
            new_instructions = swap_instructions(instructions, try_swap)
            values = do_connections(inputs, new_instructions)
            if values:
                this_z = decode_binary(values)
                if this_z == z_prime:
                    print("this_z", this_z)
                    print(try_swap)
                    swap_candidates_second_round.append(try_swap.copy())
                    break

    possible_idx = [True] * len(swap_candidates_second_round)
    while sum(possible_idx) > 1:
        inputs_new = {
                key : randint(0,1) for key in inputs.keys()
                }

        decoded_x = decode_binary(inputs_new, key="x")
        decoded_y = decode_binary(inputs_new, key="y")

        random_z_prime = decoded_x + decoded_y
        for idx in range(len(swap_candidates_second_round)):
            new_instructions = swap_instructions(instructions, swap_candidates_second_round[idx])
            values = do_connections(inputs_new, new_instructions)
            this_z = decode_binary(values)
            if this_z != random_z_prime:
                possible_idx[idx] = False

    actual_swaps = swap_candidates_second_round[possible_idx.index(True)]

    new_instructions = swap_instructions(instructions, actual_swaps)
    values = do_connections(inputs, new_instructions)
    swap_z = decode_binary(values)

    print("real answer:", z_prime)
    print("swaped answers:", swap_z)

    names = []
    for idx in actual_swaps:
        names.append(instructions[idx]["output"])

    password = ",".join(sorted(names))

    return password


if __name__ == "__main__":
    print("test")
    print(task1(test_input))
    print(task1(test_input_2))

    # print(task2(test_input))
    # print()
    #
    print("real")
    print(task1(real_input))
    print(task2(real_input))