# Author: Auiannce Euwing '26
# Organization: DataSquad
# Description: This script processes event data to generate insights and visualize a Bubble Graph, 
# where the x-axis represents locations and the y-axis represents event times.
# Last successfully executed on: 2025/04/08


import pandas as pd
import numpy as np
import re
from dateutil import parser
# import matplotlib.pyplot as plt  # No longer used since we're not plotting

# === Load and clean event data ===
def cleanEventTimeString(datetime_str):
    if pd.isna(datetime_str):
        return pd.NaT
    cleaned_str = re.sub(r'GMT[+-]\d{4}.*', '', datetime_str).strip()
    try:
        return parser.parse(cleaned_str)
    except Exception:
        return pd.NaT

file_path = "Data/Data-PEPS-TDX Tickets - Merged Report.csv"
df = pd.read_csv(file_path, dtype=str)
df.columns = df.columns.str.strip()

# === Column setup ===
peps_column = "Peps Location"
other_column = "Other Location"
event_type_column = "Peps Event Types"
time_column = "Event Start Times"

# === Building name cleaner ===
def extract_building_name(location):
    if pd.isna(location) or location.strip().lower() == "other":
        return None
    location = location.strip().lower()
    location = re.split(r"[,/]", location)[0]
    location = re.sub(r"\d+", "", location)
    location = re.sub(r"\s+", " ", location).strip()
    return location.title()

# Map known variants to canonical names
building_aliases = {
    "Wcc": "Weitz Center",
    "Weitz": "Weitz Center",
    "Weitz Cinema": "Weitz Center",
    "Weitz Commons": "Weitz Center",
    "Sayles-Hill": "Sayles",
    "Sayles Hill": "Sayles",
    "Olin": "Olin Hall",
}

def standardize_building_name(name):
    if name is None:
        return None
    return building_aliases.get(name, name)

# === Apply building name logic ===
df["Building"] = df[peps_column].apply(extract_building_name)
df.loc[df[peps_column].str.strip().str.lower() == "other", "Building"] = df[other_column].apply(extract_building_name)
df["Building"] = df["Building"].apply(standardize_building_name)

# === Time cleaning and adjustment ===
df["Created"] = pd.to_datetime(df["Created"], format='%m/%d/%Y', errors='coerce')
df = df.dropna(subset=["Created", time_column, "Building", event_type_column])
df["Event Start Times"] = df[time_column].apply(cleanEventTimeString)
df["Event Start Times"] = df["Event Start Times"] + pd.Timedelta(hours=5)  # TDX timezone correction
df = df.dropna(subset=["Event Start Times"])

# Extract and fix event hour
df["Event Hour"] = df["Event Start Times"].dt.hour.astype(int)

def adjust_hour(hour):
    if 1 <= hour <= 8:
        return hour + 12
    elif hour == 0:
        return 12  # Treat midnight as noon
    else:
        return hour

df["Adjusted Event Hour"] = df["Event Hour"].apply(adjust_hour)
df["Jittered Time"] = df["Adjusted Event Hour"] + np.random.uniform(-0.3, 0.3, size=len(df))

# === Top 9 buildings only ===
top_buildings = df["Building"].value_counts().nlargest(9).index
df_top = df[df["Building"].isin(top_buildings)].copy()

# Bubble size (not used, but previously for plotting)
# building_counts = df_top["Building"].value_counts()
# df_top["Bubble Size"] = df_top["Building"].map(lambda x: building_counts[x] * 10)

# Color assignment for event types (not used now)
# event_types = df_top[event_type_column].unique()
# event_colors = {event: plt.cm.get_cmap("tab10")(i % 10) for i, event in enumerate(event_types)}

# === Plot (COMMENTED OUT) ===
# import matplotlib.pyplot as plt
# plt.figure(figsize=(14, 8))
# plt.scatter(
#     df_top["Jittered Time"],
#     df_top["Building"],
#     s=df_top["Bubble Size"],
#     c=[event_colors[event] for event in df_top[event_type_column]],
#     alpha=0.7,
#     edgecolors="k"
# )
# legend_handles = [
#     plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=event_colors[event], markersize=10)
#     for event in event_types
# ]
# plt.legend(legend_handles, event_types, title="Event Type", loc="upper right")
# plt.xlabel("Time of Event (Hour)")
# plt.ylabel("Building")
# plt.title("Top 9 Buildings - Event Distribution by Time and Type")
# plt.xticks(range(8, 24), [f"{h}:00" for h in range(8, 24)])
# plt.xlim(8, 23)
# plt.grid(True, linestyle="--", alpha=0.6)
# plt.tight_layout()
# plt.savefig("top_9_buildings_event_bubble_chart_fixedtime.png", dpi=300, bbox_inches="tight")
# plt.show()
# print("\n✅ Plot saved as top_9_buildings_event_bubble_chart_fixedtime.png")

# === Print summary of event counts per building and type ===
print("\n===== EVENT BREAKDOWN BY BUILDING =====")
for building in top_buildings:
    building_df = df_top[df_top["Building"] == building]
    total = len(building_df)
    print(f"\n📍 {building}: {total} total events")

    event_type_counts = building_df[event_type_column].value_counts()
    for event_type, count in event_type_counts.items():
        print(f"   - {event_type}: {count}")
