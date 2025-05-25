import pandas as pd
from itertools import combinations
from geopy.distance import geodesic

# === Load site coordinates from Excel ===
latlong_df = pd.read_excel("LatLongGoogleMaps 1 (1).xlsx")  # Change filename if needed
latlong_df.columns = [col.strip().lower() for col in latlong_df.columns]
latlong_df = latlong_df.rename(columns={"site id": "site_id", "latitude": "lat", "longitude": "long"})

# === Create all 780 edges between 40 sites ===
site_pairs = list(combinations(latlong_df.itertuples(index=False), 2))

edges = []
for site1, site2 in site_pairs:
    coord1 = (site1.lat, site1.long)
    coord2 = (site2.lat, site2.long)
    distance = geodesic(coord1, coord2).meters
    edges.append({
        "From": site1.site_id,
        "To": site2.site_id,
        "Distance": round(distance, 2)
    })

# === Save to CSV ===
edges_df = pd.DataFrame(edges)
edges_df_sorted = edges_df.sort_values(by=["From", "To"])
edges_df_sorted.to_csv("edges_possible.csv", index=False)

print(" edges_possible.csv created with", len(edges_df_sorted), "edges.")

