import pandas as pd

# Load your file
df = pd.read_csv('D:\mca2sem\wholesale_market\dataset\096f32cf-2033-464c-a90d-73f338493971.csv')

# View basic info
print("Original shape:", df.shape)
print(df.info())

# Step 1: Remove duplicates
df = df.drop_duplicates()
print("After removing duplicates:", df.shape)

# Step 2: Remove rows with missing important values
df = df.dropna(subset=['State', 'District', 'Market', 'Commodity', 'Arrival_Date', 'Modal_x0020_Price'])
print("After dropping rows with essential nulls:", df.shape)

# Step 3: Strip spaces and standardize text columns
for col in ['State', 'District', 'Market', 'Commodity', 'Variety', 'Grade']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title()

# Step 4: Convert date column to datetime
df['Arrival_Date'] = pd.to_datetime(df['Arrival_Date'], errors='coerce')

# Remove rows where date conversion failed
df = df.dropna(subset=['Arrival_Date'])

# Step 5: Convert price columns to numeric
for price_col in ['Min_x0020_Price', 'Max_x0020_Price', 'Modal_x0020_Price']:
    if price_col in df.columns:
        df[price_col] = pd.to_numeric(df[price_col], errors='coerce')

# Remove rows where Modal Price is missing or zero
df = df[df['Modal_x0020_Price'] > 0]

# Optional: Remove outliers (e.g., prices above 99 percentile)
upper_limit = df['Modal_x0020_Price'].quantile(0.99)
df = df[df['Modal_x0020_Price'] <= upper_limit]

print("Final cleaned shape:", df.shape)

# Save cleaned file
df.to_csv('cleaned_dataset.csv', index=False)

print("✅ Cleaned dataset saved as 'cleaned_dataset.csv'")
