import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import warnings
warnings.filterwarnings("ignore")

print("Loading and preprocessing data...")
data = pd.read_csv('Students Social Media Addiction.csv')

# Drop Student_ID
data.drop('Student_ID', axis=1, inplace=True)

# Encode categorical columns with LabelEncoder
categorical_cols = [
    'Gender', 'Academic_Level', 'Country',
    'Most_Used_Platform', 'Affects_Academic_Performance',
    'Relationship_Status'
]

encoder = LabelEncoder()
for col in categorical_cols:
    data[col] = encoder.fit_transform(data[col])

# Feature selection
X = data.drop('Addicted_Score', axis=1)
y = data['Addicted_Score']

print(f"Features: {list(X.columns)}")
print(f"Target: Addicted_Score")
print(f"Dataset shape: {X.shape}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train RandomForest with better hyperparameters
print("\nTraining improved Random Forest model...")
model = RandomForestRegressor(
    n_estimators=100,  # Increased from 10
    max_depth=15,       # Add depth limit
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"\nModel Performance:")
print(f"MAE: {mae:.4f}")
print(f"MSE: {mse:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R² Score: {r2:.4f}")

# Test predictions with varied inputs
print("\n" + "="*60)
print("Testing predictions with different inputs:")
print("="*60)

test_cases = [
    ([20, 0, 17, 1, 5.5, 1, 1, 6, 6, 2, 2], "Low usage student"),
    ([25, 1, 17, 0, 10.0, 10, 1, 4, 3, 2, 5], "High usage student"),
    ([30, 0, 0, 5, 3.0, 5, 0, 8, 8, 0, 1], "Low addiction case"),
    ([35, 1, 50, 8, 12.0, 2, 1, 3, 2, 2, 5], "High addiction case"),
]

for features, description in test_cases:
    X_new = np.array([features])
    X_new_scaled = scaler.transform(X_new)
    pred = model.predict(X_new_scaled)[0]
    print(f"{description:.<30} Prediction: {pred:.2f}")

# Save models
print("\n" + "="*60)
print("Saving models...")
pickle.dump(model, open('RF_model.pkl', 'wb'))
pickle.dump(scaler, open('scalar.pkl', 'wb'))
print("✅ Models saved successfully!")
