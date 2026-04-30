import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "books.json")

def load_books():
    """Загружает список книг из файла JSON."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_books(books):
    """Сохраняет список книг в файл JSON."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(books, file, indent=2, ensure_ascii=False)
        print("Данные успешно сохранены.")
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные:\n{str(e)}")

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Трекер прочитанных книг")
        self.root.geometry("800x500")
        
        self.books = load_books()
        
        self.create_widgets()
        self.update_table() 

    def create_widgets(self):
        input_frame = tk.LabelFrame(self.root, text="Добавить новую книгу", padx=10, pady=10)
        input_frame.pack(pady=10, fill="x", padx=20)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="e", pady=2)
        self.title_entry = tk.Entry(input_frame, width=40)
        self.title_entry.grid(row=0, column=1, columnspan=3, sticky="w", pady=2)

        tk.Label(input_frame, text="Автор:").grid(row=1, column=0, sticky="e", pady=2)
        self.author_entry = tk.Entry(input_frame, width=40)
        self.author_entry.grid(row=1, column=1, columnspan=3, sticky="w", pady=2)

        tk.Label(input_frame, text="Жанр:").grid(row=2, column=0, sticky="e", pady=2)
        self.genre_entry = tk.Entry(input_frame, width=40)
        self.genre_entry.grid(row=2, column=1, sticky="w", pady=2)

        tk.Label(input_frame, text="Страниц:").grid(row=2, column=2, sticky="e", padx=(20,0), pady=2)
        self.pages_entry = tk.Entry(input_frame, width=10)
        self.pages_entry.grid(row=2, column=3, sticky="w", pady=2)

        add_btn = tk.Button(self.root, text="Добавить книгу", command=self.add_book)
        add_btn.pack(pady=5)

        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=10, fill="both", expand=True)

        self.columns = ("title", "author", "genre", "pages")
        self.tree = ttk.Treeview(table_frame, columns=self.columns, show="headings")
        
         self.tree.heading("title", text="Название")
         self.tree.heading("author", text="Автор")
         self.tree.heading("genre", text="Жанр")
         self.tree.heading("pages", text="Страниц")
         
         self.tree.column("title", width=250)
         self.tree.column("author", width=150)
         self.tree.column("genre", width=150)
         self.tree.column("pages", width=80, anchor="e")
         
         self.tree.pack(side="left", fill="both", expand=True)

         scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
         self.tree.configure(yscrollcommand=scrollbar.set)
         scrollbar.pack(side="right", fill="y")

         filter_frame = tk.Frame(self.root)
         filter_frame.pack(pady=5, fill="x", padx=20)

         tk.Label(filter_frame, text="Фильтр по жанру:").pack(side="left")
         self.Вот полный, структурированный и готовый к запуску код GUI-приложения **«Book Tracker»** на Python с использованием библиотеки Tkinter.
