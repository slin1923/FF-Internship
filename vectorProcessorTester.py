"""
Testing script for vector pre-processing.
Tests the full list of processing commands that prime a vector for input to either single
or multiple vector analysis

Author: Sean Lin
Date Created: 6/23/21
Last Modified: 6/25/21
"""

import numpy as np
from vectorProcessor import vectorProcessor

def test_type_checker_raw():
    """
    tests the type of a raw vector from VEECO
    """
    vp = vectorProcessor()
    vec1 = [np.NAN, np.NAN, 1, 2, 3, 4, np.NAN, np.NAN, 5, 6, 7, 8, np.NAN, np.NAN]
    vec2 = ["---", "---", 1, 2, 3, 4, "---", "---", 5, 6, 7, 8, "---", "---"]
    assert vp.type_checker_raw(vec1) == True
    assert vp.type_checker_raw(vec2) == False

def test_cut_back():
    """
    tests whether cutting null values from back of list works
    """
    vp = vectorProcessor()
    vec1 = [1, 2, 3, 4, 5, np.NAN, np.NAN]
    ans = [1, 2, 3, 4, 5]
    output1 = vp.cut_back(vec1)
    assert output1[0] == 2
    assert output1[1] == ans, "answers dont match"
    vec2 = [np.NAN, np.NAN, 1, 2, 3, 4, 5]
    ans = [np.NAN, np.NAN, 1, 2, 3, 4, 5]
    output2 = vp.cut_back(vec2)
    assert output2[0] == 0
    assert output2[1] == ans


def test_cut_front():
    """
    tests whether cutting null values from front of list works
    """
    vp = vectorProcessor()
    vec1 = [1, 2, 3, 4, 5, np.NAN, np.NAN]
    ans = [1, 2, 3, 4, 5, np.NAN, np.NAN]
    output1 = vp.cut_front(vec1)
    assert output1[0] == 0
    assert output1[1] == ans, "answers d ont match"
    vec2 = [np.NAN, np.NAN, 1, 2, 3, 4, 5]
    ans = [1, 2, 3, 4, 5]
    output2 = vp.cut_front(vec2)
    assert output2[0] == 2
    assert output2[1] == ans

def test_patch():
    """
    tests whether patching null values in the middle of a vector works
    method of patching: linear interpolation
    """
    vp = vectorProcessor()
    vec1 = [1, 2, 3, np.NAN, np.NAN, np.NAN, 4, 5]
    ans = [1, 2, 3, 3.25, 3.50, 3.75, 4, 5]
    patched_boi = vp.patch_vector(vec1)
    assert patched_boi == ans

def test_type_checker_post():
    """
    tests whether final vector is primed for analysis
    """
    vp = vectorProcessor()
    vec1 = [np.NAN, np.NAN, 1, 2, 3, np.NAN, 4, 5, 6, np.NAN, np.NAN]
    vec2 = [0, 1, 1.1, 2, 2.2, 3, 3.3]
    assert vp.type_checker_post(vec1) == False
    assert vp.type_checker_post(vec2) == True

def full_stack_test():
    """
    tests all functions across a single vector.
    """
    vp = vectorProcessor()
    vec = [np.NAN, np.NAN, np.NAN, 1, 2, np.NAN, 4, np.NAN, np.NAN, 7, 8, 9, np.NAN]
    ans = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if vp.type_checker_raw(vec):
        processedVec = vp.cut_front(vec)[1]
        processedVec = vp.cut_back(processedVec)[1]
        processedVec = vp.patch_vector(processedVec)
        assert vp.type_checker_post(processedVec) == True
        assert processedVec == ans
    else:
        print("did not pass full stack test")

if __name__ == '__main__':
    test_type_checker_raw()
    print("raw type checking test passed")
    test_cut_back()
    print("cut back test passed")
    test_cut_front()
    print("cut front test passed")
    test_patch()
    print("patch test passed")
    test_type_checker_post()
    print("post type checking test passed")
    full_stack_test()
    print("passed full stack test!")

