import pytest

from fastabm.core import Grid


def test_grid_initialization():
    grid = Grid(4, 6, int)

    assert grid.width == 4
    assert grid.height == 6

    assert len(grid.cells) == grid.height
    assert len(grid.cells[0]) == grid.width


def test_grid_initialization_bad_factory():
    with pytest.raises(ValueError):
        Grid(4, 6, lambda x: x)


def test_grid_indexing():
    grid = Grid(4, 6, int)

    # Check that no weird reference errors
    # Changing one initial value should not affect others
    grid[0, 0] = 9
    assert grid[0, 1] == 0
    assert grid[1, 0] == 0

    assert grid[0, 0] == 9
    assert grid.cells[0][0] == 9

    grid[2, 2] = 5
    assert grid[2, 2] == 5
    assert grid.cells[2][2] == 5


def test_grid_initialization_with_list():
    grid = Grid(4, 6, list)
    assert grid[0, 0] == []


def test_grid_from_iterable():
    matrix = [[1, 2], [3, 4]]
    grid = Grid.from_iterable(matrix)

    assert grid.width == 2
    assert grid.height == 2
    assert grid[0, 0] == 1
    assert grid[0, 1] == 2
    assert grid._dtype == int


def test_grid_from_iterable_references_maintained():
    matrix = [[[1], [2]], [[3], [4]]]
    grid = Grid.from_iterable(matrix)
    print(grid.cells)

    assert grid.width == 2
    assert grid.height == 2
    assert grid[0, 0] == [1]

    # Modifying original element
    matrix[0][0].append(99)
    # Should reflect in grid
    assert grid[0, 0] == [1, 99]


def test_grid_from_iterable_not_a_list():
    with pytest.raises(ValueError):
        Grid.from_iterable([1, [3, 1]])


def test_grid_from_iterable_dimension_mismatch():
    with pytest.raises(ValueError):
        Grid.from_iterable([[1, 2], [1, 2, 3]])


def test_grid_out_of_bounds():
    grid = Grid(3, 3)

    with pytest.raises(IndexError):
        grid[4, 6] = 1

    with pytest.raises(IndexError):
        _ = grid[0, 5]


def test_grid_bad_keys():
    grid = Grid(2, 2)

    with pytest.raises(KeyError):
        grid[5] = 2

    with pytest.raises(KeyError):
        grid[1, 1, 1] = 4

    with pytest.raises(KeyError):
        _ = grid[1]

    with pytest.raises(KeyError):
        _ = grid[1, 1, 1]


def test_grid_slicing():
    grid = Grid(4, 4)
    center = grid[1:3, 1:3]

    assert len(center) == 2
    assert len(center[0]) == 2


def test_grid_row_slice():
    grid = Grid(4, 4)
    grid[2, 0] = 1
    grid[2, 1] = 2
    grid[2, 2] = 3
    grid[2, 3] = 4

    row = grid[2, :]

    assert row == [1, 2, 3, 4]


def test_grid_column_slice():
    grid = Grid(4, 4)
    grid[0, 2] = 1
    grid[1, 2] = 2
    grid[2, 2] = 3
    grid[3, 2] = 4

    col = grid[:, 2]

    assert col == [1, 2, 3, 4]
