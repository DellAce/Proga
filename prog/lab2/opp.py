# Командный текстовый редактор с восстановленными проверками и читаемыми if-блоками


class TextEditor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.text = []
        self.history = []
        self.clipboard = ""
        self.modified = False

        try:
            with open(file_name, "r", encoding="utf-8") as f:
                self.text = f.read().splitlines()
        except FileNotFoundError:
            self.text = []

    def insert(self, text, row=None, col=None):
        if row is None:
            self.text.append(text)
        else:
            row = int(row)
            while len(self.text) <= row:
                self.text.append("")
            if col is None:
                self.text[row] += text
            else:
                col = int(col)
                line = self.text[row]
                if col > len(line):
                    line += " " * (col - len(line))
                self.text[row] = line[:col] + text + line[col:]
        self.modified = True

    def delete(self):
        self.text = []
        self.modified = True

    def delrow(self, row):
        row = int(row)
        if 1 <= row <= len(self.text):
            self.text.pop(row - 1)
            self.modified = True
        else:
            print("Ошибка: строка вне диапазона")

    def delcol(self, col):
        col = int(col)
        for i in range(len(self.text)):
            if col < len(self.text[i]):
                self.text[i] = self.text[i][:col] + self.text[i][col + 1 :]
        self.modified = True

    def swap(self, r1, r2):
        r1, r2 = int(r1) - 1, int(r2) - 1
        if 0 <= r1 < len(self.text) and 0 <= r2 < len(self.text):
            self.text[r1], self.text[r2] = self.text[r2], self.text[r1]
            self.modified = True
        else:
            print("Ошибка: строка вне диапазона")

    def show(self):
        for i, line in enumerate(self.text):
            print(f"{i+1:03}: {line}")

    def save(self):
        with open(self.file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(self.text))
        self.modified = False
        print("Сохранено.")

    def copy(self, row, start=None, end=None):
        row = int(row) - 1
        if 0 <= row < len(self.text):
            line = self.text[row]
            if start is None:
                self.clipboard = line
            else:
                start = int(start)
                if end is None:
                    self.clipboard = line[start:]
                else:
                    end = int(end)
                    self.clipboard = line[start:end]
        else:
            print("Ошибка: строка вне диапазона")

    def paste(self, row):
        row = int(row) - 1
        while len(self.text) <= row:
            self.text.append("")
        self.text[row] += self.clipboard
        self.modified = True

    def undo(self, steps=1):
        for _ in range(steps):
            if self.history:
                self.text = self.history.pop()
            else:
                print("Нечего отменять.")
                break

    def push_state(self):
        self.history.append(self.text[:])


class InsertCommand:
    def __init__(self, editor, text, row=None, col=None):
        self.editor = editor
        self.text = text
        self.row = row
        self.col = col

    def execute(self):
        self.editor.push_state()
        self.editor.insert(self.text, self.row, self.col)


class DeleteCommand:
    def __init__(self, editor):
        self.editor = editor

    def execute(self):
        self.editor.push_state()
        self.editor.delete()


class DelRowCommand:
    def __init__(self, editor, row):
        self.editor = editor
        self.row = row

    def execute(self):
        self.editor.push_state()
        self.editor.delrow(self.row)


class DelColCommand:
    def __init__(self, editor, col):
        self.editor = editor
        self.col = col

    def execute(self):
        self.editor.push_state()
        self.editor.delcol(self.col)


class SwapCommand:
    def __init__(self, editor, r1, r2):
        self.editor = editor
        self.r1 = r1
        self.r2 = r2

    def execute(self):
        self.editor.push_state()
        self.editor.swap(self.r1, self.r2)


class CopyCommand:
    def __init__(self, editor, row, start=None, end=None):
        self.editor = editor
        self.row = row
        self.start = start
        self.end = end

    def execute(self):
        self.editor.copy(self.row, self.start, self.end)


class PasteCommand:
    def __init__(self, editor, row):
        self.editor = editor
        self.row = row

    def execute(self):
        self.editor.push_state()
        self.editor.paste(self.row)


def main():
    import sys

    if len(sys.argv) < 2:
        print("Укажите путь к файлу")
        return

    file_name = sys.argv[1]
    editor = TextEditor(file_name)

    while True:
        command = input(">>> ").strip()
        if not command:
            continue

        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        try:
            if cmd == "insert":
                if not args:
                    print("Ошибка: не указан текст")
                    continue
                text = args[0].strip('"')
                row = None
                col = None
                if len(args) >= 2:
                    row = int(args[1])
                if len(args) == 3:
                    col = int(args[2])
                if len(args) > 3:
                    print("Ошибка: слишком много аргументов")
                    continue
                InsertCommand(editor, text, row, col).execute()

            elif cmd == "del":
                DeleteCommand(editor).execute()

            elif cmd == "delrow":
                if not args:
                    print("Ошибка: укажите номер строки")
                    continue
                DelRowCommand(editor, int(args[0])).execute()

            elif cmd == "delcol":
                if not args:
                    print("Ошибка: укажите номер столбца")
                    continue
                DelColCommand(editor, int(args[0])).execute()

            elif cmd == "swap":
                if len(args) != 2:
                    print("Ошибка: нужно указать две строки")
                    continue
                SwapCommand(editor, int(args[0]), int(args[1])).execute()

            elif cmd == "copy":
                if len(args) == 1:
                    CopyCommand(editor, int(args[0])).execute()
                elif len(args) == 2:
                    CopyCommand(editor, int(args[0]), int(args[1])).execute()
                elif len(args) == 3:
                    CopyCommand(
                        editor, int(args[0]), int(args[1]), int(args[2])
                    ).execute()
                else:
                    print("Ошибка: неправильное количество аргументов для copy")

            elif cmd == "paste":
                if not args:
                    print("Ошибка: укажите строку для вставки")
                    continue
                PasteCommand(editor, int(args[0])).execute()

            elif cmd == "undo":
                if len(args) > 1:
                    print("Ошибка: слишком много аргументов для undo")
                    continue
                steps = int(args[0]) if args else 1
                editor.undo(steps)

            elif cmd == "save":
                editor.save()

            elif cmd == "show":
                editor.show()

            elif cmd == "exit":
                if editor.modified:
                    answer = input("Сохранить изменения перед выходом? (y/n): ").lower()
                    if answer == "y":
                        editor.save()
                print("Выход.")
                break

            else:
                print("Неизвестная команда.")

        except ValueError:
            print("Ошибка: ожидается числовой аргумент")
        except Exception as e:
            print("Ошибка выполнения команды:", e)


if __name__ == "__main__":
    main()
