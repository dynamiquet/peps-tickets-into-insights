# Author: Dynamique '27
# Organization: DataSquad
# Description: This script is used to plot the output of the functions in both "analy_tdx_peps.py" and "Compare_StartTime_to_Created.py"
# Last Successfully ran: 2025/02/21

import matplotlib.pyplot as plt
import numpy as np
from analyze_tdx_tickets import *
from analyze_tdx_merged_tickets import *

# Runs the function provided as argument (e.g loadByDay) and returns the time (day) and the load (number of events) as 2 lists
def parseImportedFunction(imported_function):
    temp_dict = imported_function().to_dict()
    data = list(temp_dict.keys())
    frequency = list(temp_dict.values())
    return data, frequency

def main():
    plt.title("Test Title")
    data, frequency = parseImportedFunction(loadByHour) # Change this to loadByHour to test another function, for example
    plt.bar(data, frequency) # Plot as a bar. You can plot as plot too, using "plot"
    plt.xlabel("Data (Specify, e.g. days, hours, etc.)")
    plt.ylabel("Frequency")

    plt.show()


if __name__ == "__main__":
    main()