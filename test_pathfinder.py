from PathFinder import *


def test_empty_maze():
    maze = Mazze(maze=MAZE)
    routes = maze.find_route((0, 0), (9, 9))
    assert isinstance(routes, list)
