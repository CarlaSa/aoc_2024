import numpy as np
from torch.backends.mkl import verbose

from helper import time_wrapper, memoized, np_repr

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

class BetterMaze(object):
    def __init__(self, some_input):

        self.obstacles = list()
        self.start_position = None
        self.map = []
        for j, line in enumerate(some_input.strip().splitlines()):
            mapline = []
            for i, symbol in enumerate(line):
                if symbol == "^":
                    self.start_position = (j,i)
                    mapline.append(".")
                    continue
                if symbol == "#":
                    self.obstacles.append((j, i))
                mapline.append(symbol)
            self.map.append(mapline)

        self.map = np.array(self.map)
        self.height, self.width = self.map.shape

        self.obstacles = set(self.obstacles)
        assert self.start_position is not None

        self.path = [self.start_position]
        self.temp_obs =  []

    def check(self, coord):
        y, x = coord
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return "outside"
        if (y, x) in self.obstacles:
            return "obstacle"
        else:
            return "safe"

    def __repr__(self):
        out_map = np.full((self.height, self.width), "󠀠⬛️", dtype=object)
        for obstacle in self.obstacles:
            out_map[*obstacle] = "🌳"

        for path_part in self.path:
            out_map[*path_part] = "👣"

        out_map[self.path[-1]] = "🚶"

        return np_repr(out_map)

    def reset(self):
        self.path = [self.start_position]
        for coord in self.temp_obs:
            self.obstacles.remove(coord)
        self.temp_obs = []

    def add_obstacle(self, coord):
        assert coord not in self.obstacles
        self.obstacles.add(coord)
        self.temp_obs.append(coord)

    def add_path(self, coord):
        self.path.append(coord)

class Maze(object):
    symbol_to_value = {
            ".": 1,  # free field,
            "^": 2,  # current position
            "X": 3,  # visited
            "#": 9,  # obstacle
            }
    value_to_symbol = dict((v, k) for k, v in symbol_to_value.items())

    def __init__(self, some_input=None):

        self.height = None
        self.width = None
        self.values = None
        self.path = None
        self.start_position = None
        self.temp_obs = list()

        if some_input is not None:
            self.init_from_input(some_input)

    def init_from_input(self, some_input):
        # obstacle_coords = list()
        # for line in some_input.splitlines():
        #     for elem in line:
        #         if len(line.strip()) == 0:
        #             continue
        #         if elem == "#":
        #             obstacle_coords.append(self.value_to_symbol[elem])
        #
        # self.obstacles = [[elem == "#" for elem in line] for line in some_input.splitlines() if
        #                   len(line.strip()) > 0]

        self.values = [[self.symbol_to_value[elem] for elem in line] for line in some_input.splitlines() if
                       len(line.strip()) > 0]
        self.height = len(self.values)
        self.width = len(self.values[0])
        assert all(len(v) == self.width for v in self.values)
        self.path = set()
        self.start_position = self.find_current_position()


    def find_current_position(self):
        for i, row in enumerate(self.values):
            for j, elem in enumerate(row):
                if elem == self.symbol_to_value["^"]:
                    assert self[i, j] == 2
                    return i, j


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

    def add_path(self, coord):
        self[coord] = 3
        self.path.add(coord)

    def move_me(self, coord):
        y, x = coord

    # def check_field(self, coord):
    #     y, x = coord
    #     if x < 0 or x >= self.width or y < 0 or y >= self.height:
    #         return "oob"
    #     if self[y][x] != 3:
    #         return }

    def remove_path(self):
        for coord in self.path:
            self[coord] = 1
        self.path = set()
        self[self.start_position] = 2

    def add_obstacle(self, coord):
        assert self[coord] == 1
        self[coord] = 9
        self.temp_obs.append(coord)

    def reset(self):
        self.remove_path()
        for coord in self.temp_obs:
            self[coord] = 1



class Game:
    def __init__(self, some_input=None, maze=None):
        if maze is None:
            assert some_input is not None
            self.maze = BetterMaze(some_input)
        # else:
        #     assert isinstance(maze, Maze)
        #     assert some_input is None
        #     self.maze = maze
        self.current_position = self.maze.start_position
        self.current_direction = "n"
        self.state_cache = set()
        self.next_position_cache = dict()

        self.__move_by_direction ={
                "n": (-1, 0),
                "e": (0, 1),
                "s": (1, 0),
                "w": (0, -1),
                }
        self.__turn_by_direction ={"n": "e", "e": "s", "s": "w", "w": "n"}

    def restart(self, start_position = None):
        self.maze.reset()
        self.current_position = self.maze.start_position
        self.current_direction = "n"
        self.state_cache = set()

    def turn(self):
        self.current_direction = self.__turn_by_direction[self.current_direction]

    def next_position(self):
        hashed = hash(self.current_position) + hash(self.current_direction)
        if hashed in self.next_position_cache:
            return self.next_position_cache[hashed]
        move = self.__move_by_direction[self.current_direction]
        next_position = tuple(c + m for (c, m) in zip(self.current_position, move))
        self.next_position_cache[hashed] = next_position
        return next_position

    def loop(self):
        while self.current_position:

            state = hash(self.current_position) + hash(self.current_direction)
            if state in self.state_cache:
                return "Time_loop"
            self.state_cache.add(state)

            self.step()

    def find_time_loops(self, ):
        directly_after_start = self.next_position()
        coordinates = set()
        self.loop()
        path = self.maze.path
        self.restart()
        for potential_obstacle in path:
            if self.maze.check(potential_obstacle) == "safe" and potential_obstacle != directly_after_start:
            # if self.maze[potential_obstacle] == 1 and potential_obstacle != directly_after_start:
                self.maze.add_obstacle(potential_obstacle)
                if self.loop() == "Time_loop":
                    coordinates.add(potential_obstacle)

            self.restart()
            # if len(coordinates) == 100:
            #     break
        return len(coordinates)


    def step(self):
        next_position = self.next_position()
        next_safe = self.maze.check(next_position)
        # next_value = self.maze[next_position]  # custom data structure -- false if out of bounds

        if next_safe == "obstacle":
            self.turn()
        elif next_safe == "safe":
            self.maze.add_path(self.current_position)
            self.current_position = next_position
        elif next_safe == "outside":
            self.maze.add_path(self.current_position)
            self.current_position = False



@time_wrapper
def task1(some_input, verbose=False):
    game = Game(some_input)
    if verbose:
        print(game.maze)
    game.loop()
    if verbose:
        print(game.maze)
    return len(game.maze.path)


@time_wrapper
def task2(some_input):
    game = Game(some_input)
    return game.find_time_loops()


if __name__ == "__main__":
    print("test")
    print(task1(test_input, True))
    print(task2(test_input))
    print()

    print("real")
    print(task1(real_input))
    print(task2(real_input))