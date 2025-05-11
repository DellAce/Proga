adr-mode: adr-mode.o
	ld -melf_i386 -o adr-mode adr-mode.o

adr-mode.o: adr-mode.S my-macro
	as -ahlsm=adr-mode.lst --32 -gstabs+ -o adr-mode.o adr-mode.S
