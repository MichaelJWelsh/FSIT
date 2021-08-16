##############################################################################################################
# File Name: fs_format.py
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
#       Completed FS formats:
#           -   TSLA (Tesla)
#
##############################################################################################################


# External imports
from re import escape, sub



# Global vars
number_regex = ".*?\s*(\(\d+(?:\.\d*)?\)|\-?\d+(?:\.\d*)?)\s.*"
units_regex = "\s*([tT]housand|[mM]ill|[bB]ill)\w*\s*"



# Escape the passed arg if string
def escape_if_string(var):

    return escape(var) if isinstance(var, str) else var

# end escape_if_string



# Creates a regex from the string by first turning it into a literal string, then inserting a units regex into the right place, if it is a string passed
def escape_then_insert_units_regex_if_str(var):

    return sub(units_regex, escape(units_regex), escape(var)) if isinstance(var, str) else var

# end escape_then_insert_units_regex_if_str



# Creates a regex from the preceding string by first turning it into a literal string, then appending number_regex, if it is a string passed
def escape_then_append_num_regex_if_string(var):

    return r"^" + escape(var) + number_regex + r"$" if isinstance(var, str) else var

# end escape_then_append_num_regex



# Used for when a category in a company's F.S. is omitted or combined
class NotAvailable:

    def __init__(description=""):

        self.description = "N/A"
        if description != "":
            self.description += " (%s)" % description
        # end if

    # end __init__

# end class NotAvailable



# Used for when the number listed under a category needs to be multiplied by '-1'
class OppositeOf:

    def __init__(regex_str=""):

        self.regex = escape_then_append_num_regex(regex_str)

    # end __init__

# end class OppositeOf



# Used for when a multiple categories in a company's F.S. represent one standard category should be added
class Add:

    def __init__(*regexes):

        self.regex_list = [escape_then_append_num_regex_if_string(elem) for elem in list(regexes)]

    # end __init__

# end class Add


# Used for when the string shouldn't be converted to a string literal, rather be treated as a regex
class AsRegex():

    def __init__(raw_regex_str):

        self.raw_regex_str = raw_regex_str

    # end __init__

# end class AsRegex



# Represents a company's financial statement format (maps their format to standard format with regexes)
class FS_Format:

    """
    Many companies use different wording/phrases to indicate the same thing.  This class maps companies
    wording/phrases regex to a standard meaning, thus creating a standard financial statement format for
    processing.
    """

    @classmethod
    def __init__(
        self,
        incstmt_title,
        incstmt_units,
        incstmt_revenue,
        incstmt_cost_of_revenue,
        incstmt_sales_and_marketing_expenses,
        incstmt_research_and_development_expenses,
        incstmt_general_and_administration_expenses,
        incstmt_other_operating_expenses,
        incstmt_net_interest_income,
        incstmt_extraordinary_income,
        incstmt_income_taxes,
        incstmt_net_income,
        balsht_title,
        balsht_units,
        balsht_cash_and_equivalents,
        balsht_accounts_receivable,
        balsht_inventory,
        balsht_prepaid_assets,
        balsht_other_current_assets,
        balsht_non_current_receivables,
        balsht_non_current_investments,
        balsht_property_plant_equipment,
        balsht_patents_trademarks_other_intangibles,
        balsht_goodwill,
        balsht_other_non_current_assets,
        balsht_accounts_payable,
        balsht_notes_payable,
        balsht_accrued_expenses,
        balsht_taxes_payable,
        balsht_other_current_liabilities,
        balsht_long_term_debt,
        balsht_deferred_tax,
        balsht_provisions,
        balsht_other_non_current_liabilities,
        balsht_share_capital,
        balsht_additional_paid_in_capital,
        balsht_retained_earnings,
        balsht_treasury_stocks,
        balsht_other_equity,
        cshflw_title,
        cshflw_units,
        cshflw_net_income,
        cshflw_depreciation,
        cshflw_other_non_cash_items,
        cshflw_deferred_taxes,
        cshflw_working_capital,
        cshflw_other_operating_activities,
        cshflw_property_plant_equipment_net,
        cshflw_intangible_assets_net,
        cshflw_businesses_net,
        cshflw_investments_net,
        cshflw_other_investing_activities,
        cshflw_issuances_of_common_stock,
        cshflw_purchase_of_stock_for_treasury,
        cshflw_payment_of_cash_dividends,
        cshflw_payment_of_debt_net,
        cshflw_other_financing_activities,
        cshflw_cash_and_equivalents_start,
    ):

        """
        Constructor for a company's financial statement format.

        Sometimes certain categories in a financial statement are omitted or combined.  For example, TSLA
        combines sales-and-marketing and general-and-administration expenses into one category.  To indicate
        this, set the argument to 'NotAvailable(<optional string description>)'.

        Sometimes certain categories contain a number that needs to be multiplied by '-1' to fit the standard
        format category.  To do this, set the argument to 'OppositeOf(<str>)'.

        Sometimes certain categories are split into multiple categories and need to be added together.  For
        example, TSLA splits net-interest-income into one category for interest income and one category for
        interest expenses.  To indicate that multiple categories need to be added, set the argument to
        'Add(<first str>, <second str>, ...)'.  The 'OppositeOf' class can be embedded in the 'Add' class
        constructor (i.e. 'Add(OppositeOf(<first str>), <second str>, ...)'). To bypass constructor from
        automatically converting passed argument to a string literal, use the AsRegex class, similarly to
        the 'OppositeOf' class.
        """

        # Set fields
        self.incstmt_title = escape_if_string(incstmt_title)
        self.incstmt_units = escape_then_insert_units_regex_if_str(incstmt_units)
        self.incstmt_revenue = escape_then_append_num_regex_if_string(incstmt_revenue)
        self.incstmt_cost_of_revenue = escape_then_append_num_regex_if_string(incstmt_cost_of_revenue)
        self.incstmt_sales_and_marketing_expenses = escape_then_append_num_regex_if_string(incstmt_sales_and_marketing_expenses)
        self.incstmt_research_and_development_expenses = escape_then_append_num_regex_if_string(incstmt_research_and_development_expenses)
        self.incstmt_general_and_administration_expenses = escape_then_append_num_regex_if_string(incstmt_general_and_administration_expenses)
        self.incstmt_other_operating_expenses = escape_then_append_num_regex_if_string(incstmt_other_operating_expenses)
        self.incstmt_net_interest_income = escape_then_append_num_regex_if_string(incstmt_net_interest_income)
        self.incstmt_extraordinary_income = escape_then_append_num_regex_if_string(incstmt_extraordinary_income)
        self.incstmt_income_taxes = escape_then_append_num_regex_if_string(incstmt_income_taxes)
        self.incstmt_net_income = escape_then_append_num_regex_if_string(incstmt_net_income)
        self.balsht_title = escape_if_string(balsht_title)
        self.balsht_units = escape_then_insert_units_regex_if_str(balsht_units)
        self.balsht_cash_and_equivalents = escape_then_append_num_regex_if_string(balsht_cash_and_equivalents)
        self.balsht_accounts_receivable = escape_then_append_num_regex_if_string(balsht_accounts_receivable)
        self.balsht_inventory = escape_then_append_num_regex_if_string(balsht_inventory)
        self.balsht_prepaid_assets = escape_then_append_num_regex_if_string(balsht_prepaid_assets)
        self.balsht_other_current_assets = escape_then_append_num_regex_if_string(balsht_other_current_assets)
        self.balsht_non_current_receivables = escape_then_append_num_regex_if_string(balsht_non_current_receivables)
        self.balsht_non_current_investments = escape_then_append_num_regex_if_string(balsht_non_current_investments)
        self.balsht_property_plant_equipment = escape_then_append_num_regex_if_string(balsht_property_plant_equipment)
        self.balsht_patents_trademarks_other_intangibles = escape_then_append_num_regex_if_string(balsht_patents_trademarks_other_intangibles)
        self.balsht_goodwill = escape_then_append_num_regex_if_string(balsht_goodwill)
        self.balsht_other_non_current_assets = escape_then_append_num_regex_if_string(balsht_other_non_current_assets)
        self.balsht_accounts_payable = escape_then_append_num_regex_if_string(balsht_accounts_payable)
        self.balsht_notes_payable = escape_then_append_num_regex_if_string(balsht_notes_payable)
        self.balsht_accrued_expenses = escape_then_append_num_regex_if_string(balsht_accrued_expenses)
        self.balsht_taxes_payable = escape_then_append_num_regex_if_string(balsht_taxes_payable)
        self.balsht_other_current_liabilities = escape_then_append_num_regex_if_string(balsht_other_current_liabilities)
        self.balsht_long_term_debt = escape_then_append_num_regex_if_string(balsht_long_term_debt)
        self.balsht_deferred_tax = escape_then_append_num_regex_if_string(balsht_deferred_tax)
        self.balsht_provisions = escape_then_append_num_regex_if_string(balsht_provisions)
        self.balsht_other_non_current_liabilities = escape_then_append_num_regex_if_string(balsht_other_non_current_liabilities)
        self.balsht_share_capital = escape_then_append_num_regex_if_string(balsht_share_capital)
        self.balsht_additional_paid_in_capital = escape_then_append_num_regex_if_string(balsht_additional_paid_in_capital)
        self.balsht_retained_earnings = escape_then_append_num_regex_if_string(balsht_retained_earnings)
        self.balsht_treasury_stocks = escape_then_append_num_regex_if_string(balsht_treasury_stocks)
        self.balsht_other_equity = escape_then_append_num_regex_if_string(balsht_other_equity)
        self.cshflw_title = escape_if_string(cshflw_title)
        self.cshflw_units = escape_then_insert_units_regex_if_str(cshflw_units)
        self.cshflw_net_income = escape_then_append_num_regex_if_string(cshflw_net_income)
        self.cshflw_depreciation = escape_then_append_num_regex_if_string(cshflw_depreciation)
        self.cshflw_other_non_cash_items = escape_then_append_num_regex_if_string(cshflw_other_non_cash_items)
        self.cshflw_deferred_taxes = escape_then_append_num_regex_if_string(cshflw_deferred_taxes)
        self.cshflw_working_capital = escape_then_append_num_regex_if_string(cshflw_working_capital)
        self.cshflw_other_operating_activities = escape_then_append_num_regex_if_string(cshflw_other_operating_activities)
        self.cshflw_property_plant_equipment_net = escape_then_append_num_regex_if_string(cshflw_property_plant_equipment_net)
        self.cshflw_intangible_assets_net = escape_then_append_num_regex_if_string(cshflw_intangible_assets_net)
        self.cshflw_businesses_net = escape_then_append_num_regex_if_string(cshflw_businesses_net)
        self.cshflw_investments_net = escape_then_append_num_regex_if_string(cshflw_investments_net)
        self.cshflw_other_investing_activities = escape_then_append_num_regex_if_string(cshflw_other_investing_activities)
        self.cshflw_issuances_of_common_stock = escape_then_append_num_regex_if_string(cshflw_issuances_of_common_stock)
        self.cshflw_purchase_of_stock_for_treasury = escape_then_append_num_regex_if_string(cshflw_purchase_of_stock_for_treasury)
        self.cshflw_payment_of_cash_dividends = escape_then_append_num_regex_if_string(cshflw_payment_of_cash_dividends)
        self.cshflw_payment_of_debt_net = escape_then_append_num_regex_if_string(cshflw_payment_of_debt_net)
        self.cshflw_other_financing_activities = escape_then_append_num_regex_if_string(cshflw_other_financing_activities)
        self.cshflw_cash_and_equivalents_start = escape_then_append_num_regex_if_string(cshflw_cash_and_equivalents_start)

    # end __init__

# end class FS_Format



##############################################################################################################
#
#
#                                           Company FS Formats
#
#
##############################################################################################################

# incstmt_net_income, balsht_total_assets, balsht_total_liabilities,
# balsht_total_equity, balsht_total_liabilities_and_equity, cshflw_total_operating_activities,
# cshflw_total_investing_activities, cshflw_total_financing_activities, cshflw_cash_and_equivalents_end


TSLA = FS_Format(
    incstmt_title="Consolidated Statements of Operations",
    incstmt_units="(in millions, except per share data)",
    incstmt_revenue="Total revenues",
    incstmt_cost_of_revenue="Total cost of revenues",
    incstmt_sales_and_marketing_expenses=NotAvailable("Combined into General and Administration Expenses"),
    incstmt_research_and_development_expenses="Research and development",
    incstmt_general_and_administration_expenses="Selling, general and administrative",
    incstmt_other_operating_expenses="Restructuring and other",
    incstmt_net_interest_income=Add("Interest income", "Interest expense"),
    incstmt_extraordinary_income="Other (expense) income, net",
    incstmt_income_taxes="Provision for income taxes",
    incstmt_net_income="Net income (loss)",
    balsht_title="Consolidated Balance Sheets",
    balsht_units="(in millions, except per share data)",
    balsht_cash_and_equivalents="Cash and cash equivalents",
    balsht_accounts_receivable="Accounts receivable, net",
    balsht_inventory="Inventory",
    balsht_prepaid_assets=NotAvailable("Combined into Other Current Assets"),
    balsht_other_current_assets="Prepaid expenses and other current assets",
    balsht_non_current_receivables=NotAvailable(),
    balsht_non_current_investments=NotAvailable(),
    balsht_property_plant_equipment="Property, plant and equipment, net",
    balsht_patents_trademarks_other_intangibles="Intangible assets, net",
    balsht_goodwill="Goodwill",
    balsht_other_non_current_assets=Add("Operating lease vehicles, net", "Solar energy systems, net", "Operating lease right-of-use assets", "Other non-current assets"),
    balsht_accounts_payable="Accounts payable",
    balsht_notes_payable=NotAvailable(),
    balsht_accrued_expenses="Accrued liabilities and other",
    balsht_taxes_payable=NotAvailable(),
    balsht_other_current_liabilities=Add("Deferred revenue", "Customer deposits", "Current portion of debt and finance leases"),
    balsht_long_term_debt="Debt and finance leases, net of current portion",
    balsht_deferred_tax=NotAvailable(),
    balsht_provisions=NotAvailable(),
    balsht_other_non_current_liabilities=Add("Deferred revenue, net of current portion", "Other long-term liabilities", "Commitments and contingencies", "Redeemable noncontrolling interests in subsidiaries", "Convertible senior notes"),
    balsht_share_capital=NotAvailable(),
    balsht_additional_paid_in_capital=AsRegex("Additional paid-in capital (?:\([12]\))?"),
    balsht_retained_earnings=OppositeOf("Accumulated deficit"),
    balsht_treasury_stocks=NotAvailable(),
    balsht_other_equity=Add("Accumulated other comprehensive income (loss)", "Noncontrolling interests in subsidiaries"),
    cshflw_title="Consolidated Statements of Cash Flows",
    cshflw_units="(in millions)",
    cshflw_net_income="Net income (loss)",
    cshflw_depreciation="Depreciation, amortization and impairment",
    cshflw_other_non_cash_items="",
    cshflw_deferred_taxes="",
    cshflw_working_capital="",
    cshflw_other_operating_activities="",
    cshflw_property_plant_equipment_net="",
    cshflw_intangible_assets_net="",
    cshflw_businesses_net="",
    cshflw_investments_net="",
    cshflw_other_investing_activities="",
    cshflw_issuances_of_common_stock="",
    cshflw_purchase_of_stock_for_treasury="",
    cshflw_payment_of_cash_dividends="",
    cshflw_payment_of_debt_net="",
    cshflw_other_financing_activities="",
    cshflw_cash_and_equivalents_start=""
) # end FS_Format TSLA
