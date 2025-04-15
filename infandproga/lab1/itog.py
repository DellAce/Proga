cordinates = (1,1)
while True:
    print(Введите смещение в формате буква:цифра)
    try:
        tempsm=input().strip
        if "R" in tempsm:
            sm=tempsm.split(",")
            cordinates=(cordinates[0]+int(sm[1]),cordinates[1])
        elif "L" in tempsm:
            sm=tempsm.split(",")
            cordinates=(cordinates[0]-int(sm[1]),cordinates[1])
        elif "U" in tempsm:
            sm=tempsm.split(",")
            cordinates=(cordinates[0],cordinates[1]+int(sm[1]))
        elif "D" in tempsm:
            sm=tempsm.split(",")
            cordinates=(cordinates[0],cordinates[1]-int(sm[1]))
        else:
            print("Неверный ввод")
            continue
        if cordinates[0]>100 or cordinates[1]>100 or cordinates[0]<1 or cordinates[1]<1:
            print("Вы вышли за пределы поля")
            break
        