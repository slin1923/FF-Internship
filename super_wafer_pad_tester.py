"""
super_wafer_pad tester is a tester script for class super_wafer_pad

Author: Sean Lin
Date Created: 7/2/21
Last modified: 7/6/21
"""
from super_wafer_pad import super_wafer_pad
import matplotlib.pyplot as plt
import numpy as np

def test_single_rect():
    """
    simple sanity test for single rectangle with manual data collection
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(223)
    ax3 = fig.add_subplot(122)
    plt.tight_layout()
    nom_x = 75
    nom_y = 95
    meas_x = [73.5, 75.9, 73.5, 78.4, 75.9, 73.5, 73.5]
    meas_y = [95.5, 95.5, 93.1, 93.1, 95.5, 93.1, 95.5]
    swp = super_wafer_pad(nom_x, nom_y, meas_x, meas_y)
    ax3.set_xlim(-nom_x * 0.75, nom_x * 0.75)
    ax3.set_ylim(-nom_y * 0.75, nom_y * 0.75)
    ax1.hist(meas_x)
    ax2.hist(meas_y)
    #swp.plot_measured_rects(ax3)
    swp.plot_nominal_rect(ax3)
    swp.plot_average_rect(ax3)
    plt.show()

def test_random():
    """
    test for randomly generated measurements over a uniform distribution
    """
    nom_x = 75
    nom_y = 95
    meas_x = []
    meas_y = []
    for i in np.arange(100):
        x_err = np.random.uniform(- nom_x / 10 - 1, nom_x / 10 - 1)
        y_err = np.random.uniform(- nom_y / 10 - 1, nom_y / 10 - 1)
        meas_x.append(nom_x + x_err)
        meas_y.append(nom_y + y_err)
    swp = super_wafer_pad(nom_x, nom_y, meas_x, meas_y)
    fig, ax1, ax2, ax3 = swp.initiate_plots()
    ax3.set_xlim(-nom_x * 0.7, nom_x * 0.7)
    ax3.set_ylim(-nom_y * 0.7, nom_y * 0.7)
    ax1.hist(meas_x)
    ax2.hist(meas_y)
    avg_x, avg_y = swp.find_average_dimensions()
    std_x, std_y = swp.find_std_and_quartile()
    swp.plot_nom_averages_stds(avg_x, avg_y, std_x, std_y, ax1, ax2)
    swp.plot_measured_rects(ax3)
    swp.plot_nominal_rect(ax3)
    swp.plot_average_rect(ax3)
    ax1.legend(loc='lower right')
    ax2.legend(loc='lower right')
    ax3.legend(loc='upper left')
    plt.show()

if __name__ == '__main__':
    test_random()