from collections import deque
from parse_file import find_adjacent

def bfs(nodes, edges, origin, destinations):
    frontier = deque()
    frontier.append((origin, [origin]))
    visited = set()
    nodes_created = 1

    while frontier:
        current_node, path = frontier.popleft()

        if current_node in destinations:
            return current_node, nodes_created, path

        if current_node not in visited:
            visited.add(current_node)

            neighbors = [(end, cost) for (start, end), cost in edges.items() if start == current_node]
            neighbors.sort()

            for neighbor, _ in find_adjacent(current_node,edges):
                if neighbor not in visited:
                    frontier.append((neighbor, path + [neighbor]))
                    nodes_created +=1

    return None, nodes_created, []
