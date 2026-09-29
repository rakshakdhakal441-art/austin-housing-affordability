import pandas as pd 

df = pd.read_csv(
"data/processed/acs_travis_tracts.csv",
dtype={
    "state": str,
    "county": str,
    "tract": str,
    "GEOID": str,
    }
)

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns)

print("\nFirst 5 rows:")
print(df.head())

import numpy as np 

columns_to_clean = [
    "B19013_001E",
    "B25064_001E"
]

for col in columns_to_clean:
    df.loc[df[col] < 0, col] = np.nan

print("\nMissing values after cleaning:")
print(df[columns_to_clean].isna().sum())

model_columns = [
    "affordability_stress_pct",
    "B19013_001E",
    "B25064_001E",
    "B25001_001E",
    "B25003_003E"
]

print("\nMissing values in modeling columns:")
print(df[model_columns].isna().sum())

print("\nRows with at least one missing modeling value:")
print(df[model_columns].isna().any(axis=1).sum())

model_df = df.dropna(subset=model_columns).copy()

print("\nOriginal dataset shape:")
print(df.shape)

print("\nModeling dataset shape:")
print(model_df.shape)

model_df = model_df.rename(columns={
    "B19013_001E": "median_household_income",
    "B25064_001E": "median_gross_rent",
    "B25001_001E": "total_housing_units",
    "B25003_003E": "renter_occupied_units"
})

print("\nRenamed columns:")
print(model_df.columns)

print("\nTracts with zero total housibg units:")
print((model_df["total_housing_units"]==0).sum())

model_df["renter_share_pct"]= (
    model_df["renter_occupied_units"]
    / model_df["total_housing_units"]
)*100

print("\nRenter share summary:")
print(model_df["renter_share_pct"].describe())

print("\nTracts with zero median household income:")
print((model_df["median_household_income"]==0).sum())

model_df["rent_to_income_pct"] = (
    model_df["median_gross_rent"]*12
    / model_df["median_household_income"]
)*100

print("\nRent-to-income proxy summary:")
print(model_df["rent_to_income_pct"].describe())

model_df.to_csv(
    "data/processed/modeling_dataset.csv",
    index = False
)

print("\nSaved file: data/processed/modeling_dataset.csv ")

print("\nDuplicate GEOIDs:")
print(model_df["GEOID"].duplicated().sum())

print("\nFinal modeling dataset shape:")
print(model_df.shape)


check_df = pd.read_csv(
    "data/processed/modeling_dataset.csv",
    dtype={"GEOID":str}
)

print("\nReloaded saved dataset shape:")
print(check_df.shape)

print("\nMissing values in saved modeling dataset:")
print(check_df.isna().sum())

