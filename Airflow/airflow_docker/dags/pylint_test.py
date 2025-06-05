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


if __name__ == "__main__":
    num = int(input("Enter your number: "))
    print("Your square root is:", get_sqrt(num))
