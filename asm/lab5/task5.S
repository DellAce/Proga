
#  as -ahlsm=task5.lst --32 -gstabs+ -o task5.o task5.S
#   ld -melf_i386 -o task5-exe-S task5.o
.include "my-macro"
.bss
    .lcomm buf, 1       # буфер для одного байта
    .lcomm outbuf, 4    # буфер для вывода числа

.section .data
A:
        .long 1,2,3,4,5,6
        .long 7,8,9,10,11,12
        .long 13,14,15,16,17,18
        .long 19,20,21,22,23,24
        .long 25,26,27,28,29,30
        .long 31,32,33,34,35,36

k:  .byte 0              # первая цифра
l:  .byte 0              # вторая цифра

.section .text
.globl _start
_start:
        xor     %esi,%esi

read_loop:
        mov     $3,%eax              # sysread
        xor     %ebx,%ebx            # stdin
        mov     $buf,%ecx
        mov     $1,%edx
        int     $0x80
        test    %eax,%eax            # EOF / ошибка ждём дальше
        jle     read_loop

        xor     %eax,%eax
        movb    buf,%al              # al считанный символ
        cmp     $'0',%al             # меньше '0' ? = пропуск
        jb      read_loop
        cmp     $'5',%al             # больше '5' ? = пропуск
        ja      read_loop
        sub     $'0',%al             # al = 0‑5

        cmp     $0,%esi              # это первая цифра?
        je      store_k         # да, сохраняем её
        movb    %al,l            # вторая → l
        inc     %esi
        cmp     $2,%esi
        jl      read_loop            # ещё нет двух – заново
        jmp     compute
store_k:
        movb    %al,k            # первая → k
        inc     %esi
        jmp     read_loop

compute:
        xor     %esi,%esi            # i = 0

calc_loop:
        xor     %ebx,%ebx
        movb    k,%bl           # k в EBX
        xor     %edx,%edx
        movb    l,%dl        # l в EDX

        # A[k][i]
        mov     %ebx,%eax            # k
        imul    $24,%eax             # k * 24
        mov     %esi,%ecx            # i
        shl     $2,%ecx              # i * 4
        add     %ecx,%eax
        add     $A,%eax
        mov     (%eax),%eax          # EAX = A[k][i]

        # A[i][l]
        mov     %esi,%ecx
        imul    $24,%ecx             # i * 24
        mov     %edx,%edi            # l
        shl     $2,%edi              # l * 4
        add     %edi,%ecx
        add     $A,%ecx
        mov     (%ecx),%ecx          # ECX = A[i][l]

        add     %ecx,%eax            # сумма
        call    print_int            # печать

        inc     %esi                 # i++
        cmp     $6,%esi
        jl      calc_loop

        Finish

print_int:
        mov     $10,%ecx             # делитель
        xor     %edx,%edx
        div     %ecx                 # EAX = десятки, EDX = единицы

        mov     $outbuf,%edi
        cmp     $0,%eax
        jne     two_digits
        add     $'0',%dl             # одна цифра
        mov     %dl,(%edi)
        movb    $'\n',1(%edi)
        mov     $2,%edx              # len = 2
        jmp     write_out

two_digits: # подготовка двух цифр
        add     $'0',%al             # десятки
        add     $'0',%dl             # единицы
        mov     %al,(%edi)
        mov     %dl,1(%edi)
        movb    $'\n',2(%edi)
        mov     $3,%edx              # len = 3

write_out:
        mov     $4,%eax              # sys_write
        mov     $1,%ebx              # fd = 1 (stdout)
        mov     $outbuf,%ecx
        int     $0x80
        ret
