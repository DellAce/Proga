def main():
    forbidden = set()

    print("Введите запретные зоны в формате 'X,Y,W,H' (пустая строка для окончания ввода):")
    while True:
        try:
            line = input().strip()
        except EOFError:
            break
        if not line:
            break

        try:
            parts = line.split(",")
            if len(parts) != 4:
                print("Неверный формат строки запретной зоны. Пропускаю строку.")
                continue

            X, Y, W, H = map(int, parts)

            for xx in range(X, X + W):
                for yy in range(Y, Y + H):
                    forbidden.add((xx, yy))
        except ValueError:
            print("Ошибка преобразования координат зоны. Пропускаю строку.")
            continue

    print("\nВведите высокоуровневые команды (R,L,U,D,B), например 'R,4' или 'B,2'.")
    print("Пустая строка - завершить ввод команд:")

    high_level_commands = []
    while True:
        try:
            line = input().strip()
        except EOFError:
            break
        if not line:
            break
        high_level_commands.append(line)

    direction_map = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}
    reverse_direction = {"R": "L", "L": "R", "U": "D", "D": "U"}

    current_x, current_y = 1, 1
    path = [(current_x, current_y)]
    command_history = []

    def execute_movement(dir_char, steps, x, y):
        dx, dy = direction_map[dir_char]
        for _ in range(steps):
            new_x = x + dx
            new_y = y + dy
            if not (1 <= new_x <= 100 and 1 <= new_y <= 100):
                print("Ошибка: выход за границы поля.")
                return None, None
            if (new_x, new_y) in forbidden:
                print("Ошибка: попытка зайти в запретную зону.")
                return None, None
            path.append((new_x, new_y))
            x, y = new_x, new_y
        return x, y

    def execute_back(n, x, y):
        nonlocal command_history
        non_b_commands = [cmd for cmd in command_history if cmd[0] != "B"]

        if n > len(non_b_commands):
            print("Ошибка: недостаточно команд для отмены.")
            return None, None

        # Команды для отката
        to_revert = non_b_commands[-n:][::-1]
        # Удаляем откатываемые команды из истории
        for cmd in to_revert:
            command_history.remove(cmd)

        for dir_char, steps in to_revert:
            rev_dir = reverse_direction[dir_char]
            x, y = execute_movement(rev_dir, steps, x, y)
            if x is None:
                return None, None
        return x, y

    for line in high_level_commands:
        parts = [p.strip() for p in line.split(",")]

        if len(parts) == 1:
            dir_char = parts[0].upper()
            if dir_char == "B":
                current_x, current_y = execute_back(1, current_x, current_y)
                if current_x is None:
                    return
                continue
            else:
                print(f"Ошибка: непонятная команда: {line}")
                continue

        elif len(parts) == 2:
            dir_char = parts[0].upper()
            try:
                steps = int(parts[1])
            except ValueError:
                print(f"Ошибка: вторым параметром должно быть число: {line}")
                continue

            if dir_char in direction_map:
                new_x, new_y = execute_movement(dir_char, steps, current_x, current_y)
                if new_x is None:
                    return
                current_x, current_y = new_x, new_y
                command_history.append((dir_char, steps))
            elif dir_char == "B":
                current_x, current_y = execute_back(steps, current_x, current_y)
                if current_x is None:
                    return
            else:
                print(f"Ошибка: неизвестная команда: {line}")
                continue
        else:
            print(f"Ошибка: неверный формат команды: {line}")
            continue

    print("\nИтоговая низкоуровневая программа (последовательность координат):")
    for x, y in path[1:]:
        print(f"{x},{y}")


if __name__ == "__main__":
    main()
