import os
import gspread
from google.oauth2.service_account import Credentials
import validation
import common
import externalprice
from prettytable import PrettyTable, ALL
from prettytable.colortable import ColorTable, Themes
import datetime
from colorama import Fore, Back, Style, init

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Global constants
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
CF = common.CommonFunctions()

try:
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET = GSPREAD_CLIENT.open('Charger_consumption_2023')
except Exception as ge:
    print(Fore.LIGHTRED_EX + str(ge))
    print(Fore.LIGHTRED_EX + "A technical error has occurred, please try again later.")
    input("\nThe application will terminate, press enter...")
    exit()

def create_report():
    """
    Shows dialog an recieves users input (month)
    Validates input data and creates a report
    Report is created as a new workbook in the worksheet
    and shown to the user as a prettytable-formatted table
    """

    consumption = SHEET.worksheet('Consumption_2023')
    DEFAULT_PRICE = 0.50

    print(Fore.LIGHTMAGENTA_EX + "**** CREATE REPORT ****\n")

    # Prompt user to choose month (ex 1 = january, 2 = february etc)
    user_month = CF.choose_month()

    # Create report name
    month_short = datetime.datetime(2023, int(user_month), 1).strftime("%b")
    month_long = datetime.datetime(2023, int(user_month), 1).strftime("%B")
    report_name = f"Report_{month_short}_2023"

    # Check if report exists for chosen month
    if CF.report_exists(SHEET, report_name):
        print(Fore.LIGHTRED_EX + f"{report_name} already exists.")
        input("Press enter to continue\n")
        return

    # Fetch price from external api
    print(Fore.LIGHTGREEN_EX + f"Getting the price for {month_long}...\n")

    try:
        user_price = externalprice.get_avgprice_for_month(int(user_month))
        print(Fore.LIGHTGREEN_EX + f"Found price for {month_long}: \
            {user_price} SEK \n")
    except Exception as e:
        print(Fore.LIGHTRED_EX + "Something went wrong when communicating with\
             external api")
        print(Fore.LIGHTRED_EX + str(e))
        print(Fore.LIGHTGREEN_EX + f"Using default price: {DEFAULT_PRICE} SEK")
        user_price = DEFAULT_PRICE

    # Calculate cost for each charger
    print(Fore.LIGHTGREEN_EX + 'Calculate cost per charger...\n')
    # Code from S O
    records = (consumption.get_all_records
               (value_render_option="UNFORMATTED_VALUE"))

    # find all rows for the chosen month
    found_records = []
    for record in records:
        # m = str(record.get('Month'))
        # print(f"m={m} user_month={user_month}")
        if str(record.get('Month')) == user_month:
            found_records.append(record)

    report_list = calculate_cost(found_records, user_price)

    # Create new worksheet
    print(Fore.LIGHTGREEN_EX + f"Creating report {report_name}...\n")
    report_header = ['ChargerName', 'TotalConsumption', 'TotalCost']
    report = SHEET.add_worksheet(report_name, 100, 20)
    report.append_row(report_header)
    report.format('A1:C1', {'textFormat': {'bold': True}})

    # Iterate report_list and add rows to the new worksheet
    for row in report_list:
        report.append_row([row['ChargerName'], row['Consumption'],
                          row['Cost']])
    report.set_basic_filter(1, 1, len(report_list)+1, 3)

    # Update status worksheet ()
    # month_long = datetime.datetime(2023,int(user_month),1).strftime("%B")

    print(Fore.LIGHTGREEN_EX + f"Updating report status...\n")
    d = datetime.datetime.now()
    date_str = d.strftime("%x")

    status = SHEET.worksheet('Status_2023')
    cell = status.find(month_long)
    # print(f"Found {month_long} in row:{cell.row} col:{cell.col}")
    status.update_cell(cell.row, 2, user_price)
    status.update_cell(cell.row, 3, report_name)
    status.update_cell(cell.row, 4, date_str)
    print(Fore.LIGHTGREEN_EX + f"Status updated.")
    input("\nPress enter to show report")
    os.system('clear')
    show_report(user_month)

# end def


def calculate_cost(data, price):
    """
        #TODO Add docstring
    """
    cost_records = {}

    # iterate the data
    for row in data:
        ch_name = row['ChargerName']
        consumption = row['Consumption']

        # Check if chargername already exists. and then add the consumption
        if ch_name in cost_records:
            cost_records[ch_name]['Consumption'] += consumption
        else:
            cost_records[ch_name] = {'Consumption': consumption, 'Cost': 0}

        # calculate the cost
        cost_records[ch_name]['Cost'] = (cost_records[ch_name]['Consumption']
                                         * price)

    # Create and return list of dictionaries
    result = []

    # Iterate through each charger and its details stored in charger_totals
    for name, details in cost_records.items():
        charger = {
            'ChargerName': name,
            'Consumption': details['Consumption'],
            'Cost': round(details['Cost'], 2)
        }
        # Append the dictionary to the result list
        result.append(charger)

    return result

# end def


def delete_report():
    """
    Shows dialog where user choose which months data to erase
    """

    print(Fore.LIGHTMAGENTA_EX + "**** DELETE REPORT ****\n")

    # Prompt user to choose month (ex 1 = january, 2 = february etc)
    user_month = CF.choose_month()

    # Create report name
    month_short = datetime.datetime(2023, int(user_month), 1).strftime("%b")
    month_long = datetime.datetime(2023, int(user_month), 1).strftime("%B")

    report_name = f"Report_{month_short}_2023"

    # Check if report exists
    if not CF.report_exists(SHEET, report_name):
        print(Fore.LIGHTRED_EX + f"{report_name} can not be found.")
        input("Press enter to continue\n")
        return

    # Delete the worksheet
    print(Fore.LIGHTGREEN_EX + f"Deleting report for {month_long}...\n")
    report_to_delete = SHEET.worksheet(report_name)
    SHEET.del_worksheet(report_to_delete)
    print(Fore.LIGHTGREEN_EX + f"{report_name} deleted. \n")

    # Update status (refactor with function in common)
    print(Fore.LIGHTGREEN_EX + f"Updating report status...\n")
    status = SHEET.worksheet('Status_2023')
    cell = status.find(report_name)
    status.update_cell(cell.row, 2, '')
    status.update_cell(cell.row, 3, '')
    status.update_cell(cell.row, 4, '')
    print(Fore.LIGHTGREEN_EX + f"Status for {month_long} updated.")
    input("\nPress enter to continue")
# end def


def show_status():
    """
    Returns the status for all months
    (month, price, report, date)
    """
    print(Fore.LIGHTMAGENTA_EX + "**** SHOW REPORT STATUS ****\n")

    # Get the data from the workbook 'Status_2023'
    consumption = SHEET.worksheet('Status_2023')
    data = consumption.get_all_values()
    # print(data)
    # Sort the data, starting with january, but how?
    # (Add a new column with number or is it posible to use a function
    # to convert month name to month number)

    # Create table
    status_table = PrettyTable()
    status_table = ColorTable(theme=Themes.OCEAN)
    status_table.field_names = ["Month", "Price", "Report", "Date"]
    # status_table.add_rows(data[0])

    status_table.hrules = ALL

    for idx in range(1, len(data)):
        # Iterates the rows in the data from the workbook and adds them
        # to the table
        status_table.add_row(data[idx])
    print(status_table)
    input("\nPress enter to continue")
# end def


def show_report(month):
    """
    Shows report for the chosen month
    """
    print(Fore.LIGHTMAGENTA_EX + "**** SHOW REPORT ****\n")

    if month == 0:
        user_month = CF.choose_month()
    else:
        user_month = month

    # Create report name
    month_short = datetime.datetime(2023, int(user_month), 1).strftime("%b")
    report_name = f"Report_{month_short}_2023"

    # Check if the report exists
    if not CF.report_exists(SHEET, report_name):
        print(Fore.LIGHTRED_EX + f"{report_name} can not be found.")
        input("Press enter to continue\n")
        return

    # clear screen
    os.system('clear')

    # Get the data from the workbook
    report_to_show = SHEET.worksheet(report_name)
    data = report_to_show.get_all_values()
    # print(data)
    # Sort the data, starting with january, but how?
    # (Add a new column with number or is it possible to use a function
    # to convert month name to month number)

    print(Fore.LIGHTMAGENTA_EX + f"SHOW REPORT - {report_name}\n")

    # Create table
    status_table = PrettyTable()
    status_table = ColorTable(theme=Themes.OCEAN)
    status_table.field_names = ["Charger Name", "Total Consumption",
                                "Total Cost"]
    # status_table = PrettyTable(data[0])
    status_table.hrules = ALL

    for idx in range(1, len(data)):
        # Iterates the rows in the data from the workbook and
        # adds them to the table
        status_table.add_row(data[idx])
    print(status_table)
    input("\nPress enter to continue")


# end def

def show_help():
    """
    Shows instructions for how to use the system
    """
    print("**** HELP ****\n")
    input("Press enter to continue")
    # TODO Print help text
# end def

# def exit():
    """
    Exits the application
    """
    pass
# end def


def main():
    """
    The main function. Shows the menu and awaits user input
    User input is validated and then the chosen option is invoked
    Application exits when the user choose 6 - Exit
    """
    # Set variables
    show_menu = True
    init(autoreset=True)

    while show_menu:
        # Clear the terminal screen
        os.system('clear')

        # Print the menu
        print(Fore.LIGHTBLUE_EX + "E.     C.     C.     S.")
        print(Fore.LIGHTBLUE_EX + "\n***** MAIN  MENU *****\n")
        print(Fore.LIGHTGREEN_EX + "1 - SHOW REPORT STATUS")
        print(Fore.LIGHTGREEN_EX + "2 - CREATE REPORT")
        print(Fore.LIGHTGREEN_EX + "3 - SHOW REPORT")
        print(Fore.LIGHTGREEN_EX + "4 - DELETE REPORT")
        print(Fore.LIGHTGREEN_EX + "5 - HELP")
        print(Fore.LIGHTRED_EX + "6 - EXIT")

        # Prompt the user for input and validate the chosen option
        choice = input("\nSelect option (1-6) \n")
        while (not validation.validate_choice(choice)):
            print(Fore.LIGHTRED_EX + "Option must be a number between 1 and 6")
            choice = input("Select option (1-6) \n")

        try:
            os.system('clear')
            if (choice == "1"):
                # comment:
                show_status()
            elif (choice == "2"):
                # comment:
                create_report()
            elif (choice == "3"):
                # comment:
                show_report(0)
            elif (choice == "4"):
                # comment:
                delete_report()
            elif (choice == "5"):
                # comment:
                show_help()
            elif (choice == "6"):
                # comment:
                print("Exiting E.C.C.S")
                show_menu = False
            # end if
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Something unexpected happened.")
            print(str(e))
            input("Press enter to continue\n")

    # end while
# end def


main()

exit()
