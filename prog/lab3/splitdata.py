def split_data(content, interval):
    intervals = []
    current_interval = []
    start_time = None

    for row in content:
        if not row:
            continue
        try:
            time = float(row[0])
            if start_time is None:
                start_time = time

            if time < start_time + interval:
                current_interval.append(float(row[1]))
            else:
                intervals.append((start_time, start_time + interval, current_interval))
                start_time = time
                current_interval = [float(row[1])]
        except ValueError:
            print(f"Ошибка преобразования строки в число: {row[0]}")
            continue

    if current_interval:
        intervals.append((start_time, start_time + interval, current_interval))

    return intervals
