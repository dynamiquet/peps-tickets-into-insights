# Author: Auiannce Euwing '26
# Organization: DataSquad
# Description: This code creates a Bubble Graph were the y-axis is time and the x-axis is locations 
# Last Successfully ran: 2025/03/06

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import re

matplotlib.use("Agg")  

# Load the CSV file
file_path = "Data/Data-PEPS-TDX Tickets - Merged Report.csv"

# Read CSV without parsing dates initially
df = pd.read_csv(file_path)

# Function to clean and parse Event Start Times
def clean_datetime(value):
    if pd.isna(value) or not isinstance(value, str):
        return None
    match = re.search(r'([A-Za-z]{3} \d{2} \d{4} \d{2}:\d{2}:\d{2})', value)
    if match:
        return pd.to_datetime(match.group(1), format="%b %d %Y %H:%M:%S", errors="coerce")
    return None

# Apply the cleaning function to the column
df["Event Start Times"] = df["Event Start Times"].apply(clean_datetime)

# Drop rows where Event Start Times could not be parsed
df = df.dropna(subset=["Event Start Times"])

# Extract relevant columns
peps_column = "Peps Location"
other_column = "Other Location"
event_type_column = "Peps Event Types"
time_column = "Event Start Times"

# Replace "Other" values in Peps Locations with the corresponding values from Other Location
df[peps_column] = df.apply(lambda row: row[other_column] if row[peps_column] == "Other" else row[peps_column], axis=1)

# Rename Peps Location to Event Room for clarity
df.rename(columns={peps_column: "Event Room"}, inplace=True)

# Convert event time to the hour of the day
df["Event Hour"] = df[time_column].dt.hour.astype(int)

# Group data by event type, event hour, and event room, counting occurrences
event_counts = df.groupby([event_type_column, "Event Hour", "Event Room"]).size().reset_index(name="Event Count")

# Assign unique colors to each event room
unique_rooms = event_counts["Event Room"].unique()
room_colors = {room: plt.cm.get_cmap("tab10")(i) for i, room in enumerate(unique_rooms)}
plt.close("all")

fig, ax = plt.subplots(figsize=(14, 8))

# Create the bubble chart
scatter = ax.scatter(
    event_counts[event_type_column],
    event_counts["Event Hour"],
    s=event_counts["Event Count"] * 60,  
    c=[room_colors[room] for room in event_counts["Event Room"]],
    alpha=1.0,
    edgecolors="none"  
)

legend_handles = [
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=room_colors[room], markersize=8) for room in unique_rooms
]
ax.legend(
    legend_handles, 
    unique_rooms, 
    title="Event Room", 
    loc="upper right", 
    markerscale=0.7,  
    fontsize=9,  
    title_fontsize=10, 
    frameon=False 
)

# Improve readability of X-axis
ax.set_xticklabels(event_counts[event_type_column].unique(), rotation=55, ha="right", fontsize=10)
ax.set_yticks(range(0, 24, 2))  # Show every 2 hours instead of every hour
ax.grid(True, linestyle="--", alpha=0.6)

# Save the figure as a PNG file
output_path = "bubble_chart.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")  

# Print confirmation
print(f"Bubble chart saved as {output_path}")
