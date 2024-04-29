def validate_choice(choice):
    """
    Validates the menu choice an returns true/false
    First check for None
    Then check the type, which will catch strings, floats etc
    If the choice is an int, test if it's between (including) 1 and (including) 6
    """
    if choice is None:
        return False

    try:
        # Convert into integer
        val = int(choice)
    except ValueError:
        # return False if the conversion fails 
        return False  
        
    return (val >= 1 and int(choice) <= 6)
# end def

def validate_month(month):
    """ Validates that month is an intteger between
     1 (inclusive) and 12 (inclusive)"""
    # check for None
    if month is None:
        return False
   
    # check type and the value
    try:
        converted = int(month)
        if 1 <= converted <=12: 
            return True
    except ValueError:
        return False
# end def

