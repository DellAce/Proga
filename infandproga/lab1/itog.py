cordinates = (0,0)
while True:
    print(Введите смещение в формате буква:цифра)
    try:
        tempsm=input().strip
        if "R" in tempsm:
            sm=tempsm.split(",")
            