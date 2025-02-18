# DataSquad, Auiannce Euwing '26, code last successfully run 2025/02/18

import pandas as pd

# Load the CSV file
df = pd.read_csv("Data-PEPS-TDX Tickets - Merged Report.csv")

# Ensure column names match
peps_column = "Peps Location" 
other_column = "Other Location"  

# Replace "Other" values in Peps Locations with the corresponding values from Other Location
df[peps_column] = df.apply(lambda row: row[other_column] if row[peps_column] == "Other" else row[peps_column], axis=1)

# Count the occurrences of each location
location_counts = df[peps_column].value_counts()

# Get the top 10 most popular locations
top_10_locations = location_counts.head(10)

# Display the results
print(top_10_locations)
