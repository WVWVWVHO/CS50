/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include "dictionary.h"
node_d* head;



/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // make the letterpointer node the same as the head node
    node_d* lttrpntr = head;
    int i = 0;
    int q;

    // repeat this loop as many times as there are characters in the word
    while(word[i]!='\0')
    {
        // if the character is a letter, make it lowercase and subract 97, otherwise it is an apostrophe thus return 26
        if(isalpha(word[i]))
        {
            q = ((int)tolower(word[i])) - 97;
        }
        else
        {
            q = 26;
        }
        
        // if there are no children, return false, otherwise go to the child and make the pointer i go to the next letter
        if(lttrpntr->children[q] == NULL)
        {
            return false;
        }
        else
        {
            lttrpntr = lttrpntr->children[q];
            i++;
        }
    }
    
    // if the word exists, return true, otherwise return false
    if(lttrpntr->is_word == true)
    {
        return true;
    }
    else
    {
        return false;
    }
}





/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // open dictionary
    FILE* dict = fopen(dictionary, "r");
    
    // check if dictionary really opened    
    if(dict == NULL)
    {
        printf("There is a problem with the opening of the dictionary file!");
        fclose(dict);
        return false;
    }

    // make first node, check if there was memory available to make the node and finally make all the 27 node pointers NULL
    head = NULL;
    head = malloc(sizeof(node_d));
    if(head == NULL)
    {
        return false;   
    }
    for(int k=0; k<27; k++)
    {
        head->children[k] = NULL;
    }
    // make the current node the same as the head node
    node_d* current = head;
    
    // create a char 'C', an int 'I' and an int 'words'
    char c;
    int i;
    int words = 0;
    
    // repeat this loop 'till the end of the dictionary
    while(!feof(dict))
    {
        // make the current node the same as the head node, again
        current = head;
        bool boolcheck = false;
        
        // repeat this loop as long as the next character is a letter or an apostrophe
        while(isalpha(c = fgetc(dict)) || c=='\'')
        {
            boolcheck = true;
            
            if(isalpha(c))
            {
                i = (int)tolower(c) - 97;
            }
            else
            {
                i = 26;
            }
            
            // if there is no pointer to the next child, make a pointer, and make its children NULL
            if(current->children[i]==NULL)
            {
                //node_d* new_node;
                current->children[i] = malloc(sizeof(node_d));
                current->children[i]->is_word = false;
                for(int j=0; j<27; j++)
                {
                    current->children[i]->children[j] = NULL;
                }
            }
            // go to the next node
            current = current->children[i];
        }
        
        if(boolcheck == true)
        {
            current->is_word = true;
            words++;
        }
    } 
    
    // if there are words saved, return the number of words, return true and close the dictionary
    if(words > 0)
    {
        fclose(dict);
        dictsize = words;
        return true;
    }
    // otherwise close the dictionary and return false
    else
    {
        fclose(dict);
        return false;
    }
}






/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    // return the size of the dictionary 
    return dictsize;
}





/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
int z = 0; // remembers the letter the grandchild is, so it won't have to look for it during recursion
bool empty = false; // checks if the tree is emptied

bool unload(void)
{
    remove_pointer = head;
    while(empty == false)
    {
        rmv(remove_pointer);
    }
    return true;
}


bool rmv()
{
    // just stop if the remove_pointer is NULL
    if(remove_pointer == NULL)
    {
        return false;
    }

    // check for every letter if one of the children has a value
    for(int x=z; x<27; x++)
    {
        if(remove_pointer->children[x] != NULL)
        {
            // check for every letter if one of the grandchildren has a value
            for(int y=0; y<27; y++)
            {
                // if one of the grandchildren has a value, go to the child
                if(remove_pointer->children[x]->children[y] != NULL)
                {
                    remove_pointer = remove_pointer->children[x];
                    z = y;
                    return rmv(remove_pointer);
                }
            }
            // if there are no grandchildren, free the child, make the pointer NULL and return to the head
            free(remove_pointer->children[x]);
            remove_pointer->children[x]=NULL;
            remove_pointer = head;
            z = 0;
            return false;
        }
    }
    // if none of the children has a value, the tree is empty and 'true' can be returned
    free(remove_pointer);
    empty = true;
    return true;
}