# СДЕЛАТЬ ПРОВЕРКУ НА 65 536 БУКВАЛЬНО

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
    Puts "Вводите цифру, друг мой!"     # макровызов вывода строки в
                    # файл stdout (подсказка ввода)

kbd_input:
    Getchar $c          # макровызов ввода байта из stdin в
            # промежуточный буфер c

    cmpl $0, %eax     # наступило событие EOF (конец файла stdin) ?
    je print_sum      # Да - выводим сумму

    cmpb $'\n', c     # это символ перевода строки ?
    je kbd_input     # ДА - на ввод следующего символа
    cmpb $'9', c      # код больше кода символа '9' ?
    ja print_err_msg    # ДА - на вывод сообщения об ошибке
    cmpb $'0', c    # код меньше кода символа '0' ?
    jb print_err_msg    # ДА - на вывод сообщения об ошибке

    movb c, %al         # загружаем символ из c
    subb $48, %al       # преобразуем в цифру (ASCII - '0')
    xor %ah, %ah        # обнуляем старшие 8 бит
    addw summ, %ax      # прибавляем к текущей сумме
    movw %ax, summ      # сохраняем обратно


    jmp show_prompt    # на ввод следующего символа

print_sum:
    xor %eax, %eax
    movw summ, %eax        # загружаем сумму в eax
    lea outbuf + 16, %edi    # edi — указатель на конец буфера
    mov $0, %ecx             # счётчик цифр

.print_loop:
    movl $0, %edx            # обнуляем edx (старшая часть делимого)
    idivl ten                 # делим edx:eax на 10
    addb $'0', %dl           # остаток -> ASCII символ
    decl %edi
    movb %dl, (%edi)         # сохраняем символ в буфер
    incl %ecx                # увеличиваем длину строки
    test %eax, %eax
    jnz .print_loop

    # write
    movl $4, %eax
    movl $1, %ebx
    movl %edi, %ecx
    movl %ecx, %edx
    int $0x80

    jmp stop

print_err_msg:
    Puts "Не цифровая клавиша. Повторите ввод"    # вывод сообщения об ошибке
    jmp show_prompt     # на ввод следующего символа

stop:
    Exit $0

.end
