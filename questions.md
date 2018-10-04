# Questions

## What's `stdint.h`?

stdint.h is a header file which enables users to set the amount of memory which a data type uses.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

The point of using this statement create unsigned (if they have a u) or signed (if they have no u) integers with a specific size of exactly 8 bits or 32 bits.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

A 'BYTE' is one byte.  A 'DWORD' is four bytes.  A 'LONG' is 4 bytes.  A 'WORD' is 2 bytes.

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

The first two bytes of the file need correspond to the ascii value of 'BM'.  In decimal, this translates to 66 and 77.  In hexadecimal, this translates to 0x42 and 0x4d.

## What's the difference between `bfSize` and `biSize`?

bfSize is the size in bytes of the bitmap files.  It is equal to the biImageSize + biSize.  In contrast, biSize is the size in bytes of the structure being created, namely the header files.

## What does it mean if `biHeight` is negative?

If biHeight is negetive, the bit map is a top-down device independent bitmap and its origin is the upper-left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

The color depth or bits per pixel is specified in the biBitCount field.

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

fopen would return NULL in lines 24 or 32 if c is unable to properly open the file.

## Why is the third argument to `fread` always `1` in our code? (For example, see lines 40, 44, and 75.)

The third argument in fread is always 1 because the number of elements we are trying to read is always 1.

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

padding becomes 3 if 'bi.biWidth' is '3'.

## What does `fseek` do?

In general, fseek moves the position indicator of a file by a provided number of bytes specified.  

## What is `SEEK_CUR`?

'SEEK_CUR' is the current position position of the pointer file prior to the shift.
