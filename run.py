import os
import gspread
from google.oauth2.service_account import Credentials
import validation
import common
from prettytable import PrettyTable, ALL
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

    # Prompt user to choose month (ex 1 = january, 2 = february etc)
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

def delete_report():
    """
    Shows dialog where user choose which months data to erase 
    """
    print("***** ERASE MONTH *****")
    
    # Prompt user to choose month (ex 1 = january, 2 = february etc)
    user_month = input("Enter month (1-12) \n")

    # Validate the chosen month
    while (not validation.validate_month(user_month)):
        user_month = input("Enter month (1-12) \n")

     # Create report name
    month_short = datetime.datetime(2023,int(user_month),1).strftime("%b")
    report_name = f"Report_{month_short}_2023"

    # Check if report exists

    # Ask user if they want to proceed

    # Delete the worksheet
    report_to_delete = SHEET.worksheet(report_name)
    SHEET.del_worksheet(report_to_delete)
    print(f"{report_name} deleted")
    
    # Update status (refactor with function in common, at least some of the code) 
    status = SHEET.worksheet('Status_2023')
    cell = status.find(report_name)
    print(f"Found {report_name} in row:{cell.row} col:{cell.col}")
    status.update_cell(cell.row,2,'')
    status.update_cell(cell.row,3,'')
    status.update_cell(cell.row,4,'')
    print(f"Status for {user_month} updated.")
    input("Press enter to continue")
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
    status_table.hrules=ALL

    for idx in range(1, len(data)):
        # Iterates the rows in the data from the workbook and adds them to the table
        status_table.add_row(data[idx])
    print (status_table)
    input("Press enter to continue")
# end def

def show_report():
    """
    Shows report for the chosen month
    """
    print("show report")

    # Prompt user to choose month (ex 1 = january, 2 = february etc)
    user_month = input("Enter month (1-12) \n")

    # Validate the chosen month
    while (not validation.validate_month(user_month)):
        user_month = input("Enter month (1-12) \n")

     # Create report name
    month_short = datetime.datetime(2023,int(user_month),1).strftime("%b")
    report_name = f"Report_{month_short}_2023"


    # TODO Check if the report exists

    # Get the data from the workbook
    report_to_show = SHEET.worksheet(report_name)
    data = report_to_show.get_all_values()
    # print(data)
    # Sort the data, starting with january, but how? (Add a new column with number 
    # or is it posible to use a function to convert month name to month number) 

    # Create table
    status_table = PrettyTable(data[0]) 
    status_table.hrules=ALL

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
    #TODO Print help text
# end def

#def exit():
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

    while show_menu:
         # Clear the terminal screen
        os.system('clear')

        # Print the menu
        print("E. C. C. S.")
        print("\n**** Main Menu ****\n")
        print("1 - SHOW REPORT STATUS")
        print("2 - CREATE REPORT")
        print("3 - SHOW REPORT")
        print("4 - DELETE STATUS")
        print("5 - HELP")
        print("6 - EXIT")

        # Prompt the user for input and validate the chosen option
        choice = input( "Select option (1-6) \n")
        while (not validation.validate_choice(choice)):
            choice = input( "Select option (1-6) \n")

        os.system('clear')
        if (choice == "1"):
            # comment: 
            show_status()
        elif (choice == "2"):
            # comment: 
            create_report()
        elif (choice == "3"):
            # comment: 
            show_report()
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
    # end while
# end def

main()
exit()





