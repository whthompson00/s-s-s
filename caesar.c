#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int stringToInt(string s);

int main(int argc, string argv[])
{
    int x;
    //check to make sure the user inputed one string
    if (argc == 2)
    {
        //check to make sure all inputed values are ints
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            char c = argv[1][i];
            if (c < '0' || c > '9')
            {
                printf("Usage: ./caesar key \n");
                exit(0);
            }
        }
        //convert the string to an int
        x = stringToInt(argv[1]);
    }
    else
    {
        printf("Usage: ./caesar key \n");
        exit(0);
    }
    string m = get_string("plaintext: ");
    int l = strlen(m);
    char cipher [l];
    for (int i = 0; i < l; i++)
    {
        //check if char is uppercase
        if (isupper(m[i]))
        {
            //change the value of m[i] by x
            //use %26 to ensure that value remains in alphabet
            //if the shift is greater than 26, then the value wraps around to 'A'
            cipher[i] = (m[i] - 'A' + x) % 26 + 'A';
        }
        //check if char is lowercase
        else if (islower(m[i]))
        {
            //same as above but with lowercase
            cipher[i] = (m[i] - 'a' + x) % 26 + 'a';
        }
        //otherwise, do not shift.
        //Only alphabetical charachters rotate
        else
        {
            cipher[i] = m[i];
        }
    }
    //printf was not working properly for the string
    //this code prints the array of chars in proper format
    printf("ciphertext: ");
    for (int i = 0; i < l; i++)
    {
        printf("%c", cipher[i]);
    }
    printf("\n");
}

//convert the string to an int.  Made before I was aware of atoi.
int stringToInt(string s)
{
    int sum = 0;
    int ex = 1;
    //go backwar through the string, multiplying each value by 10
    //ie 123 = 3 + 20 + 100
    for (int i = strlen(s) - 1; i >= 0; i--)
    {
        int x = (int) s[i] - '0';
        sum += x * ex;
        ex *= 10;
    }
    return sum;
}
