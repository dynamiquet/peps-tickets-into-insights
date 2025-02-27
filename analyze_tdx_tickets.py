# Author: Auiannce Euwing '26, Dynamique Twizere '27
# Organization: DataSquad
# Description: This code contains functions that analyze the TDX tickets data from "Data-PEPS-TDX Tickets - Merged Report.csv" and returns the top departments by time difference between 'Event Start Times' and 'Created', the load by hour, and the load by day.
# Last Successfully ran: 2025/02/21 

import pandas as pd
import re
from dateutil import parser
import heapq

# Load the CSV file
def loadDataTickets():
    df = pd.read_csv("Data/Data-PEPS-TDX Tickets - Merged Report.csv")
    df['Created'] = pd.to_datetime(df['Created'], format='%m/%d/%Y', errors='coerce') # Convert 'Created' column to datetime (assuming format is MM/DD/YYYY)
    df = df.dropna(subset=['Created', 'Event Start Times'])  # Remove rows where dates are missing
    df['Event Start Times'] = df['Event Start Times'].apply(cleanEventTimeString)
    return df

def cleanEventTimeString(datetime_str):
    if pd.isna(datetime_str):
        return pd.NaT  # Return NaT for missing values
    cleaned_str = re.sub(r'GMT[+-]\d{4}.*', '', datetime_str).strip() # Remove timezone information like "GMT-0500 (Central Daylight Time)"

    try:
        return parser.parse(cleaned_str)
    except Exception:
        return pd.NaT  # Return NaT if parsing fails

default_df = loadDataTickets()

def parseEventStartTimes(df=default_df):
    df['event_hour_24'] = df['Event Start Times'].dt.hour
    df['event_hour'] = df['Event Start Times'].dt.strftime("%I %p")
    df['event_day'] = df['Event Start Times'].dt.day
    df['event_month'] = df['Event Start Times'].dt.month
    df['day_of_the_week'] = df['Event Start Times'].dt.day_name()

def orderEventHoursLogically(df=default_df):
    hours_order = [
    "12 AM", "01 AM", "02 AM", "03 AM", "04 AM", "05 AM", "06 AM", "07 AM", "08 AM", "09 AM", "10 AM", "11 AM",
    "12 PM", "01 PM", "02 PM", "03 PM", "04 PM", "05 PM", "06 PM", "07 PM", "08 PM", "09 PM", "10 PM", "11 PM"
    ]

    df["event_hour"] = pd.Categorical(df["event_hour"], categories=hours_order, ordered=True)

def orderDaysOfTheWeekLogically(df=default_df):
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df["day_of_the_week"] = pd.Categorical(df["day_of_the_week"], categories=days_order, ordered=True)

def groupDepartmentsByTimeDifference(df=default_df):
    df['Time Difference (Days)'] = (df['Event Start Times'] - df['Created']).dt.days
    dept_avg_time_diff = df.groupby('Acct/Dept')['Time Difference (Days)'].mean().round()
    return dept_avg_time_diff

def topDepartmentsByTimeDifference(df=default_df):
    grouped_dept_avg_diff = groupDepartmentsByTimeDifference(df)
    top_dept_by_diff = grouped_dept_avg_diff.nsmallest(10)
    for dept, days in top_dept_by_diff.items():
        if days < 0:
            print(f"{dept} typically creates events about {-days} days after the event has already happened.")
        elif days == 0:
            print(f"{dept} generally creates events on the same day they start.")
        else:
            print(f"{dept} typically creates events about {days} days before they start.")
    return top_dept_by_diff

def eventLoadByHour(df=default_df, number=24): # Default to 24 hours
    top_loaded_hours = df['event_hour'].value_counts().head(number)
    print(f"Top {number} loaded hours: {top_loaded_hours}")
    return top_loaded_hours

def eventLoadByDayofTheMonth(df=default_df, number=31):
    top_loaded_days = df['event_day'].value_counts().head(number)
    print(f"Top {number} loaded days: {top_loaded_days}")
    return top_loaded_days

def eventLoadByDayofTheWeek(df=default_df, number=7):
    top_loaded_days = df['day_of_the_week'].value_counts().head(number)
    print(f"Top {number} loaded days of the week: {top_loaded_days}")
    return top_loaded_days

if __name__ == "__main__":
    df = loadDataTickets()
    parseEventStartTimes()

    eventLoadByDayofTheWeek()
    # eventLoadByHour()
    # eventLoadByDayofTheMonth() 
    # topDepartmentsByTimeDifference(df)
