from typing import Tuple, Callable


class Grid:
    def __init__(self, width: int, height: int, default_factory: Callable = int):
        self.width = width
        self.height = height

        try:
            self._dtype = type(default_factory())
            self.cells = [[default_factory() for _ in range(self.width)] for _ in range(self.height)]
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
        grid.cells = [row for row in iterable]

        return grid

    def __setitem__(self, args: Tuple[int, int], value):
        if not isinstance(args, tuple) or len(args) != 2:
            raise KeyError("Grid index must be a tuple [x, y]")

        self.cells[args[0]][args[1]] = value

    def __getitem__(self, args: Tuple[int, int]):
        if not isinstance(args, tuple) or len(args) != 2:
            raise KeyError("Grid index must be a tuple [x, y]")

        # If first argument slice, use as is
        selected = self.cells[args[0]]

        # Inner lists need manual slicing however
        # First check if first element is a list
        # Ex. [[0, 1, 2]] vs [0, 1, 2]
        if isinstance(selected[0], list) and self._dtype != list:
            selected = [inner[args[1]] for inner in selected]
        else:
            # Otherwise just slice
            selected = selected[args[1]]

        return selected
