# Imports
import csv
import re
import os
import time
import pathlib
import shutil
from os import listdir
from os.path import isfile, join, dirname

# Start timer
time.sleep(2)
start_time = time.time()

# Paths
yfin_path = 'Yahoo_Finance_Financials'
std_fmt_path = join(dirname(os.getcwd()), 'feature_extraction', 'std_fmt_financials')

# If debugging, only do single financial statement
debug = False

# Convert
os.system('cls')
regex_num = re.compile(r'-?\d+(?:\.\d*)?')
exchanges = [ex for ex in listdir(yfin_path)]
for ex in exchanges:
    yfin_ex_path = join(yfin_path, ex)
    industries = [ind for ind in listdir(yfin_ex_path)]
    for ind in industries:
        yfin_ex_ind_path = join(yfin_ex_path, ind)
        std_fmt_ind_path = join(std_fmt_path, ind)
        if not os.path.isdir(std_fmt_ind_path):
            os.makedirs(std_fmt_ind_path)
        companies = [com for com in listdir(yfin_ex_ind_path)]
        for com in companies:
            yfin_ex_ind_com_path = join(yfin_ex_ind_path, com)
            if (not any(fname.endswith('_annual_financials.csv') for fname in os.listdir(yfin_ex_ind_com_path))) or \
              (not any(fname.endswith('_annual_balance-sheet.csv') for fname in os.listdir(yfin_ex_ind_com_path))) or \
              (not any(fname.endswith('_annual_cash-flow.csv') for fname in os.listdir(yfin_ex_ind_com_path))):
                print("-----Files not found for %s, SKIPPING!-----" % yfin_ex_ind_com_path)
                continue
            std_fmt_ind_com_path = join(std_fmt_ind_path, com)
            if not os.path.isdir(std_fmt_ind_com_path):
                os.makedirs(std_fmt_ind_com_path)
            com_financials = [f for f in listdir(yfin_ex_ind_com_path) if isfile(join(yfin_ex_ind_com_path, f))]
            com_fs_path = join(std_fmt_ind_com_path, 'annual_fs.csv')
            print("Processing %s:%s:%s" % (ex, ind, com))
            with open(com_fs_path, 'w', newline='') as fs_csv_file:
                com_fs_writer = csv.writer(fs_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                len_first_row = 0
                # Annual income statement
                yfin_annual_income_path = join(yfin_ex_ind_com_path, com + '_annual_financials.csv')
                with open(yfin_annual_income_path, 'r') as com_yfin_csv_file:
                    name_map_dict = {}
                    name_map_dict['TotalRevenue'] = 'Revenue'
                    name_map_dict['CostOfRevenue'] = 'Cost of Revenue'
                    name_map_dict['GrossProfit'] = 'Gross Margin'
                    name_map_dict['SellingGeneralAndAdministration'] = 'Selling/General/Administration Expenses'
                    name_map_dict['SellingAndMarketingExpense'] = 'SGA - Selling/Marketing Expenses'
                    name_map_dict['GeneralAndAdministrativeExpense'] = 'SGA - G&A Expenses'
                    name_map_dict['ResearchAndDevelopment'] = 'Research and Development Expenses'
                    name_map_dict['OtherOperatingExpenses'] = 'Other Operating Expenses'
                    name_map_dict['OperatingExpense'] = 'Operating Expenses'
                    name_map_dict['OperatingIncome'] = 'Income from Operations'
                    name_map_dict['NetNonOperatingInterestIncomeExpense'] = 'Net Interest Income'
                    name_map_dict['OtherIncomeExpense'] = 'Extraordinary Income'
                    name_map_dict['TaxProvision'] = 'Income Taxes'
                    name_map_dict['NetIncomeContinuousOperations'] = 'Net Income'
                    name_map_dict['EBIT'] = 'EBIT'
                    name_map_dict['BasicEPS'] = 'EPS'
                    com_yfin_reader = csv.reader(com_yfin_csv_file, delimiter=',')
                    first_row = True
                    ttm_found = False
                    while len(name_map_dict) > 0:
                        is_first_row = first_row
                        wanted_name = list(name_map_dict.keys())[0]
                        found_row = False
                        for row in com_yfin_reader:
                            if row[1].strip().lower() == "ttm" or ttm_found:
                                ttm_found = True
                                del(row[1])
                            row_name = row[0].strip()
                            del(row[0])
                            if first_row:
                                com_fs_writer.writerow([''] + row)
                                com_fs_writer.writerow(['Income Statement'])
                                com_fs_writer.writerow([''])
                                first_row = False
                                len_first_row = len(row)
                                break
                            if row_name == wanted_name:
                                found_row = row
                                break
                        if is_first_row:
                            continue
                        if found_row:
                            for i in range(len(row)):
                                row[i] = row[i].replace(',', '')
                                if not regex_num.match(row[i]):
                                    row[i] = '0'
                            com_fs_writer.writerow([name_map_dict[wanted_name]] + row)
                        else:
                            com_fs_writer.writerow([name_map_dict[wanted_name]] + [0] * len_first_row)
                        del(name_map_dict[wanted_name])
                        com_yfin_csv_file.seek(0)
                # Balance sheet - Assets
                yfin_annual_balsht_path = join(yfin_ex_ind_com_path, com + '_annual_balance-sheet.csv')
                with open(yfin_annual_balsht_path, 'r') as com_yfin_csv_file:
                    name_map_dict = {}
                    name_map_dict['CashCashEquivalentsAndShortTermInvestments'] = 'Cash and Equivalents'
                    name_map_dict['AccountsReceivable'] = 'Accounts Receivable'
                    name_map_dict['Inventory'] = 'Inventory'
                    name_map_dict['PrepaidAssets'] = 'Prepaid Assets'
                    name_map_dict['RestrictedCash'] = 'Restricted Cash'
                    name_map_dict['OtherCurrentAssets'] = 'Other Current Assets'
                    name_map_dict['CurrentAssets'] = 'Total Current Assets'
                    #name_map_dict[''] = 'Non-Current Receivables'
                    #name_map_dict[''] = 'Non-Current Investments'
                    name_map_dict['NetPPE'] = 'Property/Plant/Equipment'
                    name_map_dict['OtherIntangibleAssets'] = 'Patents/Trademarks/Other Intangibles'
                    name_map_dict['Goodwill'] = 'Goodwill'
                    name_map_dict['OtherNonCurrentAssets'] = 'Other Non-Current Assets'
                    name_map_dict['TotalNonCurrentAssets'] = 'Total Non-Current Assets'
                    name_map_dict['TotalAssets'] = 'Total Assets'
                    com_yfin_reader = csv.reader(com_yfin_csv_file, delimiter=',')
                    first_row = True
                    ttm_found = False
                    while len(name_map_dict) > 0:
                        is_first_row = first_row
                        wanted_name = list(name_map_dict.keys())[0]
                        found_row = False
                        for row in com_yfin_reader:
                            if row[1].strip().lower() == "ttm" or ttm_found:
                                ttm_found = True
                                del(row[1])
                            row_name = row[0].strip()
                            del(row[0])
                            if first_row:
                                com_fs_writer.writerow([''])
                                com_fs_writer.writerow(['Balance Sheet - Assets'])
                                com_fs_writer.writerow([''])
                                first_row = False
                                break
                            if row_name == wanted_name:
                                found_row = row
                                break
                        if is_first_row:
                            continue
                        if found_row:
                            for i in range(len(row)):
                                row[i] = row[i].replace(',', '')
                                if not regex_num.match(row[i]):
                                    row[i] = '0'
                            com_fs_writer.writerow([name_map_dict[wanted_name]] + row)
                        else:
                            com_fs_writer.writerow([name_map_dict[wanted_name]] + [0] * len_first_row)
                        del(name_map_dict[wanted_name])
                        com_yfin_csv_file.seek(0)
                # Balance sheet - Liabilities
                yfin_annual_balsht_path = join(yfin_ex_ind_com_path, com + '_annual_balance-sheet.csv')
                with open(yfin_annual_balsht_path, 'r') as com_yfin_csv_file:
                    name_map_dict = {}
                    name_map_dict['AccountsPayable'] = 'Accounts Payable'
                    name_map_dict['TradeandOtherPayablesNonCurrent'] = 'Notes Payable'
                    name_map_dict['CurrentAccruedExpenses'] = 'Accrued Expenses'
                    name_map_dict['TotalTaxPayable'] = 'Taxes Payable'
                    name_map_dict['OtherCurrentLiabilities'] = 'Other Current Liabilities'
                    name_map_dict['CurrentLiabilities'] = 'Total Current Liabilities'
                    name_map_dict['LongTermDebtAndCapitalLeaseObligation'] = 'Long Term Debt'
                    name_map_dict['NonCurrentDeferredTaxesLiabilities'] = 'Deferred Tax'
                    name_map_dict['LongTermProvisions'] = 'Provisions'
                    name_map_dict['OtherNonCurrentLiabilities'] = 'Other Non-Current Liabilities'
                    name_map_dict['TotalNonCurrentLiabilitiesNetMinorityInterest'] = 'Total Non-Current Liabilities'
                    name_map_dict['TotalLiabilitiesNetMinorityInterest'] = 'Total Liabilities'
                    com_yfin_reader = csv.reader(com_yfin_csv_file, delimiter=',')
                    first_row = True
                    while len(name_map_dict) > 0:
                        is_first_row = first_row
                        wanted_name = list(name_map_dict.keys())[0]
                        found_row = False
                        for row in com_yfin_reader:
                            row_name = row[0].strip()
                            del(row[0])
                            if first_row:
                                com_fs_writer.writerow([''])
                                com_fs_writer.writerow(['Balance Sheet - Liabilities'])
                                com_fs_writer.writerow([''])
                                first_row = False
                                break
                            if row_name == wanted_name:
                                found_row = row
                                break
                        if is_first_row:
                            continue
                        if found_row:
                            for i in range(len(row)):
                                row[i] = row[i].replace(',', '')
                                if not regex_num.match(row[i]):
                                    row[i] = '0'
                            com_fs_writer.writerow([name_map_dict[wanted_name]] + row)
                        else:
                            com_fs_writer.writerow([name_map_dict[wanted_name]] + [0] * len_first_row)
                        del(name_map_dict[wanted_name])
                        com_yfin_csv_file.seek(0)
                # Balance sheet - Equity
                yfin_annual_balsht_path = join(yfin_ex_ind_com_path, com + '_annual_balance-sheet.csv')
                with open(yfin_annual_balsht_path, 'r') as com_yfin_csv_file:
                    name_map_dict = {}
                    name_map_dict['CapitalStock'] = 'Share Capital'
                    name_map_dict['AdditionalPaidInCapital'] = 'Additional Paid in Capital'
                    name_map_dict['RetainedEarnings'] = 'Retained Earnings'
                    name_map_dict['TreasuryStock'] = 'Treasury Stock'
                    #name_map_dict[''] = 'Other Equity'
                    name_map_dict['StockholdersEquity'] = 'Total Equity'
                    com_yfin_reader = csv.reader(com_yfin_csv_file, delimiter=',')
                    first_row = True
                    while len(name_map_dict) > 0:
                        is_first_row = first_row
                        wanted_name = list(name_map_dict.keys())[0]
                        found_row = False
                        for row in com_yfin_reader:
                            row_name = row[0].strip()
                            del(row[0])
                            if first_row:
                                com_fs_writer.writerow([''])
                                com_fs_writer.writerow(['Balance Sheet - Equity'])
                                com_fs_writer.writerow([''])
                                first_row = False
                                break
                            if row_name == wanted_name:
                                found_row = row
                                break
                        if is_first_row:
                            continue
                        if found_row:
                            for i in range(len(row)):
                                row[i] = row[i].replace(',', '')
                                if not regex_num.match(row[i]):
                                    row[i] = '0'
                            com_fs_writer.writerow([name_map_dict[wanted_name]] + row)
                        else:
                            com_fs_writer.writerow([name_map_dict[wanted_name]] + [0] * len_first_row)
                        del(name_map_dict[wanted_name])
                        com_yfin_csv_file.seek(0)
                # Cashflow
                yfin_annual_cshflw_path = join(yfin_ex_ind_com_path, com + '_annual_cash-flow.csv')
                with open(yfin_annual_cshflw_path, 'r') as com_yfin_csv_file:
                    name_map_dict = {}
                    name_map_dict['NetIncomeFromContinuingOperations'] = 'Net Income'
                    name_map_dict['DepreciationAndAmortization'] = 'Depreciation'
                    name_map_dict['OtherNonCashItems'] = 'Other Non-Cash Items'
                    name_map_dict['DeferredTax'] = 'Deferred Taxes'
                    name_map_dict['ChangeInWorkingCapital'] = 'Working Capital'
                    #name_map_dict[''] = 'Other Operating Activities Cashflow'
                    name_map_dict['OperatingCashFlow'] = 'Total Operating Activities Cashflow'
                    name_map_dict['NetPPEPurchaseAndSale'] = 'Property/Plant/Equipment, Net'
                    name_map_dict['NetIntangiblesPurchaseAndSale'] = 'Intangible Assets, Net'
                    name_map_dict['NetBusinessPurchaseAndSale'] = 'Businesses, Net'
                    name_map_dict['NetInvestmentPurchaseAndSale'] = 'Investments, Net'
                    name_map_dict['NetOtherInvestingChanges'] = 'Other Investing Activities Cashflow'
                    name_map_dict['InvestingCashFlow'] = 'Total Investing Activities Cashflow'
                    name_map_dict['NetOtherInvestingChanges'] = 'Issuances of Common Stock'
                    name_map_dict['RepurchaseOfCapitalStock'] = 'Purchase of Stock for Treasury'
                    name_map_dict['CashDividendsPaid'] = 'Payment of Cash Dividends'
                    name_map_dict['NetIssuancePaymentsOfDebt'] = 'Issuances/Payment of Debt, Net'
                    name_map_dict['NetOtherFinancingCharges'] = 'Other Financing Activities Cashflow'
                    name_map_dict['FinancingCashFlow'] = 'Total Financing Activities Cashflow'
                    name_map_dict['ChangesInCash'] = 'Change in Cash'
                    name_map_dict['BeginningCashPosition'] = 'Cash and Equivalents, Start'
                    name_map_dict['EndCashPosition'] = 'Cash and Equivalents, End'
                    name_map_dict['FreeCashFlow'] = 'Free Cash Flow'
                    com_yfin_reader = csv.reader(com_yfin_csv_file, delimiter=',')
                    first_row = True
                    ttm_found = False
                    while len(name_map_dict) > 0:
                        is_first_row = first_row
                        wanted_name = list(name_map_dict.keys())[0]
                        found_row = False
                        for row in com_yfin_reader:
                            if row[1].strip().lower() == "ttm" or ttm_found:
                                ttm_found = True
                                del(row[1])
                            row_name = row[0].strip()
                            del(row[0])
                            if first_row:
                                com_fs_writer.writerow([''])
                                com_fs_writer.writerow(['Cashflow'])
                                com_fs_writer.writerow([''])
                                first_row = False
                                break
                            if row_name == wanted_name:
                                found_row = row
                                break
                        if is_first_row:
                            continue
                        if found_row:
                            for i in range(len(row)):
                                row[i] = row[i].replace(',', '')
                                if not regex_num.match(row[i]):
                                    row[i] = '0'
                            com_fs_writer.writerow([name_map_dict[wanted_name]] + row)
                        else:
                            com_fs_writer.writerow([name_map_dict[wanted_name]] + [0] * len_first_row)
                        del(name_map_dict[wanted_name])
                        com_yfin_csv_file.seek(0)
            if debug:
                print("Debug enabled, processed %s, exiting..." % std_fmt_ind_com_path)
                exit()

# End timer
print("Time elapsed: %ds" % (time.time() - start_time))
