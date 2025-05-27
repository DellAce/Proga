#!/bin/bash
# Дата: 2025.05.27
# Автор: Нажеев А
# переименовывем случайный файл

if [ $# -ne 2 ]; then
  echo "$0 <каталог> <новое_имя_без_расширения>"
  exit 1
fi

dir="$1"
newbase="$2"

if [ ! -d "$dir" ]; then
  echo "каталог '$dir' не найден"
  exit 1
fi

files=()
for f in "$dir"/.* "$dir"/*; do
  [ -f "$f" ] || continue
  name=${f##*/}
  [ "$name" = "." ] && continue  
  [ "$name" = ".." ] && continue 
  files+=( "$f" )
done

if [ ${#files[@]} -eq 0 ]; then
  echo "В каталоге нет файлов"
  exit 0
fi

rand_file="${files[RANDOM % ${#files[@]}]}"
filename="${rand_file##*/}"

if [[ "$filename" == ?*.* ]]; then
    ext="${filename##*.}"
else
    ext=""
fi

if [ -n "$ext" ]; then
  newname="$newbase.$ext"
else
  newname="$newbase"
fi

newpath="$dir/$newname"

mv -- "$rand_file" "$newpath" && echo "Переименовал '$filename' → '$(basename "$newpath")'" || echo "Ошибка при переименовании"
