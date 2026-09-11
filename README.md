# Austin Housing Affordability

This project studies housing affordability stress in Austin, Texas.

The goal is to combine housing market data, Census demographic and rent-burden data, and Austin building permit data to better understand which areas may be experiencing higher affordability pressure.

## Data Sources

- Zillow Home Value Index (ZHVI)
- U.S. Census Bureau American Community Survey (ACS) 2024 5-Year
- City of Austin Construction Permits

## Current Progress

- Downloaded Zillow city-level ZHVI data
- Confirmed the 2024 ACS 5-Year dataset
- Identified ACS table B25070: Gross Rent as a Percentage of Household Income in the Past 12 Months
- Connected to the Census API using an API key stored in `.env`
- Downloaded tract-level ACS data for Travis County, Texas
- Created a tract `GEOID`
- Created an affordability stress percentage based on renter households spending 30% or more of income on rent
- Saved the processed ACS dataset to `data/processed/acs_travis_tracts.csv`
- Started checking Census data for missing and placeholder values
- Confirmed the City of Austin construction permit dataset

## Target Variable

The main target is `affordability_stress_pct`.

It represents the percentage of renter households spending at least 30% of household income on gross rent.

It is calculated using ACS table B25070.

## Current ACS Dataset

Current shape:

```text
290 rows x 14 columns