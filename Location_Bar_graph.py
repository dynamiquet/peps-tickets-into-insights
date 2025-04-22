# Author: Auiannce Euwing '26
# Organization: DataSquad
# Description: This script processes TDX event data to generate a bar graph.
# The x-axis shows event types, the y-axis shows number of events,
# and the hue represents building names. 
# Last successfully executed on: 2025/04/21


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
from dateutil import parser

# === Step 1: Load and Clean Data ===
def cleanEventTimeString(datetime_str):
    if pd.isna(datetime_str): return pd.NaT
    cleaned_str = re.sub(r'GMT[+-]\d{4}.*', '', datetime_str).strip()
    try: return parser.parse(cleaned_str)
    except: return pd.NaT

df = pd.read_csv("Data/Data-PEPS-TDX Tickets - Merged Report.csv", dtype=str)
df.columns = df.columns.str.strip()
peps_col, other_col, event_type_col = "Peps Location", "Other Location", "Peps Event Types"

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

df["Event Start Times"] = df["Event Start Times"].apply(cleanEventTimeString) + pd.Timedelta(hours=5)
df = df.dropna(subset=["Event Start Times", "Building", event_type_col])

# === Step 2: Filter to Top 9 Buildings + Always Include Kracum ===
top_buildings = df["Building"].value_counts().nlargest(9).index.tolist()
if "Kracum" not in top_buildings:
    top_buildings.append("Kracum")

df_top = df[df["Building"].isin(top_buildings)].copy()

# === Step 3: Group and Prepare Count Table ===
count_df = df_top.groupby([event_type_col, "Building"]).size().reset_index(name="Event Count")

# Ensure all event_type + building combinations exist
event_types = count_df[event_type_col].unique()
buildings = sorted(top_buildings)
full_index = pd.MultiIndex.from_product([event_types, buildings], names=[event_type_col, "Building"])
count_df = count_df.set_index([event_type_col, "Building"]).reindex(full_index, fill_value=0).reset_index()

# === Step 4: Plot Bar Graph with Distinct Colors ===
sns.set_style("whitegrid")

# Order event types on x-axis
count_df[event_type_col] = pd.Categorical(
    count_df[event_type_col],
    categories=sorted(count_df[event_type_col].unique()),
    ordered=True
)
count_df = count_df.sort_values([event_type_col, "Building"])

# Distinct color palette (10 bold colors)
custom_colors = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]
unique_buildings = sorted(count_df["Building"].unique())
palette_dict = {building: custom_colors[i % len(custom_colors)] for i, building in enumerate(unique_buildings)}

plt.figure(figsize=(18, 10))
ax = sns.barplot(
    data=count_df,
    x=event_type_col,
    y="Event Count",
    hue="Building",
    palette=palette_dict,
    dodge=True
)

# Final plot polish
ax.set_title("Bar Graph: Number of Events by Type and Location", fontsize=18)
ax.set_xlabel("Event Type", fontsize=14)
ax.set_ylabel("Number of Events", fontsize=14)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

# Legend outside the plot
plt.legend(title="Building", bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
plt.tight_layout()
plt.savefig("bar_graph_event_type_vs_location.png", dpi=300)
plt.show()