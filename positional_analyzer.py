"""
Class positional analyzer creates a vector field representing wafer bond pad positional errors.
Also plots the X/Y positional error vs X/Y positional references.
Also plots the X/Y dimensional errors vs X/Y positional references.

Author: Sean Lin
Date Created: 6/30/21
Last Modified: 7/30/21
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
class positional_analyzer(object):
    def __init__(self, wafer_diameter, nominal_x, nominal_y, measured_x, measured_y):
        """
        Constructor for the positional analyzer class
        :param wafer_diameter: diameter of the wafer at hand
        :param nominal_x: nominal x positions of wafer bond pads from PCIF or CAD files
        :param nominal_y: nominal y positions of wafer bond pads from PCIF or CAD files
        :param measured_x: measured x positions
        :param measured_y: measured y positions
        """
        self.diam = wafer_diameter
        self.nom_x = nominal_x
        self.nom_y = nominal_y
        self.meas_x = measured_x
        self.meas_y = measured_y
        assert len(self.nom_x) == len(self.nom_y) == len(self.meas_x) == len(self.meas_y), \
            "lists provided are not of comparable length"

    def find_vectors(self):
        """
        Finds the error vectors between the nominal and measured positions
        :return: [x component of error vectors, y component of error vectors]
        """
        U = [x-y for x, y in zip (self.meas_x, self.nom_x)]
        V = [x-y for x, y in zip (self.meas_y, self.nom_y)]
        U_mean = np.mean(U)
        V_mean = np.mean(V)
        U_mean_adj = [i - U_mean for i in U]
        V_mean_adj = [i - V_mean for i in V]
        return U, V, U_mean_adj, V_mean_adj

    @staticmethod
    def find_principal_components(U, V):
        """
        finds the 2 principal components of the error vectors.
        principal components represent the primary direction of variance on error vectors
        :param U: x components of error vectors
        :param V: y components of error vectors
        :return: [principal components, corresponding singular values]
        """
        pca = PCA(n_components=2)
        data = []
        for i in np.arange(len(U)):
            vector = []
            zero_vec = [0, 0]
            vector.append(U[i])
            vector.append(V[i])
            data.append(vector)
            data.append(zero_vec)
        pca.fit(data)
        return pca.components_, pca.singular_values_

    def plot_field(self, U, V, U_mean_adj, V_mean_adj, X_fails, Y_fails, X_misread, Y_misread):
        """
        plots a quiver plot with all error vectors and principal components
        includes a slider to magnify vectors for visual aid
        :param U: x components of error vectors
        :param V: y components of error vectors
        :param U_mean_adj: list U but with a scalar offset so mean U is 0
        :param V_mean_adj: list V but with a scalar offset so mean V is 0
        :param X_fails: X location of all FAILED readings (to be plotted as a RED point)
        :param Y_fails: Y location of all FAILED readings (to be plotted as a RED point)
        :param X_misread: X location of all MISREAD readings (to be plotted as an ORANGE point)
        :param Y_misread: Y location of all MISREAD readings (to be plotted as an ORANGE point)
        :return: figure containing both quiver plots
        """
        pca_comp, pca_sv = self.find_principal_components(U, V)
        pca_comp_mean_adj, pca_sv_mean_adj = self.find_principal_components(U_mean_adj, V_mean_adj)

        fig, ax = plt.subplots(1, 2, figsize=[16, 12])
        wafer1 = plt.Circle((0, 0), self.diam / 2, color='b', fill=False)
        wafer2 = plt.Circle((0, 0), self.diam / 2, color='b', fill=False)
        p1 = ax[0].quiver(self.nom_x, self.nom_y, U, V, color='gray')
        p1_mean_adj = ax[1].quiver(self.nom_x, self.nom_y, U_mean_adj, V_mean_adj, color='gray')
        p1.scale_units = "xy"
        p1_mean_adj.scale_units = "xy"
        ax[0].add_patch(wafer1)
        ax[0].set_title("Raw Error Vector Field\n**Vector Magnitudes Relative**")
        ax[0].set_xlim(-self.diam / 1.6, self.diam / 1.6)
        ax[0].set_ylim(-self.diam / 1.6, self.diam / 1.6)
        ax[1].add_patch(wafer2)
        ax[1].set_title("Mean-Zeroed Error Vector Field\n**Vector Magnitudes Relative**")
        ax[1].set_xlim(-self.diam / 1.6, self.diam / 1.6)
        ax[1].set_ylim(-self.diam / 1.6, self.diam / 1.6)
        p2 = ax[0].quiver(0, 0, pca_comp[0][0] * pca_sv[0], pca_comp[0][1] * pca_sv[0], color='g',
                          label='Principal Variance 1 with relative weight ' + str(round(pca_sv[0], 3)))
        p3 = ax[0].quiver(0, 0, pca_comp[1][0] * pca_sv[1], pca_comp[1][1] * pca_sv[1], color='r',
                          label='Principal Variance 2 with relative weight ' + str(round(pca_sv[1], 3)))
        p2_2 = ax[1].quiver(0, 0, pca_comp_mean_adj[0][0] * pca_sv_mean_adj[0],
                            pca_comp_mean_adj[0][1] * pca_sv_mean_adj[0], color='g',
                            label='Principal Variance 1 with relative weight ' + str(round(pca_sv_mean_adj[0], 3)))
        p3_2 = ax[1].quiver(0, 0, pca_comp_mean_adj[1][0] * pca_sv_mean_adj[1], pca_comp_mean_adj[1][1] *
                            pca_sv_mean_adj[1], color='r', label='Principal Variance 2 with relative weight '
                                                                 + str(round(pca_sv_mean_adj[1], 3)))
        ax[0].set_aspect('equal', adjustable='box')
        ax[1].set_aspect('equal', adjustable='box')
        if (len(X_fails) > 0):
            ax[0].scatter(X_fails, Y_fails, color='red', label='Failures')
            ax[1].scatter(X_fails, Y_fails, color='red', label='Failures')
        if (len(X_misread) > 0):
            ax[0].scatter(X_misread, Y_misread, color='orange', label='Misreads')
            ax[1].scatter(X_misread, Y_misread, color='orange', label='Misreads')
        p2.scale_units = "xy"
        p3.scale_units = "xy"
        p2_2.scale_units = "xy"
        p3_2.scale_units = "xy"
        ax[0].legend(loc='upper right')
        ax[1].legend(loc='upper right')
        fig.tight_layout()
        return fig

    def plot_errors(self, U, V, title):
        """
        plot errors plots the X and Y errors to the X and Y locations.  Also plots the line of best fit.
        :param U: X 'errors'
        :param V: Y 'errors'
        :param title: title of the error vs reference plot
        :return: slope of regression line of: x vs x, y vs y, x vs y, y vs x graphs
        """
        # initiate subplots
        fig, ax = plt.subplots(2, 2, figsize=[12.8, 9.6])
        x_v_x = ax[0][0]
        y_v_y = ax[1][0]
        x_v_y = ax[0][1]
        y_v_x = ax[1][1]

        # scatter points and fit regression lines
        x_v_x.scatter(self.nom_x, U)
        y_v_y.scatter(self.nom_y, V)
        x_v_y.scatter(self.nom_y, U)
        y_v_x.scatter(self.nom_x, V)
        p_x_v_x = np.polyfit(self.nom_x, U, 1)
        p_y_v_y = np.polyfit(self.nom_y, V, 1)
        p_x_v_y = np.polyfit(self.nom_y, U, 1)
        p_y_v_x = np.polyfit(self.nom_x, V, 1)

        # plot the linear regression line
        range = np.arange(-self.diam / 2, self.diam / 2)
        x_v_x.plot(range, p_x_v_x[0] * range + p_x_v_x[1], '-r')
        y_v_y.plot(range, p_y_v_y[0] * range + p_y_v_y[1], '-r')
        x_v_y.plot(range, p_x_v_y[0] * range + p_x_v_y[1], '-r')
        y_v_x.plot(range, p_y_v_x[0] * range + p_y_v_x[1], '-r')

        # set titles and annotations
        x_v_x.set_title("X " + title + " to X reference")
        x_v_x.set_xlabel("X reference")
        x_v_x.set_ylabel("X " + title)
        x_v_x.annotate("Slope = " + str(round(p_x_v_x[0] * 1000000, 4)) + " ppm",
                       xy=(x_v_x.get_xlim()[0], x_v_x.get_ylim()[0]), color='red', fontsize='large')
        y_v_y.set_title("Y " + title + " to Y reference")
        y_v_y.set_xlabel("Y reference")
        y_v_y.set_ylabel("Y " + title)
        y_v_y.annotate("Slope = " + str(round(p_y_v_y[0] * 1000000, 4)) + " ppm",
                       xy=(y_v_y.get_xlim()[0], y_v_y.get_ylim()[0]), color='red', fontsize='large')
        x_v_y.set_title("X " + title + " to Y reference")
        x_v_y.set_xlabel("Y reference")
        x_v_y.set_ylabel("X " + title)
        x_v_y.annotate("Slope = " + str(round(p_x_v_y[0] * 1000000, 4)) + " ppm",
                       xy=(x_v_y.get_xlim()[0], x_v_y.get_ylim()[0]), color='red', fontsize='large')
        y_v_x.set_title("Y " + title + " to X reference")
        y_v_x.set_xlabel("X reference")
        y_v_x.set_ylabel("Y " + title)
        y_v_x.annotate("Slope = " + str(round(p_y_v_x[0] * 1000000, 4)) + " ppm",
                       xy=(y_v_x.get_xlim()[0], y_v_x.get_ylim()[0]), color='red', fontsize='large')

        # finishing touches
        fig.tight_layout()

        return p_x_v_x[0], p_y_v_y[0], p_x_v_y[0], p_y_v_x[0], fig


