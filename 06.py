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
        self.temp_obs = []

        if some_input is not None:
            self.init_from_input(some_input)

    def init_from_input(self, some_input):
        self.values = [[self.symbol_to_value[elem] for elem in line] for line in some_input.splitlines() if
                       len(line.strip()) > 0]
        self.height = len(self.values)
        self.width = len(self.values[0])
        assert all(len(v) == self.width for v in self.values)
        self.path = set()
        self.start_position = self.find_current_position()

    #
    # def clone(self) -> "Maze":
    #     other = Maze()
    #     other.values = self.values
    #     other.height = self.height
    #     other.width = self.width
    #     other.path = self.path
    #     return other

    def find_current_position(self):
        for i, row in enumerate(self.values):
            for j, elem in enumerate(row):
                if elem == self.symbol_to_value["^"]:
                    assert self[i, j] == 2
                    return i, j

    # def __copy__(self):
    #     return Maze(self.values)
    #
    # def __deepcopy__(self, memo):
    #     return Maze(copy.deepcopy(self.values))

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
            self.maze = Maze(some_input)
        else:
            assert isinstance(maze, Maze)
            assert some_input is None
            self.maze = maze
        self.current_position = self.maze.start_position
        self.current_direction = "n"
        self.state_cache = set()

        self.__move_by_direction ={
                "n": (-1, 0),
                "e": (0, 1),
                "s": (1, 0),
                "w": (0, -1),
                }
        self.__turn_by_direction ={"n": "e", "e": "s", "s": "w", "w": "n"}

    def restart(self):
        self.maze.reset()
        self.current_position = self.maze.start_position
        self.current_direction = "n"
        self.state_cache = set()

    def turn(self):
        self.current_direction = self.__turn_by_direction[self.current_direction]

    def next_position(self):
        move = self.__move_by_direction[self.current_direction]
        next_position = tuple(c + m for (c, m) in zip(self.current_position, move))
        return next_position

    def loop(self, verbose=False):
        if verbose:
            print(self.maze)

        while self.current_position:

            state = hash(self.current_position) + hash(self.current_direction)
            if state in self.state_cache:
                return "Time_loop"
            self.state_cache.add(state)

            self.step()

        if verbose:
            print(self.maze)


    def find_time_loops(self, ):
        directly_after_start = self.next_position()
        coordinates = set()
        # path = self.loop(return_path=True)
        self.loop()
        path = self.maze.path
        self.restart()
        for obstacle in path:
            if self.maze[obstacle] == 1 and obstacle != directly_after_start:
                self.maze[obstacle] = 9
                if self.loop() == "Time_loop":
                    # new_game = Game(maze = self.maze)
                    # if new_game.loop() == "Time_loop":
                    coordinates.add(obstacle)
            # clear everything again
            self.restart()
            self.maze[obstacle] = 1
            # if len(coordinates) == 20:
            #     break
        return len(coordinates)

    def step(self):
        next_position = self.next_position()
        next_value = self.maze[next_position]  # custom data structure -- false if out of bounds

        if not next_value:
            self.maze.add_path(self.current_position)
            self.current_position = False

        elif next_value == 9:
            self.turn()

        else:
            assert next_value in [1, 3]  # visited or not visited
            # if next_value == 3:
            #     self.fields_visited -= 1

            self.maze[next_position] = 2
            self.maze.add_path(self.current_position)
            self.current_position = next_position


@time_wrapper
def task1(some_input):
    game = Game(some_input)
    game.loop()
    return len(game.maze.path)


@time_wrapper
def task2(some_input):
    game = Game(some_input)
    return game.find_time_loops()


if __name__ == "__main__":
    print("test")
    print(task1(test_input))
    print(task2(test_input))
    print()

    print("real")
    print(task1(real_input))
    print(task2(real_input))