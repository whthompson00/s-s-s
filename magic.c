#include <stdio.h>
#include <stdlib.h>


int checkJPEG(unsigned char input []);

int checkPDF(unsigned char input []);

int checkBMP(unsigned char input []);


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
        return 1;
    }

    //create temporary storage
    unsigned char temp [4];

    fread(&temp, 4, 1, file);


    if (checkJPEG(temp))
    {
        printf("JPEG\n");
    }
    else if (checkBMP(temp))
    {
        printf("BMP\n");
    }
    else if (checkPDF(temp))
    {
            printf("PDF\n");
    }
    else
    {
        printf("\n");
    }
    fclose(file);
}

int checkJPEG(unsigned char input [])
{
    if (input[0] == 0xff && input[1] == 0xd8 && input[2] == 0xff && (input[3] & 0xf0) == 0xe0)
    {
        return 1;
    }
    return 0;
}


int checkPDF(unsigned char input [])
{
    if (input[0] == 0x25 && input[1] == 0x50 && input[2] == 0x44 && input[3] == 0x46)
    {
        return 1;
    }
    return 0;
}

int checkBMP(unsigned char input [])
{
    if (input[0] == 0x42 && input[1] == 0x4d)
    {
        return 1;
    }
    return 0;
}
