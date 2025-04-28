from sys import *


def delcol(text_buffer, col):
    col = int(col)
    for i in range(len(text_buffer)):
        if col < len(text_buffer[i]):
            text_buffer[i] = text_buffer[i][:col] + text_buffer[i][col + 1 :]
    return text_buffer


def delrow(text_buffer, row_number):
    row_number = int(row_number)
    if row_number < 1 or row_number > len(text_buffer):
        print("Ошибка: номер строки вне диапазона")
        return text_buffer
    text_buffer.pop(row_number - 1)
    return text_buffer


def delete(text_buffer):
    return []


def show(text_buffer):
    for i, line in enumerate(text_buffer):
        print(f"{i+1:03}: {line}")


def save(file_name, text_buffer):
    with open(file_name, "w") as file:
        file.write("\n".join(text_buffer))
    return False


def undo(history, text_buffer, num_operations=1):
    for loop in range(num_operations):
        if history:
            text_buffer = history.pop()
        else:
            print("Нечего больше отменять")
            break
    return text_buffer


def insert(text_buffer, text, row=None, col=None):
    if row is None:
        text_buffer.append(text)
    else:
        row = int(row)
        while len(text_buffer) <= row:
            text_buffer.append("")
        if col is None:
            text_buffer[row] += text
        else:
            col = int(col)
            line = text_buffer[row]
            if col > len(line):
                line += " " * (col - len(line))
            text_buffer[row] = line[:col] + text + line[col:]
    return text_buffer


def copy_line(text_buffer, row, start=None, end=None):
    row = int(row)
    if row < 1 or row > len(text_buffer):
        print("Ошибка: номер строки вне диапазона")
        return ""
    line = text_buffer[row - 1]
    if start is None:
        return line
    start = int(start)
    if end is None:
        return line[start:]
    end = int(end)
    return line[start:end]


def paste(text_buffer, clipboard, row):
    row = int(row)
    while len(text_buffer) < row:
        text_buffer.append("")
    text_buffer[row - 1] += clipboard
    return text_buffer


def main():
    if len(argv) < 2:
        print("Укажите путь к файлу")
        return

    file_name = argv[1]

    try:
        with open(file_name, "r") as f:
            text_buffer = f.read().splitlines()
    except FileNotFoundError:
        text_buffer = []

    history = []
    clipboard = ""
    modified = False

    while True:
        command = input(">>> ").strip()
        if not command:
            continue

        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd == "show":
            show(text_buffer)

        elif cmd == "insert":
            if not args:
                print("Ошибка: нет текста для вставки")
                continue
            history.append(text_buffer[:])
            text = args[0].strip('"')
            if len(args) == 1:
                row = None
                col = None
            elif len(args) == 2:
                row = int(args[1])
                col = None
            elif len(args) == 3:
                row = int(args[1])
                col = int(args[2])
            else:
                print("Ошибка: неверное количество аргументов")
                continue
            text_buffer = insert(text_buffer, text, row, col)
            modified = True

        elif cmd == "delrow":
            if not args:
                print("Ошибка: укажите номер строки")
                continue
            history.append(text_buffer[:])
            text_buffer = delrow(text_buffer, args[0])
            modified = True

        elif cmd == "delcol":
            if not args:
                print("Ошибка: укажите номер столбца")
                continue
            history.append(text_buffer[:])
            text_buffer = delcol(text_buffer, args[0])
            modified = True

        elif cmd == "del":
            history.append(text_buffer[:])
            text_buffer = delete(text_buffer)
            modified = True

        elif cmd == "copy":
            if not args:
                print("Ошибка: укажите строку для копирования")
                continue
            row = args[0]
            if len(args) == 1:
                start = None
                end = None
            elif len(args) == 2:
                start = args[1]
                end = None
            elif len(args) == 3:
                start = args[1]
                end = args[2]
            clipboard = copy_line(text_buffer, row, start, end)

        elif cmd == "paste":
            if not args:
                print("Ошибка: укажите строку для вставки")
                continue
            history.append(text_buffer[:])
            text_buffer = paste(text_buffer, clipboard, args[0])
            modified = True

        elif cmd == "swap":
            if len(args) < 2:
                print("Ошибка: укажите две строки для обмена")
                continue
            history.append(text_buffer[:])
            r1, r2 = int(args[0]) - 1, int(args[1]) - 1
            if 0 <= r1 < len(text_buffer) and 0 <= r2 < len(text_buffer):
                text_buffer[r1], text_buffer[r2] = text_buffer[r2], text_buffer[r1]
                modified = True
            else:
                print("Ошибка: строки вне диапазона")

        elif cmd == "undo":
            steps = int(args[0]) if args else 1
            text_buffer = undo(history, text_buffer, steps)
            modified = True

        elif cmd == "save":
            modified = save(file_name, text_buffer)

        elif cmd == "exit":
            if modified:
                choice = input(
                    "Есть несохраненные изменения. Сохранить? (y/n): "
                ).lower()
                if choice == "y":
                    modified = save(file_name, text_buffer)
            print("Выход.")
            break

        else:
            print("Неизвестная команда")


if __name__ == "__main__":
    main()
