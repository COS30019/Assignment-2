import heapq
from parse_file import compute_heuristic

def gbfs(nodes, edges, origin, destinations):
    frontier = []
    explored = set()
    created = 0

    heapq.heappush(frontier, (compute_heuristic(nodes, origin, destinations), origin, [origin]))
    created += 1

    while frontier:
        h, node, route = heapq.heappop(frontier)
        
        if node in destinations:
            return node, created, route

        if node in explored:
            continue

        explored.add(node)

        for edge, cost in edges.items():
            src, dst = edge
            if src == node and dst not in explored:
                updated_route = route + [dst]
                heapq.heappush(frontier, (compute_heuristic(nodes, dst, destinations), dst, updated_route))
                created += 1

    return None, created, []
