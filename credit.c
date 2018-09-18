#include <stdio.h>
#include <cs50.h>
//getIntAt will return a digit from a long at a given value
//int at is where in the long the method obtains the digit from
//long z is the number which the method gets the digit from
long getIntAt(int at, long z)
{
    long m=10;
    //determine what power of 10 the digit is at
    for (int c=at;c>1;c--)
    {
        m=10*m;
    }
    long digit;
    digit=z%m;
    printf("%ld \n", digit);
    //divide the previous number by m/10 to leave just the first digit
    //the decimals will go away because it is cast as an int
    digit=digit/(m/10);
    return digit;
}
//checks to see whether credit card number is valid according to Luhn's
//long r is the number to check
//l is the length
//returns a boolean
bool check (long r, int l)
{
    int sum=0;
    //completing step 1 in Luhn's algorithm
    for(int i=2;i<l+1;i+=2)
    {
        //call the getIntAt method to obtain every other digit
        int holder=getIntAt(i,r);
        holder*=2;
        if (holder>9)
        {
            //break up the digits
            sum+=(1+holder%10);
        }
        else
        {
            sum+=holder;
        }
    }
    //completing step 2 in Luhn's algorithm
    for(int j=1;j<l+1;j+=2) 
    {
        int holder1=getIntAt(j,r);
        sum+=holder1;
    }
    //step 3 Luhn's algorithm
    if(sum%10==0)
    {
        return true;
    }
    else
    {
        return false;
    }
    
}
int main(void)
{
    long x=get_long("Please enter your credit card number: ");
    long y=x;
    int length=1;
    //boolean to keep track of whether the credit card number is valid or not
    bool b;
    //to determine the length of the user's input
    while(y>9)
    {
        y/=10;
        length++;
    }
    string type;
    //check the length to see what company the card is
    if (length==15)
    {
        int Amex1=getIntAt(15,x);
        int Amex2=getIntAt(14, x);
        if (Amex1==3&&(Amex2==4||Amex2==7))
        type="AMEX";
        //call the check method to see if card number is valid
        b=check(x, length);
    }
    else if (length==13)
    {
        type="VISA";
        //check to see if valid Visa card which begins with 4
        int v1=getIntAt(13,x);
        printf("%i \n", v1);
        if(v1==4)
        {
           //call the check method to see if card number is valid
           b=check(x, length);
        }
        else
        {
            b=false;
        }
    }
    else if (length==16)
    {
        //write code to check whether it's mastercard or Visa
        int v=x/1000000000000000;
        //call the check method to see if card number is valid
        b=check(x, length);
        //variables for checking for MasterCard
        int a1=getIntAt(16, x);
        int a2=getIntAt(15, x);
        bool sec=a2>=1&&a2<=5;
        if (v==4)
        {
            type="Visa";
        }
        //check to see if valid MasterCard number, which begin with 51, 52, 53, 54, 55
        else if(a1==5&&sec)
        {
            type="MasterCard";
        }
        else
        {
            b=false;
        }
        
        
    }
    //else return false because the number is not the length of any cards 
    else
    {
        b=false;
    }
    //if false, print invalid
    if (b==false)
    {
        printf("INVALID \n");
    }
    //otherwise print the company's name
    else
    {
        printf("%s \n", type);
    }
}
