#include <stdio.h>
#include <cs50.h> 
#include <math.h>

int main (void)
{
    float input;
    //do while loop to check the user enters a non-negative number
    do 
    {
        input = get_float("Change owed: ");
    }
    while (input <= 0);
    //cast to an int to avoid imprecision and round
    int x = round (input * 100);
    //calculate the number of quarters which can be given
    //no decimal because casting to int
    int quarter = x / 25;
    //calculate the remaining change owed after giving quarters
    x = x % 25;
    //repeat strategy for dimes
    int dime = x / 10;
    x = x % 10;
    //repeat strategy for nickels
    int nickel = x / 5;
    x = x % 5;
    //the number of pennies is equal to the remaining change
    int penny = x;
    //sum all the change
    int total = quarter + dime + nickel + penny;
    printf("%i \n", total);
}

