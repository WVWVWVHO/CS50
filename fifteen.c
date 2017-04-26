/**
 * fifteen.c
 *
 * Implements Game of Fifteen (generalized to d x d).
 *
 * Usage: fifteen d
 *
 * whereby the board's dimensions are to be d x d,
 * where d must be in [DIM_MIN,DIM_MAX]
 *
 * Note that usleep is obsolete, but it offers more granularity than
 * sleep and is simpler to use than nanosleep; `man usleep` for more.
 */
 
#define _XOPEN_SOURCE 500

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
//#include <math.h>

// constants
#define DIM_MIN 3
#define DIM_MAX 9

// board
int board[DIM_MAX][DIM_MAX];

// dimensions
int d;

// prototypes
void clear(void);
void greet(void);
void init(void);
void draw(void);
bool move(int tile);
bool won(void);

int main(int argc, string argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        printf("Usage: fifteen d\n");
        return 1;
    }

    // ensure valid dimensions
    d = atoi(argv[1]);
    if (d < DIM_MIN || d > DIM_MAX)
    {
        printf("Board must be between %i x %i and %i x %i, inclusive.\n",
            DIM_MIN, DIM_MIN, DIM_MAX, DIM_MAX);
        return 2;
    }

    // open log
    FILE *file = fopen("log.txt", "w");
    if (file == NULL)
    {
        return 3;
    }

    // greet user with instructions
    greet();

    // initialize the board
    init();

    // accept moves until game is won
    while (true)
    {
        // clear the screen
        clear();

        // draw the current state of the board
        draw();

        // log the current state of the board (for testing)
        for (int i = 0; i < d; i++)
        {
            for (int j = 0; j < d; j++)
            {
                fprintf(file, "%i", board[i][j]);
                if (j < d - 1)
                {
                    fprintf(file, "|");
                }
            }
            fprintf(file, "\n");
        }
        fflush(file);

        // check for win
        if (won())
        {
            printf("ftw!\n");
            break;
        }

        // prompt for move
        printf("Tile to move: ");
        int tile = get_int();
        
        // quit if user inputs 0 (for testing)
        if (tile == 0)
        {
            break;
        }

        // log move (for testing)
        fprintf(file, "%i\n", tile);
        fflush(file);

        // move if possible, else report illegality
        if (!move(tile))
        {
            printf("\nIllegal move.\n");
            usleep(300000);
        }

        // sleep thread for animation's sake
        usleep(300000);
    }
    
    // close log
    fclose(file);

    // success
    return 0;
}

/**
 * Clears screen using ANSI escape sequences.
 */
void clear(void)
{
    printf("\033[2J");
    printf("\033[%d;%dH", 0, 0);
}

/**
 * Greets player.
 */
void greet(void)
{
    clear();
    printf("WELCOME TO GAME OF FIFTEEN\n");
    usleep(500000);
}

/**
 * Initializes the game's board with tiles numbered 1 through d*d - 1
 * (i.e., fills 2D array with values but does not actually print them).  
 */
void init(void)
{
    int dd = d*d-1;
    for(int i=0; i<d; i++)
    {
        for(int ii=0; ii<d; ii++)
        {
            if(dd == 1)
            {
                board[i][ii] = dd;
                board[i][ii+1] = 0;
                break;
            }
            else if(dd>2 || d%2 != 0)
            {
                board[i][ii] = dd;
                dd--;
            }
            else
            {
                board[i][ii] = dd-1;
                board[i][ii+1] = dd;
                board[i][ii+2] = 0;
                break;
            }
        }
    }
    
    
    // TODO
}

/**
 * Prints the board in its current state.
 */
void draw(void)
{
    for(int q=0; q<d; q++)
    {
        for(int qq=0; qq<d; qq++)
        {
            if(board[q][qq]==48)
            {
                printf(" %i   ", board[q][qq]);
            }
            else
            {
                printf("%2i   ", board[q][qq]);
            }

        }
        printf("\n\n");
        
    }
    // TODO
}

/**
 * If tile borders empty space, moves tile and returns true, else
 * returns false. 
 */
bool move(int tile)
{
    int tile_loc[2];
    int empt_loc[2];

    for(int i=0; i<d; i++)
    {
        for(int ii=0; ii<d; ii++)
        {
            if(tile == board[i][ii])
            {
                tile_loc[0] = i; 
                tile_loc[1] = ii;
                break;
            }
        }
    }
    for(int i=0; i<d; i++)
    {
        for(int ii=0; ii<d; ii++)
        {
            if(0 == board[i][ii])
            {
                empt_loc[0] = i; 
                empt_loc[1] = ii;
                break;
            }
        }
    }    
    int r = abs(tile_loc[0] - empt_loc[0]);
    int rr = abs(tile_loc[1] - empt_loc[1]);
    //int rrr = r+rr;
    //printf("%i\n", r);
    //printf("%i\n", rr);
    //printf("%i\n", rrr);
    
    
    if((r+rr) < 2)
        {
        int temp_loc = board[empt_loc[0]][empt_loc[1]];
        board[empt_loc[0]][empt_loc[1]] = board[tile_loc[0]][tile_loc[1]];
        board[tile_loc[0]][tile_loc[1]] = temp_loc;
        
        return true;
        }
    return false;
}

/**
 * Returns true if game is won (i.e., board is in winning configuration), 
 * else false.
 */
bool won(void)
{
    int dd = 1;
    for(int i=0; i<d; i++)
    {
        for(int ii=0; ii<d; ii++)
        {
            if(ii==d-1 && i==d-1)
            {
                return true;
            }
            else if(board[i][ii] == dd)
            {
                dd++;
            }
            else
            {
                return false;
            }
        }
    }
    return false;
}