def main():
    import sys

    # -------------------------
    # ШАГ 1. Считываем запретные зоны
    # -------------------------
    forbidden = set()  # множество (x, y), в которые входить нельзя

    print(
        "Введите запретные зоны в формате 'X,Y,W,H' (пустая строка для окончания ввода):"
    )
    while True:
        line = sys.stdin.readline().strip()
        if not line:
            # Пустая строка - выходим из цикла чтения зон
            break

        # Пытаемся распарсить X,Y,W,H
        try:
            parts = line.split(",")
            if len(parts) != 4:
                print("Неверный формат строки запретной зоны. Пропускаю строку.")
                continue

            x_str, y_str, w_str, h_str = parts
            X = int(x_str)
            Y = int(y_str)
            W = int(w_str)
            H = int(h_str)

            # Добавим все клетки зоны в forbidden
            # Зона: по X от X до X+W-1, по Y от Y до Y+H-1
            for xx in range(X, X + W):
                for yy in range(Y, Y + H):
                    forbidden.add((xx, yy))
        except ValueError:
            print(
                "Неверный формат (не удалось преобразовать в числа). Пропускаю строку."
            )
            continue

    # -------------------------
    # ШАГ 2. Считываем высокоуровневую программу
    # -------------------------
    print("\nВведите высокоуровневые команды (R,L,U,D,B), например 'R,4' или 'B,2'.")
    print("Пустая строка - завершить ввод команд:")

    high_level_commands = []
    while True:
        line = sys.stdin.readline().strip()
        if not line:
            break
        high_level_commands.append(line)

    # -------------------------
    # Подготовим вспомогательные структуры
    # -------------------------

    # Смещения для обычных команд
    direction_map = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, -1),
        "D": (0, 1),
    }

    # Обратное направление для отмены
    reverse_direction = {
        "R": "L",
        "L": "R",
        "U": "D",
        "D": "U",
    }

    # Текущая позиция робота
    current_x, current_y = 1, 1  # старт - верхний левый угол (1,1)

    # Полный путь (включая старт), чтобы потом выводить итоговую траекторию
    # Но при выводе мы пропустим самую первую точку (1,1)
    path = [(current_x, current_y)]

    # История НЕ-B команд: будем хранить здесь (dir, steps),
    # чтобы потом знать, какие команды "отменять" при B,n
    command_history = []  # сюда добавляем только R,L,U,D

    # Функция, которая выполняет "обычную" команду R,L,U,D
    # steps - сколько шагов
    # direction_char - один из R,L,U,D
    # current_x, current_y - текущие координаты робота
    # Возвращает (новые_x, новые_y) при успехе или None в случае ошибки
    def execute_movement(direction_char, steps, current_x, current_y):
        dx, dy = direction_map[direction_char]

        for _ in range(steps):
            new_x = current_x + dx
            new_y = current_y + dy

            # Проверяем границы
            if not (1 <= new_x <= 100 and 1 <= new_y <= 100):
                print("Ошибка: выходим за границы поля (1..100).")
                return None, None

            # Проверяем запретную зону
            if (new_x, new_y) in forbidden:
                print("Ошибка: попытка зайти в запретную зону.")
                return None, None

            # Если всё ок, добавляем в path и обновляем текущие координаты
            path.append((new_x, new_y))
            current_x, current_y = new_x, new_y

        return current_x, current_y

    # Функция, которая "отменяет" несколько последних НЕ-B команд
    # steps_count - сколько именно команд отменить
    # current_x, current_y - текущие координаты робота перед отменой
    # Возвращает (new_x, new_y) или None при ошибке
    def execute_back(steps_count, current_x, current_y):
        # Проверим, достаточно ли в истории команд
        if steps_count > len(command_history):
            print("Ошибка: пытаемся отменить больше команд, чем выполнено.")
            return None, None

        # Берём последние steps_count команд в обратном порядке
        to_revert = command_history[-steps_count:]  # последние команды
        to_revert.reverse()  # перевернём, чтобы отменять с конца

        # Теперь удалим их из истории, т.к. мы действительно их отменяем
        command_history[:] = command_history[:-steps_count]

        # Для каждой команды сделаем "обратное" перемещение
        for dir_char, stp in to_revert:
            # Найдём обратную команду
            rev_dir = reverse_direction[dir_char]
            # Выполним столько же шагов, но в обратном направлении
            nx, ny = execute_movement(rev_dir, stp, current_x, current_y)
            if nx is None:
                return None, None  # произошла ошибка
            current_x, current_y = nx, ny

        # Возвращаем окончательную позицию
        return current_x, current_y

    # -------------------------
    # ШАГ 3. Интерпретируем высокоуровневые команды
    # -------------------------

    for cmd_line in high_level_commands:
        parts = cmd_line.split(",")

        # Уберём лишние пробелы
        parts = [p.strip() for p in parts]

        # Если нет запятой, возможно это просто "B"
        if len(parts) == 1:
            dir_char = parts[0].upper()
            if dir_char == "B":
                steps_back = 1  # по умолчанию 1
                # Пробуем выполнить "отмену" 1 команды
                current_x, current_y = execute_back(steps_back, current_x, current_y)
                if current_x is None:
                    # Ошибка при отмене
                    return
            else:
                # Это ошибка формата
                print("Ошибка: непонятная команда:", cmd_line)
                return
        else:
            # Предположим, что первая часть - это направление (R,L,U,D,B)
            dir_char = parts[0].upper()

            # Проверим, есть ли число шагов
            try:
                steps_count = int(parts[1])
            except ValueError:
                print("Ошибка: вторым параметром должно быть число:", cmd_line)
                return

            if dir_char in ["R", "L", "U", "D"]:
                # Выполняем движение
                nx, ny = execute_movement(dir_char, steps_count, current_x, current_y)
                if nx is None:
                    # Ошибка, прекращаем
                    return
                # Добавляем команду в историю
                command_history.append((dir_char, steps_count))
                # Обновляем текущую позицию
                current_x, current_y = nx, ny
            elif dir_char == "B":
                # Отменяем steps_count последних НЕ-B команд
                nx, ny = execute_back(steps_count, current_x, current_y)
                if nx is None:
                    return
                current_x, current_y = nx, ny
            else:
                print("Ошибка: неизвестная команда:", cmd_line)
                return

    # -------------------------
    # ШАГ 4. Если дошли сюда без ошибок, выводим итоговую низкоуровневую программу
    # -------------------------
    # По условию выводим все позиции, кроме начальной (1,1).
    # path[0] = (1,1) – начальная, поэтому пропустим её и выведем с path[1:]

    print("\nИтоговая низкоуровневая программа (последовательность координат):")
    for i in range(1, len(path)):
        x, y = path[i]
        print(f"{x},{y}")


if __name__ == "__main__":
    main()
