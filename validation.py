def validate_choice(choice):
    """
    Validates the menu choice an returns true/false
    Raises a TypeError if coice is not an integer
    """
    
    try:
        # Convert it into integer
        val = int(choice)
    except ValueError:
        raise TypeError("Choice should be an integer.")    
        
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

