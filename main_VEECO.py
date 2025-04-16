"""
Executable python function that is directly called by user.

Author: Sean Lin
Date Created: 6/21/21
Last Modified: 7/30/21
"""
import csv
import os
import numpy as np
import pandas as pd
from mutliVector import multiVector
from outlierAnalyzer import outlierAnalyzer

if __name__ == '__main__':
    # ask user whether performing single-cursor or multi-cursor analysis
    prompt_analysis_type = input("What kind of analysis would you like done? \n1. For single-cursor analysis, type "
                                     "\'s\' \n2. For multi-cursor analysis, type \'m\' \n:")
    if prompt_analysis_type == "s" or prompt_analysis_type == "S":
        # ask user how many extreme values they are concerned with
        num_extrema = int(input("How many extreme values would you like to observe? : "))

        # Navigate to folder named "single_cursor"
        home_dir = os.getcwd()
        os.chdir(home_dir + "/single_cursor")
        single_cursor_dir = os.getcwd()
        for files in os.walk(single_cursor_dir):
            names = files[2]
            for name in names:

                # ensure that image files and output data from this script are not read as inputs
                if not ((name.__contains__(".png")) or (name.__contains__("_SLOPE&EXTREMA_DATA"))):
                    # read scrub mark profile information
                    raw_vector = pd.read_csv(name).drop([0, 1])
                    raw_vector.name = name
                    print("\n\n" + name)
                    name = name[:len(name) - 4]

                    # extract x values
                    x = list(map(float, raw_vector.x.tolist()))

                    # extract z values
                    z_values = raw_vector.iloc[:, 1].tolist()
                    z_values = [z if z != " ---" else np.NAN for z in z_values]  # replace all instances of " ---" with np.NAN
                    z_values = list(map(float, z_values))

                    # runs the single-cursor slope and outlier analyzer
                    oa = outlierAnalyzer(x, z_values)
                    extreme_data, slope_data, fig = oa.plot_vector(num_extrema, num_extrema)

                    # saves the plot to a png file
                    fig.savefig(name + "_PLOT.png")

                    # saves the output data to a csv file
                    with open(name + "_SLOPE&EXTREMA_DATA" + ".csv", 'w', newline="") as myfile:
                        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

                        # write the minimum Z values on the scrub mark profile vector and their locations
                        wr.writerow(["minimum Z Values", "X-location"])
                        for i in np.arange(len(extreme_data[0])):
                            min = extreme_data[1][i]
                            min_loc = extreme_data[0][i]
                            wr.writerow([min, min_loc])
                        wr.writerow([])

                        # write the maximum Z values on the scrub mark profile vector and their locations
                        wr.writerow(["maximum Z Values", "X-location"])
                        for i in np.arange(len(extreme_data[2])):
                            max = extreme_data[3][i]
                            max_loc = extreme_data[2][i]
                            wr.writerow([max, max_loc])
                        wr.writerow([])

                        # write the minimum profile slopes and their location and weight
                        wr.writerow(["Minimum Slopes (microns/micron)", "X-location", "Weight"])
                        for i in np.arange(len(slope_data[1])):
                            min_slope = slope_data[2][i]
                            min_slope_loc = slope_data[1][i]
                            min_slope_weight = slope_data[3][i]
                            wr.writerow([min_slope, min_slope_loc, min_slope_weight])
                        wr.writerow([])

                        # write the maximum profile slopes and their location and weight
                        wr.writerow(["Maximum Slopes (microns/micron)", "X-location", "Weight"])
                        for i in np.arange(len(slope_data[1])):
                            max_slope = slope_data[2][i]
                            max_slope_loc = slope_data[1][i]
                            max_slope_weight = slope_data[3][i]
                            wr.writerow([max_slope, max_slope_loc, max_slope_weight])
                    print("\nData file and plots for " + name + " generated!")
    elif prompt_analysis_type == "m" or prompt_analysis_type == "M":

        # navigate to the folder named "multi_cursor"
        home_dir = os.getcwd()
        os.chdir(home_dir + "/multi_cursor")
        multi_cursor_dir = os.getcwd()
        for files in os.walk(multi_cursor_dir):
            names = files[2]
            for name in names:

                # ensure that image files and output data from this script are not read as inputs
                if not ((name.__contains__(".png")) or (name.__contains__("CORRELATION_DATA"))):

                    # read in the data file
                    raw_data = pd.read_csv(name).drop([0, 1])
                    raw_data.name = name
                    print("\n\n" + name)
                    name = name[:len(name) - 4]

                    # prime the vectors for analysis
                    x = list(map(float, raw_data.x.tolist()))
                    raw_vectors = []
                    for i in np.arange(1, len(raw_data.columns)):
                        y = raw_data.iloc[:, i]
                        y = [z if z != " ---" else np.NAN for z in y]  # replace all instances of " ---" with np.NAN
                        y = list(map(float, y))
                        raw_vectors.append(y)

                    # perform multi-vector analysis and plot to an image
                    smartypants = multiVector(x, raw_vectors)
                    correlations, fig = smartypants.plot_vectors(False)
                    fig.savefig(name + "_PLOT.png")

                    # write correlation data to an output csv
                    with open(name + "_CORRELATION_DATA" + ".csv", 'w', newline="") as myfile:
                        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                        wr.writerow(["Scrub Mark Profile", "Correlation Coefficient"])
                        for i in np.arange(len(correlations)):
                            coefficient = correlations[i]
                            wr.writerow([i + 1, coefficient])
                    print("\nData file and plots for " + name + " generated!")
    else:
        print("your analysis type was not one of the two options.")
    input("\nPress \'Enter\' to exit program")

