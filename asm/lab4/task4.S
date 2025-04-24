# из dt over

/*
 * Программа ввода кодов цифровых символов в буфер в ОП
 */

.include "my-macro"

.bss
    .lcomm summ, 2 # 2 байта для хранения суммы
    .lcomm buf, 100 # 100 байтовый буфер для кодов прочитанных символов
    .lcomm c, 1    # однобайтовый буфер для чтения байта из файла stdin
    .lcomm outbuf, 16  # буфер для десятичного представления суммы

.data
deff: .long 48
ten:  .long 10
.text
.global _start

_start:
    sub    %esi, %esi     # указатель адреса байта в буфере buf (индексный регистр)

show_prompt:
    Puts "Вводите цифру, друг мой!"     # макровызов вывода строки в stdout

kbd_input:
    Getchar $c          # макровызов ввода байта из stdin в c

    cmpl $0, %eax     # EOF?
    je print_sum      # Да — выводим сумму

    cmpb $'\n', c
    je kbd_input
    cmpb $'9', c
    ja print_err_msg
    cmpb $'0', c
    jb print_err_msg
    
    movb c, %al
    subb deff, %al
    xor %ah, %ah
    addw summ, %ax
    jc print_overflow_msg
    movw %ax, summ
    jmp show_prompt

print_overflow_msg:
    Puts "Слишком большая сумма! Переполнение."
    jmp stop

print_sum:
    movl $0, %ebx       # счётчик цифр
    movl summ, %eax     # загрузили сумму

.nextdigit:
    movl $0, %edx
    idivl ten        # делим на 10
    addb $'0', %dl      # преобразуем цифру в не цифру


    jmp stop

print_err_msg:
    Puts "Не цифровая клавиша. Повторите ввод"
    jmp show_prompt

stop:
    Exit $0

.end