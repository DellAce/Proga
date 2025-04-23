import os
import sys


class TextEditor:
    def __init__(self, file_path):
        """
        Инициализация текстового редактора.
        Загружает содержимое файла, если он существует.
        """
        self.file_path = file_path
        self.content = []  # Содержимое файла
        self.clipboard = ""  # Буфер обмена
        self.history = []  # История изменений для отмены операций
        self.unsaved_changes = False  # Флаг наличия несохраненных изменений
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                self.content = file.readlines()

    def save(self):
        """
        Сохраняет текущее содержимое в файл.
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.writelines(self.content)
        self.unsaved_changes = False
        print("Файл сохранен.")

    def show(self):
        """
        Выводит текущее содержимое файла с номерами строк.
        """
        for i, line in enumerate(self.content, start=1):
            print(f"{i}: {line}", end="")

    def insert(self, text, num_row=None, num_col=None):
        """
        Вставляет текст в файл.
        Если не указаны строка и столбец, вставляет в конец файла.
        """
        if num_row is None:
            self.content.append(text + "\n")
        else:
            num_row -= 1
            if num_row >= len(self.content):
                self.content.extend(["\n"] * (num_row - len(self.content) + 1))
            if num_col is None:
                self.content[num_row] = self.content[num_row].rstrip("\n") + text + "\n"
            else:
                num_col -= 1
                line = self.content[num_row].rstrip("\n")
                self.content[num_row] = line[:num_col] + text + line[num_col:] + "\n"
        self.unsaved_changes = True
        self.history.append(("insert", text, num_row, num_col))

    def delete(self):
        """
        Удаляет все содержимое файла.
        """
        self.history.append(("delete", self.content.copy()))
        self.content = []
        self.unsaved_changes = True

    def delete_row(self, num_row):
        """
        Удаляет указанную строку.
        Если номер строки некорректен, выводит сообщение об ошибке.
        """
        if num_row is None or num_row < 1 or num_row > len(self.content):
            print("Ошибка: номер строки не указан или некорректен.")
            return
        self.history.append(("delete_row", num_row, self.content[num_row - 1]))
        del self.content[num_row - 1]
        self.unsaved_changes = True

    def delete_col(self, num_col):
        """
        Удаляет указанный столбец текста из всех строк.
        Если номер столбца некорректен, выводит сообщение об ошибке.
        """
        if num_col is None or num_col < 1:
            print("Ошибка: номер столбца не указан или некорректен.")
            return
        self.history.append(("delete_col", num_col, self.content.copy()))
        num_col -= 1
        for i in range(len(self.content)):
            line = self.content[i].rstrip("\n")
            if num_col < len(line):
                self.content[i] = line[:num_col] + line[num_col + 1 :] + "\n"
        self.unsaved_changes = True

    def swap(self, num_row_1, num_row_2):
        """
        Меняет местами две строки.
        Если номера строк некорректны, выводит сообщение об ошибке.
        """
        if (
            num_row_1 is None
            or num_row_2 is None
            or num_row_1 < 1
            or num_row_2 < 1
            or num_row_1 > len(self.content)
            or num_row_2 > len(self.content)
        ):
            print("Ошибка: номера строк не указаны или некорректны.")
            return
        self.history.append(("swap", num_row_1, num_row_2))
        self.content[num_row_1 - 1], self.content[num_row_2 - 1] = (
            self.content[num_row_2 - 1],
            self.content[num_row_1 - 1],
        )
        self.unsaved_changes = True

    def undo(self, num_operations=1):
        """
        Отменяет последние операции.
        Если не указано количество операций, отменяет последнюю.
        """
        for _ in range(num_operations):
            if not self.history:
                print("Нет операций для отмены.")
                return
            operation = self.history.pop()
            if operation[0] == "insert":
                _, text, num_row, num_col = operation
                if num_row is None:
                    self.content.pop()
                else:
                    num_row -= 1
                    if num_col is None:
                        self.content[num_row] = self.content[num_row].replace(
                            text + "\n", ""
                        )
                    else:
                        num_col -= 1
                        line = self.content[num_row]
                        self.content[num_row] = (
                            line[:num_col] + line[num_col + len(text) :]
                        )
            elif operation[0] == "delete":
                self.content = operation[1]
            elif operation[0] == "delete_row":
                _, num_row, line = operation
                self.content.insert(num_row - 1, line)
            elif operation[0] == "delete_col":
                self.content = operation[2]
            elif operation[0] == "swap":
                _, num_row_1, num_row_2 = operation
                self.content[num_row_1 - 1], self.content[num_row_2 - 1] = (
                    self.content[num_row_2 - 1],
                    self.content[num_row_1 - 1],
                )
        self.unsaved_changes = True

    def copy(self, num_row, start=None, end=None):
        """
        Копирует текст из указанной строки в буфер обмена.
        Можно указать диапазон символов для копирования.
        """
        if num_row < 1 or num_row > len(self.content):
            print("Ошибка: номер строки некорректен.")
            return
        line = self.content[num_row - 1].rstrip("\n")
        if start is None:
            self.clipboard = line
        elif end is None:
            self.clipboard = line[start - 1 :]
        else:
            self.clipboard = line[start - 1 : end]

    def paste(self, num_row):
        """
        Вставляет текст из буфера обмена в указанную строку.
        """
        if num_row < 1 or num_row > len(self.content):
            print("Ошибка: номер строки некорректен.")
            return
        self.insert(self.clipboard, num_row)

    def exit(self):
        """
        Завершает работу редактора.
        Если есть несохраненные изменения, предлагает сохранить их.
        """
        if self.unsaved_changes:
            choice = (
                input("Есть несохраненные изменения. Сохранить? (y/n): ")
                .strip()
                .lower()
            )
            if choice == "y":
                self.save()
        print("Выход из редактора.")
        sys.exit()


def main():
    """
    Основная функция программы.
    Обрабатывает команды пользователя и вызывает соответствующие методы.
    """
    if len(sys.argv) < 2:
        print("Ошибка: укажите путь к файлу.")
        return

    file_path = sys.argv[1]
    editor = TextEditor(file_path)

    while True:
        command = input("Введите команду: ").strip().split()
        if not command:
            continue

        cmd = command[0].lower()
        args = command[1:]

        if cmd == "insert":
            text = args[0]
            num_row = int(args[1]) if len(args) > 1 else None
            num_col = int(args[2]) if len(args) > 2 else None
            editor.insert(text.strip('"'), num_row, num_col)
        elif cmd == "del":
            editor.delete()
        elif cmd == "delrow":
            num_row = int(args[0]) if args else None
            editor.delete_row(num_row)
        elif cmd == "delcol":
            num_col = int(args[0]) if args else None
            editor.delete_col(num_col)
        elif cmd == "swap":
            if len(args) < 2:
                print("Ошибка: укажите номера строк для обмена.")
                continue
            num_row_1 = int(args[0])
            num_row_2 = int(args[1])
            editor.swap(num_row_1, num_row_2)
        elif cmd == "undo":
            num_operations = int(args[0]) if args else 1
            editor.undo(num_operations)
        elif cmd == "copy":
            num_row = int(args[0])
            start = int(args[1]) if len(args) > 1 else None
            end = int(args[2]) if len(args) > 2 else None
            editor.copy(num_row, start, end)
        elif cmd == "paste":
            num_row = int(args[0])
            editor.paste(num_row)
        elif cmd == "save":
            editor.save()
        elif cmd == "show":
            editor.show()
        elif cmd == "exit":
            editor.exit()
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
