from cs50 import get_string
import sys

# create a set in memory to store the banned words
words = set()


def main():
    # make sure the user inputed proper command line
    if len(sys.argv) != 2:
        sys.exit("Usage: python bleep.py dictionary")
    banned = sys.argv[1]
    # load the banned texts
    loaded = load(banned)
    # check to make sure it properly loaded into memory
    if not loaded:
        print(f"Could not load {banned}.")
    # prompt the user
    message = get_string("What message would you like to censor? ")
    # split the message into a list
    censored = message.split(' ')
    counter = 0
    # interate through each word the user inputted
    for c in censored:
        counter += 1
        # check if the word is banned
        if check(c):
            counter2 = 0
            # iterate through the banned word printing a * for each letter
            for letter in c:
                counter2 += 1
                # if it is the last letter, print '*' and a space
                if counter2 == len(c):
                    print("*", end=" ")
                # if there are more letters, print '*' and no space
                else:
                    print("*", end="")
        # the word is not banned.  Print the word
        else:
            # if it is the last word from the user, print and send to a new line
            if counter == len(censored):
                print(c)
            # if more words follow in the message, print and then follow with a space
            else:
                print(c, end=" ")


def load(banned):
    file = open(banned, "r")
    # iterate through the file, adding each word to the set words
    for line in file:
        words.add(line.rstrip("\n"))
    file.close()
    return True


def check(word):
    # check if the word sent is in the set words
    return word.lower() in words


if __name__ == "__main__":
    main()
