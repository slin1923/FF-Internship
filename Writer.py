"""
class Writer is a class that facilitates the writing of all analyzed numerical data
into a single CSV file.

Author: Sean Lin
Date Created: 7/20/21
Last Modified: 7/30/21
"""
class Writer(object):
    def write_single_value(self, writer, message, value):
        """
        rather unnecessary method that writes a single scalar value with an attached label to a CSV
        :param writer: writer object for CSV
        :param message: message associated with value
        :param value: value to record
        :return: NA
        """
        writer.writerow([message, value])

    def write_2_values(self, writer, x_dim, y_dim):
        """
        writes values of two lists into a series of rows in a CSV
        :param writer: writer object for CSV
        :param x_dim: list of measured X pad dimensions
        :param y_dim: list of measured Y pad dimensions
        :return: NA
        """
        for x, y in zip(x_dim, y_dim):
            writer.writerow([x, y])

    def write_4_values(self, writer, xNom, yNom, xCoord, yCoord):
        """
        writes values of four lists into a series of rows in a CSV
        :param writer: writer object for CSV
        :param xNom: list of nominal X pad locations
        :param yNom: list of nominal Y pad locations
        :param xCoord: list of measured X pad locations
        :param yCoord: list of measured Y pad locations
        :return: NA
        """
        for xn, yn, xc, yc in zip(xNom, yNom, xCoord, yCoord):
            writer.writerow([xn, yn, xc, yc])






