"""
    Class outlier Analyzer provides statistics on the extremes of a single scrub mark profile.
    statistics include
        a. the value and locations of the top n outliers above and below the zero.
        b. the magnitude and location of the n most extreme slopes.
        c. the range of a certain slopes
        d. the sharpness of each of the outliers listed.

    Author: Sean Lin
    Date Created: 6/23/21
    Last Modified 7/30/21
"""
import matplotlib.pyplot as plt
import numpy as np
from vectorProcessorTester import vectorProcessor

class outlierAnalyzer(object):
    def __init__(self, xVals, vector):
        """
        Constructor for the outlier analyzer class.
        Constructor also type checks the input vector and 'patches' it up

        :param xVals: the x-values of the scrub mark profile
        :param vector: the z-values of the scrub mark profile
        """
        vp = vectorProcessor()
        p_vec = []
        num_cut_front = 0
        num_cut_back = 0
        if not vp.type_checker_raw(vector):
            print("vector given to outlier Analyzer does not pass type checker")
        else:
            [num_cut_front, p_vec] = vp.cut_front(vector)
            [num_cut_back, p_vec] = vp.cut_back(p_vec)
            p_vec = vp.patch_vector(p_vec)

        if vp.type_checker_post(p_vec):
            self.vector = p_vec
            self.xVals = xVals[num_cut_front:len(xVals) - num_cut_back]
        else:
            print("something went wrong during processing")

    @staticmethod
    def is_local_minima(lst, index):
        """
        determines if a value at a given index in a list is a relative maxima or minima.
        values at the end are considered as well and only compared to the one adjacent value.

        :param lst: list to be considered
        :param index: index to be considered
        :return: boolean indicating whether is or is not maxima/minima
        """
        assert index < len(lst), "index out of list bounds"
        if index == 0:
            if lst[index + 1] > lst[index]:
                return True
            else:
                return False
        elif index == len(lst) - 1:
            if lst[index - 1] > lst[index]:
                return True
            else:
                return False
        else:
            if (lst[index - 1] > lst[index]) & (lst[index + 1] > lst[index]):
                return True
            else:
                return False

    @staticmethod
    def is_local_maxima(lst, index):
        """
        ^see documentation for 'is_local_minima'
        :param lst: ^
        :param index: ^
        :return: ^
        """
        assert index < len(lst), "index out of list bounds"
        if index == 0:
            if lst[index + 1] < lst[index]:
                return True
            else:
                return False
        elif index == len(lst) - 1:
            if lst[index - 1] < lst[index]:
                return True
            else:
                return False
        else:
            if (lst[index - 1] < lst[index]) & (lst[index + 1] < lst[index]):
                return True
            else:
                return False

    def find_extrema(self, num):
        """
        Finds the max/min extrema of the vector passed to the class

        :param num: number of max and min extrema to be found
        :return: a list of lists:
                [locations of mins, values of mins, locations of maxes, values of maxes]
        """
        v = self.vector
        mins = []
        corr_mins_x_values = []
        maxes = []
        corr_max_x_values = []
        for x in np.arange(num):
            mins.append(v[x])
            corr_mins_x_values.append(self.xVals[x])
            maxes.append(v[x])
            corr_max_x_values.append(self.xVals[x])
        for i in np.arange(len(v)):
            if self.is_local_minima(v, i):
                if v[i] < max(mins):
                    new_min = v[i]
                    index_of_old_min = mins.index(max(mins))
                    mins[index_of_old_min] = new_min
                    corr_mins_x_values[index_of_old_min] = self.xVals[i]
            elif self.is_local_maxima(v, i):
                if v[i] > min(maxes):
                    new_max = v[i]
                    index_of_old_max = maxes.index(min(maxes))
                    maxes[index_of_old_max] = new_max
                    corr_max_x_values[index_of_old_max] = self.xVals[i]
        print ("\n -------------EXTREMA--------------")
        for i in np.arange(len(mins)):
            print ("Min of " + str(mins[i]) + " at loc " + str(corr_mins_x_values[i]))
        print("---")
        for i in np.arange(len(maxes)):
            print ("Max of " + str(maxes[i]) + " at loc " + str(corr_max_x_values[i]))
        return [corr_mins_x_values, mins, corr_max_x_values, maxes]

    def find_derivative(self, num):
        """
        Finds the slopes of the scrub mark profile.
        Finds n number of maximum and minimum derivatives on the scrub mark profile and the x-locations they occur at.
        Finds the weight of each of the n maximum and minimum derivatives on the scrub mark profile
        **NOTE**
        for documentation of what weight is, see @staticmethod derivative_weight

        :param num: The number of derivative extremes user desires to observe
        :return: a list of lists
                [list of all discrete slopes, location of min slopes, min slopes, weights of min slopes,
                location of max slopes, max slopes, weights of max slopes]
        """
        xstep = np.mean(np.diff(self.xVals))
        ysteps = np.diff(self.vector)
        yderiv = ysteps / xstep
        derivmin = np.sort(yderiv)[0:num]
        derivmax = np.sort(yderiv)[::-1][0:num]
        weightsmin = []
        weightsmax = []
        corrXmin = []
        corrXmax = []
        yderivList = yderiv.tolist()
        for d in derivmin:
            i = yderivList.index(d)
            weight = self.derivative_weight(i, yderiv)
            xVal = self.xVals[i]
            corrXmin.append(xVal)
            weightsmin.append(weight)
        for d in derivmax:
            i = yderivList.index(d)
            weight = self.derivative_weight(i, yderiv)
            xVal = self.xVals[i]
            corrXmax.append(xVal)
            weightsmax.append(weight)
        print("\n-------------SLOPES--------------")
        for i in np.arange(len(derivmin)):
            print("Min slope of " + str(derivmin[i]) + " at loc " + str(corrXmin[i]) +
                  " with weight " + str(weightsmin[i]))
        print("---")
        for i in np.arange(len(derivmin)):
            print("Max slope of " + str(derivmax[i]) + " at loc " + str(corrXmax[i]) +
                  " with weight " + str(weightsmax[i]))
        return [yderiv, corrXmin, derivmin, weightsmin, corrXmax, derivmax, weightsmax]

    @staticmethod
    def derivative_weight(index, derivative_vector):
        """
        finds the weight of a specific slope.  The 'weight' of a slope is calculated by finding the number
        discrete steps between the most recent point where the slope hits zero and the nearest next point
        where the slope will hit zero again.
        intuitively, the weight of the slope can be thought of as the 'duration' of the slope before the slope
        changes sign

        weight is intended as an indicator

        :param index: index to be considered
        :param derivative_vector: list-represented function to be considered
        :return: the 'weight' of the slope
        """
        count = 0
        if derivative_vector[index] > 0:
            upward_index = index
            downward_index = index -1
            while upward_index < len(derivative_vector) and derivative_vector[upward_index] > 0:
                upward_index += 1
                count += 1
            while downward_index >= 0 and derivative_vector[downward_index] > 0:
                downward_index -= 1
                count += 1
            return count
        else:
            upward_index = index
            downward_index = index - 1
            while upward_index < len(derivative_vector) and derivative_vector[upward_index] < 0:
                upward_index += 1
                count += 1
            while downward_index >= 0 and derivative_vector[downward_index] < 0:
                downward_index -= 1
                count += 1
            return count

    def plot_vector(self, num_extrema, num_derivs):
        """
        plots the scrub mark profile passed to the class as well as relevant points indicating extrema and
        points where slope maximizes

        :param: num_extrema: number of maxes and mins to be analyzed on the scrub mark profile
        :param: num_derivs: number of max and min slopes to be analyzed on the scrub mark profile
        :return: [extreme_data (list), slope_data(list), figure to be saved]
        """
        fig, ax = plt.subplots(2, figsize=(12.6, 9.8))

        # plots the original scrub mark profile
        ax[0].set_title("Z-values")
        ax[0].set_ylabel("microns")
        ax[0].plot(self.xVals, self.vector)
        ax[0].hlines(y = np.mean(self.vector), xmin=self.xVals[0], xmax=self.xVals[len(self.xVals)-1],
                   linestyles='--', colors='plum')

        # plots the maxima and minima on the scrub mark profile
        extrema_data = self.find_extrema(num_extrema)
        ax[0].plot(extrema_data[0], extrema_data[1], 'rv')
        ax[0].plot(extrema_data[2], extrema_data[3], 'g^')

        # finds and plots the derivatives of the scrub mark profile
        slope_data = self.find_derivative(num_derivs)
        ax[0].grid(axis="x")
        ax[1].set_title("Slopes")
        ax[1].set_ylabel("microns/micron")
        ax[1].plot(self.xVals[:len(self.xVals) - 1], slope_data[0], 'orange')
        ax[1].hlines(y=np.mean(slope_data[0]), xmin=self.xVals[0], xmax=self.xVals[len(self.xVals)-1],
                   linestyles='--', colors='plum')

        # plots the maxima and minima on the derivative of the scrub mark profile
        ax[1].plot(slope_data[1], slope_data[2], 'bv')
        ax[1].plot(slope_data[4], slope_data[5], 'm^')
        ax[1].grid(axis="x")
        fig.tight_layout(pad=2.0)

        return extrema_data, slope_data, fig


