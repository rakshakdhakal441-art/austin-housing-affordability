# Using this so python can acess file from my computer
import os
#This lets my code communicate with the website 
import requests
#This helps read the .env which has the API key 
from dotenv import load_dotenv
#Importing pandas
import pandas as pd

#tells python to open .env file aand load the valuse in it 
load_dotenv()

# find the thing called CENSUS_API_KEY and store its value 
api_key = os.getenv("CENSUS_API_KEY")

# for safety reaons print if the key got load not the actual key 
print("API key loaded:", api_key is not None)



# the adress of the census API
url = "https://api.census.gov/data/2024/acs/acs5"

# instruction we sent to census
params = {
    #"get": "NAME,B25070_001E",#tract name and the Census variable B25070_001E
   "get": "NAME,B25070_001E,B25070_007E,B25070_008E,B25070_009E,B25070_010E,B19013_001E,B25064_001E,B25001_001E,B25003_003E",
    "for": "tract:*",# gives me all of the census tract
    "in": "state:48 county:453",# only gives me tract inside Texas(48) and Travis county(453).
    "key": api_key# letting census knwo that I have api key 
}

# this mean go to this census url and ask for the data using the parameters
response = requests.get(url, params=params)


#Checking if the request worked
print("Status code:", response.status_code)

data = response.json()

df = pd.DataFrame(data[1:], columns=data[0])

df["GEOID"] = df["state"] + df["county"] + df["tract"]

print(df[["NAME", "GEOID"]].head())

print(df.head())
print(df.shape)
print(df.columns)

numeric_columns = [
    "B25070_001E",
    "B25070_007E",
    "B25070_008E",
    "B25070_009E",
    "B25070_010E",
    "B19013_001E",
    "B25064_001E",
    "B25001_001E",
    "B25003_003E"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print(df[numeric_columns].dtypes)



print("Tracts with zero total renters:")
print((df["B25070_001E"] == 0).sum())


df["rent_burden_30plus"] = (
    df["B25070_007E"]
    + df["B25070_008E"]
    + df["B25070_009E"]
    + df["B25070_010E"]
)

df["affordability_stress_pct"] = (
    df["rent_burden_30plus"] / df["B25070_001E"]
) * 100

df.loc[
    df["B25070_001E"] == 0,
    "affordability_stress_pct"
] = pd.NA

print(
    df[
        [
            "NAME",
            "B25070_001E",
            "rent_burden_30plus",
            "affordability_stress_pct"
        ]
    ].head(10)
)


print("Missing affordability stress values:")
print(df["affordability_stress_pct"].isna().sum())

print("Minimum affordability stress:")
print(df["affordability_stress_pct"].min())

print("Maximum affordability stress:")
print(df["affordability_stress_pct"].max())


df.to_csv("data/processed/acs_travis_tracts.csv", index=False)

print("Saved file: data/processed/acs_travis_tracts.csv")


predictor_columns = [
    "B19013_001E",
    "B25064_001E",
    "B25001_001E",
    "B25003_003E"
]

for col in predictor_columns:
    print(col)
    print("Minimum:", df[col].min())
    print("Maximum:", df[col].max())
    print("Negative values:", (df[col] < 0).sum())
    print()