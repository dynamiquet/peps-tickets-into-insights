# Author: Auiannce Euwing '26, Dynamique Twizere '27
# Organization: DataSquad
# Description: This code pulls from the TDX_PEPS_Tickets_Report_January.csv and contains functions that return the top popular locations, other locations, compares the created date and the resolved date, returns the top departments, requestors, and people responsible for tickets.
# Last Successfully ran: 2025/03/24

import pandas as pd

# Load the dataset
def loadDataTickets():
    file_path = "Data/TDX_Peps_Tickets_Report_January.csv"  
    df = pd.read_csv(file_path, parse_dates=['Created', 'Resolved Date'])
    return df
default_df = loadDataTickets()

# Identify the most popular locations
def topLocations(df=default_df, number=30):
    all_locations = pd.concat([df['PEPS Location'], df['Other Location'].dropna()])
    combined_locations = all_locations.value_counts().head(number)
    print("\nCombined Top Locations:\n", combined_locations)
    return combined_locations

# Compare created date vs resolved date
def resolutionTime(df=default_df): # Not really needed?
    df['Resolution Time (Days)'] = (df['Resolved Date'] - df['Created']).dt.days
    resolution_stats = df['Resolution Time (Days)'].describe()
    print("\nResolution Time Statistics:\n", resolution_stats)
    return resolution_stats

# Identify the top 5 departments that request the most events
def topDepartments(df=default_df, number=5):
    top_departments = df['Acct/Dept'].value_counts().head(number)
    print("\nTop 5 Departments by Number of Events:\n", top_departments)
    return top_departments

# Identify the top 5 requestors
def topRequestors(df=default_df, number=5):
    top_requestors = df['Requestor'].value_counts().head(number)
    print("\nTop 5 Requestors:\n", top_requestors)
    return top_requestors

# Identify the top 10 people responsible for events
def topResponsiblePeople(df=default_df, number=5):
    top_responsible_people = df['Responsibility'].value_counts().head(number)
    print("\nTop 10 People Responsible for Events:\n", top_responsible_people)
    return top_responsible_people

if __name__ == "__main__":
    df = loadDataTickets()
    # print(df.info())
    topLocations()
    resolutionTime()
    # topDepartments()
    # topRequestors()
    # topResponsiblePeople() 