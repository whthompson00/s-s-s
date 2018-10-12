// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 100000

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Create a matrix of node pointers for each letter of the alphabet to reduce run time
node *hashtable[N];

// Hash function FNV
// taken from http://www.eternallyconfuzzled.com/tuts/algorithms/jsw_tut_hashing.aspx
unsigned long hash(const char *str)
{
    unsigned h = 2166136261;
    for (int i = 0; i < strlen(str); i++)
    {
        h = (h * 16777619) ^ str[i];
    }
    //use mod to keep h within bounds of hashtable
    return h % N;
}

//counter to keep track of the number of words in the dictionary
int counter = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        //create node for the new entry
        node *insert = malloc(sizeof(node));
        //check to make sure malloc properly assigned memory
        if (insert == NULL)
        {
            unload();
            return false;
        }
        //copy the word into the node
        strcpy(insert->word, word);
        //find the location of the word in the hashtable
        int location = hash(word);
        //assign the pointer in the new node to point to the first node in the linked list
        insert->next = hashtable[location];
        //make insert the new first node in the linked list
        hashtable[location] = insert;
        //increment counter for new word
        counter++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return counter;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int l = strlen(word);
    char lowerWord [l + 1];
    //make word all lower case to test if it is in the dictionary
    for (int i = 0; i < l; i++)
    {
        //needed to create char a because c was not assigning lowerWord[i] otherwise
        char a = tolower(word[i]);
        lowerWord[i] = a;
    }

    lowerWord [l] = '\0';
    //find the hash value of the lower case word
    int location = hash(lowerWord);
    //create a node pointer starting at location in the hashtable
    node *ptr = hashtable[location];
    //move through the linked list until NULL is reached
    while (ptr != NULL)
    {
        char *wordCheck = ptr->word;
        bool b = false;
        //make sure the word being checked and the word in the linked list are the same length
        //this condition prevents substrings from being accepted
        if (strlen(wordCheck) == l)
        {
            int j = 0;
            //move through the words and check each element of the array
            for (int i = 0; i < l; i++)
            {
                if (!(lowerWord[i] == wordCheck[j]))
                {
                    //ignore apostrophes
                    if(lowerWord[i] == '\'')
                    {
                        //to ensure that the letters are being compared at the same index, ignoring apostrophes
                        j--;
                    }
                    //if the letters are not the same at the same index, then the words are not the same
                    else
                    {
                        b = false;
                        break;
                    }
                }
                j++;
                b = true;
            }
        }
        //all the letters of the word and the dictionary entry are the same.  The word exists.
        if (b)
        {
            return true;
        }
        //move to the next node in the linked list
        ptr = ptr->next;
    }
    //if the hashtable entry at location is NULL return void
    return false;
}

//a recursive method which deletes a linked list
void deleter(node *temp)
{
    //make sure that the node exists
    if (!temp)
    {

    }
    //do recursion until next is NULL
    else if (temp->next)
    {
        deleter(temp->next);
    }
    //free the node called
    free(temp);
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    int i = 0;
    //iterate through the hashtable to clear each bucket
    for (i = 0; i < N; i++)
    {
        //ensure the entry is not NULL
        if (hashtable[i])
        {
            //delete the linked list in the hashtable at i
            deleter(hashtable[i]);
        }

    }
    //if the for loop did not reach the end, then the function failed
    if (i != N)
    {
        return false;
    }
    return true;
}

