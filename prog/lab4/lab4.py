from ctypes import *
import sys

lib = CDLL("./libprimes.so")
lib.calculate_primes.argtypes = [POINTER(c_int), c_int]
lib.calculate_primes.restype = None


def main():
    if len(sys.argv) != 3:
        print("Usage: python lab4_1.py <start> <end>")
        return
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    if start < 4 or end < 4 or start > end or start % 2 != 0 or end % 2 != 0:
        print("Неверные аргументы, необходимо 2 четных числа >= 4 и старт < конец.")
        return
    n = end + 1
    ARRAY = c_int * (n)
    primes = ARRAY()
    for k in range(start, end + 1):
        lib.calculate_primes(primes, n)
        normas = []
        for i in range(2, k // 2 + 1):
            if primes[i] == 1 and primes[k - i] == 1:
                normas.append((i, k - i))
        count = len(normas)
        min_pair = normas[0] if normas else None
        print(f"{k} {count} {min_pair}")
