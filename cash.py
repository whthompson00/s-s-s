from cs50 import get_float


quarter = 25
dime = 10
nickel = 5


def main():
    change = 0
    money = -1
    # keep prompting the user until they enter a positive float
    while (money < 0):
        money = get_float("Change owed: ") * 100
    # Divide amount by quarters and truncate the decimal to find out how many quarters are necessary
    change += money // quarter
    # calculate the remaining amount
    money = money % quarter
    # repeat process for dimes
    change += money // dime
    money = money % dime
    # repeat process for nickels
    change += money // nickel
    money = money % nickel
    # add pennies
    change += money
    print(int(change))
    print()


if __name__ == "__main__":
    main()