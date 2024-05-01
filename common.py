import validation
from colorama import Fore, Back, Style, init
import gspread


class CommonFunctions:
    def __init__(self):
        pass

    def choose_month(self):
        """
        Prompts the user to choose a month
        Month is validated according to rules in validate_month
        """

        # Prompt user to choose month (ex 1 = january, 2 = february etc)
        user_month = input("Enter month (1-12) \n")

        # Validate the chosen month
        while (not validation.validate_month(user_month)):
            print(Fore.LIGHTRED_EX + f"Invalid input: {user_month}")
            user_month = input("Enter valid month (1-12) \n")
        return user_month

    # end def

    def report_exists(self, SHEET, name):
        """
            Checks if the report name exists in the
            worksheet Status_2023
        """

        status = SHEET.worksheet('Status_2023')
        if status.find(name) is None:
            return False
        else:
            return True

    # end def
