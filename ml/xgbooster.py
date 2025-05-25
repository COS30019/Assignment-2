import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import os
import joblib

def train_xgboost_for_site(site_data, site_id, output_plot_dir):
    site_data['Timestamp'] = pd.to_datetime(site_data['Timestamp'])
    site_data = site_data.sort_values(by='Timestamp').reset_index(drop=True)

    xgb_df = site_data[['Timestamp', 'Traffic_Volume']].copy()

    xgb_df.rename(columns={'Traffic_Volume': 'Volume'}, inplace=True)

    scaler = MinMaxScaler()
    xgb_df['Volume_scaled'] = scaler.fit_transform(xgb_df[['Volume']])

    xgb_df['hour'] = xgb_df['Timestamp'].dt.hour
    xgb_df['minute'] = xgb_df['Timestamp'].dt.minute
    xgb_df['dayofweek'] = xgb_df['Timestamp'].dt.dayofweek
    xgb_df['is_weekend'] = (xgb_df['dayofweek'] >= 5).astype(int)

    for i in range(1, 11):
        xgb_df[f'lag{i}'] = xgb_df['Volume_scaled'].shift(i)

    xgb_df = xgb_df.dropna().reset_index(drop=True)

    x = xgb_df.drop(['Timestamp', 'Volume', 'Volume_scaled'], axis=1)
    y = xgb_df['Volume_scaled']

    split = int(0.8 * len(x))
    x_train, x_test = x[:split], x[split:]
    y_train, y_test = y[:split], y[split:]

    model = xgb.XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        gamma=0,
        subsample=0.8,
        colsample_bytree=0.8,
        objective='reg:squarederror'
    )

    model.fit(
        x_train,
        y_train,
        eval_set=[(x_train, y_train), (x_test, y_test)],
        verbose=False,
    )

    y_pred_scaled = model.predict(x_test)

    y_pred_inv = scaler.inverse_transform(y_pred_scaled.reshape(-1, 1))
    y_test_inv = scaler.inverse_transform(y_test.values.reshape(-1, 1))

    rmse = np.sqrt(mean_squared_error(y_test_inv, y_pred_inv))
    mae = mean_absolute_error(y_test_inv, y_pred_inv)
    print(f"Site {site_id} - RMSE: {rmse:.4f}, MAE: {mae:.4f}")

    if not os.path.exists(output_plot_dir):
        os.makedirs(output_plot_dir)
    
    plt.figure(figsize=(12, 6))
    plt.plot(y_test_inv, label='Actual Traffic Volume', color='blue')
    plt.plot(y_pred_inv, label='Predicted Traffic Volume', color='orange')
    plt.title(f"XGBoost - Traffic Volume Prediction ({site_id})")
    plt.xlabel("Time Interval")
    plt.ylabel("Traffic Volume")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_plot_dir, f"xgboost_graph_{site_id}.png"))
    plt.close()

    return model, rmse, mae

if __name__ == "__main__":
    main_df = pd.read_excel("SCATSClean.xlsx")
    all_site_ids = main_df['SCATS_Number'].unique()

    trained_models = {}
    performance_metrics = {}
    
    plot_output_directory = "xgboost_graphs"
    model_output_directory = "xgboost_trained_models"

    if not os.path.exists(model_output_directory):
        os.makedirs(model_output_directory)

    for site_id in all_site_ids:
        current_site_df = main_df[main_df['SCATS_Number'] == site_id][['Timestamp', 'Traffic_Volume']].copy()
        
        if current_site_df.empty:
            continue

        model, rmse, mae = train_xgboost_for_site(current_site_df, site_id, plot_output_directory)
        
        if model is not None:
            trained_models[site_id] = model
            performance_metrics[site_id] = {'RMSE': rmse, 'MAE': mae}

            model_filename = os.path.join(model_output_directory, f"xgboost_model_{site_id}.joblib")
            joblib.dump(model, model_filename)

# === OPTIONAL: Export predictions and plot ===
from plotting import plot_volume_comparisons

# Create a list to collect all predictions
all_predictions = []

for site_id, model in trained_models.items():
    # Load and prepare site data again
    current_site_df = main_df[main_df['SCATS_Number'] == site_id][['Timestamp', 'Traffic_Volume']].copy()
    current_site_df['Timestamp'] = pd.to_datetime(current_site_df['Timestamp'])
    current_site_df = current_site_df.sort_values(by='Timestamp').reset_index(drop=True)

    scaler = MinMaxScaler()
    current_site_df['Volume_scaled'] = scaler.fit_transform(current_site_df[['Traffic_Volume']])

    current_site_df['hour'] = current_site_df['Timestamp'].dt.hour
    current_site_df['minute'] = current_site_df['Timestamp'].dt.minute
    current_site_df['dayofweek'] = current_site_df['Timestamp'].dt.dayofweek
    current_site_df['is_weekend'] = (current_site_df['dayofweek'] >= 5).astype(int)

    for i in range(1, 11):
        current_site_df[f'lag{i}'] = current_site_df['Volume_scaled'].shift(i)

    current_site_df = current_site_df.dropna().reset_index(drop=True)

    x = current_site_df.drop(['Timestamp', 'Traffic_Volume', 'Volume_scaled'], axis=1)
    y = current_site_df['Volume_scaled']

    split = int(0.8 * len(x))
    x_test = x[split:]
    y_test = y[split:]

    y_pred_scaled = model.predict(x_test)
    y_pred_inv = scaler.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()
    y_test_inv = scaler.inverse_transform(y_test.values.reshape(-1, 1)).flatten()

    timestamps = current_site_df['Timestamp'].iloc[split:].values

    for actual, pred, ts in zip(y_test_inv, y_pred_inv, timestamps):
        all_predictions.append({
            'Site_ID': site_id,
            'Timestamp': ts,
            'Actual_Volume': actual,
            'Predicted_Volume': pred
        })


# Save and plot
os.makedirs("results", exist_ok=True)
df_preds = pd.DataFrame(all_predictions)
df_preds.to_csv("results/XGBoost_Actual_vs_Predicted.csv", index=False)

plot_volume_comparisons(df_preds, model_name="XGBoost")
