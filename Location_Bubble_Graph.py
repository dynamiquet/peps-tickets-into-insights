# Author: Auiannce Euwing '26
# Organization: DataSquad
# Description: This code creates a Bubble Graph where the y-axis is time and the x-axis is locations
# Last Successfully ran: 2025/03/06


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re


# Load the dataset
file_path = "Data/Data-PEPS-TDX Tickets - Merged Report.csv"
df = pd.read_csv(file_path, dtype=str)  # Load as string to preserve formatting


# Column names
peps_column = "Peps Location"
other_column = "Other Location"
event_type_column = "Peps Event Types"
time_column = "Event Start Times"


# Function to extract the first 3 letters from a location name
def extract_building_code(location):
   return str(location)[:3].upper() if pd.notnull(location) else "UNK"  # "UNK" for unknown locations


# Create a new "Building" column combining "Peps Location" and "Other Location"
df["Building"] = df[peps_column].apply(extract_building_code)
df.loc[df[peps_column] == "Other", "Building"] = df[other_column].apply(extract_building_code)


# Function to clean timestamps (removes timezone information)
def clean_timestamp(timestamp):
   match = re.search(r"([A-Za-z]{3} \w{3} \d{1,2} \d{4} \d{2}:\d{2}:\d{2})", str(timestamp))
   return match.group(1) if match else None


# Apply cleaning function
df["Cleaned Event Start Times"] = df[time_column].apply(clean_timestamp)


# Convert to datetime format
df["Parsed Event Start Times"] = pd.to_datetime(df["Cleaned Event Start Times"], errors="coerce")


# Drop rows with invalid dates
df = df.dropna(subset=["Parsed Event Start Times", "Building", event_type_column])


# Extract event hour
df["Event Hour"] = df["Parsed Event Start Times"].dt.hour.astype(int)


# Adjust event start times: Shift 1-8 AM to 13-20 PM
df["Adjusted Event Hour"] = df["Event Hour"].apply(lambda x: x + 12 if 1 <= x <= 8 else x)


# Apply jitter for better visualization
df["Jittered Time"] = df["Adjusted Event Hour"] + np.random.uniform(-0.3, 0.3, size=len(df))


# Count occurrences of each building
building_counts = df["Building"].value_counts()


# Assign unique colors to event types
event_types = df[event_type_column].unique()
event_colors = {event: plt.cm.get_cmap("tab10")(i % 10) for i, event in enumerate(event_types)}


# Compute bubble sizes based on event count per building
df["Bubble Size"] = df["Building"].map(lambda x: building_counts[x] * 10)


# Create bubble chart
plt.figure(figsize=(14, 8))
scatter = plt.scatter(
   df["Jittered Time"],  # X-axis: Adjusted event time with jitter
   df["Building"],  # Y-axis: Building code
   s=df["Bubble Size"],  # Bubble size based on event count
   c=[event_colors[event] for event in df[event_type_column]],  # Color by event type
   alpha=0.7,
   edgecolors="k"
)


# Create legend for event types
legend_handles = [
   plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=event_colors[event], markersize=10)
   for event in event_types
]
plt.legend(legend_handles, event_types, title="Event Type", loc="upper right")


# Labels and title
plt.xlabel("Time of Event (Hour)")
plt.ylabel("Building")
plt.title("Event Distribution by Building and Time (Bubble Chart)")


# Adjust x-axis ticks
plt.xticks(range(0, 25, 1), [f"{h}:00" for h in range(0, 25)])  # Show every hour


# Show grid
plt.grid(True, linestyle="--", alpha=0.6)


# Save the plot as PNG
output_path = "building_event_bubble_chart.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")  # High-resolution image


# Display message
print(f"Plot saved as {output_path}")