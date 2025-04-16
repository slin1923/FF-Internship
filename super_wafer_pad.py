"""
Class super wafer pad analyzes and visualizes the wafer pad dimensions.
Plots a histogram of all the measured pad X dimensions and Y dimensions.
Plots a super bond-pad style overlay plot with all the measured pad geometries.

Author: Sean Lin
Date Created: 7/2/21
Last Modified: 7/30/21
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

class super_wafer_pad(object):

    def __init__(self, nom_x, nom_y, meas_x, meas_y):
        """
        constructor for super_wafer_pad
        :param nom_x: integer describing wafer pad x size
        :param nom_y: integer describing wafer pad y size
        :param meas_x: list of measured wafer pad x sizes
        :param meas_y: list of measured wafer pad y sizes
        """
        self.nom_x = nom_x
        self.nom_y = nom_y
        self.meas_x = meas_x
        self.meas_y = meas_y
        assert len(self.meas_x) == len(self.meas_y), \
            "lists provided are not of comparable length"

    def find_average_dimensions(self):
        """
        finds averages of all x and y dimensions
        :return: [average x dimensions, average y dimension]
        """
        average_x = np.mean(self.meas_x)
        average_y = np.mean(self.meas_y)
        return average_x, average_y

    def find_std_and_quartile(self):
        """
        finds std and other relevant statistics of all x and y dimensions
        :return: [std x dimensions, std y dimensions]
        """
        std_x = np.std(self.meas_x)
        std_y = np.std(self.meas_y)
        return std_x, std_y

    def plot_nom_averages_stds(self, avg_x, avg_y, std_x, std_y, axis_x, axis_y):
        """
        plot averages stds plots the averages and standard deviations of the measured dimensions
        :param avg_x: average x width
        :param avg_y: average y width
        :param std_x: standard dev of x widths
        :param std_y: standard dev of y widths
        :param axis_x: axis to plot x data on
        :param axis_y: axis to plot y data on
        :return: NA
        """
        ax_x_xrange = axis_x.get_xlim()[1] - axis_x.get_xlim()[0]
        ax_x_yrange = axis_x.get_ylim()[1]
        ax_y_xrange = axis_y.get_xlim()[1] - axis_y.get_xlim()[0]
        ax_y_yrange = axis_y.get_ylim()[1]
        axis_x.axvline(x=self.nom_x, color="red", label="Nominal")
        axis_x.annotate(str(round(self.nom_x, 2)), xy=(self.nom_x + ax_x_xrange * 0.01, ax_x_yrange * 0.9),
                        rotation=90)
        axis_x.axvline(x=avg_x, color="limegreen", label="Average")
        axis_x.annotate(str(round(avg_x, 2)), xy=(avg_x + ax_x_xrange * 0.01, ax_x_yrange * 0.9),
                        rotation=90)
        axis_x.axvline(x=avg_x + std_x, color="gold", label="1 sigma")
        axis_x.annotate(str(round(avg_x + std_x, 2)), xy=((avg_x + std_x) + ax_x_xrange * 0.01, ax_x_yrange * 0.9),
                        rotation=90)
        axis_x.axvline(x=avg_x - std_x, color="gold")
        axis_x.annotate(str(round(avg_x - std_x, 2)), xy=((avg_x - std_x) + ax_x_xrange * 0.01, ax_x_yrange * 0.9),
                        rotation=90)
        axis_x.annotate(str("X-bias = " + str(round(avg_x - self.nom_x, 2))) + " microns", xy=(axis_x.get_xlim()[0], 0),
                        fontsize='large')
        axis_y.axvline(x=self.nom_y, color="red", label="Nominal")
        axis_y.annotate(str(round(self.nom_y, 2)), xy=(self.nom_y + ax_y_xrange * 0.01, ax_y_yrange * 0.9), rotation=90)
        axis_y.axvline(x=avg_y, color="limegreen", label="Average")
        axis_y.annotate(str(round(avg_y, 2)), xy=(avg_y + ax_y_xrange * 0.01, ax_y_yrange * 0.9), rotation=90)
        axis_y.axvline(x=avg_y + std_y, color="gold", label="1 sigma")
        axis_y.annotate(str(round(avg_y + std_y, 2)), xy=((avg_y + std_y) + ax_y_xrange * 0.01, ax_y_yrange * 0.9),
                        rotation=90)
        axis_y.axvline(x=avg_y - std_y, color="gold")
        axis_y.annotate(str(round(avg_y - std_y, 2)), xy=((avg_y - std_y) + ax_y_xrange * 0.01, ax_y_yrange * 0.9),
                        rotation=90)
        axis_y.annotate(str("Y-bias = " + str(round(avg_y - self.nom_y, 2))) + " microns", xy=(axis_y.get_xlim()[0], 0),
                        fontsize='large')

    def initiate_plots(self):
        """
        initiate plots creates and labels the subplot layout desired to represent the data
        :return: [figure, ax for histogram of x widths, ax for histogram of y widths, ax for super overlay]
        """
        fig = plt.figure(figsize=[12.8, 9.6])
        ax1 = fig.add_subplot(221)
        ax1.set_xlabel("X-Widths in microns")
        ax1.set_ylabel("Frequency")
        ax1.set_title("Measured X Widths")
        ax2 = fig.add_subplot(223)
        ax2.set_xlabel("Y-Widths in microns")
        ax2.set_ylabel("Frequency")
        ax2.set_title("Measured Y Widths")
        ax3 = fig.add_subplot(122)
        ax3.set_xlabel("X Dimension in microns")
        ax3.set_ylabel("Y Dimension in microns")
        ax3.set_title("Super Wafer Pad Overlay \n **AXES NOT SAME SCALE**")
        ax3.set_xlim(-self.nom_x * 0.8, self.nom_x * 0.8)
        ax3.set_ylim(-self.nom_y * 0.8, self.nom_y * 0.8)
        plt.tight_layout()
        return fig, ax1, ax2, ax3

    def plot_nominal_rect(self, ax):
        """
        plot nominal rect plots the nominal rectangle contained within the floats nom_x and nom_y
        :param ax: matplotlib axis to plot the rectangle on
        :return: NA
        """
        self.plot_rectangle(self.nom_x, self.nom_y, ax, 'red', 3, "Nominal Pad", 0.5)
        ax.annotate(str(self.nom_x), xy=(0, ax.get_ylim()[1] * 0.85), color='red', fontsize='large', fontweight='bold')
        ax.annotate(str(self.nom_y), xy=(ax.get_xlim()[1] * 0.85, 0), color='red', fontsize='large', fontweight='bold',
                    rotation=270)

    def plot_measured_rects(self, ax):
        """
        plot measured rects plots the measured rectangles contained within the lists meas_x and meas_y
        :param ax: matplotlib axis to plot the rectangle on
        :return: NA
        """
        for i in np.arange(len(self.meas_x)):
            self.plot_rectangle(self.meas_x[i], self.meas_y[i], ax, 'blue', 0.3, None, 0.3)

    def plot_average_rect(self, ax):
        """
        plot average rect plots the rectangle average of all measured rectangles
        :param ax: matplotlib axis to plot the rectangle on
        :return: NA
        """
        average_x = np.mean(self.meas_x)
        average_y = np.mean(self.meas_y)
        self.plot_rectangle(average_x, average_y, ax, 'limegreen', 3, "Average Measured Pad", 1)
        ax.annotate(str(round(average_x, 2)), xy=(0, ax.get_ylim()[0] * 0.9), color='limegreen', fontsize='large',
                    fontweight='bold')
        ax.annotate(str(round(average_y, 2)), xy=(ax.get_xlim()[0] * 0.9, 0), color='limegreen', fontsize='large',
                    fontweight='bold', rotation=270)

    @staticmethod
    def plot_rectangle(x, y, ax, col, linw, label, transparency):
        """
        plot_rectangle is a static helper method that acts as a basis for plotting rectangles
        :param x: x-width of the rectangle to be plotted
        :param y: y-width of the rectangle to be plotted
        :param ax: axis to plot the rectangle on
        :param col: color to plot the rectangle in
        :param linw: linewidth to plot the rectangle in
        :param label: the label of the rectangle to display on legend
        :param transparency: the transparency of the rectangle
        :return: NA
        """
        rect = mpatches.Rectangle((- x/2, - y/2), x, y, color=col, fill=False, linewidth=linw, label=label,
                                  alpha=transparency)
        ax.add_patch(rect)





