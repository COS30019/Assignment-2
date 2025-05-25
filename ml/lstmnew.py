import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
from plotting import plot_volume_comparisons
import os

# Load and clean data
df = pd.read_excel("SCATSClean.xlsx")
df.dropna(inplace=True)
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df = df.sort_values(by=['SCATS_Number', 'Timestamp'])

# Create sequences
def create_sequences(data, window=4):
    X, y = [], []
    for i in range(len(data) - window):
        X.append(data[i:i+window])
        y.append(data[i+window])
    return np.array(X), np.array(y)

all_predictions = []
performance = []  # ✅ moved to the top before loop

# Loop through each SCATS site
for site_id in df['SCATS_Number'].unique():
    print(f"\n=== Processing Site ID: {site_id} ===")

    site_data = df[df['SCATS_Number'] == site_id]
    site_data = site_data.set_index('Timestamp').resample('h').sum().fillna(0)

    if len(site_data) < 20:
        print("Skipping due to insufficient data.")
        continue

    # Fit scaler on original data
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(site_data[['Traffic_Volume']])

    # Create input-output sequences
    X, y = create_sequences(scaled, window=4)
    if len(X) == 0:
        print("Skipping due to insufficient sequences.")
        continue

    X = X.reshape((X.shape[0], X.shape[1], 1))

    # Train/test split
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # Build LSTM model
    model = Sequential()
    model.add(Input(shape=(X.shape[1], 1)))
    model.add(LSTM(64))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)

    # Predict and inverse scale
    y_pred_scaled = model.predict(X_test, verbose=0)
    y_pred = scaler.inverse_transform(y_pred_scaled)
    y_test_actual = scaler.inverse_transform(y_test)

    # Save predictions with actual values
    timestamps = site_data.index[split:]  # get corresponding timestamps for y_test

    for actual, pred, ts in zip(y_test_actual.flatten(), y_pred.flatten(), timestamps):
        all_predictions.append({
            'Site_ID': site_id,
            'Timestamp': ts,
            'Actual_Volume': actual,
            'Predicted_Volume': pred
        })


    # Metrics
    rmse = np.sqrt(mean_squared_error(y_test_actual, y_pred))
    mae = mean_absolute_error(y_test_actual, y_pred)
    print(f" RMSE: {rmse:.2f}, MAE: {mae:.2f}")

    # Save performance per site
    performance.append({
        'Site_ID': site_id,
        'RMSE': round(rmse, 2),
        'MAE': round(mae, 2)
    })

# Export actual vs predicted to CSV
os.makedirs("results", exist_ok=True)
pred_df = pd.DataFrame(all_predictions)
pred_df.to_csv("results/LSTM_Actual_vs_Predicted.csv", index=False)

# Call the graph generator
plot_volume_comparisons(pred_df, model_name="LSTM")

# Export performance summary
performance_df = pd.DataFrame(performance)
performance_df = performance_df.sort_values(by='RMSE')
performance_df.to_csv("results/LSTM_Performance_Summary.csv", index=False)

print("\n LSTM Performance Summary")
print(performance_df.to_string(index=False))

# Show best-performing site
best = performance_df.iloc[0]
print(f"\n Best Performing Site: {int(best['Site_ID'])} (RMSE: {best['RMSE']}, MAE: {best['MAE']})")
