# Author: Dynamique '27
# Organization: DataSquad
# Description: This script is used to plot the output of the functions in both "analyze_tdx_tasks.py", and "analyze_tdx_tickets.py"
# Last successfully ran on May 16, 2025



from analyze_tdx_tickets import *
from analyze_merged_tdx_tickets import *
from analyze_tdx_tasks import *
import matplotlib.pyplot as plt
import seaborn as sns

def plotTaskLoad(df, time_unit, dept_filter=None):
    """
    Plot the task load by hour or day.

    Args:
        df (DataFrame): The DataFrame containing task data.
        time_unit (str): The time unit to plot ('hour' or 'day').
        dept_filter (str, optional): Filter for department. Options are "media_only" or None.

    Returns:
        None
    """
    if dept_filter == "media_only":
        df = dropConvoAndLTC(df)
    
    suffix = "M" if dept_filter=="media_only" else "E" if dept_filter=="no_media" else ""
    plt.figure(figsize=(12, 6))
    if time_unit.lower() == 'hour':
        column = 'task_hour'
        x_label = 'Hour of the Day'

    elif time_unit.lower() == 'day':
        column = 'task_day'
        x_label = 'Day of the Month'

    else:
        raise ValueError("Invalid time_unit. Use 'hour' or 'day'.")

    sns.countplot(x=column, data=df, color='#0b84e0')

    plt.title(f'Tasks by {x_label} (2022-2025) [{suffix}]', fontsize=15, fontweight='bold')
    plt.xlabel(x_label, fontsize=14, fontweight='bold')
    plt.ylabel('Number of Tasks', fontsize=14, fontweight='bold')
    plt.xticks(plt.xticks()[0][::2])  # Skips one tick
    plt.show()

def dropConvoAndLTC(df):
    """
    Drop tasks related to LTC and Convo events.

    Args:
        df (DataFrame): The DataFrame containing task data.

    Returns:
        DataFrame: The filtered DataFrame.
    """
    LTC = (df['task_hour_24'] == 11) & (df['day_of_the_week'] == 'Tuesday')
    convo = ((df['task_hour_24'] == 10) & (df['day_of_the_week'] == 'Friday'))
    return df[~(LTC | convo)]

def plotDayofTheWeekByHour(df, dept_filter=None):
    """
    Plot a heatmap of tasks by hour and day of the week.

    Args:
        df (DataFrame): The DataFrame containing task data.
        dept_filter (str, optional): Filter for department. Options are "media_only" or None.

    Returns:
        None
    """
    if dept_filter == "media_only":
        df = dropConvoAndLTC(df)

    suffix = "M" if dept_filter=="media_only" else "E" if dept_filter=="no_media" else ""
    heatmap_data = df.pivot_table(index='task_hour', columns='day_of_the_week', aggfunc='size', fill_value=0)
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_data, cmap='Blues', annot=True, fmt='d')
    plt.title(f'Tasks by Hour and Day of the Week (2022-2025) [{suffix}]', fontsize=15, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.xlabel('Day of the Week', fontsize=14, fontweight='bold')
    plt.ylabel('Hour of the Day', fontsize=14, fontweight='bold')
    plt.show()

def plotDayByMonth(df, dept_filter=None):
    """
    Plot a heatmap of tasks by day and month.

    Args:
        df (DataFrame): The DataFrame containing task data.
        dept_filter (str, optional): Filter for department. Options are "media_only" or None.

    Returns:
        None
    """
    if dept_filter == "media_only":
        df = dropConvoAndLTC(df)
    suffix = "M" if dept_filter=="media_only" else "E" if dept_filter=="no_media" else ""
    heatmap_data = df.pivot_table(index='task_day', columns='task_month_name', aggfunc='size', fill_value=0)
    heatmap_data.index = heatmap_data.index.astype(int)
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_data, cmap='Blues', annot=True, fmt='d')
    plt.title(f'Tasks by Month and Day (2022-2025) [{suffix}]', fontsize=15, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.xlabel('Month of the Year', fontsize=14, fontweight='bold')
    plt.ylabel('Day of the Month', fontsize=14, fontweight='bold')
    plt.yticks(rotation=0)  # Ensures the numbers on the y-axis are written in a normal direction facing up
    plt.show()

def plotDayOfTheWeekByWeekOfTheTermYearly(df, dept_filter=None):
    """
    Plot tasks by day of the week and week of the term for each year.

    Args:
        df (DataFrame): The DataFrame containing task data.
        dept_filter (str, optional): Filter for department. Options are "media_only" or None.

    Returns:
        None
    """
    if dept_filter == "media_only":
        df = dropConvoAndLTC(df)    
    
    suffix = "M" if dept_filter=="media_only" else "E" if dept_filter=="no_media" else ""
    terms_years = df['term_year'].unique()
    for term_year in terms_years:
        term_df = df[df['term_year'] == term_year]
        
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weeks_order = sorted(term_df['week_of_the_term'].unique(), key=lambda x: int(x.split()[1]))

        heatmap_data = term_df.pivot_table(index='day_of_the_week', columns='week_of_the_term', aggfunc='size', fill_value=0)
        heatmap_data = heatmap_data.reindex(index=days_order, columns=weeks_order)

        plt.figure(figsize=(14, 8))
        sns.heatmap(heatmap_data, cmap='Blues', annot=True)
        plt.title(f'Tasks by Day of the Week and Week of the Term ({term_year}) [{suffix}]', fontsize=15, fontweight='bold')
        plt.ylabel('', fontsize=14, fontweight='bold')
        plt.yticks(rotation=45)
        plt.gca().invert_yaxis()
        plt.xlabel('Week of the Term', fontsize=14, fontweight='bold')
        plt.show()

def plotDayOfTheWeekByWeekOfTheTermTotal(df, dept_filter=None):
    """
    Plot tasks by day of the week and week of the term across all years.

    Args:
        df (DataFrame): The DataFrame containing task data.
        dept_filter (str, optional): Filter for department. Options are "media_only" or None.

    Returns:
        None
    """
    if dept_filter == "media_only":
        df = dropConvoAndLTC(df)    
    
    terms = df['term'].unique()
    suffix = "M" if dept_filter=="media_only" else "E" if dept_filter=="no_media" else ""
    for term in terms:
        term_df = df[df['term'] == term]
        
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weeks_order = sorted(term_df['week_of_the_term'].unique(), key=lambda x: int(x.split()[1]))

        heatmap_data = term_df.pivot_table(index='day_of_the_week', columns='week_of_the_term', aggfunc='size', fill_value=0)
        heatmap_data = heatmap_data.reindex(index=days_order, columns=weeks_order)

        plt.figure(figsize=(14, 8))
        sns.heatmap(heatmap_data, cmap='Blues', annot=True)
        plt.title(f'Tasks by Day of the Week and Week of the Term ({term.capitalize()} 2022-2025) [{suffix}]', fontsize=15, fontweight='bold')
        plt.ylabel('', fontsize=14, fontweight='bold')
        plt.yticks(rotation=30)
        plt.gca().invert_yaxis()
        plt.xlabel('Week of the Term', fontsize=14, fontweight='bold')
        plt.show()

def plotTopLocations(df=default_df, top_n=10):
    """
    Plot the top N locations by the number of events.

    Args:
        df (DataFrame): The DataFrame containing event data.
        top_n (int): The number of top locations to display.

    Returns:
        None
    """
    top_locations = topLocations(df, top_n)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_locations.values, y=top_locations.index, color='#0b84e0')
    plt.title(f'Top {top_n} Locations (2022-2025)', fontsize=15, fontweight='bold')
    plt.xlabel('Number of Events', fontsize=14, fontweight='bold')
    plt.ylabel('Location', fontsize=14, fontweight='bold')
    plt.show()

def plotTopDepartments(df=default_df, top_n=10):
    """
    Plot the top N departments by the number of events.

    Args:
        df (DataFrame): The DataFrame containing event data.
        top_n (int): The number of top departments to display.

    Returns:
        None
    """
    top_departments = topDepartments(df, top_n)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_departments.values, y=top_departments.index, color='#0b84e0')
    plt.title(f'Top {top_n} Departments by Number of Events (2022-2025)', fontsize=15, fontweight='bold')
    plt.xlabel('Number of Events', fontsize=14, fontweight='bold')
    plt.ylabel('Department', fontsize=14, fontweight='bold')
    plt.show()

def plotTopRequestors(df=default_df, top_n=10):
    """
    Plot the top N requestors by the number of events.

    Args:
        df (DataFrame): The DataFrame containing event data.
        top_n (int): The number of top requestors to display.

    Returns:
        None
    """
    top_requestors = topRequestors(df, top_n)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_requestors.values, y=top_requestors.index, color='#0b84e0')
    plt.title(f'Top {top_n} Requestors (2022-2025)', fontsize=15, fontweight='bold')
    plt.xlabel('Number of Events', fontsize=14, fontweight='bold')
    plt.ylabel('Requestor', fontsize=14, fontweight='bold')
    plt.show()

def plotTopResponsiblePeople(df=default_df, top_n=10):
    """
    Plot the top N responsible people by the number of events.

    Args:
        df (DataFrame): The DataFrame containing event data.
        top_n (int): The number of top responsible people to display.

    Returns:
        None
    """
    top_responsible_people = topResponsiblePeople(df, top_n)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_responsible_people.values, y=top_responsible_people.index, color='#0b84e0')
    plt.title(f'Top {top_n} Responsible People (2022-2025)', fontsize=15, fontweight='bold')
    plt.xlabel('Number of Events', fontsize=14, fontweight='bold')
    plt.ylabel('Responsible Person', fontsize=14, fontweight='bold')
    plt.show()

def plotTopLocationsByEventStartTime(df, top_n=15):
    """
    Plot a bubble chart of the top N locations by event start time.

    Args:
        df (DataFrame): The DataFrame containing event data.
        top_n (int): The number of top locations to display.

    Returns:
        None
    """
    # Combine 'Peps Location' and 'Other Location' into one column
    df['Location'] = df['Peps Location'].where(df['Peps Location'] != "Other", df['Other Location'])
    df = df.dropna(subset=['Location'])

    print(df.info())

    top_locations = df['Location'].value_counts().head(top_n)
    
    # Plot 
    bubble_data = df[df['Location'].isin(top_locations.index)].groupby(['event_hour', 'Location']).size().reset_index(name='counts')

    plt.figure(figsize=(20, 8))

    sns.scatterplot(data=bubble_data, x='event_hour', y='Location', size='counts', hue='Location', palette='viridis', sizes=(1, 700), legend=True, alpha=0.6)
    plt.title(f'{top_n} Most Used Locations (2022-2025)', fontsize=15, fontweight='bold')
    plt.xlabel('Event Start Time', fontsize=14, fontweight='bold')
    plt.ylabel('', fontsize=14, fontweight='bold')
    plt.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Move the legend to the far side
    plt.xticks(plt.xticks()[0][::2])  # Skips the first 5 ticks on the x-axis
    
    plt.show()

def loadMergedDataTickets():
    """
    Load merged ticket data from the CSV file.

    Returns:
        DataFrame: The loaded DataFrame.
    """
    df = pd.read_csv("Data/Data-PEPS-TDX Tickets - Merged Report.csv")
    df['Created'] = pd.to_datetime(df['Created'], format='%m/%d/%Y', errors='coerce') # Convert 'Created' column to datetime (assuming format is MM/DD/YYYY)
    df = df.dropna(subset=['Created', 'Event Start Times'])  # Remove rows where dates are missing
    df['Event Start Times'] = df['Event Start Times'].apply(cleanEventTimeString)
    df['Event Start Times'] = df['Event Start Times'] + pd.Timedelta(hours=5)  # Adds 5 hours to account for the TDX data time zone conversion
    return df

def cleanEventTimeString(datetime_str):
    """
    Clean and parse the event start time string.

    Args:
        datetime_str (str): The datetime string to clean.

    Returns:
        datetime: The cleaned datetime object.
    """
    if pd.isna(datetime_str): # missing values
        return pd.NaT  
    cleaned_str = re.sub(r'GMT[+-]\d{4}.*', '', datetime_str).strip()

    try:
        return parser.parse(cleaned_str)
    except Exception:
        return pd.NaT

def parseEventStartTimes(df=default_df):
    """
    Parse the 'Event Start Times' column to extract time-related information.

    Args:
        df (DataFrame): The DataFrame containing event data.

    Returns:
        None
    """
    if 'Event Start Times' not in df.columns:
        raise KeyError("The 'Event Start Times' column is missing from the DataFrame.")
    df['event_hour_24'] = df['Event Start Times'].dt.hour
    df['event_hour'] = df['Event Start Times'].dt.strftime("%I %p")
    df['event_day'] = df['Event Start Times'].dt.day
    df['event_month'] = df['Event Start Times'].dt.month
    df['day_of_the_week'] = df['Event Start Times'].dt.day_name()

if __name__ == "__main__":
    df, dept_filter = loadTasks()
    parseTaskStartTimes(df)
    orderTaskHoursLogically(df)
    orderDaysOfTheWeekLogically(df)
    orderTaskMonthsLogically(df)
    
    # plotTaskLoad(df, "hour", dept_filter)
    # plotTaskLoad(df, "day", dept_filter)
    # plotDayofTheWeekByHour(df, dept_filter)
    # plotDayByMonth(df, dept_filter)
   
    df1 = taskLoadByWeekOfTheTerm(df, "winter")
    plotDayOfTheWeekByWeekOfTheTermYearly(df1, dept_filter)
    plotDayOfTheWeekByWeekOfTheTermTotal(df1, dept_filter)
    


    df2 = loadMergedDataTickets()
    # parseEventStartTimes(df2)
    # plotTopLocationsByEventStartTime(df2)

    # # Plotting functions from analyze_tdx_tickets.py (Do not involve time )
    df3 = loadDataTickets()
    # plotTopLocations(df3)
    # plotTopDepartments(df3)
    # plotTopRequestors(df3)
    # plotTopResponsiblePeople(df3)