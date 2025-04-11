import sys
from dfs import dfs
from bfs import bfs
from gbfs import gbfs
from astar import astar
from cus1 import cus1
from cus2 import cus2

def search():
    if len(sys.argv) != 3:
        print("Incorrect number of arguments")
        sys.exit()

    filename = sys.argv[1]
    method = sys.argv[2].lower()

    methods = {
        "dfs": dfs,
        "bfs": bfs,
        "gbfs": gbfs,
        "as": astar,
        "cus1": cus1,
        "cus2": cus2
    }

    if method not in methods:
        print("Unknown method")
        sys.exit()

    selected_method = methods[method]
    goal, nodes_created, path = selected_method(filename, method)

    if goal:
        print('{} {}'.format(filename, method))
        print('{} {}'.format(goal, nodes_created))
        print(", ".join([str(node) for node in path]))
    else:
        print("Goal not found")

if __name__ == "__main__":
    search()