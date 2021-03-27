import pytest

from fastabm.core import Grid


def test_grid_initialization():
    grid = Grid(4, 6, int)

    assert grid.width == 4
    assert grid.height == 6

    assert len(grid._cells) == grid.height
    assert len(grid._cells[0]) == grid.width


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
    assert grid._cells[0][0] == 9

    grid[2, 2] = 5
    assert grid[2, 2] == 5
    assert grid._cells[2][2] == 5


def test_grid_initialization_with_list():
    grid = Grid(4, 6, list)
    assert grid[0, 0] == []


def test_grid_from_iterable():
    matrix = [[1, 2], [3, 4]]
    grid = Grid.from_iterable(matrix)

    assert grid.width == 2
    assert grid.height == 2
    assert grid[0, 0] == 1
    assert grid[0, 1] == 3
    assert grid._dtype == int


def test_grid_from_iterable_references_maintained():
    matrix = [[[1], [2]], [[3], [4]]]
    grid = Grid.from_iterable(matrix)

    assert grid.width == 2
    assert grid.height == 2
    assert grid[0, 0] == [1]
    assert grid[0, 1] == [3]

    # Modifying original element
    matrix[0][0].append(99)

    # Should reflect in grid
    assert grid[0, 0] == [1, 99]


def test_grid_from_iterable_not_a_list():
    with pytest.raises(ValueError):
        Grid.from_iterable([1, [3, 1]])


def test_grid_contains():
    grid = Grid(2, 2)

    assert grid.contains(0, 0)
    assert grid.contains(1, 1)
    assert grid.contains(1, 2) is False


def test_grid_get_8_neighborhood():

    grid = Grid(4, 4)

    neighborhood = set(grid.get_neighborhood(2, 2))
    expected_neighborhood = set([(1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (1, 2)])

    assert neighborhood == expected_neighborhood


def test_grid_get_8_neighborhood_torus():

    grid = Grid(4, 4)

    neighborhood = set(grid.get_neighborhood(3, 3))
    expected_neighborhood = set([(0, 3), (0, 0), (3, 0), (2, 0), (2, 3), (2, 2), (3, 2), (0, 2)])

    assert neighborhood == expected_neighborhood


def test_grid_get_8_neighborhood_no_torus():

    grid = Grid(4, 4)

    neighborhood = set(grid.get_neighborhood(3, 3, torus=False))
    expected_neighborhood = set([(2, 3), (2, 2), (3, 2)])

    assert neighborhood == expected_neighborhood


def test_grid_get_4_neighborhood():

    grid = Grid(4, 4)

    neighborhood = set(grid.get_neighborhood(2, 2, four=True))
    expected_neighborhood = set([(2, 1), (3, 2), (2, 3), (1, 2)])

    assert neighborhood == expected_neighborhood


def test_grid_get_4_neighborhood_torus():

    grid = Grid(4, 4)

    neighborhood = set(grid.get_neighborhood(3, 3, four=True))
    expected_neighborhood = set([(0, 3), (3, 0), (2, 3), (3, 2)])

    assert neighborhood == expected_neighborhood


def test_grid_get_4_neighborhood_no_torus():

    grid = Grid(4, 4)

    neighborhood = set(grid.get_neighborhood(3, 3, four=True, torus=False))
    expected_neighborhood = set([(2, 3), (3, 2)])

    assert neighborhood == expected_neighborhood


def test_grid_get_neighbors():
    matrix = [[1, 2, 3, 4], [4, 5, 6, 7], [7, 8, 9, 10], [11, 12, 13, 14]]
    grid = Grid.from_iterable(matrix)

    neighbors = list(grid.get_neighbors(0, 2, four=True))

    assert set(neighbors) == set([8, 10, 4, 11])


def test_grid_get_neighbors_iterables():
    matrix = [[[1], [2, 3], []], [[4], [5], []], [[6, 7, 8], [], []]]
    grid = Grid.from_iterable(matrix)

    neighbors = list(grid.get_neighbors(1, 1, four=True))

    assert set(neighbors) == set([2, 3, 4])


def test_grid_move():
    matrix = matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    grid = Grid.from_iterable(matrix)

    (nx, ny) = grid.move(matrix[0][0], 0, 0, 1, 0)

    assert grid[1, 0] == 1
    assert grid[0, 0] == 0
    assert nx == 1
    assert ny == 0

    grid.move(matrix[0][1], 1, 0, 0, 0)
    assert grid[1, 0] == 0
    assert grid[0, 0] == 1


def test_grid_move_torus():
    matrix = matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    grid = Grid.from_iterable(matrix)

    (nx, ny) = grid.move(matrix[0][0], 0, 0, 4, 0)

    assert grid[1, 0] == 1
    assert grid[0, 0] == 0
    assert nx == 1
    assert ny == 0


def test_grid_move_out_of_bounds():
    matrix = matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    grid = Grid.from_iterable(matrix)

    (nx, ny) = grid.move(matrix[0][0], 0, 0, 1, 0, torus=False)
    assert nx == 1
    assert ny == 0

    with pytest.raises(ValueError):
        (nx, ny) = grid.move(matrix[0][0], 0, 0, 4, 0, torus=False)


def test_grid_move_list_error():
    matrix = matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    grid = Grid.from_iterable(matrix)

    with pytest.raises(ValueError):
        (nx, ny) = grid.move([matrix[0][0]], 0, 0, 1, 0)
        assert nx == 1
        assert ny == 0


def test_grid_move_with_iterables():
    matrix = [[[1], [2, 3]], [[4], [5]], [[6, 7, 8], []]]
    grid = Grid.from_iterable(matrix)

    grid.move(matrix[0][0][0], 0, 0, 1, 0)

    assert grid[1, 0] == [2, 3, 1]
    assert grid[0, 0] == []

    grid.move(matrix[0][1][2], 1, 0, 0, 0)
    assert grid[1, 0] == [2, 3]
    assert grid[0, 0] == [1]


def test_grid_from_iterable_dimension_mismatch():
    with pytest.raises(ValueError):
        Grid.from_iterable([[1, 2], [1, 2, 3]])


def test_grid_out_of_bounds():
    grid = Grid(3, 3)

    with pytest.raises(IndexError):
        grid[4, 6] = 1

    with pytest.raises(IndexError):
        _ = grid[0, 5]


def test_grid_iterable():
    grid = Grid(3, 2)

    expected_order = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    actual_order = [(r, c) for el, (r, c) in grid]

    assert actual_order == expected_order


def test_grid_iterable_list_elements():

    matrix = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    grid = Grid.from_iterable(matrix)

    for el, (row, col) in grid:
        assert el == matrix[row][col]


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
