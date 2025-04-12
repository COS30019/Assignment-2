from parse_file import compute_heuristic, find_adjacent

def bs(nodes, edges, origin, destinations, beam_width = 3):
    current_level = [(compute_heuristic(nodes, origin, destinations), origin, [origin], 0)]
    visited = set()
    created = 1

    while current_level:
        possible_nodes = []
        
        for _, current, path, g in current_level:
            if current in destinations:
                return current, created, path
            
            if current in visited:
                continue

            visited.add(current)

            for adjacent_node, cost in find_adjacent(current, edges):
                if adjacent_node not in visited:
                    g_new = g + cost
                    h_new = compute_heuristic(nodes, adjacent_node, destinations)
                    f_new = g_new + h_new
                    possible_nodes.append((f_new, adjacent_node, path + [adjacent_node], g_new))
                    created = created + 1

            if not possible_nodes:
                break

            possible_nodes.sort()

            current_level = possible_nodes[:beam_width]

    return None, created, []