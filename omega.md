# Omega Directive

## Questions

6.1. In bubble sort, if the elements are already correctly ordered, then the program will simply compare all the elements to their neighboor once, giving it runtime n.  However, even if all the elements are correctly ordered, using selection sort, the algorithm needs to compare every digit to all the remaining numbers to ensure that number is in fact in the right spot.  Hence, the fastest runtime for selection sort is still n^2.

6.2. The big theta of merge sort is nlogn because the way the sort work is through recursion where the problem is split in two logn times.  And when reassembling the array after splitting it, n comparisons need to be made at each step, making big theta n*logn.

6.3. The implementation of strlen in C requires iterating through the whole string until the NULL charachter is reached which will necessarily run at big theta n.

6.4. Python could store the length of the list in some sort of table and then only have to look up the length of the list when len is called.  This could give constant runtime.

6.5. isupper will simply check if the char is between ascii values of 'A' and 'Z', inclusive.  Because isupper only requires two comparisons, the time to determine whether or not a char is capitalized is constant.

## Debrief

a. Looking up the documentation of the strlen and isupper program as well as looking up how python stores lists.

b. 25 minutes
