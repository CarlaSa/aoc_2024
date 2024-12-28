from string import whitespace
from helper import time_wrapper

test_input = f"""2333133121414131402"""

with open("inputs/input_09.txt", "r") as f:
    real_input = f.read()


def print_dm(dm_uncompressed):
    map_free = lambda x: "." if x == -99 else str(x)
    temp = map(map_free, dm_uncompressed)
    print("".join(temp))

def preprocess(some_input):
    dm_dense = list(int(i) for i in some_input if not i in whitespace)
    space_available = sum(dm_dense)
    dm_uncompressed = [None] * space_available
    dm_block_list= list()
    dm_ws_list = list()
    current_idx = 0
    is_free = False
    current_label = 0
    for block_size in dm_dense:
        if is_free:
            label = -99
            dm_ws_list.append(dict(start = current_idx, end = current_idx + block_size, size = block_size))

        else:
            label = current_label
            current_label += 1
            dm_block_list.append(dict(start = current_idx, end = current_idx + block_size, size = block_size))

        for j in range(current_idx, current_idx + block_size):
            dm_uncompressed[j] = label
        current_idx += block_size
        is_free = not is_free
    return dm_uncompressed, dm_block_list, dm_ws_list

def defragment(dm_uncmprst, verbose =False):
    if verbose:
        print_dm(dm_uncmprst)
    pointer_right = len(dm_uncmprst) - 1
    pointer_left = 0
    while pointer_right > pointer_left:
        while dm_uncmprst[pointer_right] == -99:
            pointer_right -= 1
        while dm_uncmprst[pointer_left] != -99:
            pointer_left += 1
        if pointer_right <= pointer_left:
            break
        dm_uncmprst[pointer_right], dm_uncmprst[pointer_left] = dm_uncmprst[pointer_left], dm_uncmprst[pointer_right]
        if verbose:
            print_dm(dm_uncmprst)
    return dm_uncmprst

def defragment_whole_blocks(dm_uncmprst, dm_block_list, dm_ws_list, verbose =False):
    if verbose:
        print_dm(dm_uncmprst)

    for ws in dm_ws_list:
        ws["used"] = False

    for block in dm_block_list[::-1]:
        if verbose:
            other_out_str = [" "] * len(dm_uncmprst)
            for i in range(block["size"]):
                other_out_str[block["start"] + i] = "^"
            other_out_str = "".join(other_out_str)
            print(other_out_str)

            print_dm(dm_uncmprst)

        block_start = block["start"]
        size_block = block["size"]

        for i, ws in enumerate(dm_ws_list):
            if ws["used"]:
                continue

            if ws["end"] > block_start:
                break

            if size_block <= ws["size"]:
                ws["used"] = True
                for j in range(size_block):
                    dm_uncmprst[ws["start"] + j], dm_uncmprst[block_start + j] = (
                            dm_uncmprst[block_start + j], dm_uncmprst[ws["start"]  + j])

                if size_block < ws["size"]:
                    dm_ws_list[i]["start"] = ws["start"] + size_block
                    dm_ws_list[i]["size"] = ws["size"] - size_block
                    dm_ws_list[i]["used"] = False
                break
    if verbose:
        print_dm(dm_uncmprst)
    return dm_uncmprst

@time_wrapper
def task1(some_input):
    dm_uncompressed, _, _ = preprocess(some_input)
    dm_defrag = defragment(dm_uncompressed)
    checksum = sum(i*j for (i,j) in enumerate(dm_defrag) if j != -99)
    return checksum

@time_wrapper
def task2(some_input, verbose = False):
    dm_uncompressed, dm_block_list, dm_ws_list = preprocess(some_input)
    dm_defrag = defragment_whole_blocks(dm_uncompressed, dm_block_list, dm_ws_list, verbose = verbose)
    checksum = sum(i * j for (i, j) in enumerate(dm_defrag) if j != -99)
    return checksum


if __name__ == "__main__":
    print("test")
    print(task1(test_input))
    print(task2(test_input))
    print()

    print("real")
    print(task1(real_input))
    print(task2(real_input))