import math


def get_sqrt(num):
    return math.sqrt(num)

if __name__ == "__main__":
    num = int(input("Enter your number: "))
    print("Your square root is:", get_sqrt(num))