#!/bin/bash
# Вывод веденных переменных на экран
# Автор: Нажеев А
# Дата создания: 2025-05-26

read -p "Введите значение a: " a
read -p "Введите значение b: " b

# выводим на экран
echo "Значения:"
echo "  a = $a"
echo "  b = $b"

# пример использования declare
declare -i int_var
read -p "Введите число: " int_var
echo "int_var = $int_var"