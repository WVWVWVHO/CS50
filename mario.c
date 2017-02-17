#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // ask for an height between the 1 and 23
    int height;
    do
    {
        printf("Height: ");
        height = get_int();
    }
    while(height > 23 || height <0);


    // print the whole piramid
    for(int i=1; i<=height; i++)
    {

        // print the spaces before the #'s  
        for(int k=0; k<(height-i); k++)
            {
                printf(" ");
            }

        // print first #'s
        for(int j=i; j>0; j--)
            {
                printf("#");
            }

        // print the two spaces        
            printf("  ");    

        // print the last #'s            
        for(int z=i; z>0; z--)
            {
                printf("#");
            }            

        // print a last return            
        printf("\n");
    }
}