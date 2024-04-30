import validation
from colorama import Fore, Back, Style, init
import gspread

# common functions
# TODO Make this into a class

# may not be needed
def format_month_name(month):
    """
    Format
    """
    
# end def

def add_zero(number):
    """
    Adds a leading zero to the number to make it two digits 
    """
    zero = '0' if number < 9 else '' 
    return (f"{usermonth}-{x+1}")
# end def

# THESE FUNCTIONS WILL BE CREATED...

def create_report_name(month):
    """
    Purpose: arg
    """
    pass
# end def

def update_status_worksheet(ws, price, report, date):
    """
    Purpose: one
    """
    
# end def


def choose_month():
    """ 
    
    """

    # Prompt user to choose month (ex 1 = january, 2 = february etc)
    user_month = input("Enter month (1-12) \n")
    
    # Validate the chosen month
    while (not validation.validate_month(user_month)):
        print(Fore.LIGHTRED_EX + f"Invalid input: {user_month}")
        user_month = input("Enter valid month (1-12) \n")
    return user_month

# end def

def report_exists(SHEET, name):
    """ 

    """

    status = SHEET.worksheet('Status_2023')
    if status.find(name) == None:
        return False
    else:
        return True

