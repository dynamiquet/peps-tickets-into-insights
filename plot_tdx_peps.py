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
    
    sns.countplot(x=column, data=df, color='Gray')
    
    plt.title(f'Event Load by {x_label}')
    plt.xlabel(x_label)
    plt.ylabel('Number of Events')
    plt.xticks(plt.xticks()[0][::2]) # Skips one tick

def plotDayofTheWeekByHour(df):
    heatmap_data = df.pivot_table(index='event_hour', columns='day_of_the_week', aggfunc='size', fill_value=0)
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_data, cmap='Blues', annot=True, fmt='d')
    plt.title('Heatmap of Event Load by Hour and Day of the Week')
    plt.gca().invert_yaxis()
    plt.ylabel('Hour of the Day')
    plt.xlabel('Day of the Week')
    plt.show()

def plotDayByMonth(df):
    heatmap_data = df.pivot_table(index='event_month', columns='event_day', aggfunc='size', fill_value=0)
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_data, cmap='Blues', annot=True, fmt='d')
    plt.title('Heatmap of Event Load by Day and Month')
    plt.gca().invert_yaxis()
    plt.xlabel('Day of the Month')
    plt.ylabel('Month of the Year')
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
        plt.title(f'Heatmap of Event Load by Day of the Week and Week of the Term ({term_year})')
        plt.ylabel('Day of the Week')
        plt.gca().invert_yaxis()
        plt.xlabel('Week of the Term')
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
        plt.title(f'Heatmap of Event Load by Day of the Week and Week of the Term (Total for {term.capitalize()})')
        plt.ylabel('Day of the Week')
        plt.gca().invert_yaxis()
        plt.xlabel('Week of the Term')
        plt.show()

if __name__ == "__main__":
    df = loadMergedDataTickets()
    parseEventStartTimes(df)
    orderEventHoursLogically(df)
    orderDaysOfTheWeekLogically(df)

    #### Plotting 
    # df1 = eventLoadByWeekOfTheTerm(df, "fall")
    # plotDayOfTheWeekByWeekOfTheTermYearly(df1)
    # plotDayOfTheWeekByWeekOfTheTermTotal(df1)
    
    plotEventLoad(df, "hour")
    plotEventLoad(df, "day")
    plotDayofTheWeekByHour(df)
    plotDayByMonth(df)