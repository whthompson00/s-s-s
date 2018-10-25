from cs50 import get_string


def main():
    # prompt user for name
    s = get_string("What is your name? \n")
    # print hello followed by their name
    print(f"hello, {s}")


if __name__ == "__main__":
    main()