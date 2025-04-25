# Командный текстовый редактор с использованием классов и undo

class TextEditor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.text = []  # основной текст, список строк
        self.history = []  # стек для undo
        self.clipboard = ""  # буфер обмена
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
                self.text[i] = self.text[i][:col] + self.text[i][col+1:]
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

    def undo(self):
        if self.history:
            self.text = self.history.pop()
            print("Undo выполнен.")
        else:
            print("Нечего отменять.")

    def push_state(self):
        self.history.append(self.text[:])  # сохраняем копию состояния


# Пример команды Insert в виде класса
class InsertCommand:
    def __init__(self, editor, text, row=None, col=None):
        self.editor = editor
        self.text = text
        self.row = row
        self.col = col

    def execute(self):
        self.editor.push_state()
        self.editor.insert(self.text, self.row, self.col)


# Команда удаления всего текста
class DeleteCommand:
    def __init__(self, editor):
        self.editor = editor

    def execute(self):
        self.editor.push_state()
        self.editor.delete()


# Команда удаления строки
class DelRowCommand:
    def __init__(self, editor, row):
        self.editor = editor
        self.row = row

    def execute(self):
        self.editor.push_state()
        self.editor.delrow(self.row)


def main():
    pass  # Здесь будет обработка ввода пользователя


if __name__ == "__main__":
    main()
