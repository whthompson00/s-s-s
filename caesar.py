import sys
from cs50 import get_string

letters = 26


def main():
    # make sure user entered proper command line
    if len(sys.argv) != 2:
        print("Usage: python caesar.py k")
        sys.exit(1)
    # cast the user's input to an int
    x = int(sys.argv[1])

    # prompt user for message
    p = get_string("plaintext:  ")
    if not p:
        sys.exit(1)
    # create cipher to store new message
    cipher = ""
    # iterate through the message, letter by letter
    for c in p:
        # check if the char is upper, lower, or not alphabetical
        if(c.isupper()):
            # rotate by x, while using mod letters to ensure the letter remains within bounds of alphabet
            cipher += chr((ord(c) - ord('A') + x) % letters + ord('A'))
        elif(c.islower()):
            # same as above except for lowercase letters
            cipher += chr((ord(c) - ord('a') + x) % letters + ord('a'))
        else:
            # just add the non-alphabetical char to the message as is
            cipher += c
    # print the new message with
    print(f"ciphertext: {cipher}")


if __name__ == "__main__":
    main()
