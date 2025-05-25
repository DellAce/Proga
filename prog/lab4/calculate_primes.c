#include "calculate_primes.h"

void calculate_primes(int *primes, int n) {
    for (int i = 2; i <= n; i++) {
        *(primes + i) = 1;
    }

    *(primes + 0) = 0;
    *(primes + 1) = 0;

    for (int i = 2; i <= n; i++) {
        if (*(primes + i) == 0)
            continue;

        for (unsigned long j = i * i; j <= (unsigned long) n; j += i) {
            *(primes + j) = 0;
        }
    }
}
