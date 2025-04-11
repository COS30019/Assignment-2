import heapq
from parse_file import find_adjacent, compute_heuristic

def astar(nodes, edges, origin, goals):
    frontier = [(compute_heuristic(nodes, origin, goals), origin, [origin], 0)]
    visited = set()
    created = 1
    while frontier:
        f, node, path, g = heapq.heappop(frontier)
        if node in goals:
            return node, created, path
        visited.add(node)

        adjacent = find_adjacent(node, edges)
        for adjacent_node, cost in adjacent:
            if adjacent_node not in visited:
                g_new = g + cost
                f_new = g_new + compute_heuristic(nodes, adjacent_node, goals)
                heapq.heappush(frontier, (f_new, adjacent_node, path + [adjacent_node], g_new))
                created += 1
    return None, created, []
