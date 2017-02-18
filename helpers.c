/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // if n is smaller than 0, return false
    if(n<=0)
    {
        return false;
    }

    // create two integers, a minimum and a maximum  
    int min = 0;
    int max = n;
        
    for(int r=0; r<log(n)+1; r++)
    {
        int av = (min+max)/2;
        
        // if the value is exactly in the middle, return true
        if(values[av] == value)
        {
            return true;
        }    
        
        else if (values[av] < value)
        {
            min = av + 1;
        }

        else if (values[av] > value)
        {
            max = av - 1;
        }
    }
    return false;
}


/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    for(int i=0; i<n-1; i++)
    {
        for(int k=0; k<(n-i-1); k++)
        {
            if (values[k] > values[k+1])
            {
                int kk = values[k];
                values[k] = values[k+1];
                values[k+1] = kk;
            }
        }
    }

}
