/*
 * Программа ввода кодов цифровых символов и вычисления суммы
 * одноцифровых чисел с проверкой переполнения.
 * 
 * Используется ввод из стандартного ввода (stdin).
 * Вывод суммы в десятичной системе.
 * 
 * Ассемблирование: as -ahlsm=task4.lst --32 -gstabs+ -o task4.o task4.S
 * Редактирование связей:  ld -melf_i386 -o task4-exe-S task4.o
 */

.include "my-macro"

.bss
    .lcomm summ, 2        # накопленная сумма (word)
    .lcomm c, 1           # однобайтовый буфер для Getchar
    .lcomm last, 1        # последний введённый символ
    .lcomm buffer, 12     # буфер для печати числа (макс 11 цифр + \0)

.data
    deff: .long 48         # константа '0' (для макросов)

.text
.global _start

_start:
    sub %esi, %esi       # очистка регистра esi для использования в качестве счетчика

show_prompt:
    Puts "Вводите цифру, друг мой!"     # макровызов вывода строки в stdout

kbd_input:
    Getchar $c             # ввод байта -> c,   EAX == 0 при EOF
    cmpl $0, %eax          # проверка на EOF
    je output_sum          # если EOF, переходим к выводу суммы

    cmpb $'\n', c          # проверка на перевод строки
    je last_in_eax          # если перевод строки, готовим последний символ
    cmpb $'9', c           # проверка на символ больше '9'
    ja print_err_msg        # если больше '9', выводим сообщение об ошибке
    cmpb $'0', c           # проверка на символ меньше '0'
    jb print_err_msg        # если меньше '0', выводим сообщение об ошибке

    movb c, %al            # перенос кода символа в AL
    movb %al, last         # сохранение последнего введенного символа

    Puts "Цифра! Хорошо."   # сообщение об успешном вводе цифры
    jmp show_prompt        # возврат к вводу

last_in_eax:
    xor %eax, %eax          # очистка регистра eax
    movb last, %al          # передача кода последнего символа в AL
    subb $48, %al           # преобразование символа в цифру

    xor %cx, %cx            # очистка регистра cx
    movb %al, %cl           # перенос цифры в CL
    movw summ, %ax          # получение текущей суммы
    addw %cx, %ax           # добавление цифры к сумме
    jc print_overflow_msg   # если переполнение, вывод сообщения
    movw %ax, summ          # обновление суммы
    jmp kbd_input           # возврат к вводу

print_overflow_msg:
    Puts "Сумма превышает допустимое значение."  # сообщение о переполнении
    jmp stop

print_err_msg:
    Puts "Не цифровая клавиша. Повторите ввод"  # сообщение об ошибке ввода
    jmp show_prompt

output_sum:
    xor %eax, %eax          # очистка регистра eax
    movw summ, %ax          # получение суммы в AX
    xor %ebx, %ebx          # сброс счетчика символов

print_digit:
    xor %edx, %edx          # сброс регистра edx
    movw $10, %cx           # делитель 10
    div %cx                 # деление AX на 10, остаток в DX
    add $48, %dl            # преобразование остатка в ASCII-код
    movb %dl, buffer(%ebx)  # запись цифры в буфер
    incl %ebx               # увеличение счетчика
    test %ax, %ax           # проверка на ноль
    jnz print_digit         # если не ноль, продолжаем деление

print_number:
    decl %ebx               # декремент счетчика символов
    cmp $0, %ebx            # проверка на конец вывода
    jl finish_output

    lea buffer(%ebx), %ecx  # получение адреса текущей цифры
    push %ebx               # сохранение счетчика
    movl $4, %eax           # sys_write
    movl $1, %ebx           # дескриптор stdout
    movl $1, %edx           # длина вывода 1
    int $0x80               # системный вызов

    pop %ebx                # восстановление счетчика
    jmp print_number        # печать следующей цифры

finish_output:
    movb $'\n', buffer     # перевод строки в буфер
    movl $4, %eax
    movl $1, %ebx
    lea buffer, %ecx
    movl $1, %edx
    int $0x80

stop:
    Exit $0

.end
