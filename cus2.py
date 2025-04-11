import heapq
from parse_file import compute_heuristic, find_adjacent

def cus2(nodes, edges, origin, destinations):
    frontier = []
    heapq.heappush(frontier, (0 + compute_heuristic(nodes, origin, destinations), origin, [origin], 0))
    visited = set()
    created = 1

    while frontier:
        f, current, path, depth = heapq.heappop(frontier)

        if current in destinations:
            return current, created, path

        if current in visited:
            continue
        visited.add(current)

        for neighbor, _ in find_adjacent(current, edges):
            if neighbor not in visited:
                new_depth = depth + 1
                f_new = compute_heuristic(nodes, neighbor, destinations) + new_depth * 0.5
                heapq.heappush(frontier, (f_new, neighbor, path + [neighbor], new_depth))
                created += 1

    return None, created, []
