from typing import Callable, Tuple, Union


class Grid:
    _four_neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    _eight_neighbors = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

    def __init__(self, width: int, height: int, default_factory: Callable = list):
        self.width = width
        self.height = height
        self.default_factory = default_factory

        try:
            self._dtype = type(default_factory())
            self._cells = [[default_factory() for _ in range(self.width)] for _ in range(self.height)]
        except Exception as e:
            raise ValueError(f"Invalid default factory specified.\n{e}")

    @classmethod
    def from_iterable(cls, iterable):
        if not (isinstance(iterable, list) and isinstance(iterable[0], list)):
            raise ValueError("Iterable argument is not a two dimensional array.")

        height = len(iterable)
        width = len(iterable[0])

        # Check that all rows have same dimensions
        for row in iterable:
            if (not isinstance(row, list)) or len(row) != width:
                raise ValueError("Found rows with unequal dimensions.")

        # Copy rows but keep references
        grid = Grid(width, height)
        grid._dtype = type(iterable[0][0])
        grid.default_factory = grid._dtype
        grid._cells = [row for row in iterable]

        return grid

    def contains(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def get_neighborhood(self, x, y, four=False, torus=True):
        deltas = self._four_neighbors if four else self._eight_neighbors

        for delta in deltas:
            x_new = (x + delta[0]) % self.width if torus else x + delta[0]
            y_new = (y + delta[1]) % self.height if torus else y + delta[1]

            if torus or self.contains(x_new, y_new):
                yield (x_new, y_new)

    def get_neighbors(self, x, y, four=False, torus=True):
        for col, row in self.get_neighborhood(x, y, four, torus):
            if self._dtype == list:
                yield from self._cells[row][col]
            else:
                yield self._cells[row][col]

    def move(self, item, from_x, from_y, to_x, to_y, torus=True):
        if isinstance(item, list):
            raise ValueError("List item not acceptable in move.")

        if not torus and not self.contains(to_x, to_y):
            raise ValueError("Move to location is out of bounds.")

        if torus:
            from_x = from_x % self.width
            to_x = to_x % self.width
            from_y = from_y % self.height
            to_y = to_y % self.height

        if self._dtype == list:
            self._cells[from_y][from_x].remove(item)
            self._cells[to_y][to_x].append(item)
        else:
            self._cells[from_y][from_x] = self.default_factory()
            self._cells[to_y][to_x] = item

        return (to_x, to_y)

    def __setitem__(self, args: Tuple[Union[slice, int], Union[slice, int]], value):
        if not isinstance(args, tuple) or len(args) != 2:
            raise KeyError("Grid index must be a tuple [x, y]")

        self._cells[args[1]][args[0]] = value

    def __getitem__(self, args: Tuple[Union[slice, int], Union[slice, int]]):
        if not isinstance(args, tuple) or len(args) != 2:
            raise KeyError("Grid index must be a tuple [x, y]")

        # If first argument slice, use as is
        selected = self._cells[args[1]]

        # Inner lists need manual slicing however
        # First check if first element is a list
        # Ex. [[0, 1, 2]] vs [0, 1, 2]
        if isinstance(args[1], slice):
            selected = [inner[args[0]] for inner in selected]
        else:
            # Otherwise just slice or index
            selected = selected[args[0]]

        return selected

    def __iter__(self):
        for i, row in enumerate(range(self.height)):
            for j, el in enumerate(self._cells[row]):
                yield el, (i, j)
