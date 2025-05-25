import pandas as pd
from geopy.distance import geodesic

EDGE_FILE = "edges_possible.csv"

def load_nodes():
    df = pd.read_csv(EDGE_FILE)
    df.columns = df.columns.str.strip()
    node_ids = set(df['From']).union(set(df['To']))
    return {node: {} for node in node_ids}

def load_edges():
    df = pd.read_csv(EDGE_FILE)
    df.columns = df.columns.str.strip()
    forward = [(row['From'], row['To']) for _, row in df.iterrows()]
    reverse = [(to, frm) for frm, to in forward]
    return forward + reverse


# Provide latlong_map from main.py to this file
latlong_map = {}  # <-- This will be set from main.py

def compute_heuristic(nodes, current, goals):
    if current not in latlong_map:
        return 0

    min_time = float('inf')
    for goal in goals:
        if goal in latlong_map:
            coord1 = latlong_map[current]
            coord2 = latlong_map[goal]
            distance = geodesic(coord1, coord2).meters
            time = distance / 16.67  # Convert meters to seconds assuming 60 km/h
            min_time = min(min_time, time)

    return min_time if min_time != float('inf') else 0


def find_adjacent(current, edges):
    return [to for frm, to in edges if frm == current]
