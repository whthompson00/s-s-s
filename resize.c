#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    //make sure 3 command line arguments were entered
    if (argc != 4)
    {
        printf("Usage: resize n infile outfile\n");
        return 1;
    }

    int n = atoi(argv[1]);

    //check that n is between 1 and 100
    if (n < 1 || n > 100)
    {
        printf("Usage: resize n infile outfile\n");
        return 1;
    }
    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    //open input file
    FILE *inptr = fopen(infile, "r");
    //check to make sure c was able to open the infile properly
    if (inptr == NULL)
    {
        printf("Usage: resize n infile outfile\n");
        return 1;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    //check to make sure c was able to open the outfile properly
    if (outptr == NULL)
    {
        fclose(inptr);
        printf("Usage: resize n infile outfile\n");
        return 1;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        printf("Unsupported file format.\n");
        return 1;
    }
    //track padding for the original bmp
    int paddingOriginal = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    //track padding for the new bmp
    int paddingNew = (4 - (bi.biWidth * n * sizeof(RGBTRIPLE)) % 4) % 4;

    //need to rewrite the header file for the new data
    //create a copy of the original data so the original is not manipulated
    BITMAPFILEHEADER bfCopy = bf;
    BITMAPINFOHEADER biCopy = bi;

    //change biSizeImage based on the changes to width, height, and padding
    biCopy.biSizeImage = sizeof(RGBTRIPLE) * (bi.biWidth * n) * (abs(bi.biHeight) * n) + (paddingNew * abs(bi.biHeight * n));
    //change width by n
    biCopy.biWidth = (bi.biWidth) * n;
    //change height by n
    biCopy.biHeight = (bi.biHeight) * n;
    //change bf size based on the new biSizeImage
    bfCopy.bfSize = biCopy.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    //write outfile's BITMAPFILEHEADER
    fwrite(&bfCopy, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&biCopy, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        //repeat the same code for n rows.
        for (int h = 0; h < n; h++)
        {
            // temporary storage
            RGBTRIPLE triple;
            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                //for loop to print the same pixel n times consecutively
                for (int k = 0; k < n; k++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            //add the padding for the new bmp after every line
            for (int k = 0; k < paddingNew; k++)
            {
                fputc(0x00, outptr);
            }

            //check to make sure not about to move to next row of original
            if (h != n - 1)
            {
                //send the position of the scanner back to th beginning of the row to rescan
                fseek(inptr, -bi.biWidth * sizeof(RGBTRIPLE), SEEK_CUR);
            }
        }
        // skip over padding in the original because moving to next row
        fseek(inptr, paddingOriginal, SEEK_CUR);
    }
    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}