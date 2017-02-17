#include <cs50.h>
#include <stdio.h>
#include <math.h>


int main(void)
{
    // ask for the amount of change
    double change;
    do
    {
        printf("How much change is owed?\n$");
        change = get_double();
    }
    while(change <= 0);

    // change  the double floating point dollar value to a integer value in cents
    int cents = change * 100;



    // k is the minimum amount of coins needed
    int k = 0;
   
    // number of $0.25 coins needed        
    while (cents>=25)
    {
        cents = cents - 25;
        k++;
    }
    
    // number of $0.10 coins needed        
    while (cents>=10)
    {
        cents = cents - 10;
        k++;
    }
    
    // number of $0.05 coins needed        
    while (cents>=5)
    {
        cents = cents - 5;
        k++;
    }
    
    // number of $0.01 coins needed        
    while (cents>=1)
    {
        cents = cents - 1;
        k++;
    }
    
    printf("%i\n", k);
}