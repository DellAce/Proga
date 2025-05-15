
#include "lab4.h"

void calculate_primes(int *primes, int n)
{

    for (int i = 0; i <= n; i++)
        primes[i] = 1;

    if (n >= 0)
        primes[0] = 0;
    if (n >= 1)
        primes[1] = 0;

    for (int p = 2; p * p <= n; p++)
        if (primes[p])
            for (int j = p * p; j <= n; j += p)
                primes[j] = 0;
}
