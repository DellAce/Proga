from sys import *


def delcol():
    pass  # адднуть


def delrow(file_name, row_number):
    file = open(file_name, "w+")
    lines = file.readlines()
    file.close()
    if row_number == None:
        print("Не указана строка для удаления")
        return False
    if row_number > len(lines) or row_number < 1:
        print("Вышли за пределы файла")
        return False
    lines.pop(row_number - 1)
    file = open(file_name, "w+")
    for line in lines:
        file.write(line)
    file.close()
    return True


def delete(file_name):
    file = open(file_name, "w")
    file.write("")
    file.close()


def show(file_name):
    file = open(file_name, "r")
    file_text = file.read()
    file.close()
    return file_text


def save(file_name, not_saved_text):
    file = open(file_name, "w+")
    file.write(not_saved_text)
    file.close()
    return True


def main():

    pass  # TODO: write your code here


if __name__ == "__main__":
    main()
