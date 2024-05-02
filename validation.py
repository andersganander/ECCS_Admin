def validate_choice(choice):
    """ Validates the menu choice (1-6)
    :param choice: the menu option to validate
    :type choice: int
    :return: 'True' if it's a valid option, 'False' otherwise
    """

    return validate_int(choice, 1, 6)
# end def


def validate_month(month):
    """ Validates the month (1-12)
    :param month: the month to validate
    :type month: int
    :return: 'True' if it's a valid month, 'False' otherwise
    """

    return validate_int(month, 1, 12)
# end def


def validate_int(val, min_int, max_int):
    """ Validate that val is an integer between min_int and max_int
    First check for None
    Then check the type, which will catch strings, floats etc
    If the choice is an int, test if it's between (inclusive) min_int
    and max_int

    :param val: The value to validate
    :type val: int
    :param min_int: The start of the interval
    :type min_int: int
    :param max_int: The end of the interval
    :type min_int: int

    :return: 'True' if val is in the interval, 'False' otherwise
    :rtype: bool
    """

    if val is None:
        return False

    try:
        # Convert into integer
        int_val = int(val)
    except ValueError:
        # return False if the conversion fails
        return False

    return (int_val >= min_int and int_val <= max_int)
