import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# ------------------ Файл для сохранения данных ------------------
DATA_FILE = "trainings.json"

# ------------------ Класс приложения ------------------
class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner - План тренировок")
        self.root.geometry("750x500")
        self.root.resizable(False, False)

        # Данные: список словарей
        self.trainings = []
        self.load_data()

        # Создание интерфейса
        self.create_widgets()
        self.update_table()

    # ------------------ Загрузка / сохранение JSON ------------------
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.trainings = json.load(f)
            except:
                self.trainings = []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, indent=4, ensure_ascii=False)

    # ------------------ Создание элементов интерфейса ------------------
    def create_widgets(self):
        # Рамка для ввода данных
        input_frame = tk.LabelFrame(self.root, text="Добавить тренировку", padx=10, pady=10)
        input_frame.pack(pady=10, padx=10, fill="x")

        # Дата
        tk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = tk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))

        # Тип тренировки
        tk.Label(input_frame, text="Тип тренировки:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(input_frame, textvariable=self.type_var, values=["Бег", "Велосипед", "Плавание", "Силовая", "Йога"], width=12)
        self.type_combo.grid(row=0, column=3, padx=5, pady=5)
        self.type_combo.current(0)

        # Длительность
        tk.Label(input_frame, text="Длительность (мин):").grid(row=0, column=4, sticky="e", padx=5, pady=5)
        self.duration_entry = tk.Entry(input_frame, width=10)
        self.duration_entry.grid(row=0, column=5, padx=5, pady=5)

        # Кнопка добавления
        add_btn = tk.Button(input_frame, text="➕ Добавить тренировку", command=self.add_training, bg="#4CAF50", fg="white")
        add_btn.grid(row=0, column=6, padx=10, pady=5)

        # Рамка для фильтров
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(pady=5, padx=10, fill="x")

        tk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_type_var = tk.StringVar(value="Все")
        filter_type_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type_var, values=["Все", "Бег", "Велосипед", "Плавание", "Силовая", "Йога"], width=12)
        filter_type_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=0, column=2, padx=5, pady=5)
        self.filter_date_entry = tk.Entry(filter_frame, width=15)
        self.filter_date_entry.grid(row=0, column=3, padx=5, pady=5)

        filter_btn = tk.Button(filter_frame, text="🔍 Применить фильтр", command=self.update_table, bg="#2196F3", fg="white")
        filter_btn.grid(row=0, column=4, padx=10, pady=5)

        reset_btn = tk.Button(filter_frame, text="❌ Сбросить фильтры", command=self.reset_filters, bg="#FF9800", fg="white")
        reset_btn.grid(row=0, column=5, padx=5, pady=5)

        # Таблица (Treeview)
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("date", "type", "duration"), show="headings", height=12)
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность (мин)")
        self.tree.column("date", width=120, anchor="center")
        self.tree.column("type", width=150, anchor="center")
        self.tree.column("duration", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопка удаления выбранной записи
        del_btn = tk.Button(self.root, text="🗑 Удалить выбранную тренировку", command=self.delete_selected, bg="#f44336", fg="white")
        del_btn.pack(pady=5)

    # ------------------ Добавление тренировки с проверкой ------------------
    def add_training(self):
        date = self.date_entry.get().strip()
        train_type = self.type_var.get()
        duration = self.duration_entry.get().strip()

        # Проверка даты
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return

        # Проверка длительности
        if not duration:
            messagebox.showerror("Ошибка", "Введите длительность")
            return
        try:
            duration_val = float(duration)
            if duration_val <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
            return

        # Добавляем запись
        self.trainings.append({
            "date": date,
            "type": train_type,
            "duration": duration_val
        })
        self.save_data()
        self.update_table()

        # Очистка поля длительности
        self.duration_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", "Тренировка добавлена!")

    # ------------------ Обновление таблицы с учетом фильтров ------------------
    def update_table(self):
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Получаем фильтры
        filter_type = self.filter_type_var.get()
        filter_date = self.filter_date_entry.get().strip()

        # Фильтрация данных
        filtered = self.trainings
        if filter_type != "Все":
            filtered = [t for t in filtered if t["type"] == filter_type]
        if filter_date:
            try:
                datetime.strptime(filter_date, "%Y-%m-%d")
                filtered = [t for t in filtered if t["date"] == filter_date]
            except ValueError:
                # Если дата фильтра неверна — просто игнорируем фильтр по дате
                pass

        # Заполняем таблицу
        for t in filtered:
            self.tree.insert("", tk.END, values=(t["date"], t["type"], f"{t['duration']} мин"))

    # ------------------ Сброс фильтров ------------------
    def reset_filters(self):
        self.filter_type_var.set("Все")
        self.filter_date_entry.delete(0, tk.END)
        self.update_table()

    # ------------------ Удаление выбранной тренировки ------------------
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите тренировку для удаления")
            return

        # Получаем данные выбранной строки
        item = self.tree.item(selected[0])
        values = item["values"]
        if values:
            date, train_type, duration_str = values
            duration = float(duration_str.replace(" мин", ""))

            # Ищем и удаляем из списка
            for i, t in enumerate(self.trainings):
                if t["date"] == date and t["type"] == train_type and t["duration"] == duration:
                    del self.trainings[i]
                    break

            self.save_data()
            self.update_table()
            messagebox.showinfo("Успех", "Тренировка удалена")


# ------------------ Точка входа ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()