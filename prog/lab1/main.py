coordinates = (1, 1)
zone = []
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
        zone.append(tuple(map(int, coords_input.split(","))))
        for i in range(len(zone)):
            if len(zone[i]) != 4:
                print("Ошибка формата, ожидалось 4 числа.")
                continue
    except:
        print("Ошибка ввода(1)")
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
            non_B_command = []
            for cmd in history:
                if cmd[0] != "B":
                    non_B_command.append(cmd)
                    continue

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

                    path.append(coordinates)
                if check:
                    break
            if check:
                break
            count = 0
            for i in reversed(range(len(history))):
                if history[i][0] != "B":
                    count += 1
                    del history[i]
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

            path.append(coordinates)

        if check:
            break
        history.append((dirrection, steps))
    except:
        print("Ошибка ввода(2)")
        continue

for i in range(len(path)):
    coordinates = path[i]
    if not (1 <= coordinates[0] <= 100 and 1 <= coordinates[1] <= 100):
        print("Вы вышли за пределы поля")
        check = True
        break
for i in range(len(zone)):
    coordinates = path[i]
    if (zone[i][0] <= coordinates[0] < zone[i][0] + zone[i][2]) and (
        zone[i][1] <= coordinates[1] < zone[i][1] + zone[i][3]
    ):
        print("Вы попали в запретную зону")
        check = True
        break


if check == False:
    print("Путь:")
    for step in path:
        print(f"{step[0]},{step[1]}")
