"""
XY wizard is a class that handles the extraction of XY coordinates from AutoCAD drawings.
XY coordinates are found relative to the center of the wafer (set as the origin)
XY wizard works on one pad per unit (marked off by street fiducials).
The XY coordinate of the same pad across all units is written to a CSV file.
User may choose to sample down to a smaller sample size with reduced coverage density.
In case user chooses to sample down, number of output coordinates corresponds to user-specified value.

**NOTE**
This script assumes the wafer is symmetric about the X and Y axes.
    Unit layout information from the first quadrant is prompted from the user.
    The layout of the first quadrant is assumed for all 3 other quadrants.

Therefore, the script works best for wafers with symmetry about the X and Y axes.

Author: Sean Lin
Date Created: 7/6/21
Date Modified: 7/28/21
"""
import numpy as np
import matplotlib.pyplot as plt

class XYwizard(object):

    def visual_verification(self, x, y, diam):
        """
        Plots all points that will be written to the csv file for Nikon input.
        The plot is meant as a means for which the user can verify that the samples are
        evenly spread out to their liking across the wafer.

        :param x: X location of all the to-be-written coordinates in millimeters
        :param y: Y location of all the to-be-written coordinates in millimeters
        :param diam: diameter of the wafer in millimeters
        :return: NA, plots a matplotlib scatter plot
        """
        print("please verify that the plotted sample array is acceptable and close the plot when done")
        fig, ax = plt.subplots()
        ax.scatter(x, y)
        wafer = plt.Circle((0, 0), diam / 2, color='b', fill=False)
        ax.set_aspect('equal')
        ax.add_patch(wafer)
        ax.set_xlim(-diam / 2, diam / 2)
        ax.set_ylim(-diam / 2, diam / 2)
        plt.show()

    def sample_down(self, x, y, num_samples):
        """
        Takes in a list of coordinates and samples down to the num_samples.
        Method of sampling down is linearly spaced points across the original list.

        If the next to-be-written point happens to lie just above the previously written point (a "stacked point"),
        for the purpose of maintaining even spacing, the true point written will be the point indexed in-between
        the previously written point and the next to-be-written point.

        :param x: list of all X coordinates
        :param y: list of all Y coordinates
        :param num_samples: number of samples in the requested smaller sample set
        :return:
        """
        samp_down_x = []
        samp_down_y = []
        previous_x = 9999 # 9999 is a dummy number used only for initiating the previous_x value
        ds_indices = np.linspace(0, len(x) - 1, num_samples)
        # gap is used to determine the interval between successive indices given the new sample size
        # gap / 2 is the offset necessary in case a to-be-written point lies just above the previously written point
        gap = ds_indices[1] - ds_indices[0]
        for i in ds_indices:
            x_to_append = x[int(i)]
            y_to_append = y[int(i)]
            if x_to_append == previous_x:
                # performs the offsetting in case of stacked points.
                j = i - (gap / 2)
                samp_down_x.append(x[int(j)])
                samp_down_y.append(y[int(j)])
                previous_x = x[int(j)]
            else:
                samp_down_x.append(x_to_append)
                samp_down_y.append(y_to_append)
                previous_x = x_to_append
        return samp_down_x, samp_down_y

    def findXY(self, xDim, yDim, steps, iCoord):
        """
        findXY finds the X and Y locations of the same pad across all units on the wafer.
        X and Y coordinates are relative to the center of the wafer (the origin)

        **NOTE**
        within all for loop conditionals, there is a "-1" offset.
        this offset exists for the purpose of edge-avoidance.
        we are not looking to sample from die sites at the very edge of the wafer.
        keeping a buffer along the edge also reduces the risk of a misread when running on the Nikons

        :param xDim: x dimension of each UNIT
        :param yDim: y dimension of each UNIT
        :param steps: number of UNITS per ROW in QUADRANT I
                      length of steps is the same as number of rows in QUADRANT I
        :param iCoord: initial coordinate of desired pad on UNIT at corner of QUADRANT 1
        :return: list x and y which are the coordinates of all analogous pads on all other die sites
        """
        currX = iCoord[0]
        currY = iCoord[1]
        x = []
        y = []
        # handles quadrant I
        for i in np.arange(len(steps) - 1):
            for j in np.arange(steps[i] - 1):
                x.append(currX)
                y.append(currY)
                currX = currX + xDim
            currX = iCoord[0]
            currY = currY + yDim

        # handles quadrant II
        currX = iCoord[0] - xDim
        currY = iCoord[1]
        for i in np.arange(len(steps) - 1):
            for j in np.arange(steps[i] - 1):
                x.append(currX)
                y.append(currY)
                currX = currX - xDim
            currX = iCoord[0] - xDim
            currY = currY + yDim

        # handles quadrant III
        currX = iCoord[0] - xDim
        currY = iCoord[1] - yDim
        for i in np.arange(len(steps) - 1):
            for j in np.arange(steps[i] - 1):
                x.append(currX)
                y.append(currY)
                currX = currX - xDim
            currX = iCoord[0] - xDim
            currY = currY - yDim

        # handles quadrant IV
        currX = iCoord[0]
        currY = iCoord[1] - yDim
        for i in np.arange(len(steps) - 1):
            for j in np.arange(steps[i] - 1):
                x.append(currX)
                y.append(currY)
                currX = currX + xDim
            currX = iCoord[0]
            currY = currY - yDim

        return x, y