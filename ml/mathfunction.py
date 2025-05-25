import numpy as np

# Converts predicted traffic volume (flow) to estimated speed in km/h
def flow_to_speed(flow):
    a = -1.4648375
    b = 93.75
    c = -flow

    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return 5  # fallback speed

    sqrt_d = np.sqrt(discriminant)
    speed1 = (-b + sqrt_d) / (2 * a)
    speed2 = (-b - sqrt_d) / (2 * a)
    valid_speeds = [s for s in (speed1, speed2) if s > 0]
    return min(max(valid_speeds), 60) if valid_speeds else 5

# Calculates haversine distance between two lat/lon points (in kilometers)
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in km
    lat1_rad, lon1_rad = np.radians([lat1, lon1])
    lat2_rad, lon2_rad = np.radians([lat2, lon2])
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# Calculates travel time (in seconds) from flow + coordinate pair
def calculate_travel_time(flow, lat1, lon1, lat2, lon2):
    speed = flow_to_speed(flow)  # km/h
    distance = haversine_distance(lat1, lon1, lat2, lon2)  # km
    travel_time = (distance / speed) * 3600 + 30  # seconds (+30s buffer)
    return travel_time, speed, distance
