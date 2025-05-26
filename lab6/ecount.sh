#! bin/bash
#####
# Сценарий: Подсчет количества вхождений слова в файлы каталога
# Автор: Тимофей Рогозин
# Дата: 2025.05.20
#####

dir=${1}
word=${2}

if [ -z ${dir} ]
then
    echo "Номер каталога не указан"
else
    if [ -z ${word} ]
    then
        echo "Слово не указано"
    else
        ls -1 "${dir}/" | while read i 
        do
            echo ${i}: `grep -c ${word} "${dir}/${i}"`
        done
    fi
fi