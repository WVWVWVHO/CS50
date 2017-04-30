#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./copy infile outfile\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[1];

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // make outptr NULL
    FILE *outptr = NULL;
    
    // make buffer space free
    typedef uint8_t BYTE;
    BYTE buffer[512];
    
    // make counting variable, to count the number of photo's collected
    int i = 0;

    // make buffer and store 512 bytes there
    while(fread(buffer, 512, 1, inptr)==1)
    {
        // is it the start of a JPEG?
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // check if there is an outfile, if there is one close it
            if(outptr != NULL) 
            {
                fclose(outptr);
            }

            // make new file with ascending file names
            char filename[8];
            sprintf(filename,"%.3d.jpg", i);
            outptr = fopen(filename, "w");
            if (outptr == NULL)
            {
                fclose(inptr);
                fprintf(stderr, "Could not create %s.\n", filename);
                return 3;
            }
            
            // write the first 512 bytes to the new file
            fwrite(buffer, 512, 1, outptr);
            i++;

        }
        
        // write the 512 bytes that were saved in the buffer in the output file if there is already a file, otherwise do nothing
        else if(i>0)
        {
        fwrite(buffer, 512, 1, outptr);
        }
        
    }
}