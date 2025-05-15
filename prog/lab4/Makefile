CC      = gcc
CFLAGS  = -Wall -Wextra -O2
PYTHON  = python3

# ----------------------------------------------------------------------
all: libprimes.so                         # «make» без целей → собрать .so

# Сборка разделяемой библиотеки
libprimes.so: lab4.c lab4.h
	$(CC) $(CFLAGS) -fPIC -shared -o $@ lab4.c

# Проверочный запуск (пример из задания)
run: libprimes.so lab4.py
	$(PYTHON) lab4.py 4 10

clean:
	$(RM) libprimes.so
.PHONY: all run clean
