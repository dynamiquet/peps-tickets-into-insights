# DataSquad, Auiannce Euwing '26, code last successfully run 2025/01/14
# This code pulls from the TDX_Peps_Tickets_Report_January.csv and returns the 5 most popular Peps locations, 5 most popular Other locations, Compares the created date and the resolved date, returns the 5 most popular departments, 5 most popular requestors and the top 10 people responsible for tickets.  


import pandas as pd

# Load the dataset
file_path = "TDX_Peps_Tickets_Report_January.csv"  
df = pd.read_csv(file_path, parse_dates=['Created', 'Resolved Date'])

# 1. Identify the most popular locations
popular_locations = df['PEPS Location'].value_counts().head(5)
print("Most Popular Locations:")
print(popular_locations)

# 2. Identify the most popular other locations
popular_other_locations = df['Other Location'].dropna().value_counts().head(5)
print("\nMost Popular Other Locations:")
print(popular_other_locations)

# 3. Compare created date vs resolved date
df['Resolution Time (Days)'] = (df['Resolved Date'] - df['Created']).dt.days
resolution_stats = df['Resolution Time (Days)'].describe()
print("\nResolution Time Statistics:")
print(resolution_stats)

# 4. Identify the top 5 departments that request the most events
top_departments = df['Acct/Dept'].value_counts().head(5)
print("\nTop 5 Departments by Number of Events:")
print(top_departments)

# 5. Identify the top 5 requestors
top_requestors = df['Requestor'].value_counts().head(5)
print("\nTop 5 Requestors:")
print(top_requestors)

# 6. Identify the top 10 people responsible for events
top_responsible_people = df['Responsibility'].value_counts().head(10)
print("\nTop 10 People Responsible for Events:")
print(top_responsible_people)

# Event Start Times
