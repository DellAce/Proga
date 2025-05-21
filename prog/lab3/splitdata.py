def split_data(content, interval):
    intervals = []
    current_interval = []
    start_time = None
    prev_time = None

    for row in content:
        if not row:
            continue
        try:
            time = float(row[0])
            value = float(row[1])
            if start_time is None:
                start_time = time

            if time < start_time + interval:
                current_interval.append(value)
            else:
                intervals.append((start_time, prev_time, current_interval))
                start_time = time
                current_interval = [value]

            prev_time = time
        except ValueError:
            print(f"Ошибка преобразования строки в число: {row[0]}")
            continue

    if current_interval:
        intervals.append((start_time, prev_time, current_interval))

    return intervals
