from urllib.request import urlopen
import calendar
import json

TIMEOUT = 5
BASEURL = "https://www.elprisetjustnu.se/api/v1/prices/2023/"


def get_avgprice_for_date(userdate):
    """
    Fetch energy prices for the userdate from https://www.elprisetjustnu.se
    Returns the average price
    """

    url = BASEURL + userdate+"_SE3.json"

    # store the response of URL
    response = urlopen(url, timeout=TIMEOUT)

    # storing the JSON response from url in data
    data_json = json.loads(response.read())

    # iterate all dicts and get the price, then calculate the average
    tot_price = 0.00
    nr_of_items = 0

    # get the price and add it to the sum
    for d in data_json:
        curr_price = float(d.get('SEK_per_kWh'))
        tot_price += curr_price
        nr_of_items += 1

    # calculate the average price
    avg_price = tot_price / nr_of_items

    return avg_price


def get_avgprice_for_month(month):
    """
    Fetch the energy prices for all days in the month
    Returns the average price
    """
    avg_month_price = 0
    month_total = 0

    # get the number of days for the month
    nr_of_days = calendar.monthrange(2023, month)[1]

    # add a zero at the beginning of the monthnumber if needed
    zero = '0' if month <= 9 else ''
    usermonth = f"{zero}{month}"

    # iterate number of days in the month
    for x in range(nr_of_days):
        zero = '0' if x < 9 else ''
        userdate = f"{usermonth}-{x+1}"
        month_total += get_avgprice_for_date(f"{usermonth}-{zero}{x+1}")

    return round((month_total / nr_of_days), 2)


def get_external_price(month):
    """

    """
    try:
        return get_avgprice_for_month(month)
    except Exception as e:
        print("Something went wrong when communicating with external api")
        print(str(e))

# end def
# print(get_external_price(9))
