# Song that Never Ends

## Questions

8.1. RecursionError: maximum recursion depth exceeded while calling a Python object

8.2. See `song.c`.

8.3. Segmentation fault

8.4. Everytime the sing function is called, more memory in the stack is used.  Thus, as sing is called recursively, eventually, the stack runs out of memory it can use, which causes a segmentation fault.

8.5. See `song.py`.

8.6. That function was recursive in that for every step, he found the middle of the remaining array.  Then he checked whether the middle came before or after the array.  Then depending on the answer, he threw away the half of the list which did not contain the array.  Then he repeated that process, until he found the name.

## Debrief

a. https://stackoverflow.com/questions/2964852/why-infinite-recursion-leads-to-seg-fault

b. 20 minutes
