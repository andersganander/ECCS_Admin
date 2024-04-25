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

