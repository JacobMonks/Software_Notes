"""
This is a smaple file for testing linting in GitHub Actions.
It will utilize Flake8
"""
import math


def get_sqrt(num):
    """
    This function returns the square root of the number given.
    """
    return math.sqrt(num)


def get_log(num):
    return math.log10(num)

    
# This gets run if the file itself is run.
if __name__ == "__main__":
    """
    This program asks the user for an input number anf returns the square root of that number.
    """
    num = int(input("Enter your number: "))
    print("Your square root is:", get_sqrt(num))
