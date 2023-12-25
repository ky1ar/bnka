import re

class Validator:
    @staticmethod
    def validate_dni(dni):
        return dni.isdigit()

    @staticmethod
    def validate_phone(phone):
        return all(char.isdigit() or char == '+' for char in phone)

    @staticmethod
    def validate_name_last(name, last):
        return all(char.isalpha() or char.isspace() for char in name + last)

    @staticmethod
    def validate_email(email):
        pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return bool(re.match(pattern, email))