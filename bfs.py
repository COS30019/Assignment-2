import sys
from collections import deque

def bfs(nodes, edges, origin, destinations):
    frontier = deque([(origin, [origin])])
    explored = set()
    nodes_created = 1

    while frontier:
        current, path = frontier.popleft()
        if current in destinations:
            return current, nodes_created, path
        
        explored.add(current)

        for neighbor, _ in sorted(edges.get(current, [])):
            if neighbor not in explored and all(neighbor != n for n, _ in frontier):
                frontier.append((neighbor, path + [neighbor]))
                nodes_created += 1
    
    return None, nodes_created, []
