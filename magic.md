# Like Magic

## Questions

4.1. BM

4.2. %PDF

4.3. When creating a file, magic numbers are merely a stylistic convention and not necessarily a rule.  As a result, some files might coincidentally begin with a sequence of magic numbers, even if that file is not of the same type as the magic numbers.  Hence, the presense of magic numbers will likely indicate the type of file but not necessarily indicate the type.

4.4. In binary, 0xf0 is equal to 11110000.  As a result, when proforming a bitwise AND with 0xf0, the last 4 digits will always be 0.  However, 0xe0 is 16 less than 0xf0. So in binary, 0xe0 is 11100000. And all 16 values which we need to check will all have a 0 in 2^4 place.  Hence, proforming a bitwise AND for 0fx0 and any of the correct values will always yield 11100000 or 0xe0.

4.5. In Zamayla's code, the computer only has to perform one operation and make one comparison.  In contrast, the original code has to make 16 different comparisons, making it much slower.  It also takes must less time to write.

4.6. See `magic.c`.

## Debrief

a. PSET 3

b. 30 minutes
