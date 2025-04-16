"""
Main method that vertically integrates all classes within project.
Method crawls through all sub-folders for wafers in the Nikon_Outputs directory and generates
the proper plots and csv results from each.
Call this method when usage is necessary.

Author: Sean Lin
Date Created: 7/8/21
Last Modified: 8/06/21
"""
import os
import shutil
import matplotlib.pyplot as plt
import csv
from cleaner import Cleaner
from positional_analyzer import positional_analyzer
from super_wafer_pad import  super_wafer_pad
from Writer import Writer

if __name__ == '__main__':
    # Navigating to the folder "Nikon_Outputs"
    home_dir = os.getcwd()
    Nikon_output_dir = home_dir + "/Nikon_Outputs"
    processed_dir = home_dir + "/PROCESSED_DATA&PLOTS"
    os.chdir(Nikon_output_dir)

    # Iterate through all wafer sub-folders within "Nikon_Outputs"
    for root, osubdirs, ofiles in os.walk(Nikon_output_dir):
        for folder in osubdirs:
            # Navigate into the wafer folder iterated across
            os.chdir(Nikon_output_dir + "/" + folder)
            curr_wafer_folder_dir = os.getcwd()
            for root, subdirs, files in os.walk(curr_wafer_folder_dir):
                # iterating through each file in the wafer's folder
                for name in files:
                    # checking that file iterated across is not a PROCESSED.csv output, XYin.csv input,
                    # FAILURE.csv output, or image
                    if not (name.__contains__("XYin")):
                        # creates the output folder in the "PROCESSED_DATA&PLOTS" directory if not already present
                        # if output folder is already present, delete it and recreate an empty one with same name
                        output_folder = os.path.join(processed_dir, name[:len(name) - 4] + "_DATA&PLOTS")
                        if not (os.path.isdir(output_folder)):
                            os.mkdir(output_folder)
                        else:
                            shutil.rmtree(output_folder)
                            os.mkdir(output_folder)
                        print("\n\n\n-----" + name[:len(name) - 4] + "-----\n")

                        # READING IN THE DATA CSV FILE and letting the cleaner class work
                        cleaner = Cleaner(name)
                        nom_X_dims, nom_Y_dims = cleaner.get_nominal_pad_sizes()
                        X_fail_locations = cleaner.get_X_fails()
                        Y_fail_locations = cleaner.get_Y_fails()
                        name = name[:len(name) - 4]
                        nom_X_pos, nom_Y_pos, meas_X_pos, meas_Y_pos = cleaner.extract_XY()
                        meas_X_dims, meas_Y_dims = cleaner.extract_widths()
                        meas_X_dims, meas_Y_dims, meas_X_pos, meas_Y_pos, nom_X_pos, nom_Y_pos, \
                        misread_X_dims, misread_Y_dims, misread_X_pos, misread_Y_pos, misread_nom_X_pos, \
                        misread_nom_Y_pos = cleaner.remove_outliers(meas_X_dims, meas_Y_dims, meas_X_pos, meas_Y_pos,
                                                                    nom_X_pos, nom_Y_pos)

                        # walk into the folder where all output plot pngs and output csvs will be deposited
                        os.chdir(output_folder)

                        # analyzes global wafer pad positions
                        pa = positional_analyzer(300000, nom_X_pos, nom_Y_pos, meas_X_pos, meas_Y_pos)
                        U, V, U_mean_adj, V_mean_adj = pa.find_vectors()
                        err_vector_fig = pa.plot_field(U, V, U_mean_adj, V_mean_adj, X_fail_locations, Y_fail_locations,
                                                       misread_nom_X_pos, misread_nom_Y_pos)
                        p_xvx_reg, p_yvy_reg, p_xvy_reg, p_yvx_reg, XY_positional_error_fig = pa.plot_errors(U_mean_adj,
                                                        V_mean_adj, "positional error")
                        # saves the error vector field as a png
                        err_vector_fig.savefig(name + "_ERR_VECTORS.png", dpi=199)
                        plt.close()
                        # saves the positional error vs positional reference plot as a png
                        XY_positional_error_fig.savefig(name + "_ERR_POSITIONS.png", dpi=199)
                        plt.close()

                        # analyzes super wafer pad overlay
                        swp = super_wafer_pad(nom_X_dims, nom_Y_dims, meas_X_dims, meas_Y_dims)
                        avg_x, avg_y = swp.find_average_dimensions()
                        std_x, std_y = swp.find_std_and_quartile()
                        fig, ax1, ax2, ax3 = swp.initiate_plots()
                        swp.plot_nominal_rect(ax3)
                        swp.plot_measured_rects(ax3)
                        swp.plot_average_rect(ax3)
                        ax1.hist(meas_X_dims)
                        ax2.hist(meas_Y_dims)
                        swp.plot_nom_averages_stds(avg_x, avg_y, std_x, std_y, ax1, ax2)
                        ax1.legend(loc='lower right')
                        ax2.legend(loc='lower right')
                        ax3.legend(loc='upper left')
                        # saves the super bond-pad style overlay plot as a png
                        fig.savefig(name + "_PAD_OVERLAY.png", dpi=199)
                        plt.close()

                        # cross-analyzes pad dimension error vs reference position
                        X_dims_errors = [nom_X_dims - j for j in meas_X_dims]
                        Y_dims_errors = [nom_Y_dims - j for j in meas_Y_dims]
                        d_xvx_reg, d_yvy_reg, d_xvy_reg, d_yvx_reg, XY_dimensional_error_figs\
                            = pa.plot_errors(X_dims_errors, Y_dims_errors, "pad width error")
                        # saves the dimensional error vs positional reference plot as a png
                        XY_dimensional_error_figs.savefig(name + "_ERR_DIMENSIONS.png", dpi=199)
                        plt.close()

                        # writes data to PROCESSED.csv
                        with open(name + '_PROCESSED.csv', 'w', newline="") as myfile:
                            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                            writer = Writer()
                            writer.write_single_value(wr, "Nominal Pad X dimension (microns)", nom_X_dims)
                            writer.write_single_value(wr, "Average Measured Pad X dimension", avg_x)
                            writer.write_single_value(wr, "X bias", avg_x - nom_X_dims)
                            writer.write_single_value(wr, "Nominal Pad Y dimension (microns)", nom_Y_dims)
                            writer.write_single_value(wr, "Average Measured Pad Y dimension", avg_y)
                            writer.write_single_value(wr, "Y bias", avg_y - nom_Y_dims)
                            wr.writerow([])
                            writer.write_single_value(wr, "Positional X error vs X reference regression slope",
                                                      p_xvx_reg)
                            writer.write_single_value(wr, "Positional Y error vs Y reference regression slope",
                                                      p_yvy_reg)
                            writer.write_single_value(wr, "Positional X error vs Y reference regression slope",
                                                      p_xvy_reg)
                            writer.write_single_value(wr, "Positional Y error vs X reference regression slope",
                                                      p_yvx_reg)
                            wr.writerow([])
                            writer.write_single_value(wr, "Dimensional X error vs X reference regression slope",
                                                      d_xvx_reg)
                            writer.write_single_value(wr, "Dimensional Y error vs Y reference regression slope",
                                                      d_yvy_reg)
                            writer.write_single_value(wr, "Dimensional X error vs Y reference regression slope",
                                                      d_xvy_reg)
                            writer.write_single_value(wr, "Dimensional Y error vs X reference regression slope",
                                                      d_yvx_reg)
                            wr.writerow([])
                            wr.writerow(["Measured pad X Dimensions", "Measured pad Y Dimensions"])
                            writer.write_2_values(wr, meas_X_dims, meas_Y_dims)
                            wr.writerow([])
                            wr.writerow(["Nominal X positions", "Nominal Y positions", "Measured X positions",
                                         "Measured Y positions"])
                            writer.write_4_values(wr, nom_X_pos, nom_Y_pos, meas_X_pos, meas_Y_pos)

                        # writes failures and misreads into the FAILURES.csv
                        with open(name + '_FAILURES.csv', 'w', newline='') as myfile:
                            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                            writer = Writer()
                            wr.writerow(["Failed X locations", "Failed Y locations"])
                            writer.write_2_values(wr, X_fail_locations, Y_fail_locations)
                            wr.writerow([])
                            wr.writerow(["Nominal X locations", "Nominal Y locations", "Misread X locations",
                                         "Misread Y locations"])
                            writer.write_4_values(wr, misread_nom_X_pos, misread_nom_Y_pos, misread_X_pos,
                                                  misread_Y_pos)
                            wr.writerow([])
                            wr.writerow(["Misread Pad X dimension", "Misread Pad Y dimension"])
                            writer.write_2_values(wr, misread_X_dims, misread_Y_dims)
                        print('\n' + name + ' processed and plotted!')

                        # moves the file with the raw Nikon output you have been reading from into the output folder
                        shutil.move(curr_wafer_folder_dir + '/' + name + '.csv', output_folder)

                        # return to the wafer folder you were in to keep looking for input files
                        os.chdir(curr_wafer_folder_dir)

    input("\nPress \'Enter\' to exit Program")
