import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense
from plotting import plot_volume_comparisons  # assumes plotting.py is in the same folder or PYTHONPATH

# Load and prepare data
df = pd.read_excel("SCATSClean.xlsx")
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df = df.sort_values(by=['SCATS_Number', 'Timestamp']).reset_index(drop=True)

# Sequence creation function
def create_sequences(data, window_size=10):
    sequences = []
    for site_id in data['SCATS_Number'].unique():
        site_data = data[data['SCATS_Number'] == site_id].copy()
        site_data = site_data.sort_values(by='Timestamp').reset_index(drop=True)

        scaler = MinMaxScaler()
        site_data['Volume_scaled'] = scaler.fit_transform(site_data[['Traffic_Volume']])

        vol = site_data['Volume_scaled'].values
        for i in range(window_size, len(vol)):
            seq_x = vol[i - window_size:i]
            seq_y = vol[i]
            sequences.append((seq_x, seq_y, site_id, site_data.loc[i, 'Timestamp'], scaler))
    return sequences

# Create sequences
window_size = 10
all_sequences = create_sequences(df, window_size)

# Extract features
X = np.array([x[0] for x in all_sequences])
y = np.array([x[1] for x in all_sequences])
site_ids = np.array([x[2] for x in all_sequences])
timestamps = np.array([x[3] for x in all_sequences])
scalers = np.array([x[4] for x in all_sequences])

# Reshape for GRU
X = X.reshape((X.shape[0], X.shape[1], 1))

# Split data
X_train, X_test, y_train, y_test, site_train, site_test, scalers_train, scalers_test = train_test_split(
    X, y, site_ids, scalers, test_size=0.2, random_state=42, shuffle=True
)

# Scale y_train/y_test globally just for training
global_scaler = MinMaxScaler()
y_train_scaled = global_scaler.fit_transform(y_train.reshape(-1, 1))
y_test_scaled = global_scaler.transform(y_test.reshape(-1, 1))

# Build and train GRU model
model = Sequential()
model.add(GRU(units=64, return_sequences=False, input_shape=(X.shape[1], 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train_scaled, epochs=20, batch_size=32, validation_data=(X_test, y_test_scaled))

# Predict and inverse scale
y_pred_scaled = model.predict(X_test)

# Save actual and predicted values
all_predictions = []
for pred, true, scaler, site, ts in zip(y_pred_scaled, y_test, scalers_test, site_test, timestamps):
    pred_unscaled = scaler.inverse_transform([[pred[0]]])[0][0]
    true_unscaled = scaler.inverse_transform([[true]])[0][0]
    all_predictions.append({
        'Site_ID': site,
        'Timestamp': ts,
        'Actual_Volume': true_unscaled,
        'Predicted_Volume': pred_unscaled
    })


# Save to CSV
os.makedirs("results", exist_ok=True)
result_df = pd.DataFrame(all_predictions)
result_df.to_csv("results/GRU_Actual_vs_Predicted.csv", index=False)

# Generate graphs
plot_volume_comparisons(result_df, model_name="GRU")
