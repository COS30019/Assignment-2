import heapq
from parse_file import compute_heuristic, find_adjacent
# Load GRU-predicted travel times between SCATS sites
gru_travel_times = {
    ('2000', '3001'): 125.6,
    ('3001', '3002'): 91.2,
    # Add the rest of your GRU outputs here as (origin, destination): time_in_seconds
}

def astar(nodes, edges, origin, destinations):
    frontier = []
    heapq.heappush(frontier, (0 + compute_heuristic(nodes, origin, destinations), origin, [origin], 0))
    visited = set()
    created = 1
    
    while frontier:
        f, current, path, g = heapq.heappop(frontier)
        if current in destinations:
             return current, created, path
        
        if current in visited:
             continue
        visited.add(current)
        
        for adjacent_node in find_adjacent(current, edges):
             cost = gru_travel_times.get((current, adjacent_node), 9999)  # fallback if not found
            if adjacent_node not in visited:
                g_new = g + cost
                f_new = g_new + compute_heuristic(nodes, adjacent_node, destinations)
                heapq.heappush(frontier, (f_new, adjacent_node, path + [adjacent_node], g_new))
                created += 1
    return None, created, []
