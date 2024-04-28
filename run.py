import os
import gspread
from google.oauth2.service_account import Credentials
import validation
import common
from prettytable import PrettyTable
import datetime

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
    
    consumption = SHEET.worksheet('Consumption_2023')

    os.system('clear')
    print("Create Report")
    print('-------------')

    # Prompt user to choose month (ex january or jan)
    user_month = input("Enter month (1-12) \n")

    # Validate the chosen month
    while (not validation.validate_month(user_month)):
        user_month = input("Enter month (1-12) \n")

    # Check if report exists for chosen month

    # Check that price exists (UPDATE FLOWCHART)
    user_price = 0.5
    
    # Calculate cost for each charger
    print('Calculate cost...')
    # Code from S O
    records = consumption.get_all_records(value_render_option="UNFORMATTED_VALUE")
    print(records)
    # find all rows for the chosen month
    found_records = []
    for record in records:
        #m = str(record.get('Month')) 
        #print(f"m={m} user_month={user_month}")
        if str(record.get('Month')) == user_month:
            found_records.append(record)
    print("*********** Found records **************")
    print(found_records)
    print(f"Found records antal: {len(found_records)}")

    report_list = calculate_cost(found_records, user_price)
    print('****** report_list ******')
    print(report_list)

    # Create report name
    month_short = datetime.datetime(2023,int(user_month),1).strftime("%b")
    report_name = f"Report_{month_short}_2023"

    # Create new worksheet
    report_header = ['ChargerName','TotalConsumption','TotalCost']
    report = SHEET.add_worksheet(report_name, 100, 20)
    report.append_row(report_header)
    report.format('A1:C1', {'textFormat': {'bold': True}})

    # Iterate report_list and add rows to the new worksheet
    for row in report_list:
        report.append_row([row['ChargerName'], row['Consumption'], row['Cost']])
    report.set_basic_filter(1, 1, len(report_list)+1, 3)

    # Update status worksheet ()
    month_long = datetime.datetime(2023,int(user_month),1).strftime("%B")
    d = datetime.datetime.now()
    date_str = d.strftime("%x")
    print(date_str)
    print(month_long)
    status = SHEET.worksheet('Status_2023')
    cell = status.find(month_long)
    print(f"Found {month_long} in row:{cell.row} col:{cell.col}")
    status.update_cell(cell.row,2,user_price)
    status.update_cell(cell.row,3,report_name)
    status.update_cell(cell.row,4,date_str)

    input("Press enter to continue")
# end def

def calculate_cost(data, price):
    """
    
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
            cost_records[ch_name] = {'Consumption': consumption, 'Cost':0}

        # calculate the cost
        cost_records[ch_name]['Cost'] = cost_records[ch_name]['Consumption'] * price 
    
    print('*********  Calculate cost *************')
    print(cost_records)

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




##################### TEMP CODE

def combine_charger_consumptions(data, price_per_unit):
    # Dictionary to hold combined results with consumption totals and costs
    charger_totals = {}

    # Iterate through each item in the input list
    for entry in data:
        # Get charger name and consumption
        charger_name = entry['ChargerName']
        consumption = entry['Consumption']

        # If the charger name is already in the dictionary, add to its consumption
        if charger_name in charger_totals:
            charger_totals[charger_name]['Consumption'] += consumption
        else:
            # Otherwise, initialize it in the dictionary with consumption and cost
            charger_totals[charger_name] = {'Consumption': consumption, 'Cost': 0}

        # Update cost for the current consumption increment
        charger_totals[charger_name]['Cost'] = charger_totals[charger_name]['Consumption'] * price_per_unit

    # Create a list of dictionaries from the accumulated totals
    result_list = [{'ChargerName': name, 'Consumption': details['Consumption'], 'Cost': round(details['Cost'], 2)} for name, details in charger_totals.items()]
    return result_list
