coordinates = (1, 1)
zone = (0, 0, 0, 0)
path = []
check = False
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
    print("Введите смещение в формате R,3 / L,2 / D,1 / U,1 (пустая строка — выход):")
    try:
        temp_sm = input().strip()
        if not temp_sm:
            break

        sm = temp_sm.split(",")
        if len(sm) != 2:
            print("Неверный формат команды")
            continue

        smeshenie = sm[0].upper()
        steps = int(sm[1])

        for loop in range(steps):
            if smeshenie == "R":
                coordinates = (coordinates[0] + 1, coordinates[1])
            elif smeshenie == "L":
                coordinates = (coordinates[0] - 1, coordinates[1])
            elif smeshenie == "D":
                coordinates = (coordinates[0], coordinates[1] + 1)
            elif smeshenie == "U":
                coordinates = (coordinates[0], coordinates[1] - 1)
            else:
                print("Неверное направление, попробуйте R, L, U, D")
                break

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
        if check == True:
            break
    except:
        print("Ошибка ввода")
        continue
if check == False:
    print("Путь:")
    for step in path:
        print(f"{step[0]},{step[1]}")
