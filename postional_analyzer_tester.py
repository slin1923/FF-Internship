"""
Tester class for positional_analyzer

Author: Sean Lin
Date Created: 6/30/21
Last Modified: 7/02/21
"""
from positional_analyzer import positional_analyzer
import numpy as np
def test_simple_hypothetical():
    """
    a sanity checker on a simple set of measurements
    """
    diameter = 304800
    nom_x = [53880, -53880, -53880, 53880]
    nom_y = [53880, 53880, -53880, -53880]
    meas_x = [70000, -70000, -70000, 70000]
    meas_y = [70000, 70000, -70000, -70000]
    pa = positional_analyzer(diameter, nom_x, nom_y, meas_x, meas_y)
    U, V, U_mean_adj, V_mean_adj = pa.find_vectors()
    pa.plot_field(U, V, U_mean_adj, V_mean_adj)
    pa.plot_errors(U_mean_adj, V_mean_adj, "test translation")

def test_random_many():
    """
    tests 200 randomly generated points on the wafer with random errors
    """
    diameter = 304800
    nom_x = []
    nom_y = []
    meas_x = []
    meas_y = []
    for i in np.arange(200):
        x = np.random.uniform(-diameter / 2, diameter / 2)
        y = np.random.uniform(-diameter / 2, diameter / 2)
        if x**2 + y**2 < (diameter / 2)**2:
            nom_x.append(x)
            nom_y.append(y)
            error_x = np.random.uniform(-100, 100)
            error_y = np.random.uniform(-100, 100)
            meas_x.append(x + error_x)
            meas_y.append(y + error_y)
    pa = positional_analyzer(diameter, nom_x, nom_y, meas_x, meas_y)
    U, V, U_mean_adj, V_mean_adj = pa.find_vectors()
    pa.plot_field(U, V, U_mean_adj, V_mean_adj)
    pa.plot_errors(U_mean_adj, V_mean_adj, "test random")

def test_translational_many():
    """
    tests 200 randomly generated points on the wafer with slightly varying errors
    that all point in the same general direction
    """
    diameter = 304800
    nom_x = []
    nom_y = []
    meas_x = []
    meas_y = []
    for i in np.arange(200):
        x = np.random.uniform(-diameter / 2, diameter / 2)
        y = np.random.uniform(-diameter / 2, diameter / 2)
        if x ** 2 + y ** 2 < (diameter / 2) ** 2:
            nom_x.append(x)
            nom_y.append(y)
            error_x = np.random.uniform(120, 100)
            error_y = np.random.uniform(-120, -100)
            meas_x.append(x + error_x)
            meas_y.append(y + error_y)
    pa = positional_analyzer(diameter, nom_x, nom_y, meas_x, meas_y)
    U, V, U_mean_adj, V_mean_adj = pa.find_vectors()
    pa.plot_field(U, V, U_mean_adj, V_mean_adj)
    pa.plot_errors(U_mean_adj, V_mean_adj, "test translation")

def test_divergence_many():
    """
    tests 200 randomly generated points on the wafer with errors that diverge from center
    """
    diameter = 304800
    nom_x = []
    nom_y = []
    meas_x = []
    meas_y = []
    for i in np.arange(200):
        x = np.random.uniform(-diameter / 2, diameter / 2)
        y = np.random.uniform(-diameter / 2, diameter / 2)
        if x ** 2 + y ** 2 < (diameter / 2) ** 2:
            nom_x.append(x)
            nom_y.append(y)
            error_x = x * 0.001
            error_y = y * 0.001
            meas_x.append(x + error_x)
            meas_y.append(y + error_y)
    pa = positional_analyzer(diameter, nom_x, nom_y, meas_x, meas_y)
    U, V, U_mean_adj, V_mean_adj = pa.find_vectors()
    pa.plot_field(U, V, U_mean_adj, V_mean_adj)
    pa.plot_errors(U_mean_adj, V_mean_adj, "test divergence")

if __name__ == '__main__':
    # test_simple_hypothetical()
    # test_random_many()
    # test_translational_many()
    test_divergence_many()