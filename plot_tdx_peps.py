# Author: Dynamique '27
# Organization: DataSquad
# Description: This script is used to plot the output of the functions in both "analy_tdx_peps.py" and "Compare_StartTime_to_Created.py"
# Last Successfully ran: 2025/02/26

import matplotlib.pyplot as plt
from analyze_tdx_tickets import *
from analyze_tdx_merged_tickets import *
import seaborn as sns

# Plots event load based on time unit ('hour' or 'day').
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
    
    sns.countplot(x=column, data=df, palette='viridis')
    
    plt.title(f'Event Load by {x_label}')
    plt.xlabel(x_label)
    plt.ylabel('Number of Events')
    plt.xticks(plt.xticks()[0][::2]) # Skips one tick

def plotDayofTheWeekByHour(df):
    heatmap_data = df.pivot_table(index='event_hour', columns='day_of_the_week', aggfunc='size', fill_value=0)
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='d')
    plt.title('Heatmap of Event Load by Hour and Day of the Week')
    plt.gca().invert_yaxis()
    plt.ylabel('Hour of the Day')
    plt.xlabel('Day of the Week')
    plt.show()

def plotDayByMonth(df):
    heatmap_data = df.pivot_table(index='event_month', columns='event_day', aggfunc='size', fill_value=0)
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='d')
    plt.title('Heatmap of Event Load by Day and Month')
    plt.gca().invert_yaxis()
    plt.xlabel('Day of the Month')
    plt.ylabel('Month of the Year')
    plt.show()

# TO DO: Plot EVENT LOAD by DAY OF THE WEEK by WEEK OF THE TERM
# This going to be a heatmap with week number on x-axis; day of the week on y-axis; and the number of events as the color intensity

def plotDayOfTheWeekOfTheTerm(df):
    heatmap_data = df.pivot_table(index='day_of_the_week', columns='week_of_the_term', aggfunc='size', fill_value=0)
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='d')
    plt.title('Heatmap of Event Load by Day of the Week and Week of the Term')
    plt.ylabel('Day of the Week')
    plt.xlabel('Week of the Term')
    plt.show()

if __name__ == "__main__":
    df = loadDataTickets()
    parseEventStartTimes(df)
    orderEventHoursLogically(df)
    orderDaysOfTheWeekLogically(df)

    df1 = divideUpTrimesters(df)
    plotDayOfTheWeekOfTheTerm(df1)

    #### Plotting

    # plotEventLoad(df, "hour")
    # plotEventLoad(df, "day")
    # plotDayofTheWeekByHour(df)
    # plotDayByMonth(df)