#include <stdio.h>
#include <stdlib.h>

void sing(void);

int main(void)
{
    sing();
}

void sing(void)
{
    printf("This is the song that doesn't end.");
    printf("Yes, it goes on and on my friend.");
    printf("Some people started singing it not knowing what it was,");
    printf("And they'll continue singing it forever just because...");
    sing();
}