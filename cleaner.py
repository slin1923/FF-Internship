"""
class cleaner is a simple script that cleans the Nikon data from a raw output csv so the data is readable by the other
classes contained within this project

Author: Sean Lin
Date Created: 7/6/21
Last Modified: 7/30/21
"""
import numpy as np
import pandas as pd
import csv
class Cleaner(object):
    def __init__(self, filename):
        """
        constructor for the Cleaner class.  Raw Nikon output CSVs contain 20 mysterious extra blank rows.  If any manual
        edits to the CSV such as removal of blank rows, constructor accounts for both possibilities.

        constructor also creates instance variables
            1. self.dataset: the CLEAN dataset that the cleaner will be working with
            2. self.X_fails: the X locations of all the failed points
            3. self.Y_fails: the Y locations of all the failed points

        :param filename: string that contains name of .csv file
        """
        with open(filename) as csv_file:
            reader = csv.reader(csv_file)
            row1 = next(reader)
            if (len(row1) == 1):
                raw_data = pd.read_csv(filename, skiprows=20)
            else:
                raw_data = pd.read_csv(filename)
        self.dataset, self.X_fails, self.Y_fails = self.clean(raw_data)

    def get_nominal_pad_sizes(self):
        """
        get_nominal_pad_sizes returns the nominal pad size as indicated by the raw Nikon output csv.
        Looks into the rows labeled 'HW_L1' and 'VW_L1' and set any non-zero value as the value.

        :return: nominal X pad dimension and nominal Y pad dimension
        """
        nom_X_dimension = 0
        nom_Y_dimension = 0
        for index, row in self.dataset.iterrows():
            if row[2] == "HW_L1":
                if not (row[3] == 0):
                    nom_X_dimension = row[3]
            if row[2] == "VW_L2":
                if not (row[3] == 0):
                    nom_Y_dimension = row[3]
        return nom_X_dimension, nom_Y_dimension

    def extract_XY(self):
        """
        extract XY extracts the X and Y global location data from the raw .csv file
        extracted locations are coordinates measured in microns

        :return: [nominal X locations, nominal Y locations, measured X locations, measured Y locations]
        """
        rslt_df_X = self.dataset.loc[self.dataset['Unnamed: 2'] == 'X']
        rslt_df_Y = self.dataset.loc[self.dataset['Unnamed: 2'] == 'Y']
        nom_X = rslt_df_X['Nominal'].tolist()
        nom_Y = rslt_df_Y['Nominal'].tolist()
        meas_X = rslt_df_X['1'].tolist()
        meas_Y = rslt_df_Y['1'].tolist()
        return nom_X, nom_Y, meas_X, meas_Y

    def extract_widths(self):
        """
        extract widths extracts the X and Y widths of each wafer pad.
        extracted widths are in microns
        :return: [measured X widths, measured Y widths]
        """
        rslt_df_HW = self.dataset.loc[self.dataset['Unnamed: 2'] == 'HW_L1']
        rslt_df_VW = self.dataset.loc[self.dataset['Unnamed: 2'] == 'VW_L2']
        meas_x_widths = rslt_df_HW['1'].tolist()
        meas_y_widths = rslt_df_VW['1'].tolist()
        return meas_x_widths, meas_y_widths

    @staticmethod
    def clean(dataset):
        """
        clean is a method that pre-processes the output csv so that readings off of the Nikon
        that return an error are removed from the dataset.

        All error readings from the Nikon are output as the value 9999.9999.
        This method finds and drops all pad data that corresponds to 9999.9999

        There is a tiny chance a pad was not read as an error, but the nominal data matches
        9999.9999 microns exactly.  This edge case is small enough to ignore.
        :return: cleaned dataset (list), X locations of FAILURES, Y locations of FAILURES
        """
        rows_to_drop = []
        nom_err_X_location = []
        nom_err_Y_location = []
        num_rows_removed = 0
        for index, row in dataset.iterrows():
            if (row['1'] == 9999.9999) or (row['1'] == np.NAN):
                rows_to_drop.append(index)
                if (row[2] == 'X'):
                    nom_err_X_location.append(row['Nominal'])
                if (row[2] == 'Y'):
                    nom_err_Y_location.append(row['Nominal'])
                num_rows_removed += 1
        print(str(int(num_rows_removed / 5)) + " failed measurements removed")
        return dataset.drop(labels=rows_to_drop), nom_err_X_location, nom_err_Y_location

    def remove_outliers(self, meas_X_dims, meas_Y_dims, meas_X_pos, meas_Y_pos, nom_X_pos, nom_Y_pos):
        """
        remove_outliers removes outlying data from the raw Nikon file that may worsen the scale of plots if not removed.
        These typically occur when the Nikon caliper identifies a confocal feature at a nominal spot, but this nominal
        feature is heavily distorted or is along the edge of the wafer and is thus neither a true pad or a misread.

        The determination of outliers is dependent upon the pad DIMENSIONS, NOT LOCATIONS.  The Nikon never outputs
        grossly outlying LOCATIONS because the field-of-view of the Nikon caliper is limited already.  However, pad
        DIMENSIONS can certainly be read as much smaller or larger than they should be, thus DIMENSIONS are a better
        indicator of outlying data.

        Even though DIMENSIONS are used as the metric for determining outlying data, once an outlier has been IDed
        the corresponding reading is tossed out of ALL LISTS, not just the lists storing X and Y dimensions.

        An outlier is considered any data point outside of 4 standard deviations.  4 standard deviations was chosen
        because typical wafers contain on the order of 1000 units, thus taking 1000 as the theoretical max good point
        sample size (assuming no sampling down), there is still an expected number of 0 outlying points.

        :param meas_X_dims: RAW list of all measured X pad dimensions
        :param meas_Y_dims: RAW list of all measured Y pad dimensions
        :param meas_X_pos: RAW list of all measured X pad positions
        :param meas_Y_pos: RAW list of all measured Y pad positions
        :param nom_X_pos: nominal pad X positions taken from AutoCAD
        :param nom_Y_pos: nominal pad Y positions taken from AutoCAD
        :return: X_dims_cleaned, Y_dims_cleaned, X_pos_cleaned, Y_pos_cleaned, X_nom_cleaned, Y_nom_cleaned,
        X_dims_misread, Y_dims_misread, X_pos_misread, Y_pos_misread, X_nom_misread, Y_nom_misread
        ** basically returns all input lists with the outlier removed and then returns the data for outliers removed**
        """
        # for storage of good data
        X_dims_cleaned = []
        Y_dims_cleaned = []
        X_pos_cleaned = []
        Y_pos_cleaned = []
        X_nom_cleaned = []
        Y_nom_cleaned = []

        # for storage of misread 'outlier' data
        X_dims_misread = []
        Y_dims_misread = []
        X_pos_misread = []
        Y_pos_misread = []
        X_nom_misread = []
        Y_nom_misread = []

        # finds the 4 std dev range outside of which data will be consider a 'misread outlier'
        x_dim_upper = np.mean(meas_X_dims) + 4 * np.std(meas_X_dims)
        x_dim_lower = np.mean(meas_X_dims) - 4 * np.std(meas_X_dims)
        y_dim_upper = np.mean(meas_Y_dims) + 4 * np.std(meas_Y_dims)
        y_dim_lower = np.mean(meas_Y_dims) - 4 * np.std(meas_Y_dims)
        outlier_count = 0
        for i in np.arange(len(meas_X_dims)):
            if (x_dim_lower < meas_X_dims[i] < x_dim_upper):
                if (y_dim_lower < meas_Y_dims[i] < y_dim_upper):
                    X_dims_cleaned.append(meas_X_dims[i])
                    Y_dims_cleaned.append(meas_Y_dims[i])
                    X_pos_cleaned.append(meas_X_pos[i])
                    Y_pos_cleaned.append(meas_Y_pos[i])
                    X_nom_cleaned.append(nom_X_pos[i])
                    Y_nom_cleaned.append(nom_Y_pos[i])
            else:
                outlier_count += 1
                X_dims_misread.append(meas_X_dims[i])
                Y_dims_misread.append(meas_Y_dims[i])
                X_pos_misread.append(meas_X_pos[i])
                Y_pos_misread.append(meas_Y_pos[i])
                X_nom_misread.append(nom_X_pos[i])
                Y_nom_misread.append(nom_Y_pos[i])
        print(str(outlier_count) + " outlying measurements removed (> 4 Std Dev)")
        return X_dims_cleaned, Y_dims_cleaned, X_pos_cleaned, Y_pos_cleaned, X_nom_cleaned, Y_nom_cleaned, \
               X_dims_misread, Y_dims_misread, X_pos_misread, Y_pos_misread, X_nom_misread, Y_nom_misread

    def get_X_fails(self):
        """
        simple accessor method for retrieving instance variable self.X_fails
        :return:
        """
        return self.X_fails

    def get_Y_fails(self):
        """
        simple accessor method for retrieving instance variable self.Y_fails
        :return:
        """
        return self.Y_fails