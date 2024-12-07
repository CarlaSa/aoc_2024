from helper import time_wrapper
import copy

test_input = f"""
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

with open("inputs/input_06.txt", "r") as f:
    real_input = f.read()


class Maze(object):
    def __init__(self, some_input):
        self.symbol_to_value = {
                ".": 1,  # free field,
                "^": 2,  # current position
                "X": 3,  # visited
                "#": 9,  # obstacle
                }
        self.value_to_symbol = dict((v, k) for k, v in self.symbol_to_value.items())

        if isinstance(some_input, str):
            self.values = [[self.symbol_to_value[elem] for elem in line] for line in some_input.splitlines() if
                       len(line.strip()) > 0]
        else:
            self.values = some_input

        self.height = len(self.values)
        self.width = len(self.values[0])
        assert all(len(v) == self.width for v in self.values)

    def find_current_position(self):
        for i, row in enumerate(self.values):
            for j, elem in enumerate(row):
                if elem == self.symbol_to_value["^"]:
                    assert self[i, j] == 2
                    return i, j

    def __copy__(self):
        return Maze(self.values)

    def __deepcopy__(self, memo):
        return Maze(copy.deepcopy(self.values))



    def __repr__(self):
        representation = ""
        for line in self.values:
            representation += " ".join(self.value_to_symbol[elem] for elem in line)
            representation += "\n"
        return representation

    def __getitem__(self, coord):
        y, x = coord
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.values[y][x]

    def __setitem__(self, coord, value):
        y, x = coord
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        self.values[y][x] = value


class Game:
    def __init__(self, some_input=None):
        self.maze = Maze(some_input)
        self.current_position = self.maze.find_current_position()
        self.current_direction = "n"
        self.fields_visited = 0
        self.state_cache = []

    def turn(self):
        self.current_direction = {"n": "e", "e": "s", "s": "w", "w": "n"}[self.current_direction]

    def next_position(self):
        move_by_direction = {
                "n": [-1, 0],
                "e": [0, 1],
                "s": [1, 0],
                "w": [0, -1],
                }
        move = move_by_direction[self.current_direction]
        next_position = [c + m for (c, m) in zip(self.current_position, move)]
        return next_position

    def loop(self, verbose=False):
        if verbose:
            print(self.maze)

        while self.current_position:

            state = (self.current_position, self.current_direction)
            if state in self.state_cache:
                return "Time_loop"
            self.state_cache.append(state)

            self.step()
        if verbose:
            print(self.maze)

    def find_time_loops(self, verbose=False):
        obstacle_coords = []
        while self.current_position:
            if self.would_obstacle_break_game():
                next_coordinate = tuple(self.next_position())
                obstacle_coords.append(next_coordinate)
            self.step()
        return len(obstacle_coords), len(set(obstacle_coords))

    def would_obstacle_break_game(self):
        save_direction = self.current_direction
        save_position = self.current_position
        save_fields_visited = self.fields_visited
        save_maze = copy.deepcopy(self.maze)
        save_state_cache = self.state_cache

        self.turn()
        is_time_loop = self.loop() == "Time_loop"

        self.current_direction = save_direction
        self.current_position = save_position
        self.fields_visited = save_fields_visited
        self.maze = save_maze
        self.state_cache = save_state_cache

        return is_time_loop

    def step(self):
        next_position = self.next_position()
        next_value = self.maze[next_position]  # custom data structure -- false if out of bounds

        if not next_value:
            self.fields_visited += 1
            self.maze[self.current_position] = 3
            self.current_position = False

        elif next_value == 9:
            self.turn()

        else:
            assert next_value in [1, 3]  # visited or not visited
            if next_value == 3:
                self.fields_visited -= 1

            self.fields_visited += 1
            self.maze[next_position] = 2
            self.maze[self.current_position] = 3
            self.current_position = next_position


@time_wrapper
def task1(some_input):
    game = Game(some_input)
    game.loop()
    return game.fields_visited


# @time_wrapper
def task2(some_input):
    game = Game(some_input)
    return game.find_time_loops()


if __name__ == "__main__":
    print("test")
    # print(task1(test_input))
    print(task2(test_input))
    print()

    print("real")
    print(task1(real_input))
    print(task2(real_input))