##############################################################################################################
# File Name: main.py
# Revision: 0.0.0
# Date: 2021-May-05
#
# Author(s)
#
# Name:             Michael Welsh
# Email:            mjw6093@psu.edu
#
# Revision      Date            Initials        Brief
#
# 0.0.0         2021-May-05     mjw             Initial version
#
# Notes:
#       N/A
#
##############################################################################################################



##############################################################################################################
# Ideas/TODOs:
#
#   Single FS Analysis (Each FS might be an object of the FS class)  ("FS")
#       - One function takes a financial statement, and creates a new standard format easily readable
#           financial statement derivative
#       - One function takes this standard format FS, parses and stores variables containing information
#       - One function takes these variables and calculates ratios
#       - One function takes all this information and thresholds, and "scores" the company, pointing out
#           really good and really bad things
#       - One function takes this score analysis, and just prints everything out in a nice format
#       - One function takes this score analysis, and saves it
#       - One function takes this score analysis (saved in file), and loads it as an object of this class
#
#   Collective FS Analysis (SAME COMPANY) (collection of FS class objects represented as a single class) ("Company")
#       - A company consists of many financial statements over the years
#       - One function takes all these, and calculates more ratios and growth percentages
#       - One function takes all this information and more thresholds, and "scores" the company, pointing out
#           really good and really bad things. Also calculates DCF/Bond valuations based on spot price
#       - One function takes this analysis, and just prints everything out in a nice format
#       - One function takes this analysis, and saves it
#       - One function takes this analysis (saved in file), and loads it as an object of this class
#
#   Collective FS Analysis (SAME INDUSTRY) (collection of collective-same-company-FS objects) ("Industry")
#       - An industry consists of multiple companies
#       - One function takes all these, and calculates more ratios and such (necessary????)
#       - One function takes all these, and analyzes and ranks and lists pros/cons/ranking
#       - One function takes this analysis, and just prints everything out in a nice format
#       - One function takes this analysis, and saves it
#       - One function takes this analysis (saved in file), and loads it as an object of this class
#
#   Collective FS Analysis (SAME EXCHANGE) (collection of multiple industries) ("Exchange")
#       - An exchange consists of multiple industries of multiple companies with tradeable stock
#       - One function takes all these, and calculates more ratios and such (necessary????)
#       - One function takes all these, and analyzes and ranks and lists pros/cons/ranking
#       - One function takes this analysis, and just prints everything out in a nice format
#       - One function takes this analysis, and saves it
#       - One function takes this analysis (saved in file), and loads it as an object of this class
#
##############################################################################################################



# Internal imports
from fs import FS



def main():

    """
    TODO
    """

    # TODO
    x = FS()




# end main













if __name__ == "__main__":
    main()
# end if
