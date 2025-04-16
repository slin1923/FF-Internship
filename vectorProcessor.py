"""
Class VecComp handles the pre-processing of all vectors taken from the VEECO software.
Preprocessing entails
    a. verification that data is in form of list
    b. verification that data in list is of correct type
    c. linear interpolation of any missing values within the list

Author: Sean Lin
Date Created: 6/22/2021
Last modified: 7/30/2021
"""
import math
import numpy as np
import pandas as pd

class vectorProcessor(object):

    def type_checker_raw(self, vector):
        """
        type_checker checks whether the input list contains only float values or np.NAN

        :param vector: the list to be checked
        :return: T/F to indicate whether type checker was passed
        """
        good = True
        if isinstance(vector, list):
            for x in vector:
                good = (isinstance(x, int) or isinstance(x, float)) and good
            return good
        else:
            # print ("vector is not a list")  #  UNCOMMENT FOR DEBUGGING
            return False

    def cut_back(self, vector):
        """
        cuts all np.NAN valued elements from the back of a list
        :param vector: list to be snipped
        :return: [number of items removed, snipped list]
        """
        count = 0
        for i in np.arange(len(vector))[::-1]:
            if math.isnan(vector[i]):
                count = count + 1
            else:
                break
        new_vector = vector[:len(vector) - count]
        return [count, new_vector]

    def cut_front(self, vector):
        """
        cuts all np.NAN valued elements from the front of a list.
        :param vector: list to be snipped
        :return: [number of items removed, snipped list]
        """
        count = 0
        for i in np.arange(len(vector)):
            if math.isnan(vector[i]):
                count = count + 1
            else:
                break
        new_vector = vector[count:]
        return [count, new_vector]

    def patch_vector(self, vector):
        """
        patch_vector is a static method that patches up raw vectors extracted from VEECO
        method of patching missing values: linear interpolation
        :param vector: vector represented by a list that needs to be patched
        :return: the patched vector/list
        """
        pandas_series = pd.Series(vector).interpolate().tolist()
        return pandas_series

    def type_checker_post(self, vector):
        """
            type_checker checks whether the input list contains only float values and does not contain np.NAN

            :param vector: the list to be checked
            :return: T/F to indicate whether type checker was passed
        """
        good = True
        if isinstance(vector, list):
            for x in vector:
                good = ((isinstance(x, float) or isinstance(x, int)) and not math.isnan(x)) and good
            return good
        else:
            # print ("vector is not a list")  #  UNCOMMENT FOR DEBUGGING
            return False




