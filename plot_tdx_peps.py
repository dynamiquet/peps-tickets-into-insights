# Author: Dynamique '27
# Organization: DataSquad
# Description: This script is used to plot the output of the functions in both "analy_tdx_peps.py" and "Compare_StartTime_to_Created.py"
# Last Successfully ran: 2025/02/26 

from analyze_tdx_tickets import *
from analyze_merged_tdx_tickets import *
import matplotlib.pyplot as plt
import seaborn as sns

def plotEventLoad(df, time_unit):
    plt.figure(figsize=(12, 6))
    if time_unit.lower() == 'hour':
        column = 'event_hour'
        x_label = 'Hour of the Day'

    elif time_unit.lower() == 'day':
        column = 'event_day'
        x_label = 'Day of the Month'

    else:
        raise ValueError("Invalid time_unit. Use 'hour' or 'day'.")

    sns.countplot(x=column, data=df, color='#0b84e0')

    plt.title(f'Event Load by {x_label} (2022-2025)', fontsize=16, fontweight='bold')
    plt.xlabel(x_label, fontsize=14, fontweight='bold')
    plt.ylabel('Number of Events', fontsize=14, fontweight='bold')
    plt.xticks(plt.xticks()[0][::2]) # Skips one tick
    plt.show()
    
def plotDayofTheWeekByHour(df):
    heatmap_data = df.pivot_table(index='event_hour', columns='day_of_the_week', aggfunc='size', fill_value=0)
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_data, cmap='Blues', annot=True, fmt='d')
    plt.title('Event Load by Hour and Day of the Week (2022-2025)', fontsize=16, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.xlabel('Day of the Week', fontsize=14, fontweight='bold')
    plt.ylabel('Hour of the Day', fontsize=14, fontweight='bold')
    plt.show()

def plotDayByMonth(df):
    heatmap_data = df.pivot_table(index='event_month', columns='event_day', aggfunc='size', fill_value=0)
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_data, cmap='Blues', annot=True, fmt='d')
    plt.title('Event Load by Day and Month (2022-2025)', fontsize=16, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.xlabel('Day of the Month', fontsize=14, fontweight='bold')
    plt.ylabel('Month of the Year', fontsize=14, fontweight='bold')
    plt.show()

def plotDayOfTheWeekByWeekOfTheTermYearly(df):
    terms_years = df['term_year'].unique()
    for term_year in terms_years:
        term_df = df[df['term_year'] == term_year]
        
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weeks_order = sorted(term_df['week_of_the_term'].unique(), key=lambda x: int(x.split()[1]))

        heatmap_data = term_df.pivot_table(index='day_of_the_week', columns='week_of_the_term', aggfunc='size', fill_value=0)
        heatmap_data = heatmap_data.reindex(index=days_order, columns=weeks_order)

        plt.figure(figsize=(14, 8))
        sns.heatmap(heatmap_data, cmap='Blues', annot=True)
        plt.title(f'Event Load by Day of the Week and Week of the Term ({term_year})', fontsize=16, fontweight='bold')
        plt.ylabel('', fontsize=14, fontweight='bold')
        plt.yticks(rotation=45)
        plt.gca().invert_yaxis()
        plt.xlabel('Week of the Term', fontsize=14, fontweight='bold')
        plt.show()

def plotDayOfTheWeekByWeekOfTheTermTotal(df):
    terms = df['term'].unique()
    for term in terms:
        term_df = df[df['term'] == term]
        
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weeks_order = sorted(term_df['week_of_the_term'].unique(), key=lambda x: int(x.split()[1]))

        heatmap_data = term_df.pivot_table(index='day_of_the_week', columns='week_of_the_term', aggfunc='size', fill_value=0)
        heatmap_data = heatmap_data.reindex(index=days_order, columns=weeks_order)

        plt.figure(figsize=(14, 8))
        sns.heatmap(heatmap_data, cmap='Blues', annot=True)
        plt.title(f'Event Load by Day of the Week and Week of the Term ({term.capitalize()} 2022-2025)', fontsize=16, fontweight='bold')
        plt.ylabel('', fontsize=14, fontweight='bold')
        plt.yticks(rotation=30)
        plt.gca().invert_yaxis()
        plt.xlabel('Week of the Term', fontsize=14, fontweight='bold')
        plt.show()

def plotTopLocations(df=default_df, top_n=10):
    top_locations = topLocations(df, top_n)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_locations.values, y=top_locations.index, color='#0b84e0')
    plt.title(f'Top {top_n} Locations (2022-2025)', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Events', fontsize=14, fontweight='bold')
    plt.ylabel('Location', fontsize=14, fontweight='bold')
    plt.show()

def plotTopDepartments(df=default_df, top_n=10):
    top_departments = topDepartments(df, top_n)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_departments.values, y=top_departments.index, color='#0b84e0')
    plt.title(f'Top {top_n} Departments by Number of Events (2022-2025)', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Events', fontsize=14, fontweight='bold')
    plt.ylabel('Department', fontsize=14, fontweight='bold')
    plt.show()

def plotTopRequestors(df=default_df, top_n=10):
    top_requestors = topRequestors(df, top_n)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_requestors.values, y=top_requestors.index, color='#0b84e0')
    plt.title(f'Top {top_n} Requestors (2022-2025)', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Events', fontsize=14, fontweight='bold')
    plt.ylabel('Requestor', fontsize=14, fontweight='bold')
    plt.show()

def plotTopResponsiblePeople(df=default_df, top_n=10):
    top_responsible_people = topResponsiblePeople(df, top_n)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_responsible_people.values, y=top_responsible_people.index, color='#0b84e0')
    plt.title(f'Top {top_n} Responsible People (2022-2025)', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Events', fontsize=14, fontweight='bold')
    plt.ylabel('Responsible Person', fontsize=14, fontweight='bold')
    plt.show()

def plotTopLocationsByEventStartTime(df, top_n=15):
    # Combine 'Peps Location' and 'Other Location' into one column
    df['Location'] = df['Peps Location'].where(df['Peps Location'] != "Other", df['Other Location'])
    df = df.dropna(subset=['Location'])

    print(df.info())

    top_locations = df['Location'].value_counts().head(top_n)
    
    # Plot 
    bubble_data = df[df['Location'].isin(top_locations.index)].groupby(['event_hour', 'Location']).size().reset_index(name='counts')

    plt.figure(figsize=(20, 8))

    sns.scatterplot(data=bubble_data, x='event_hour', y='Location', size='counts', hue='Location', palette='viridis', sizes=(1, 700), legend=True, alpha=0.6)
    plt.title(f'{top_n} Most Used Locations (2022-2025)', fontsize=16, fontweight='bold')
    plt.xlabel('Event Start Time', fontsize=14, fontweight='bold')
    plt.ylabel('', fontsize=14, fontweight='bold')
    plt.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Move the legend to the far side
    plt.xticks(plt.xticks()[0][::2])  # Skips the first 5 ticks on the x-axis
    
    plt.show()

if __name__ == "__main__":
    df = loadMergedDataTickets()
    parseEventStartTimes(df)
    orderEventHoursLogically(df)
    orderDaysOfTheWeekLogically(df)

    plotTopLocationsByEventStartTime(df)

    #### Plotting 
    # df1 = eventLoadByWeekOfTheTerm(df, "winter")
    # plotDayOfTheWeekByWeekOfTheTermYearly(df1)
    # plotDayOfTheWeekByWeekOfTheTermTotal(df1)
    
    # plotEventLoad(df, "hour")
    # plotEventLoad(df, "day")
    # plotDayofTheWeekByHour(df)
    # plotDayByMonth(df)

    # # Plotting functions from analyze_tdx_tickets.py (Do not involve time )
    df2 = loadDataTickets()
    plotTopLocations(df2)
    plotTopDepartments(df2)
    plotTopRequestors(df2)
    plotTopResponsiblePeople(df2)