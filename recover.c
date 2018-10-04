#include <stdio.h>
#include <stdlib.h>


int checkJPEG(unsigned char input []);

int main(int argc, char *argv[])
{
    //make sure user enter one command line argument
    if (argc != 2)
    {
        printf("Usage: ./recover image");
        return 1;
    }

    //open input file
    FILE *file = fopen(argv[1], "r");

    //check to make sure c was able to open the infile properly
    if (file == NULL)
    {
        printf("Usage: ./recover image");
        return 2;
    }
    //counter will track the number
    int counter = 0;
    //filename stores the name of the jpeg. 8 because each name has 3 numbers, '.', jpg, and the null charachter
    char filename [8];
    //test whether or not a JPEG has been found yet or not
    int JPEG = 1;
    FILE *image;

    //create temporary storage
    unsigned char temp [512];

    //iterates through the whole input file until there are less than 512 BYTES left, meaning no more JPEGs
    while (fread(&temp, 512, 1, file))
    {
        //checks if a JPEG has been found yet
        if (JPEG)
        {
            //checks if the first 4 BYTEs match aJPEG
            if (checkJPEG(temp))
            {
                //create a string which will hold the content of image
                sprintf(filename, "%03i.jpg", counter);
                //increment the number of JPEGs found by 1
                counter ++;
                //stores image at the buffer at filename
                image = fopen(filename, "w");
                //write the first block of 512 BYTEs into image
                fwrite(&temp, 512, 1, image);
                //change JPEG because a JPEG has been found
                JPEG = 0;
            }
        }
        else
        {
            //checks if the first 4 BYTEs match aJPEG
            if (checkJPEG(temp))
            {
                //close the previous image
                fclose(image);
                //create the next string which will hold the content of next image
                sprintf(filename, "%03i.jpg", counter);
                //increment the number of JPEGs found by 1
                counter ++;
                //stores image at the buffer at filename
                image = fopen(filename, "w");
                //write the first block of 512 BYTEs into image
                fwrite(&temp, 512, 1, image);
            }
            //still in the same JPEG as before
            else
            {
                //write in the next 512 BYTEs of the JPEG into image
                fwrite(&temp, 512, 1, image);
            }
        }
    }
    fclose(image);
}

int checkJPEG(unsigned char input [])
{
    if (input[0] == 0xff && input[1] == 0xd8 && input[2] == 0xff && (input[3] & 0xf0) == 0xe0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}
