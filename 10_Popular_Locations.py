# Author: Auiannce '26
# Organization: DataSquad
# Description: This code created a bar chart for the top 10 most reserved locations. 
# Last Successfully ran: 2025/02/25
import pandas as pd
import matplotlib.pyplot as plt


# Load the CSV file
df = pd.read_csv("Data/Data-PEPS-TDX Tickets - Merged Report.csv")

# Ensure column names match
peps_column = "Peps Location" 
other_column = "Other Location"  

# Replace "Other" values in Peps Locations with the corresponding values from Other Location
df[peps_column] = df.apply(lambda row: row[other_column] if row[peps_column] == "Other" else row[peps_column], axis=1)

# Count the occurrences of each location
location_counts = df[peps_column].value_counts()

# Get the top 10 most popular locations
top_10_locations = location_counts.head(10)

# Create a horizontal bar chart
plt.figure(figsize=(10, 6))
plt.barh(top_10_locations.index[::-1], top_10_locations.values[::-1], color="blue")
plt.xlabel("Number of Events")
plt.ylabel("Location")
plt.title("Top 10 Most Popular Reserved Event Locations")
plt.grid(axis="x", linestyle="--", alpha=0.7)

# Show the plot
plt.show()
