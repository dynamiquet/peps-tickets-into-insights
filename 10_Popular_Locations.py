import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import re

# Force Matplotlib to use a non-interactive backend for PNG output
matplotlib.use("Agg")

# Load the CSV file
file_path = "Data/Data-PEPS-TDX Tickets - Merged Report.csv"

# Read CSV without parsing dates initially
df = pd.read_csv(file_path)

# Column names
peps_column = "Peps Location"
other_column = "Other Location"
event_type_column = "Peps Event Types"
time_column = "Event Start Times"

# Replace "Other" values in Peps Locations with the corresponding values from Other Location
df[peps_column] = df.apply(lambda row: row[other_column] if row[peps_column] == "Other" else row[peps_column], axis=1)

# Rename Peps Location to Event Room for clarity
df.rename(columns={peps_column: "Event Room"}, inplace=True)

# Count the occurrences of each location
location_counts = df["Event Room"].value_counts()

# Get the top 10 most popular locations
top_10_locations = location_counts.head(10).index.tolist()

# Filter the dataframe to only include events at the top 10 locations
df = df[df["Event Room"].isin(top_10_locations)]

# Convert event start times to datetime format
df[time_column] = pd.to_datetime(df[time_column], errors="coerce")

# Drop rows with missing values in key columns
df = df.dropna(subset=["Event Room", event_type_column, time_column])

# Convert event time to numerical format (hour of the day)
df["Event Hour"] = df[time_column].dt.hour.astype(int)

# Group data by event type, event hour, and event room, counting occurrences
event_counts = df.groupby([event_type_column, "Event Hour", "Event Room"]).size().reset_index(name="Event Count")

# Assign unique colors to each event room
unique_rooms = event_counts["Event Room"].unique()
room_colors = {room: plt.cm.get_cmap("tab10")(i) for i, room in enumerate(unique_rooms)}

# Remove all previous figures to prevent overlay issues
plt.close("all")

# Create a clean figure
fig, ax = plt.subplots(figsize=(14, 8))

# Create the bubble chart
scatter = ax.scatter(
    event_counts[event_type_column],
    event_counts["Event Hour"],
    s=event_counts["Event Count"] * 60,  # Increase bubble size for better visibility
    c=[room_colors[room] for room in event_counts["Event Room"]],
    alpha=1.0,  # Remove transparency
    edgecolors="none"
)

# Create a legend for event rooms at the bottom
legend_handles = [
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=room_colors[room], markersize=10) for room in unique_rooms
]
ax.legend(legend_handles, unique_rooms, title="Event Room", loc="lower center", bbox_to_anchor=(0.5, -0.2), ncol=5)

# Labels and title
ax.set_xlabel("Event Type", fontsize=12)
ax.set_ylabel("Time of Event (Hour)", fontsize=12)
ax.set_title("Bubble Chart of Events for Top 10 Locations", fontsize=14)

# Improve readability of X-axis
ax.set_xticklabels(event_counts[event_type_column].unique(), rotation=55, ha="right", fontsize=10)
ax.set_yticks(range(0, 24, 2))  # Show every 2 hours instead of every hour
ax.grid(True, linestyle="--", alpha=0.6)

# Save the figure as a PNG file
output_path = "bubble_chart_top10_locations.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")  # High-quality output

# Print confirmation
print(f"Bubble chart saved as {output_path}")
