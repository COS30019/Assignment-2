

def bfs(nodes, edges, origin, destinations):
    frontier = deque()
    frontier.append((origin, [origin]))
    visited = set()
    nodes_created = 0

    while frontier:
        current_node, path = frontier.popleft()
        nodes_created += 1

        if current_node in destinations:
            return current_node, nodes_created, path

        if current_node not in visited:
            visited.add(current_node)

            neighbors = [(end, cost) for (start, end), cost in edges.items() if start == current_node]
            neighbors.sort()

            for neighbor, _ in neighbors:
                if neighbor not in visited:
                    frontier.append((neighbor, path + [neighbor]))

    return None, nodes_created, []
