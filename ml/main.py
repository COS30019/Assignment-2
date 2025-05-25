import pandas as pd
import os
import sys
import parse_file
import subprocess
from mathfunction import calculate_travel_time
from parse_file import load_nodes, load_edges
from astar import astar  
from kshort import k_shortest_paths


# File paths
EDGE_FILE = "edges_possible.csv"
LATLONG_FILE = "LatLongGoogleMaps 1 (1).xlsx"
PREDICTION_FILES = {
    "GRU": "results/GRU_Actual_vs_Predicted.csv",
    "LSTM": "results/LSTM_Actual_vs_Predicted.csv",
    "XGBoost": "results/XGBoost_Actual_vs_Predicted.csv"
}
MODEL_SCRIPTS = {
    "GRU": "gru.py",
    "LSTM": "lstmnew.py",
    "XGBoost": "xgbooster.py"
}

# Run ML models first
def run_all_models():
    print(" Checking for existing model output files...")

    all_exist = all(os.path.exists(path) for path in PREDICTION_FILES.values())

    if all_exist:
        print("  All model output files found. Skipping model execution.\n")
        return

    print("Running all ML models (GRU, LSTM, XGBoost)...")
    for model, script in MODEL_SCRIPTS.items():
        print(f" Running {model} model...")
        result = subprocess.run([sys.executable, script], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  Error running {model}:")
            print(result.stderr)
        else:
            print(f"  {model} completed successfully.")
    print("  All model outputs saved in /results folder.\n")


# Generate edges before running anything else
print(" Generating edge file using edge_gen.py...")
result = subprocess.run([sys.executable, "edges_gen.py"], capture_output=True, text=True)

if result.returncode != 0:
    print("Error running edge_gen.py:")
    print(result.stderr)
    sys.exit(1)
else:
    print("Edge file generated successfully.")

# Load lat-long map
def build_latlong_dict(latlong_file):
    df = pd.read_excel(latlong_file)
    df.columns = df.columns.str.strip()

    # Rename your actual columns to expected names
    df.rename(columns={
        'Site ID': 'SCATS Number',
        'Lat': 'Latitude',
        'Long': 'Longitude'
    }, inplace=True)

    if 'SCATS Number' not in df.columns or 'Latitude' not in df.columns or 'Longitude' not in df.columns:
        raise ValueError("Missing expected columns in lat/long file.")

    return dict(zip(df['SCATS Number'], zip(df['Latitude'], df['Longitude'])))


# Build travel time lookup
def build_travel_time_lookup(model_name, edge_file, prediction_file, latlong_map):
    edges_df = pd.read_csv(edge_file)
    pred_df = pd.read_csv(prediction_file)
    travel_time_lookup = {}
   

    for _, row in edges_df.iterrows():
        start, end = row['From'], row['To']
        if start not in latlong_map or end not in latlong_map:
            continue

        match = pred_df[(pred_df['Site_ID'] == end)].sort_values(by='Timestamp', ascending=False).head(1)
        if match.empty:
            continue

        volume = match['Predicted_Volume'].values[0]
        lat1, lon1 = latlong_map[start]
        lat2, lon2 = latlong_map[end]
        travel_time, _, _ = calculate_travel_time(volume, lat1, lon1, lat2, lon2)
        travel_time_lookup[(start, end)] = travel_time
        travel_time_lookup[(end, start)] = travel_time  


    return travel_time_lookup

# Main program
def main():
    run_all_models()

    while True:
        print(" Welcome to the Traffic-Based Route Guidance System (TBRGS)")

        nodes = load_nodes()
        edges = load_edges()

        try:
            origin = int(input("Enter origin SCATS site number: "))
            destination = int(input("Enter destination SCATS site number: "))
        except ValueError:
            print(" Invalid input. Please enter numeric SCATS site numbers.")
            continue

        print("Select model to use: [1] GRU, [2] LSTM, [3] XGBoost")
        model_input = input("Enter choice (1/2/3): ").strip()
        model_map = {'1': 'GRU', '2': 'LSTM', '3': 'XGBoost'}
        model_name = model_map.get(model_input)

        if model_name not in PREDICTION_FILES:
            print(" Invalid model choice. Please try again.")
            continue

        print(f"\n Using model: {model_name}")

        latlong_map = build_latlong_dict(LATLONG_FILE)
        parse_file.latlong_map = latlong_map
        travel_time_lookup = build_travel_time_lookup(model_name, EDGE_FILE, PREDICTION_FILES[model_name], latlong_map)

        goal, created, path, total_time = astar(nodes, edges, origin, [destination], travel_time_lookup)

        if path:
            print("\n A* Optimal Route:")
            print(f"→ Path: {' -> '.join(map(str, path))}")
            print(f"Total predicted travel time: {total_time:.2f} seconds")
            print(f"Nodes created: {created}")
            print("Finding alternative paths using Yen's algorithm...")
            alt_paths = k_shortest_paths(edges, travel_time_lookup, origin, destination, k=10)
            # Filter out the A* path
            alt_paths = [p for p in alt_paths if p[0] != path][:4]
            if alt_paths:
                print("\n Alternative Routes (via Yen's):")
                for i, (alt_path, alt_time) in enumerate(alt_paths, 1):
                    print(f"Alt {i}: {' -> '.join(map(str, alt_path))} | Time: {alt_time:.2f} sec")
            else:
                print("\n No alternative paths found.")
        else:
            print(" No path found.")


        # Ask the user if they want to try again
        cont = input("\n Do you want to find another route? (yes/no): ").strip().lower()
        if cont not in ["yes", "y"]:
            print(" Exiting the system. Goodbye!")
            break

if __name__ == "__main__":
    main()
