import re

class validations(object):

    def validate_email(email):
        test_email = re.match(r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', email)
        if test_email is not None :
            return True

        return False

    def validate_url(url):
        test_url = re.match(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+?\.[a-zA-Z]{2,3}$", url)

        if test_url is not None:
            return True

        return False

    def validate_phone_number(number):
        test_number = re.match(r'^07', number)

        if test_number is None :
            return False

        return True