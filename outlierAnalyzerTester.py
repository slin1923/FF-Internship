"""
    A tester script for the outlier Analyzer Class

    Author: Sean Lin
    Date Created: 6/23/21
    Last Modified: 6/24/21
"""
import numpy as np
from outlierAnalyzer import outlierAnalyzer

def test_patch_vector():
    """
    tester method for the patch_vector method in outlierAnalysis class
    :return
    """
    oa = outlierAnalyzer([], [])
    vec1 = [0, 1, 2, 3, np.NAN, 6]
    xVals1 = [1, 2, 3, 4, 5, 6]
    ans1 = [[1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4.5, 6]]
    assert oa.ns_patch_vector(xVals1, vec1) == ans1
    vec2 = [np.NAN, np.NAN, np.NAN, np.NAN, 1, 2, 3, 4]
    xVals2 = [1, 2, 3, 4, 5, 6, 7, 8]
    ans2 = [[5, 6, 7, 8], [1, 2, 3, 4]]
    assert oa.ns_patch_vector(xVals2, vec2) == ans2
    vec3 = [1, 2, 3, 4, np.NAN, np.NAN]
    xVals3 = [1, 2, 3, 4, 5, 6]
    ans3 = [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 4, 4]]
    assert oa.ns_patch_vector(xVals3, vec3) == ans3

def test_find_extrema():
    xVals = np.arange(20)
    vector = [np.NAN, 1, 2, 3, 4, 5, 4, 3, np.NAN, 2, 1, 0, -1, -2, -3, -2, -3, -1, 1, np.NAN]

if __name__ == "__main__":
    test_patch_vector()
    print("patch_vector_passed")

