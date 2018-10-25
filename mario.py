from cs50 import get_int


def main():
    while True:
        # continue to prompt user for height until they input between 1 and 8, inclusive
        x = get_int("Height: ")
        if x >= 1 and x <= 8:
            break
    # iterates from 1 to x + 1
    for y in range(1, x + 1):
        # for a given row, print correct number of spaces before '#'
        for space in range(x-y):
            print(" ", end="")
        # print the correct number of # for a given row
        for dash in range(y):
            print("#", end="")
        # print a space in between the two pyramids
        print("  ", end="")
        # print correct number of # following the spaces
        for dash2 in range(y):
            print("#", end="")
        # move to the next line
        print()


if __name__ == "__main__":
    main()