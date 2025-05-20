import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error

df = pd.read_csv("Final_SCATS_with_LatLong.csv")
site_df = df[df['Site ID'] == 970].copy()
site_df['Timestamp'] = pd.to_datetime(site_df['Timestamp'])
site_df = site_df.sort_values(by='Timestamp').reset_index(drop=True)

xgb_df = site_df[['Timestamp', 'Volume']].copy()

# Scale values to range 0 - 1.
scaler = MinMaxScaler()
xgb_df['Volume_scaled'] = scaler.fit_transform(xgb_df[['Volume']])

xgb_df['hour'] = xgb_df['Timestamp'].dt.hour
xgb_df['minute'] = xgb_df['Timestamp'].dt.minute
xgb_df['dayofweek'] = xgb_df['Timestamp'].dt.dayofweek
xgb_df['is_weekend'] = (xgb_df['dayofweek'] >= 5).astype(int)

for i in range(1, 11):
    xgb_df[f'lag{i}'] = xgb_df['Volume_scaled'].shift(i)

xgb_df = xgb_df.dropna().reset_index(drop=True)

x = xgb_df.drop(['Timestamp', 'Volume', 'Volume_scaled'], axis = 1)
y = xgb_df['Volume_scaled']

# 80/20 training/testing split.
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
    verbose=50
)

y_pred = model.predict(x_test)

y_pred_inv = scaler.inverse_transform(y_pred.reshape(-1, 1))
y_test_inv = scaler.inverse_transform(y_test.values.reshape(-1, 1))

rmse = np.sqrt(mean_squared_error(y_test_inv, y_pred_inv))
mae = mean_absolute_error(y_test_inv, y_pred_inv)
print(f"RMSE: {rmse: .4f}")
print(f"MAE: {mae: .4f}")

plt.figure(figsize=(12, 6))
plt.plot(y_test_inv, label='Actual Traffic Volume', color='blue')
plt.plot(y_pred_inv, label='Predicted Traffic Volume', color='red')
plt.title("XGBoost - Traffic Volume Prediction")
plt.xlabel("Time Step")
plt.ylabel("Traffic Volume")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
xgb.plot_importance(model, max_num_features=10)
plt.ylabel('Feature Importance for Traffic Prediction')
plt.show()
