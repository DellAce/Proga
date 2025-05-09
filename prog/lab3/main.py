import csv
import sys
from statistics import mean, median, mode
from splitdata import split_data


def read_data_from_file(filename):
    try:
        with open(filename, newline="") as csvfile:
            content = list(csv.reader(csvfile))
            return content
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)


def calculate_statistics(data):
    try:
        count = len(data)
        avg = mean(data)
        med = median(data)
        mod = mode(data)
        return count, avg, med, mod
    except Exception:
        print(f"Ошибка при вычислении статистики")
        return None


def main():
    if len(sys.argv) != 3:
        print("Использование: python main.py <файл> <интервал>")
        sys.exit(1)

    filename = sys.argv[1]
    interval = int(sys.argv[2])

    content = read_data_from_file(filename)
    intervals = split_data(content, interval)

    for start, end, values in intervals:
        count, avg, med, mod = calculate_statistics(values)
        print(
            f"Интервал {start} - {end}: Кол-во: {count}, Среднее: {avg}, Медиана: {med}, Мода: {mod}"
        )


if __name__ == "__main__":
    main()
