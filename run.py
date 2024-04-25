import gspread
from google.oauth2.service_account import Credentials
import validation

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

consumption = SHEET.worksheet('Status_2023')
data = consumption.get_all_values()
#print(data)

# \n is needed for getting it to work in Heroku
# data_str = input("Please enter:\n")

def main():
    pass

def register_price():
    """
    Shows dialog and recieve users input (month and price)
    """
    print("register price")
# end def

def create_report():
    """
    Shows dialog an recieves users input (month)
    """
    print("create report")
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
# end def

def show_help():
    """
    Shows instructions for how to use the system
    """
    print("show help")
# end def

def exit():
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

    match (choice):
        case ("1"):
            register_price() 
        case ("2"):
            create_report()
        case ("3"):
            erase_month()
        case ("4"):
            show_status()
        case ("5"):
            help()
    # end match

main_menu()