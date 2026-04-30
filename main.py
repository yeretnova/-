import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

# --- 1. НАСТРОЙКИ И ПЕРЕМЕННЫЕ ---
API_KEY = "YOUR_API_KEY_HERE" # <-- ВСТАВЬТЕ СЮДА СВОЙ КЛЮЧ С exchangerate-api.com
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

# Получаем путь к папке со скриптом для сохранения JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

# Список валют (можно расширить)
CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CNY", "RUB", "CHF"]

# --- 2. ФУНКЦИИ РАБОТЫ С ФАЙЛОМ ИСТОРИИ ---
def load_history():
    """Загружает историю из файла JSON."""
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_history(entry):
    """Сохраняет новую запись в файл JSON."""
    history = load_history()
    history.append(entry)
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=2, ensure_ascii=False)
        print("История успешно сохранена.")
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить историю:\n{str(e)}")

# --- 3. ФУНКЦИИ РАБОТЫ С API ---
def get_exchange_rate(base_currency, target_currency):
    """Запрашивает курс обмена у API."""
    try:
        response = requests.get(f"{BASE_URL}{base_currency}")
        response.raise_for_status() # Проверка на ошибки HTTP (404, 500 и т.д.)
        data = response.json()
        
        if data.get("result") == "error":
            raise Exception(data.get("error-type", "Неизвестная ошибка API"))
            
        rate = data["conversion_rates"].get(target_currency)
        if rate is None:
            raise Exception(f"Конвертация из {base_currency} в {target_currency} недоступна.")
        return rate
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка сети", f"Проверьте подключение к интернету.\n{str(e)}")
        return None

# --- 4. ОСНОВНАЯ ЛОГИКА ПРИЛОЖЕНИЯ ---
class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер валют")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        
        self.create_widgets()
        self.load_history_to_table() # Загружаем историю при запуске

    def create_widgets(self):
        # Рамка для элементов управления
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        # Валюта 'Из'
        tk.Label(control_frame, text="Из:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.from_currency_var = tk.StringVar(value="USD")
        self.from_currency_menu = ttk.Combobox(control_frame, 
                                               textvariable=self.from_currency_var,
                                               values=CURRENCIES,
                                               font=("Arial", 12),
                                               width=5,
                                               state="readonly")
        self.from_currency_menu.grid(row=0, column=1, padx=5)

        # Валюта 'В'
        tk.Label(control_frame, text="В:", font=("Arial", 12)).grid(row=0, column=2, padx=5)
        self.to_currency_var = tk.StringVar(value="EUR")
        self.to_currency_menu = ttk.Combobox(control_frame,
                                             textvariable=self.to_currency_var,
                                             values=CURRENCIES,
                                             font=("Arial", 12),
                                             width=5,
                                             state="readonly")
        self.to_currency_menu.grid(row=0, column=3, padx=5)

        # Поле ввода суммы
        tk.Label(control_frame, text="Сумма:", font=("Arial", 12)).grid(row=0, column=4, padx=5)
        self.amount_entry = tk.Entry(control_frame, font=("Arial", 12), width=15)
        self.amount_entry.grid(row=0, column=5, padx=5)
        
        # Кнопка конвертации
        self.convert_btn = tk.Button(self.root, 
                                     text="Конвертировать", 
                                     font=("Arial", 12, "bold"), 
                                     bg="#4CAF50", fg="white",
                                     command=self.on_convert_click)
        self.convert_btn.pack(pady=10)

        # Результат (скрыто до нажатия кнопки)
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14), fg="blue")
        
        # Таблица истории
        self.history_tree = ttk.Treeview(self.root, columns=("ID", "Из", "В", "Сумма", "Результат"), show="headings")
        
        self.history_tree.heading("ID", text="№")
        self.history_tree.heading("Из", text="Из")
        self.history_tree.heading("В", text="В")
        self.history_tree.heading("Сумма", text="Сумма")
        self.history_tree.heading("Результат", text="Результат")
        
        self.history_tree.column("ID", width=30)
        self.history_tree.column("Из", width=60)
        self.history_tree.column("В", width=60)
        
        self.history_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def on_convert_click(self):
        """Обработчик нажатия кнопки 'Конвертировать'."""
        
        # Очистка предыдущего результата
        self.result_label.pack_forget()
        
        # Получение данных из полей
        amount_str = self.amount_entry.get()
        
         # --- ВАЛИДАЦИЯ ВВОДА ---
        if not amount_str.replace('.', '', 1).isdigit(): # Проверка на число (допускаем точку)
            messagebox.showerror("Ошибка ввода", "Пожалуйста, введите корректное число.")
            return
            
        amount = float(amount_str)
        
         if amount <= 0:
            messagebox.showerror("Ошибка ввода", "Сумма должна быть больше нуля.")
            return

         from_cur = self.from_currency_var.get()
         to_cur = self.to_currency_var.get()
         
         if from_cur == to_cur:
            messagebox.showwarning("Внимание", "Выбраны одинаковые валюты.")
            return

         # --- ЗАПРОС К API ---
         rate = get_exchange_rate(from_cur, to_cur)
         
         if rate is None: # Если была ошибка сети или API вернуло None
             return

         result_amount = round(amount * rate, 2)
         
         # Отображение результата на экране
         result_text = f"{amount} {from_cur} = {result_amount} {to_cur}"
         self.result_label.config(text=result_text)
         self.result_label.pack(pady=10)
         
         # Сохранение в историю (в фоне)
         history_entry = {
             "from": from_cur,
             "to": to_cur,
             "amount": amount,
             "result": result_amount,
             "rate": rate,
             "timestamp": "now" # Можно добавить реальное время через datetime
         }
         save_history(history_entry)
         
         # Обновление таблицы на экране (добавляем только последнюю строку для наглядности)
         history_len = len(self.history_tree.get_children())
         self.history_tree.insert("", "end", values=(history_len + 1, from_cur, to_cur, amount, result_amount))


    def load_history_to_table(self):
        """Загружает всю историю из файла в таблицу при старте."""
        
         for record in load_history():
             history_len = len(self.history_tree.get_children())
             self.history_tree.insert("", "end", values=(history_len + 1,
                                                        record["from"],
                                                        record["to"],
                                                        record["amount"],
                                                        record["result"]))


# --- ЗАПУСК ПРИЛОЖЕНИЯ ---
if __name__ == "__main__":
    root_window = tk.Tk()
    app = CurrencyConverterApp(root_window)
    root_window.mainloop()