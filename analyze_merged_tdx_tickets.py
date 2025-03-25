# Author: Auiannce Euwing '26, Dynamique Twizere '27
# Organization: DataSquad
# Description: This code contains functions that analyze the TDX tickets data from "Data-PEPS-TDX Tickets - Merged Report.csv" and returns the top departments by time difference between 'Event Start Times' and 'Created', the load by hour, and the load by day.
# Last Successfully ran: 2025/03/19

import pandas as pd
import re
from dateutil import parser
import heapq

# Load the CSV file
def loadMergedDataTickets():
    df = pd.read_csv("Data/Data-PEPS-TDX Tickets - Merged Report.csv")
    df['Created'] = pd.to_datetime(df['Created'], format='%m/%d/%Y', errors='coerce') # Convert 'Created' column to datetime (assuming format is MM/DD/YYYY)
    df = df.dropna(subset=['Created', 'Event Start Times'])  # Remove rows where dates are missing
    df['Event Start Times'] = df['Event Start Times'].apply(cleanEventTimeString)
    df['Event Start Times'] = df['Event Start Times'] + pd.Timedelta(hours=5)  # Adds 5 hours to account for the TDX data time zone conversion
    return df

def cleanEventTimeString(datetime_str):
    if pd.isna(datetime_str): # missing values
        return pd.NaT  
    cleaned_str = re.sub(r'GMT[+-]\d{4}.*', '', datetime_str).strip()

    try:
        return parser.parse(cleaned_str)
    except Exception:
        return pd.NaT

default_df = loadMergedDataTickets()
default_term = "fall"
term_dates = {
    "fall": [
        ("2022-09-12", "2022-11-16"),
        ("2023-09-11", "2023-11-15"),
        ("2024-09-16", "2024-11-20"),
    ],
    "winter": [
        ("2023-01-04", "2023-03-10"),
        ("2024-01-03", "2024-03-08"),
        ("2025-01-06", "2025-03-12"),
    ],
    "spring": [
        ("2023-03-27", "2023-05-29"),
        ("2024-03-25", "2024-05-29"),
        ("2025-03-31", "2025-06-04"),
    ],
}

def parseEventStartTimes(df=default_df):
    if 'Event Start Times' not in df.columns:
        raise KeyError("The 'Event Start Times' column is missing from the DataFrame.")
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
    filtered_df = df.loc[df['Created'] <= df['Event Start Times']].copy()  # Filter rows where 'Created' is not later than 'Event Start Times'
    filtered_df['Time Difference (Days)'] = (filtered_df['Event Start Times'] - filtered_df['Created']).dt.days
    dept_avg_time_diff = filtered_df.groupby('Acct/Dept')['Time Difference (Days)'].mean().round()
    return dept_avg_time_diff

def topDepartmentsByTimeDifference(df=default_df, number=10):
    grouped_dept_avg_diff = groupDepartmentsByTimeDifference(df)
    top_dept_by_diff = grouped_dept_avg_diff.nsmallest(number)
    print(f"{'Department':<50} {'Days btn creation and start date)':>20}")
    print("="*70)
    for dept, days in top_dept_by_diff.items():
        print(f"{dept:<50} {days:>20} days")
    return top_dept_by_diff

def eventLoadByHour(df=default_df, number=24):
    top_loaded_hours = df['event_hour'].value_counts().head(number)
    print(f"{'Hour':<10} {'Number of Events':>20}")
    print("="*30)
    for hour, count in top_loaded_hours.items():
        print(f"{hour:<10} {count:>20}")
    return top_loaded_hours

def eventLoadByDayofTheMonth(df=default_df, number=31):
    top_loaded_days = df['event_day'].value_counts().head(number)
    print(f"{'Day of the Month':<20} {'Number of Events':>20}")
    print("="*40)
    for day, count in top_loaded_days.items():
        print(f"{day:<20} {count:>20}")
    return top_loaded_days

def eventLoadByDayofTheWeek(df=default_df, number=7):
    top_loaded_days = df['day_of_the_week'].value_counts().head(number)
    print(f"{'Day of the Week':<20} {'Number of Events':>20}")
    print("="*40)
    for day, count in top_loaded_days.items():
        print(f"{day:<20} {count:>20}")
    return top_loaded_days

def assignWeekofTheTerm(event_start, term_start):
    event_start = pd.to_datetime(event_start)
    term_start = pd.to_datetime(term_start)

    first_monday = term_start - pd.Timedelta(days=term_start.weekday())
    days_into_term = (event_start - term_start).days
    return f"Week {(days_into_term // 7) + 1}"

def eventLoadByWeekOfTheTerm(df=default_df, term=default_term):
    if term.lower() not in term_dates:
        print("Invalid term name! Use 'fall', 'winter', or 'spring' for the name of the term")
        return

    aggregated_data = []
    term_df_list = []
    term_df = pd.DataFrame()

    for term_start, term_end in term_dates[term]:
        term_start = pd.to_datetime(term_start)
        term_end = pd.to_datetime(term_end)
        term_year = term_start.year

        # Categorize into terms
        mask = (df['Event Start Times'] >= term_start) & (df['Event Start Times'] <= term_end)
        term_df_unique = df[mask].copy()

        # Categorize into weeks of the term
        term_df_unique['week_of_the_term'] = term_df_unique['Event Start Times'].apply(lambda x: assignWeekofTheTerm(x, term_start))
        term_df_unique['day_of_the_week'] = term_df_unique['Event Start Times'].dt.day_name()
        term_df_unique['term_year'] = f"{term.capitalize()} {term_year}"
        term_df_unique['term'] = term.lower()

        term_df_list.append(term_df_unique)
    
    term_df = pd.concat(term_df_list)
    print(term_df.info())
    return term_df

if __name__ == "__main__":
    df = loadMergedDataTickets()
    parseEventStartTimes(df)
    # parseEventStartTimes()
    # print(df.info())
    # print(assign_week_of_term("2025-03-21", "2022-11-16"))

    # eventLoadByWeekOfTheTerm(df, "spring")
    # print(df['Event Start Times'].unique())
    
    # eventLoadByDayofTheWeek()
    # eventLoadByHour()
    # eventLoadByDayofTheMonth() 
    # topDepartmentsByTimeDifference(df)
