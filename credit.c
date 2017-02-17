#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>


int main(void)
{
    long long cc;  // credit card number
    int c;         // length of credit card number

    // ask credit card number    
    printf("Credit Card number: ");
    cc  = get_long_long();
    c   = floor(log10((cc)))+1;

    // if the credit card number is shorter than 13 return INVALID
    // if the credit card number is longer  than 16 return INVALID
    if (c<13 || c>16)
    {
        printf("INVALID\n");
        exit(0);
    }
 
    // make string of the long_long
    char s[20];
    sprintf(s, "%lld", cc);


    // temporary variables
    int sum1 = 0;            // second to last
    int sum2 = 0;            // last
    int sum3 = sum1 + sum2;  // sum of the sums above

    // sum of the 'second to last' numbers
    for (int i= c-2; i>=0; i = i-2)
    {
        if ((s[i]-48)*2 < 10)
        {
            sum1 = (s[i] - 48)*2 + sum1;
        }
        else 
        {
            sum1 = (s[i] - 48)*2 - 10 + 1 + sum1;
        }
    }

    // sum of the 'last' numbers
    for (int i= c-1; i>=0; i = i-2)
    {
        sum2 = (s[i]-48) + sum2;
    }    
    

    // check if sum3 ends with a 0
    if (sum3 % 10 == 0)
    {
        int two = (s[0]-48)*10+s[1]-48;

    // check if the card is from AMEX        
        if (two == 34 || two == 37)
        {
            printf("AMEX\n");
        }
  
    // check if the card is from MASTERCARD      
        if (two >= 51 && two <= 55)
        {
            printf("MASTERCARD\n");
        }

    // check if the card is from VISA        
        if (s[0]-48 == 4)
        {
            printf("VISA\n");
        }
    }

    // if the card does not end with a 0 return INVALID    
    else
    {
        printf("INVALID\n");
    }
}