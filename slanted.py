import sys
from cs50 import get_string


def main():

    # Ensure proper usage
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        exit("Usage: python slanted.py depth")
    depth = int(sys.argv[1])

    # Encrypt message
    message = get_string("Message: ")
    slanted = slant(message, depth)
    if len(message) >= depth:
        print(f"Slanted: {slanted}")


def slant(message, depth):
    newMessage = ""
    for j in range (depth):
        for i in range (0, len(message), depth):
            if i+j < len(message):
                newMessage += message[i+j]
    return newMessage



if __name__ == "__main__":
    main()
