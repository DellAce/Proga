CC      = gcc
CFLAGS  = -Wall -Wextra -O2
PYTHON  = python3

all: libprimes.so

libprimes.so: calculate_primes.c calculate_primes.h
	$(CC) $(CFLAGS) -fPIC -shared -o $@ calculate_primes.c

run: libprimes.so lab4.py
	$(PYTHON) lab4.py 4 10

clean:
	$(RM) libprimes.so
.PHONY: all run clean
