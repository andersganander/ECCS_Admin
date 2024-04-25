import gspread
from google.oauth2.service_account import Credentials
import validation

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Charger_consumption_2023')

consumption = SHEET.worksheet('Status_2023')
data = consumption.get_all_values()
print(data)

# \n is needed for getting it to work in Heroku
# data_str = input("Please enter:\n")



