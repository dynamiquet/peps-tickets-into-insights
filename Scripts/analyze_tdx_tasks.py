# Author: Auiannce Euwing '26, Dynamique Twizere '27
# Organization: DataSquad
# Description: This code contains functions that analyze the TDX tasks data from "Data/Data-PEPS-TDX Tickets - TDX Peps Task Report January 2.csv" and provides insights such as task load by hour, day of the month, day of the week, and week of the term.


import pandas as pd
import csv

def loadTasks(dept_filter=None):
    df = pd.read_csv("Data/Data-PEPS-TDX Tickets - TDX Peps Task Report January 2.csv")
    for col in ['Created', 'Task Due', 'Event Start']:
        df[col] = pd.to_datetime(df[col], format='%m/%d/%y %H:%M', errors='coerce') 
    if df['Task Due'].isna().any():
        df['Task Due'].fillna(df['Event Start'], inplace=True)
    if df['Event Start'].isna().any():
        df['Event Start'].fillna(df['Task Due'], inplace=True)

    if dept_filter == "no_media":
        df = df[~df['Title'].str.contains("STANDARD|VIDEO|MEDIA|CONVO", case=False, na=False)]
    elif dept_filter == "media_only":
        df = df[df['Title'].str.contains("STANDARD|VIDEO|MEDIA|CONVO", case=False, na=False)]

    return df, dept_filter

default_df, dept_filler = loadTasks(dept_filter=None)
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

def parseTaskStartTimes(df=default_df):
    if "Task Due" not in df.columns:
        print(" \'Task Due\' column does not exist!")
    df['task_hour_24'] = df['Task Due'].dt.hour
    df['task_hour'] = df['Task Due'].dt.strftime("%I %p")
    df['task_day'] = df['Task Due'].dt.day
    df['task_month'] = df['Task Due'].dt.month
    df['task_month_name'] = df['Task Due'].dt.strftime('%b')
    df['day_of_the_week'] = df['Task Due'].dt.day_name()
    print("hey!")

def orderTaskHoursLogically(df=default_df):
    hours_order = [
        "05 AM", "06 AM", "07 AM", "08 AM", "09 AM", "10 AM", "11 AM", "12 PM", 
        "01 PM", "02 PM", "03 PM", "04 PM", "05 PM", "06 PM", "07 PM", "08 PM", 
        "09 PM", "10 PM", "11 PM"
    ]
    df["task_hour"] = pd.Categorical(df["task_hour"], categories=hours_order, ordered=True)

def orderTaskMonthsLogically(df=default_df):
    months_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df["task_month_name"] = pd.Categorical(df["task_month_name"], categories=months_order, ordered=True)

def orderDaysOfTheWeekLogically(df=default_df):
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df["day_of_the_week"] = pd.Categorical(df["day_of_the_week"], categories=days_order, ordered=True)

def taskLoadByHour(df=default_df, number=24):
    top_loaded_hours = df['task_hour'].value_counts().head(number)
    print(f"{'Hour':<10} {'Number of tasks':>20}")
    print("="*30)
    for hour, count in top_loaded_hours.items():
        print(f"{hour:<10} {count:>20}")
    return top_loaded_hours

def taskLoadByDayofTheMonth(df=default_df, number=31):
    top_loaded_days = df['task_day'].value_counts().head(number)
    print(f"{'Day of the Month':<20} {'Number of tasks':>20}")
    print("="*40)
    for day, count in top_loaded_days.items():
        print(f"{day:<20} {count:>20}")
    return top_loaded_days

def taskLoadByDayofTheWeek(df=default_df, number=7):
    top_loaded_days = df['day_of_the_week'].value_counts().head(number)
    print(f"{'Day of the Week':<20} {'Number of tasks':>20}")
    print("="*40)
    for day, count in top_loaded_days.items():
        print(f"{day:<20} {count:>20}")
    return top_loaded_days

def assignWeekofTheTerm(task_due, term_start):
    task_due = pd.to_datetime(task_due)
    term_start = pd.to_datetime(term_start)

    first_monday = term_start - pd.Timedelta(days=term_start.weekday())
    days_into_term = (task_due - first_monday).days
    return f"Week {(days_into_term // 7) + 1}"

def taskLoadByWeekOfTheTerm(df=default_df, term=default_term):
    if term.lower() not in term_dates:
        print("Invalid term name! Use 'fall', 'winter', or 'spring' for the name of the term")
        return

    term_df_list = []
    term_df = pd.DataFrame()

    for term_start, term_end in term_dates[term]:
        term_start = pd.to_datetime(term_start)
        term_end = pd.to_datetime(term_end)
        term_year = term_start.year

        # Categorize into terms
        mask = (df['Task Due'] >= term_start) & (df['Task Due'] <= term_end)
        term_df_unique = df[mask].copy()

        # Categorize into weeks of the term
        term_df_unique['week_of_the_term'] = term_df_unique['Task Due'].apply(lambda x: assignWeekofTheTerm(x, term_start))
        term_df_unique['day_of_the_week'] = term_df_unique['Task Due'].dt.day_name()
        term_df_unique['term_year'] = f"{term.capitalize()} {term_year}"
        term_df_unique['term'] = term.lower()

        term_df_list.append(term_df_unique)
    
    term_df = pd.concat(term_df_list)
    print(term_df.info())
    return term_df

def analyzeTicketTiming(df=default_df):
    # Drop duplicate Ticket IDs to ensure ticket-level analysis
    unique_tickets = df.drop_duplicates(subset=['Ticket ID']).copy()

    # Add columns for day type and business hours
    unique_tickets['day_type'] = unique_tickets['Task Due'].dt.day_name().apply(
        lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday'
    )
    unique_tickets['business_hours'] = unique_tickets['Task Due'].dt.hour.apply(
        lambda x: 'Business Hours' if 9 <= x < 17 else 'Non-Business Hours'
    )

    # Count tickets by day type
    day_type_counts = unique_tickets['day_type'].value_counts()

    # Count tickets by business hours
    business_hours_counts = unique_tickets['business_hours'].value_counts()

    # Print results
    print(f"{'Day Type':<15} {'Number of Tickets':>20}")
    print("=" * 35)
    for day_type, count in day_type_counts.items():
        print(f"{day_type:<15} {count:>20}")

    print("\n")
    print(f"{'Time Period':<20} {'Number of Tickets':>20}")
    print("=" * 40)
    for period, count in business_hours_counts.items():
        print(f"{period:<20} {count:>20}")

    return {
        "day_type_counts": day_type_counts,
        "business_hours_counts": business_hours_counts
    }

def analyzeTicketTimingByTerm(df=default_df, term=default_term):
    if term.lower() not in term_dates:
        print("Invalid term name! Use 'fall', 'winter', or 'spring' for the name of the term")
        return

    term_df_list = []
    for term_start, term_end in term_dates[term]:
        term_start = pd.to_datetime(term_start)
        term_end = pd.to_datetime(term_end)

        # Filter data for the term
        mask = (df['Task Due'] >= term_start) & (df['Task Due'] <= term_end)
        term_df = df[mask].copy()

        # Add week of the term, day type, and business hours
        term_df['week_of_the_term'] = term_df['Task Due'].apply(lambda x: assignWeekofTheTerm(x, term_start))
        term_df['day_type'] = term_df['Task Due'].dt.day_name().apply(
            lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday'
        )
        term_df['business_hours'] = term_df['Task Due'].dt.hour.apply(
            lambda x: 'Business Hours' if 8 <= x < 17 else 'Non-Business Hours'
        )

        term_df_list.append(term_df)

    term_df = pd.concat(term_df_list)

    # Group by week of the term and count weekend/weekday events
    weekend_counts = term_df[term_df['day_type'] == 'Weekend'].groupby('week_of_the_term').size()
    weekday_counts = term_df[term_df['day_type'] == 'Weekday'].groupby('week_of_the_term').size()

    # Group by week of the term and count business/non-business hours events
    business_hours_counts = term_df[term_df['business_hours'] == 'Business Hours'].groupby('week_of_the_term').size()
    non_business_hours_counts = term_df[term_df['business_hours'] == 'Non-Business Hours'].groupby('week_of_the_term').size()

    # Print results
    print(f"{'Week of the Term':<20} {'Weekend Tasks':>20} {'Weekday Tasks':>20} {'Business Hours':>20} {'Non-Business Hours':>20}")
    print("=" * 100)
    all_weeks = sorted(
        set(weekend_counts.index)
        .union(set(weekday_counts.index))
        .union(set(business_hours_counts.index))
        .union(set(non_business_hours_counts.index)),
        key=lambda x: int(x.split()[1]) if x.split()[1].isdigit() else float('inf')
    )
    results = []
    for week in all_weeks:
        weekend_count = weekend_counts.get(week, 0)
        weekday_count = weekday_counts.get(week, 0)
        business_hours_count = business_hours_counts.get(week, 0)
        non_business_hours_count = non_business_hours_counts.get(week, 0)
        print(f"{week:<20} {weekend_count:>20} {weekday_count:>20} {business_hours_count:>20} {non_business_hours_count:>20}")
        results.append([week, weekend_count, weekday_count, business_hours_count, non_business_hours_count])

    exportToCSV(results, term)

    return {
        "weekend_counts": weekend_counts,
        "weekday_counts": weekday_counts,
        "business_hours_counts": business_hours_counts,
        "non_business_hours_counts": non_business_hours_counts
    }

def exportToCSV(data, term):
    filename = f"Results/PEPS_Overall Task Scheduling_{term.capitalize()}_Term.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Week of the Term", "Weekend Tasks", "Weekday Tasks", "Business Hours", "Non-Business Hours"])
        writer.writerows(data)

    print(f"CSV exported as {filename}")

if __name__ == "__main__":
    df, dept_filler = loadTasks("no_media")
    parseTaskStartTimes(df)
    # taskLoadByHour()
    # taskLoadByDayofTheMonth()
    # taskLoadByWeekOfTheTerm()
    # analyzeTicketTiming(df)
    analyzeTicketTimingByTerm(df, "winter")