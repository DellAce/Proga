#include <stdio.h>
#include <stdlib.h>

int main()
{
    int eax = 5, ebx = 1; //  регистры
    while (eax != 0)      // пока не 0 продолжаем цикл
    {
        ebx = ebx * eax; // умножаем
        eax--;           // декремент
    }
    printf("ebx = %d\n", ebx); // принтф ebx
    return 0;
}