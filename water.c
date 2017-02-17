#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // ask the user for the number of minutes he/she showers
    int minutes;
    do
    {
        printf("Minutes: ");
        minutes = get_int();
    }
    while(minutes < 0);
    
    // print the equivalent number of bottles
    printf("Bottles: %i\n", minutes*12);
}