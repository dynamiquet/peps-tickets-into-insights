# Author: Auiannce Euwing '26
# Organization: DataSquad
# Description: This code uses the TDX Peps Tickets Report January with Source.csv file to analyze the ticket sources and create a bar chart of the number of tickets by source.
# Last Successfully ran: 2025/04/08


import pandas as pd
import matplotlib.pyplot as plt

# === Load dataset with Source column ===
file_path = "Data/Data-PEPS-TDX Tickets - TDX Peps Tickets Report January with Source.csv"
df = pd.read_csv(file_path, dtype=str)
df.columns = df.columns.str.strip()

# === Columns ===
source_column = "Source"
requestor_column = "Requestor"

# === Filter out known staff-created tickets ===
excluded_names = {"Wiebke Kuhn", "Dann Hurlbert", "Matt Burr"}
df_filtered = df[~df[requestor_column].isin(excluded_names)].copy()

# === Fill missing sources and clean ===
df_filtered[source_column] = df_filtered[source_column].fillna("Unknown").str.strip()

# === Count tickets by source ===
source_counts = df_filtered[source_column].value_counts()

# === Print breakdown to terminal ===
print("\n===== TICKET SOURCES BREAKDOWN (excluding PEPS staff) =====")
for source, count in source_counts.items():
    print(f"{source}: {count} tickets")

# === Create bar chart ===
plt.figure(figsize=(10, 6))
bars = plt.barh(source_counts.index, source_counts.values, color="#6A9FB5")

# Add labels
for bar in bars:
    plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
             str(bar.get_width()), va='center')

# Styling
plt.xlabel("Number of Tickets")
plt.title("Number of Tickets by Source (Excluding PEPS Staff)")
plt.tight_layout()


# Save and show
plt.savefig("ticket_sources_bar_chart.png", dpi=300, bbox_inches="tight")
plt.show()
print("\n✅ Ticket source chart saved as ticket_sources_bar_chart.png")