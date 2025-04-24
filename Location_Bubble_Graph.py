# Author: Auiannce Euwing '26
# Organization: DataSquad
# Description: This script processes TDX event data to generate a bubble graph visualization.
# The x-axis represents the time of day (6 AM to 11 PM, labeled in AM/PM format), and the y-axis represents the top buildings where events occur.
# Bubble size and color both correspond to the number of events at a given time and location.
# A custom legend illustrates the mapping from bubble size to event count.
# Last successfully executed on: 2025/04/21


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from dateutil import parser

# === Helper Functions ===
def cleanEventTimeString(datetime_str):
    if pd.isna(datetime_str): return pd.NaT
    cleaned_str = re.sub(r'GMT[+-]\d{4}.*', '', datetime_str).strip()
    try: return parser.parse(cleaned_str)
    except: return pd.NaT

# === Load and Prepare Data ===
df = pd.read_csv("Data/Data-PEPS-TDX Tickets - Merged Report.csv", dtype=str)
df.columns = df.columns.str.strip()
peps_col, other_col = "Peps Location", "Other Location"

def extract_building_name(loc):
    if pd.isna(loc) or loc.strip().lower() == "other": return None
    loc = re.split(r"[,/]", loc.strip().lower())[0]
    loc = re.sub(r"\d+", "", loc)
    return re.sub(r"\s+", " ", loc).strip().title()

aliases = {
    "Wcc": "Weitz Center", "Weitz": "Weitz Center", "Weitz Cinema": "Weitz Center",
    "Weitz Commons": "Weitz Center", "Sayles-Hill": "Sayles", "Sayles Hill": "Sayles",
    "Olin": "Olin Hall", "Kracum": "Kracum", "Kracum Hall": "Kracum"
}
def standardize_building(name):
    if name is None: return None
    return aliases.get(name, name)

df["Building"] = df[peps_col].apply(extract_building_name)
df.loc[df[peps_col].str.strip().str.lower() == "other", "Building"] = df[other_col].apply(extract_building_name)
df["Building"] = df["Building"].apply(standardize_building)

df["Created"] = pd.to_datetime(df["Created"], format='%m/%d/%Y', errors='coerce')
df["Event Start Times"] = df["Event Start Times"].apply(cleanEventTimeString) + pd.Timedelta(hours=5)
df = df.dropna(subset=["Created", "Event Start Times", "Building"])

df["Hour"] = df["Event Start Times"].dt.hour
df = df[df["Hour"].between(6, 23)]
df["Time Label"] = df["Event Start Times"].dt.strftime("%I %p")

top_buildings = df["Building"].value_counts().nlargest(9).index.tolist()
if "Kracum" not in top_buildings:
    top_buildings.append("Kracum")
df_top = df[df["Building"].isin(top_buildings)].copy()

# === Group and Count ===
grouped = df_top.groupby(["Building", "Hour", "Time Label"]).size().reset_index(name="Event Count")
grouped = grouped.sort_values("Hour")

# === Plot ===
fig, ax = plt.subplots(figsize=(16, 10))

# Moderate size scaling for visible differences
size_base = 35
sizes = size_base * grouped["Event Count"] ** 1.4

scatter = ax.scatter(
    grouped["Time Label"], grouped["Building"],
    s=sizes,
    c=grouped["Event Count"],
    cmap="Blues",
    alpha=0.85,
    edgecolors="k"
)

# Horizontal color bar
cbar = plt.colorbar(scatter, orientation="horizontal", pad=0.15, aspect=40)
cbar.set_label("Number of Events")

# Legend entries: 5, 10, 15, 20+
legend_event_counts = [5, 10, 15, 20]
legend_sizes = [size_base * count ** 1.4 for count in legend_event_counts]
legend_labels = [f"{count} Events" for count in legend_event_counts[:-1]] + ["20+ Events"]

legend_handles = [
    plt.scatter([], [], s=size, edgecolors='k', facecolors='lightblue', alpha=0.7, label=label)
    for size, label in zip(legend_sizes, legend_labels)
]
ax.legend(
    handles=legend_handles,
    title="Bubble Size Legend",
    bbox_to_anchor=(1.17, 0.5),
    loc="center left",
    frameon=True,
    borderpad=2.0,
    labelspacing=2.2,
    handletextpad=2.5
)

# Titles, labels, grid
ax.set_title("Bubble Graph: Event Time vs. Location", fontsize=16)
ax.set_xlabel("Time of Day", fontsize=12)
ax.set_ylabel("Building", fontsize=12)
plt.xticks(rotation=45)
ax.grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("bubble_graph_time_vs_location_better_sizes.png", dpi=300)
plt.show()



