"""
   class multiVector is responsible for performing analysis on a SET of VEECO scrub mark profiles.

   Author: Sean Lin
   Date Created: 6/22/2021
   Last Modified: 7/29/2021
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from vectorProcessor import vectorProcessor

class multiVector(object):

    def find_PC(self, data):
        """
        finds the first principle component of the set of vectors.

        :param data: 2D list of vectors
        :return: first principle component vector
        """
        pca = PCA(n_components=1)
        pca.fit(data)
        return pca.components_[0]

    def dot_products(self, data):
        """
        takes a dot product between the normalized vector i and normalized average vector to determine a correlation
        coefficient.  This coefficient acts as a metric for how similar each individual vector is to the average vector.

        :param data: 2D list of vectors
        :return: list of dot products (correlation coefficients)
        """
        # finds the norm of the average scrub mark profile vector
        avg_norm = np.linalg.norm(self.average_vector(data))
        # uses norm found above to normalize average scrub mark profile vector to magnitude 1
        avg_normalized = [x / avg_norm for x in self.average_vector(data)]
        d_prods = []
        count = 0
        print("\n-------------CORR COEFFS--------------")
        for lst in data:
            count += 1
            # finds the norm of the ith scrub mark profile vector
            list_norm = np.linalg.norm(lst)
            # uses norm found above to normalize ith scrub mark profile vector to magnitude 1
            list_normalized = [x / list_norm for x in lst]
            d_prod = np.dot(list_normalized, avg_normalized)
            d_prods.append(d_prod)
            print("Correlation coefficient of vector " + str(count) + " : " + str(d_prod))
        return d_prods

    @staticmethod
    def average_vector(data):
        """
        finds the single average vector of all vectors in data
        :param data: 2D list of vectors
        :return: average vector
        """
        avg_vector = []
        for i in np.arange(len(data[0])):
            values = []
            for lst in data:
                values.append(lst[i])
            avg_vector.append(np.mean(values))
        return avg_vector

    def plot_vectors(self, boolPCA):
        """
        final output for all data
        :param boolPCA: boolean determined by user which prompts either to show or not show principle component
        :return: [correlation coefficients of all the individuals scrub marks with average scrub mark (list),
         figure to be saved]
        """
        colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan"]
        fig, ax = plt.subplots(2, figsize=(12.6, 9.8))
        d_prods = self.dot_products(self.data)
        for lst in self.data:
            ax[0].plot(self.xVals, lst, '--')
        ax[0].plot(self.xVals, self.average_vector(self.data), 'r-', label="average")
        if boolPCA:
            ax[0].plot(self.xVals, self.find_PC(self.data), 'k-', label="principal component")
        categorical = []
        for i in np.arange(len(self.data)):
            categorical.append("mark " + str(i))
        barplot = ax[1].bar(categorical, d_prods)
        for i in np.arange(len(self.data)):
            barplot[i].set_color(colors[i % 10])
        fig.tight_layout(pad=2.0)
        ax[0].set_title("Z-height all marks")
        ax[0].set_ylabel("microns")
        ax[1].set_title("Correlation Between mark i and average")
        ax[0].legend()
        return d_prods, fig


    @staticmethod
    def align_data(xVals, data):
        """
        static method align_data makes sure that all the scrub mark profile vectors in data are of the same length.
        If np.NAN values are cut from the beginning or end of any vectors, the length of vectors will no longer
        be uniform.  All other vectors are snipped until their lengths match the length of the shortest vector.
        X values are also snipped accordingly.  Lengths of vectors are final after snipping.

        Utilizes vectorProcessor class to help snip NAN values off of ends of vectors
        and return the number of elements snipped.

        :param xVals: x values corresponding to all vectors
        :param data: 2D list of vectors
        :return: aligned 2D list of vectors (may not be patched)
        """
        global list
        vp = vectorProcessor()
        allNumCutFront = []
        allNumCutBack = []
        for list in data:
            numCutFront = 0
            numCutBack = 0
            if not vp.type_checker_raw(list):
                print("vector in dataset does not pass type checker")
            else:
                numCutFront = vp.cut_front(list)[0]
                numCutBack = vp.cut_back(list)[0]
            allNumCutFront.append(numCutFront)
            allNumCutBack.append(numCutBack)
        # find the max number of elements cut from both the front and back across ALL scrub mark profile vectors in set.
        # idea is that you can only be as long as the shortest vector in your set.
        maxCutFront = max(allNumCutFront)
        maxCutBack = max(allNumCutBack)
        snipped_data = []
        for list in data:
            snipped_list = list[maxCutFront:len(list) - maxCutBack]
            snipped_data.append(snipped_list)
        xVals_snipped = xVals[maxCutFront:len(list) - maxCutBack]
        return xVals_snipped, snipped_data

    @staticmethod
    def patch_data(data):
        """
        patch_data is a function that patches all np.NAN values in the middle of a list for all
        lists in data.
        Utilizes vectorProcessor class.

        :param data: 2D list of all vectors
        :return: patched 2D list of all vectors
        """
        vp = vectorProcessor()
        patched_data = []
        for lst in data:
            patched_list = vp.patch_vector(lst)
            patched_data.append(patched_list)
        return patched_data

    def __init__(self, xVals, data):
        """
        constructor for the PCA class
        :param xVals: list of all x values on vector(s)
        :param data: 2D list containing all vectors
        """
        self.xVals, unpatched_data = self.align_data(xVals, data)
        self.data = self.patch_data(unpatched_data)
