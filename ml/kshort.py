# kshort.py
import networkx as nx

def k_shortest_paths(edges, travel_time_lookup, origin, destination, k=4):
    G = nx.DiGraph()

    # Add edges with weights (skip unusable ones)
    for a, b in edges:
        weight = travel_time_lookup.get((a, b), 9999)
        if weight < 9999:
            G.add_edge(a, b, weight=weight)

    if not G.has_node(origin) or not G.has_node(destination):
        print(" Origin or destination not in graph.")
        return []

    try:
        # Generator for shortest simple paths (Yen's Algorithm)
        path_gen = nx.shortest_simple_paths(G, origin, destination, weight='weight')
        results = []

        for path in path_gen:
            if len(results) >= k:
                break
            try:
                total_time = sum(
                    travel_time_lookup.get((path[i], path[i+1]), 9999)
                    for i in range(len(path) - 1)
                )
                results.append((path, total_time))
            except Exception as e:
                print(f" Skipping invalid path due to error: {e}")
                continue

        return results

    except nx.NetworkXNoPath:
        print(" No path found (Yen's).")
        return []
    except Exception as e:
        print(f" Unexpected error during Yen's algorithm: {e}")
        return []
