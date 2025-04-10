#include <stdio.h>
#include <stdlib.h>

void main()
{
    int eax = 5, ebx = 1; // типо регистры
    while (eax != 0)      // пока не 0 продолжаем цикл
    {
        ebx = ebx * eax; // умножаем
        eax--;           // декремент
    }
    printf("ebx = %d\n", ebx); // принтф ebx
}