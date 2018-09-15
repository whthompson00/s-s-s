#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //make the user input a char to account for user's entering words
    char n=0;
    //check to see whether value is between 1-8 in ascii
    while (n<49||n>56) 
    {
        n=get_char("Please enter a number 1-8, inclusive\n");
        if (n<49||n>56)
        {
            printf("Not a valid submission");
        }
        else 
        {
            printf("Height: %i\n", n-48);
        }
    }
    //convert char to int
    int x = n-48;
    //loop for each row of pyramid
    for (int i=1;x+1>i;i++)
    {
        int j=0;
        //loop for the indentation of each row
        while (j<x-i)
        {
            printf(" ");
            j++;
        }
        //loop for the number of "#" in each row
        int p=0;
        while (p<i)
        {
            printf("#");
            p++;
        } 
        //put gap in between to staircases 
        printf("  ");
        //loop for the number of "#" on the other side of the gap
        p=0;
        while (p<i)
        {
            printf("#");
            p++;
        }
        printf("\n");
    }
}
