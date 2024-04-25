def validate_choice(choice):
    """
    Validates the menu choice an returns true/false
    Raises a TypeError if coice is not an integer
    """
    if not (isinstance(choice, int)):
        raise TypeError("Choice should be an integer.")
    else:
        return (int(choice) >= 1 and int(choice) <= 6)
# end def

