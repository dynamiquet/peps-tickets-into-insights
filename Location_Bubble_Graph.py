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
plt.figure(figsize=(16, 10))
scatter = plt.scatter(
    grouped["Time Label"], grouped["Building"],
    s=grouped["Event Count"] * 10,  
    c=grouped["Event Count"], cmap="viridis", alpha=0.75, edgecolors="k"
)
plt.colorbar(scatter, label="Number of Events")

# Updated bubble size legend
legend_sizes = [5, 10, 15, 20, 25]
legend_handles = [
    plt.scatter([], [], s=size*10, edgecolors='k', facecolors='gray', alpha=0.7, label=f"{size} Events")
    for size in legend_sizes
]
plt.legend(
    handles=legend_handles,
    title="Bubble Size Legend",
    loc="upper right",
    frameon=True
)

plt.title("Bubble Graph: Event Time vs. Location", fontsize=16)
plt.xlabel("Time of Day", fontsize=12)
plt.ylabel("Building", fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("bubble_graph_time_vs_location.png", dpi=300)
plt.show()