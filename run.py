import os
import gspread
from google.oauth2.service_account import Credentials
import validation
import common
from prettytable import PrettyTable

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Global constants
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Charger_consumption_2023')


#print(data)

# \n is needed for getting it to work in Heroku
# data_str = input("Please enter:\n")

def main():
    pass

def register_price():
    """
    Shows dialog and recieve users input (month and price)
    """
    year_overview = SHEET.worksheet('Status_2023')
    
    os.system('clear')
    print("register price")
    print('--------------')

    # Prompt user to choose month (ex january or jan)
    user_month = input("Enter month \n")

    # Validate month


    # Check if reports exists for chosen month
    # helper function (will be used from other menu options as well)

    # Check if price exists for chosen month

    # Prompt the user to enter price
    user_price = input("Enter price \n")

    # Check if the entered price is a positive float

    # Check if the entered price is reasonable

    # Update the price in the sheet
    cell = year_overview.find(user_month)
    print(f"Found {user_month} in row:{cell.row} col:{cell.col}")
    year_overview.update_cell(cell.row,2,user_price)

    print(f"Price updated successfully: {user_price}")
    input("Press enter to continue")


# end def

def create_report():
    """
    Shows dialog an recieves users input (month)
    Validates input data and creates a report
    Report is created as a new workbook in the worksheet 
    and shown to the user as a prettytable-formatted table
    """
    os.system('clear')
    print("Create Report")
    print('-------------')

    # Prompt user to choose month (ex january or jan)
    user_month = input("Enter month \n")

    # Validate the chosen month
    while (not validation.validate_month(user_month)):
        user_month = input("Enter month \n")

    # Check if report exists for chosen month

    # Check that price exists (UPDATE FLOWCHART)

    # Calculate cost for each charger
    print('Calculate cost...')

    # Create new workbook

    # Update status workbook ()

    input("Press enter to continue")
# end def

def erase_month():
    """
    Shows dialog where user choose which months data to erase 
    """
    print("erase month")
# end def

def show_status():
    """
    Returns the status for all months
    (month, price, report, date)
    """
    print("show status")

    # Get the data from the workbook 'Status_2023'
    consumption = SHEET.worksheet('Status_2023')
    data = consumption.get_all_values()
    # print(data)
    # Sort the data, starting with january, but how? (Add a new column with number 
    # or is it posible to use a function to convert month name to month number) 

    # Create table
    status_table = PrettyTable(data[0]) 

    for idx in range(1, len(data)):
        # Iterates the rows in the data from the workbook and adds them to the table
        status_table.add_row(data[idx])
    print (status_table)
    input("Press enter to continue")
# end def

def show_help():
    """
    Shows instructions for how to use the system
    """
    print("show help")
# end def

#def exit():
    """
    Exits the application 
    """
    pass
# end def

def main_menu():
    print("\nMenu ")
    print("----")
    print("1 - REGISTER PRICE")
    print("2 - CREATE REPORT")
    print("3 - ERASE MONTH")
    print("4 - SHOW STATUS")
    print("5 - HELP")
    print("6 - EXIT")

    choice = input( "Select option (1-6) \n")
    while (not validation.validate_choice(choice)):
        choice = input( "Select option (1-6) \n")

    if (choice == "1"):
        # comment: 
        register_price()
    elif (choice == "2"):
        # comment: 
        create_report()
    elif (choice == "3"):
        # comment: 
        erase_month()
    elif (choice == "4"):
        # comment: 
        show_status()
    elif (choice == "5"):
        # comment: 
        show_help()
    # end if

main_menu()
exit()