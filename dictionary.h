/**
 * Declares a dictionary's functionality.
 */

#ifndef DICTIONARY_H
#define DICTIONARY_H

#include <stdbool.h>

// maximum length for a word
// (e.g., pneumonoultramicroscopicsilicovolcanoconiosis)
#define LENGTH 45

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word);

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary);


//define node
typedef struct node
{
    bool is_word;
    struct node *children[27];
}node_d;

//node *root;





/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void);

int dictsize;

/**
 * Unloads dictionary from memory.  Returns true if successful else false.
 */
bool unload(void);
bool rmv(node_d* remove_pointer);
node_d* remove_pointer;


#endif // DICTIONARY_H
