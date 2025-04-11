import sys
from parse_file import populate_graph, find_adjacent

def dfs(nodes, edges, origin, destinations):
    nodes_visited = set()
    stack = [(origin, [origin], 0)]
    nodes_created = 1

    while stack:
        node, path, cost = stack.pop()

        if node in nodes_visited:
            continue
        
        nodes_visited.add(node)

        if node in destinations:
            return node, nodes_created, path
        
        adjacent = find_adjacent(node, edges)

        for adjacent, edge_cost in reversed(adjacent):
            if adjacent not in nodes_visited:
                stack.append((adjacent, path + [adjacent], cost + edge_cost))
                nodes_created = nodes_created + 1
                
    return None, nodes_created, []
