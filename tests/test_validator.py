import unittest
from app.validators import Validator

class TestValidatorMethods(unittest.TestCase):
    def test_validate_dni(self):
        valid_dni = '1234567890'
        invalid_dni = 'ABC123'
        
        self.assertTrue(Validator.validate_dni(valid_dni))
        self.assertFalse(Validator.validate_dni(invalid_dni))

if __name__ == '__main__':
    unittest.main()
