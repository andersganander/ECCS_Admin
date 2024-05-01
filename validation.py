def validate_choice(choice):
    """
    Validates the menu choice an returns true/false
    First check for None
    Then check the type, which will catch strings, floats etc
    If the choice is an int, test if it's between (including) 1 and
    (including) 6
    """

    return validate_int(choice, 1, 6)
# end def


def validate_month(month):
    """ Validates that month is an intteger between
     1 (inclusive) and 12 (inclusive)"""

    return validate_int(month, 1, 12)
# end def


def validate_int(val, min_int, max_int):
    """
        Validate that val is an integer between min_int and max_int
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
