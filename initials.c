#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    // ask for the name
    string s;
    s = get_string();

    // see if the first letter is a space, if not, print this letter
    if (s[0] != 32)
    {
        printf("%c", toupper(s[0]));
    }

    // print the rest of the intials       
    for(int i=1; i<strlen(s); i++)
    {
        // see if the current letter is a space, if so, go to next letter
        if(s[i] == 32)
            {
            }
        // see if the last letter was a space AND the current letter is not a space, if so, print this letter
        else if(s[i-1] == 32 && s[i] != 32) 
        {
            printf("%c", toupper(s[i]));
        }
    }
    printf("\n");
}