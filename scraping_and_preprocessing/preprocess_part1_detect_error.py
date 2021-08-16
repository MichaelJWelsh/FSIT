# Imports
import csv
import re
import os
import time
import pathlib
import pyautogui as pag
import shutil
from os import listdir
from os.path import isfile, join

# Start timer
time.sleep(2)
start_time = time.time()

# Create exchange name to 2D list of [ticker symbols, industry] dictionary
ticker_path = 'Ticker_Symbols'
ticker_files = [f for f in listdir(ticker_path) if isfile(join(ticker_path, f))]
exchange_names = [re.search('^(.*)\.csv$', f).group(1) for f in ticker_files]

# Detect errors
yahoo_fin_path = 'Yahoo_Finance_Financials'
os.system('cls')
for ex_name in exchange_names:
    with open(join(ticker_path, ex_name + '.csv')) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            tick_symbol = row['Symbol']
            print(tick_symbol)
            industry = row['Industry']
            industry = re.sub('/', ' & ', industry)
            industry = re.sub(':\r*', '-', industry)
            industry = re.sub('\.', '_', industry)
            industry = re.sub('_$', '', industry)
            industry = re.sub('and', '&', industry)
            industry = re.sub('&([A-Za-z])', r'& \1', industry)
            if industry == '':
                industry = 'Other'
            yahoo_fin_ex_name_industry_tick_symb_path = join(yahoo_fin_path, ex_name, industry, tick_symbol)
            if not os.path.isdir(yahoo_fin_ex_name_industry_tick_symb_path):
                continue
            try:
                yahoo_fin_financial_file_list = \
                    [f for f in listdir(yahoo_fin_ex_name_industry_tick_symb_path) \
                     if isfile(join(yahoo_fin_ex_name_industry_tick_symb_path, f))]
            except:
                continue
            if len(yahoo_fin_financial_file_list) == 0:
                shutil.rmtree(yahoo_fin_ex_name_industry_tick_symb_path)
                continue
            six_tick_files = len(yahoo_fin_financial_file_list) == 6
            contains_data = True
            does_not_contain_data_list = []
            for yahoo_fin_financial_file in yahoo_fin_financial_file_list:
                yahoo_fin_financial_file_path = join(yahoo_fin_ex_name_industry_tick_symb_path, yahoo_fin_financial_file)
                if not os.path.isfile(yahoo_fin_financial_file_path):
                    print("%s - %s - %s:\n\tNot a file: %s" % (ex_name, industry, tick_symbol, yahoo_fin_financial_file))
                    continue
                try:
                    with open(yahoo_fin_financial_file_path) as csv_financial_file:
                        csv_financial_file_reader = csv.DictReader(csv_financial_file, delimiter=',')
                        num_lines = 0
                        for financial_file_entry in csv_financial_file_reader:
                            num_lines += 1
                            if num_lines > 3:
                                break
                        if num_lines < 3:
                            contains_data = False
                            does_not_contain_data_list.append(yahoo_fin_financial_file_path)
                            break
                except:
                    print("%s - %s - %s:\n\tUnable to read a file: %s" % (ex_name, industry, tick_symbol, yahoo_fin_financial_file))
            if not six_tick_files or not contains_data:
                error_msg = "%s - %s - %s:" % (ex_name, industry, tick_symbol)
                just_delete = False
                if not six_tick_files:
                    error_msg += "\n\tExpected 6 financial files, found: %d" % len(yahoo_fin_financial_file_list)
                if not contains_data:
                    error_msg += "\n\tFiles contain missing data:"
                    for f in does_not_contain_data_list:
                        error_msg += "\n\t\t%s" % f
                        if ("_annual_balance-sheet" in f or "_annual_cash-flow" in f) and industry == "Other":
                            just_delete = True
                            break
                if just_delete or "Acquisition" in row['Name'] or "Holding" in row['Name'] or "Merger" in row['Name']:
                    shutil.rmtree(yahoo_fin_ex_name_industry_tick_symb_path)
                    continue
                print(error_msg)
                if input("\nREMOVE DIRECTORY AND FILES? (y/n): ") == "y":
                    shutil.rmtree(yahoo_fin_ex_name_industry_tick_symb_path)
                os.system('cls')


# End timer
print("Time elapsed: %ds" % (time.time() - start_time))
