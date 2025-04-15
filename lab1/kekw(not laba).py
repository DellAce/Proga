import tkinter as tk
from tkinter import messagebox, scrolledtext, Canvas

def create_app():
    window = tk.Tk()
    window.title("Робот-преобразователь")
    window.geometry("800x900")  # Увеличим высоту окна

    # === Ввод запретных зон ===
    tk.Label(window, text="Запретные зоны (X,Y,W,H):").pack()
    zones_text = scrolledtext.ScrolledText(window, height=5)
    zones_text.pack(fill="x", padx=10)

    # === Ввод команд ===
    tk.Label(window, text="Высокоуровневые команды (R,L,U,D,B):").pack()
    commands_text = scrolledtext.ScrolledText(window, height=8)
    commands_text.pack(fill="x", padx=10)

    # === Вывод результата ===
    tk.Label(window, text="Результат (низкоуровневая программа):").pack()
    result_text = scrolledtext.ScrolledText(window, height=10)
    result_text.pack(fill="both", padx=10, pady=5, expand=False)

    # === Кнопка выполнения ===
    tk.Button(window, text="Выполнить", command=lambda: execute_program()).pack(pady=10)

    # === Поле визуализации ===
    tk.Label(window, text="Визуализация пути робота:").pack()
    canvas = Canvas(window, width=500, height=500, bg="white")
    canvas.pack(pady=10)

    CELL_SIZE = 5

    def draw_path(path, forbidden):
        canvas.delete("all")
        for x, y in forbidden:
            canvas.create_rectangle((x - 1) * CELL_SIZE, (y - 1) * CELL_SIZE,
                                    x * CELL_SIZE, y * CELL_SIZE, fill="red")
        for i in range(1, len(path)):
            x1, y1 = path[i - 1]
            x2, y2 = path[i]
            canvas.create_line((x1 - 0.5) * CELL_SIZE, (y1 - 0.5) * CELL_SIZE,
                               (x2 - 0.5) * CELL_SIZE, (y2 - 0.5) * CELL_SIZE,
                               fill="blue", width=2)
        sx, sy = path[0]
        canvas.create_oval((sx - 0.5) * CELL_SIZE - 2, (sy - 0.5) * CELL_SIZE - 2,
                           (sx - 0.5) * CELL_SIZE + 2, (sy - 0.5) * CELL_SIZE + 2,
                           fill="green")
        ex, ey = path[-1]
        canvas.create_oval((ex - 0.5) * CELL_SIZE - 2, (ey - 0.5) * CELL_SIZE - 2,
                           (ex - 0.5) * CELL_SIZE + 2, (ey - 0.5) * CELL_SIZE + 2,
                           fill="orange")

    def parse_zones(text):
        forbidden = set()
        for line in text.strip().splitlines():
            if not line.strip():
                continue
            try:
                x, y, w, h = map(int, line.strip().split(","))
                for xx in range(x, x + w):
                    for yy in range(y, y + h):
                        forbidden.add((xx, yy))
            except:
                messagebox.showerror("Ошибка", f"Неверный формат зоны: {line}")
                return None
        return forbidden

    def execute_program():
        result_text.delete("1.0", tk.END)

        forbidden = parse_zones(zones_text.get("1.0", tk.END))
        if forbidden is None:
            return

        direction_map = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}
        reverse_direction = {"R": "L", "L": "R", "U": "D", "D": "U"}

        current_x, current_y = 1, 1
        path = [(current_x, current_y)]
        command_history = []

        def move(dir_char, steps, x, y):
            dx, dy = direction_map[dir_char]
            for _ in range(steps):
                new_x, new_y = x + dx, y + dy
                if not (1 <= new_x <= 100 and 1 <= new_y <= 100):
                    messagebox.showerror("Ошибка", "Выход за границы поля.")
                    return None, None
                if (new_x, new_y) in forbidden:
                    messagebox.showerror("Ошибка", "Попытка зайти в запретную зону.")
                    return None, None
                path.append((new_x, new_y))
                x, y = new_x, new_y
            return x, y

        def back(n, x, y):
            nonlocal command_history
            non_b_commands = [cmd for cmd in command_history if cmd[0] != "B"]
            if n > len(non_b_commands):
                messagebox.showerror("Ошибка", "Недостаточно команд для отмены.")
                return None, None
            to_revert = non_b_commands[-n:][::-1]
            for cmd in to_revert:
                command_history.remove(cmd)
            for dir_char, steps in to_revert:
                rev = reverse_direction[dir_char]
                x, y = move(rev, steps, x, y)
                if x is None:
                    return None, None
            return x, y

        for line in commands_text.get("1.0", tk.END).strip().splitlines():
            parts = [p.strip() for p in line.strip().split(",")]
            if not parts:
                continue

            if len(parts) == 1:
                if parts[0].upper() == "B":
                    current_x, current_y = back(1, current_x, current_y)
                    if current_x is None:
                        return
                else:
                    messagebox.showwarning("Ошибка", f"Непонятная команда: {line}")
                continue

            elif len(parts) == 2:
                dir_char = parts[0].upper()
                try:
                    steps = int(parts[1])
                except:
                    messagebox.showwarning("Ошибка", f"Неверное число в команде: {line}")
                    continue

                if dir_char in direction_map:
                    new_x, new_y = move(dir_char, steps, current_x, current_y)
                    if new_x is None:
                        return
                    current_x, current_y = new_x, new_y
                    command_history.append((dir_char, steps))
                elif dir_char == "B":
                    current_x, current_y = back(steps, current_x, current_y)
                    if current_x is None:
                        return
                else:
                    messagebox.showwarning("Ошибка", f"Неизвестная команда: {line}")
                    continue
            else:
                messagebox.showwarning("Ошибка", f"Неверный формат команды: {line}")
                continue

        for x, y in path[1:]:
            result_text.insert(tk.END, f"{x},{y}\n")

        draw_path(path, forbidden)

    window.mainloop()

if __name__ == "__main__":
    create_app()
