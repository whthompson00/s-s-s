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
            printf("Error. Not a valid submission. \n");
        }
        else 
        {
            printf("Height: %i\n", n-48);
        }
    }
    //convert char to int
    int x = n-48;
    //for loop to track which line in the pyramid
    for (int i=x;i>0;i--)
    {
        //for loop to track the number of spaces printed
        for(int j=i;j>1;j--)
        {
            printf(" ");
        }
        //variable k track the number of "#"s on a given line
        int k=x-i+1;
        //for loop to track the number of "#" printed
        for(int l=0;l<k;l++)
        {
            printf("#");
        }
        printf("\n");
    }
}
