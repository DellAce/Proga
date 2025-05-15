import sys
import ctypes

lib = ctypes.CDLL("./libprimes.so")
lib.calculate_primes.argtypes = (
    ctypes.POINTER(ctypes.c_int),  # int *primes
    ctypes.c_int,  # int n
)
lib.calculate_primes.restype = None


if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} L R", file=sys.stderr)
    sys.exit(1)

L, R = map(int, sys.argv[1:])
if L % 2 or R % 2 or L < 4 or R < L:
    raise ValueError("L и R должны быть чётными, L ≥ 4, L ≤ R")


N = R
Array = ctypes.c_int * (N + 1)
prime_flags = Array()

lib.calculate_primes(prime_flags, N)


def is_prime(num: int) -> bool:
    """Проверяем простоту через готовый индикатор"""
    return bool(prime_flags[num])


for n in range(L, R + 1, 2):
    count = 0
    first_a = first_b = None

    for a in range(2, n // 2 + 1):
        b = n - a
        if is_prime(a) and is_prime(b):
            count += 1
            if first_a is None:
                first_a, first_b = a, b

    print(n, count, first_a, first_b)
