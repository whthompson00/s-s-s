#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    //check to make sure the user only inputs one word
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword \n");
        exit(0);
    }
    //create an array to store the values of the shift.
    int kj [strlen(argv[1])];
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        char c = argv[1][i];
        //check that all the chars are letters.
        if (c < 'A' || (c > 'Z' && c < 'a') || c > 'z')
        {
            printf("Usage: ./caesar key \n");
            exit(0);
        }
        else
        {
            //store the values of the shift in the array
            if (isupper(c))
            {
                kj[i] = (int) c - (int) 'A';
            }
            else
            {
                kj[i] = (int) c - (int) 'a';
            }
        }
    }
    string m = get_string("Plaintext: ");
    printf("ciphertext: ");
    int l = strlen(m);
    int v = 0;
    //go through the entire user input and shift
    for (int r = 0; r < l; r++)
    {
        char c = ' ';
        //test if the char is an alphabetical characture
        if (isupper(m[r]) || islower(m[r]))
        {
            if (isupper(m[r]))
            {
                //shift by the value of kj.
                //v % strlen(argv[1]) makes sure the letters of kj are used cyclically
                //% 26 to keep values within the alphabet
                c = (m[r] - 'A' + kj[v % strlen(argv[1]) ]) % 26 + 'A';
                printf("%c", c);
            }
            else
            {
                //same as above
                c = (m[r] - 'a' + kj[v % strlen(argv[1]) ]) % 26 + 'a';
                printf("%c", c);
            }
            //keep track of where in the cycle of kj
            v++;
        }
        //don't move the non alphabetical charactures
        else
        {
            c = m[r];
            printf("%c", c);
        }
    }
    printf("\n");
}

