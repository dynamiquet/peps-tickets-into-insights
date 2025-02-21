# Author: Auiannce Euwing '26, Dynamique Twizere '27
# Organization: DataSquad
# Description: This code contains functions that analyze the TDX tickets data from "Data-PEPS-TDX Tickets - Merged Report.csv" and returns the top departments by time difference between 'Event Start Times' and 'Created', the load by hour, and the load by day.
# Last Successfully ran: 2025/02/21 

import pandas as pd
import re
from dateutil import parser

# Load the CSV file
def loadData():
    df = pd.read_csv("Data/Data-PEPS-TDX Tickets - Merged Report.csv")
    df['Created'] = pd.to_datetime(df['Created'], format='%m/%d/%Y', errors='coerce') # Convert 'Created' column to datetime (assuming format is MM/DD/YYYY)
    df = df.dropna(subset=['Created', 'Event Start Times'])  # Remove rows where dates are missing
    return df

def clean_event_start_time_string(datetime_str):
    if pd.isna(datetime_str):
        return pd.NaT  # Return NaT for missing values
    cleaned_str = re.sub(r'GMT[+-]\d{4}.*', '', datetime_str).strip() # Remove timezone information like "GMT-0500 (Central Daylight Time)"

    try:
        return parser.parse(cleaned_str)
    except Exception:
        return pd.NaT  # Return NaT if parsing fails

def groupDepartmentsByTimeDifference(df):
    df['Time Difference (Days)'] = (df['Event Start Times'] - df['Created']).dt.days # Compute the difference in days
    dept_avg_time_diff = df.groupby('Acct/Dept')['Time Difference (Days)'].mean()
    return dept_avg_time_diff

def parseEventStartTimes(df):
    df['event_hour'] = df['Event Start Times'].dt.hour
    df['event_day'] = df['Event Start Times'].dt.day
    df['event_month'] = df['Event Start Times'].dt.month

# Return the top 10 departments with the smallest average time difference between 'Event Start Times' and 'Created'
def TopDepartmentsByTimeDifference(df):
    grouped_dept_avg_diff = groupDepartmentsByTimeDifference(df)
    top_dept_by_diff = grouped_dept_avg_diff.nsmallest(10)
    print(top_dept_by_diff)
    return(top_dept_by_diff)

#  Return sorted Series of hours of the day by event load
def loadByHour(number=24): # Default to 24 hours
    top_loaded_hours = df['event_hour'].value_counts().head(number)
    print(f"Top {number} loaded hours: {top_loaded_hours}")

# Return sorted Series of days of the month by event load
def loadByDay(number=31):
    top_loaded_days = df['event_day'].value_counts().head(number)
    print(f"Top {number} loaded days: {top_loaded_days}")
    return top_loaded_days

if __name__ == "__main__":
    df = loadData()
    df['Event Start Times'] = df['Event Start Times'].apply(clean_event_start_time_string) # Clean the 'Event Start Times' column
    parseEventStartTimes(df)
    loadByHour()
    loadByDay()
