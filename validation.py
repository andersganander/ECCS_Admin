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
    """ Validates month"""
    # check type

    # check non etc

    valid_months = months = [
    "january", "jan",
    "february", "feb",
    "march", "mar",
    "april", "apr",
    "may", "may",
    "june", "jun",
    "july", "jul",
    "august", "aug",
    "september", "sep",
    "october", "oct",
    "november", "nov",
    "december", "dec"
    ]

    if month.lower() in valid_months:
        return True
    else:
        return False

