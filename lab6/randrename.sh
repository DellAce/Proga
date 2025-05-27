#!/bin/bash
# Дата: 2025.05.27
# Автор: Нажеев А
# переименовываем случайный файл из заданного каталога

# переданы два параметра
if [ $# -ne 2 ]; then
  echo "Использование: $0 <каталог> <новое_имя_без_расширения>"
  exit 1
fi

dir="$1"
newbase="$2"

# каталог существует и не пусты
if [ ! -d "$dir" ]; then
  echo "Ошибка: каталог '$dir' не найден"
  exit 1
fi

# все файлы в массив
files=( "$dir"/* )
if [ ${#files[@]} -eq 0 ]; then
  echo "В каталоге нет файлов"
  exit 0
fi

rand_file="${files[RANDOM % ${#files[@]}]}"

# сохраняем расширение и формируем новое имя
ext="${rand_file##*.}"
newpath="$dir/$newbase.$ext"

mv -- "$rand_file" "$newpath" \
  && echo "Переименовал '$(basename "$rand_file")' → '$(basename "$newpath")'"
