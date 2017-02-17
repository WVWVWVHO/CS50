#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>


int main(int argc, string argv[])
{
    // if there are more or less than two arguments in the command line, return ERROR
    if (argc != 2)
    {
        printf("ERROR");
        return 1;   
    }

    // change the inputted variable from a string to an integer  
    string num = argv[1];
    int k = atoi(num);

    // ask user to input the plaintext   
    printf("plaintext:");
    string p = get_string();

    // convert the plaintext to ciphertext
    printf("ciphertext: ");
    for(int i=0, n=strlen(p); i<n; i++)
    {
        // if the character is a letter convert it, using k
        if (isalpha(p[i]))
        {
            if (isupper(p[i]))
            {
                int c = p[i] - 65;
                c = (c + k) % 26;
                c = c + 65;
                printf("%c", c);
            }
            else
            {
                int c = p[i] - 97;
                c = (c + k) % 26;
                c = c + 97;
                printf("%c", c);   
            }
        }
        // if the character is not a letter just return it        
        else
        {
            printf("%c",p[i]);
        }
    }
    
    // print final return and return 0
    printf("\n");
    return 0;
}