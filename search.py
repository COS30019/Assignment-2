import sys
from parse_file import populate_graph
from dfs import dfs
from bfs import bfs
from gbfs import gbfs
from astar import astar
from dls import cus1
from bs import bs

def search():
    if len(sys.argv) != 3:
        print("Incorrect number of arguments")
        sys.exit()

    filename = sys.argv[1]
    method = sys.argv[2].lower()

    nodes, edges, origin, destinations = populate_graph(filename)

    methods = {
        "dfs": dfs,
        "bfs": bfs,
        "gbfs": gbfs,
        "as": astar,
        "dls": cus1,
        "bs": bs
    }

    if method not in methods:
        print("Unknown method")
        sys.exit()

    selected_method = methods[method]
    goal, nodes_created, path = selected_method(nodes, edges, origin, destinations)

    if goal:
        print('{} {}'.format(filename, method))
        print('{} {}'.format(goal, nodes_created))
        print(", ".join([str(node) for node in path]))
    else:
        print("Goal not found")

if __name__ == "__main__":
    search()
