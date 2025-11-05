import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# === Load dataset ===
df = pd.read_csv("cleaned_dataset.csv")

# === Features and target ===
X = df[['State', 'District', 'Market', 'Commodity', 'Variety', 'Grade', 'Arrival_Date']]
y = df['Modal_x0020_Price']

# Convert Arrival_Date to datetime and extract useful parts
df['Arrival_Date'] = pd.to_datetime(df['Arrival_Date'], errors='coerce')
X['Year'] = df['Arrival_Date'].dt.year
X['Month'] = df['Arrival_Date'].dt.month
X['Day'] = df['Arrival_Date'].dt.day
X = X.drop(columns=['Arrival_Date'])

# === Preprocess categorical columns with OneHotEncoding ===
categorical_cols = ['State', 'District', 'Market', 'Commodity', 'Variety', 'Grade']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ],
    remainder='passthrough'  # keep Year, Month, Day as is
)

# === Build pipeline with preprocessing + model ===
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# === Train/test split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Fit model ===
model.fit(X_train, y_train)

# === Predict ===
y_pred = model.predict(X_test)

# === Evaluate ===
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("✅ Linear Regression Results:")
print(f"RMSE: {rmse:.2f}")
print(f"R² Score: {r2:.2f}")

# === Try predicting an example ===
example = pd.DataFrame([{
    'State': 'Karnataka',
    'District': 'Bangalore',
    'Market': 'KR Market',
    'Commodity': 'Tomato',
    'Variety': 'Hybrid',
    'Grade': 'FAQ',
    'Year': 2024,
    'Month': 9,
    'Day': 10
}])

pred_price = model.predict(example)
print(f"Predicted Modal Price for example: {pred_price[0]:.2f}")
