import unittest
import validation


class TestValidateChoice(unittest.TestCase):
    """ Test case for testing validation of users chhoice in the menu 
    """
    
    def test_choice(self):
        self.assertFalse(validation.validate_choice(-1))
        self.assertFalse(validation.validate_choice(None))
        self.assertFalse(validation.validate_choice(0))
        self.assertFalse(validation.validate_choice(8))
        self.assertFalse(validation.validate_choice(''))
        self.assertFalse(validation.validate_choice('Test'))
        self.assertTrue(validation.validate_choice(1))
        self.assertTrue(validation.validate_choice(6))

class TestValidateMonth(unittest.TestCase):
    """ Test case for testing validation of month 
    """

    def test_month(self):

        self.assertFalse(validation.validate_month('stringthatisnotavalidmonth'))
        self.assertFalse(validation.validate_month(''))
        self.assertFalse(validation.validate_month(None))
        self.assertFalse(validation.validate_month(0))
        self.assertTrue(validation.validate_month(1))
        self.assertTrue(validation.validate_month(12))

       




if __name__ == "__main__":
    unittest.main()