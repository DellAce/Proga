coordinates = (1, 1)
zone = (0, 0, 0, 0)
path = []
check = False
history = []
reverse = {"R": "L", "L": "R", "U": "D", "D": "U"}

while True:
    print(
        "Введите координаты зоны в формате x,y,w,h (пустая строка для окончания ввода):"
    )
    try:
        coords_input = input().strip()
        if not coords_input:
            break
        zone = tuple(map(int, coords_input.split(",")))
        if len(zone) != 4:
            print("Ошибка формата, ожидалось 4 числа.")
            continue
    except:
        print("Ошибка ввода")
        continue

while True:
    print(
        "Введите смещение в формате R,3 / L,2 / D,1 / U,1 / B,1 (пустая строка — выход):"
    )
    try:
        temp_sm = input().strip()
        if not temp_sm:
            break

        sm = temp_sm.split(",")
        if len(sm) == 1 and sm[0].upper() == "B":
            steps_back = 1
        elif len(sm) == 2 and sm[0].upper() == "B":
            steps_back = int(sm[1])
        else:
            steps_back = False

        if steps_back is not False:
            for cmd in history:
                if cmd[0] != "B":
                    non_B_command = cmd
            if steps_back > len(non_B_command):
                print("Ошибка: недостаточно команд для отката.")
                check = True
                break

            for commands in reversed(non_B_command[-steps_back:]):
                cmd_dir = commands[0]
                cmd_steps = commands[1]
                rev_dir = reverse[cmd_dir]
                for loop in range(cmd_steps):
                    if rev_dir == "R":
                        coordinates = (coordinates[0] + 1, coordinates[1])
                    elif rev_dir == "L":
                        coordinates = (coordinates[0] - 1, coordinates[1])
                    elif rev_dir == "D":
                        coordinates = (coordinates[0], coordinates[1] + 1)
                    elif rev_dir == "U":
                        coordinates = (coordinates[0], coordinates[1] - 1)

                    if not (1 <= coordinates[0] <= 100 and 1 <= coordinates[1] <= 100):
                        print("Вы вышли за пределы поля")
                        check = True
                        break

                    if (zone[0] <= coordinates[0] < zone[0] + zone[2]) and (
                        zone[1] <= coordinates[1] < zone[1] + zone[3]
                    ):
                        print("Вы попали в запретную зону")
                        check = True
                        break

                    path.append(coordinates)
                if check:
                    break
            if check:
                break
            count = 0
            for i in range(len(history) - 1, -1, -1):
                if history[i][0] != "B":
                    count += 1
                    history.pop(i)
                    if count == steps_back:
                        break
            continue

        if len(sm) != 2:
            print("Неверный формат команды")
            continue

        dirrection = sm[0].upper()
        steps = int(sm[1])

        if dirrection not in ["R", "L", "U", "D"]:
            print("Неверное направление")
            continue

        for loop in range(steps):
            if dirrection == "R":
                coordinates = (coordinates[0] + 1, coordinates[1])
            elif dirrection == "L":
                coordinates = (coordinates[0] - 1, coordinates[1])
            elif dirrection == "D":
                coordinates = (coordinates[0], coordinates[1] + 1)
            elif dirrection == "U":
                coordinates = (coordinates[0], coordinates[1] - 1)

            if not (1 <= coordinates[0] <= 100 and 1 <= coordinates[1] <= 100):
                print("Вы вышли за пределы поля")
                check = True
                break

            if (zone[0] <= coordinates[0] < zone[0] + zone[2]) and (
                zone[1] <= coordinates[1] < zone[1] + zone[3]
            ):
                print("Вы попали в запретную зону")
                check = True
                break

            path.append(coordinates)

        if check:
            break
        history.append((dirrection, steps))
    except:
        print("Ошибка ввода")
        continue

if check == False:
    print("Путь:")
    for step in path:
        print(f"{step[0]},{step[1]}")
