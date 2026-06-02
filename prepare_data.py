import pandas as pd

files = [
    "data/daily_sales_data_0.csv",
    "data/daily_sales_data_1.csv",
    "data/daily_sales_data_2.csv"
]

dfs = []

for file in files:
    df = pd.read_csv(file)

    # Keep only pink morsels
    df = df[df["product"] == "pink morsel"]

    # Remove $ and convert price to float
    df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)

    # Calculate sales
    df["sales"] = df["price"] * df["quantity"]

    # Keep only required columns
    df = df[["sales", "date", "region"]]

    dfs.append(df)

# Combine all files
final_df = pd.concat(dfs, ignore_index=True)

# Save output
final_df.to_csv("output.csv", index=False)

print("output.csv created successfully!")