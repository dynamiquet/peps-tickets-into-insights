# DataSquad, Auiannce Euwing '26, code last successfully run 2025/02/18


import pandas as pd
import re
from dateutil import parser

# Load the CSV file
df = pd.read_csv("Data-PEPS-TDX Tickets - Merged Report.csv") 

# Convert 'Created' column to datetime (assuming format is MM/DD/YYYY)
df['Created'] = pd.to_datetime(df['Created'], format='%m/%d/%Y', errors='coerce')

# Function to clean 'Event Start Times' by removing the timezone information
def clean_datetime_string(datetime_str):
    if pd.isna(datetime_str):
        return pd.NaT  # Return NaT for missing values
    # Remove timezone information like "GMT-0500 (Central Daylight Time)"
    cleaned_str = re.sub(r'GMT[+-]\d{4}.*', '', datetime_str).strip()
    try:
        return parser.parse(cleaned_str)
    except Exception:
        return pd.NaT  # Return NaT if parsing fails

# Apply the function to clean and parse the datetime column
df['Event Start Times'] = df['Event Start Times'].apply(clean_datetime_string)

# Ensure both columns have valid datetime values
df = df.dropna(subset=['Created', 'Event Start Times'])  # Remove rows where dates are missing

# Compute the difference in days
df['Time Difference (Days)'] = (df['Event Start Times'] - df['Created']).dt.days

# Group by Acct/Dept and calculate the average time difference
dept_avg_time_diff = df.groupby('Acct/Dept')['Time Difference (Days)'].mean()

# Get the top 10 departments that request tickets closest to the event start time (smallest difference)
top_10_departments = dept_avg_time_diff.nsmallest(10)

# Display the results
print(top_10_departments)
