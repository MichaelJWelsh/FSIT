##############################################################################################################
# File Name: fs.py
# Revision: 0.0.0
# Date: 2021-May-09
#
# Author(s)
#
# Name:             Michael Welsh
# Email:            mjw6093@psu.edu
#
# Revision      Date            Initials        Brief
#
# 0.0.0         2021-May-09     mjw             Initial version
#
# Notes:
#       N/A
#
##############################################################################################################



##############################################################################################################
# TODO:
#   -
#
##############################################################################################################



# External imports
import tkinter as tk
from tkinter import filedialog



# Internal imports
import fs_format
from fs_format import FS_Format



class FS:

    """
    TODO Represents a single financial statement (quarterly/annual/etc).
    """

    ##########################################################################################################
    #
    #                                           Private Methods
    #
    ##########################################################################################################

    @classmethod
    def __load_from_html_file(self, file_path):

        """
        TODO raises exception
        """

        # TODO beware of negative and parenthesis values
        # TODO change
        with open(file_path, 'r') as file:
            i = 0
            for line in file:
                i += 1
                print(line)
                if i == 10:
                    break
                # end if
            # end for
        # end with

    # end __load_from_html_file

    ##########################################################################################################
    #
    #                                           Public Methods
    #
    ##########################################################################################################

    @classmethod
    def __init__(self):

        """
        TODO raises exception on failure
        """

        # Obtain file (through dialog) from which to load financial statement
        tk.Tk().withdraw()
        # TODO update this message to include accepted extensions and other info
        print("Please select a file to load in financial statement.")
        # TODO filter so only certain extensions allowed
        file_path = filedialog.askopenfilename()

        # TODO determine if file is acceptable type and load via that type
        self.__load_from_html_file(file_path)

    # end __init__

# end class FS
