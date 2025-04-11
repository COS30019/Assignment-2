import heapq
from parse_file import compute_heuristic, find_adjacent,

def astar(nodes, edges, origin, destinations):
    frontier = []
    heapq.heappush(frontier, (0 + compute_heuristic(nodes, origin, destinations)))
    visited = set()
    created = 1
           
    while frontier:
        f, current, path, g = heapq.heappop(frontier)

        if current in destinations:
           return current, created, path
                         
        if current in visited:
           continue             
        visited.add(node)

        for adjacent_node, cost in find_adjacent(current, edges):
            if adjacent_node not in visited:
                g_new = g + cost
                f_new = g_new + compute_heuristic(nodes, adjacent_node, destinations)
                heapq.heappush(frontier, (f_new, adjacent_node, path + [adjacent_node], g_new))
                created += 1
    return None, created, []
