from config import root
import tkinter as tk
from tkinter import filedialog, Button
import sys
import webbrowser
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from logic import load, visualize

def upload_file():
    from buttons import method
    file_path = filedialog.askopenfilename()
    if file_path:
        G = load.load_graph(file_path)          # получаем граф
        print(method.get())
        positions = load.compute_layout(G, method=method.get())    # считаем позиции
        visualize.visualize_network(G, positions, output_path='network_viz.html')       # строим интерактивную схему
        webbrowser.open('./network_viz.html', new=0, autoraise=True)

def main_menu():
    from buttons import upload_file_btn, info_btn, sugiyama_btn, radial_btn, auto_btn
    text = tk.Text(
    root,
    state='disabled',          # только чтение
    bd=0,                      # нет внешней рамки
    highlightthickness=0,      # нет рамки фокуса
    wrap=tk.WORD,              # перенос по словам
    font=("Arial", 12)
    )

    sugiyama_btn.pack()
    radial_btn.pack()
    auto_btn.pack()

    text.pack(expand=True, fill='both', padx=10, pady=10)

    text.config(state='normal')
    text.insert('1.0', "Добро пожаловать в систему ОВКС!\nВыберите файл формата *.json, *.txt или *.csv\nЧтобы ознакомиться с допустимой структурой файлов, нажмите \"Справка\"")
    text.config(state='disabled')

    upload_file_btn.pack()
    info_btn.pack()

def go_back(current_win):
    current_win.destroy()
    root.deiconify()

def get_info():
    root.withdraw()
    info_win = tk.Toplevel(root)
    info_win.title("Справка")
    info_win.geometry("350x600")
    #info_win.resizable(False, False)

    text = tk.Text(
    info_win,
    state='disabled',          # только чтение
    bd=0,                      # нет внешней рамки
    highlightthickness=0,      # нет рамки фокуса
    wrap=tk.WORD,              # перенос по словам
    font=("Arial", 12)
    )

    text.pack(expand=True, fill='both', padx=10, pady=10)

    text.config(state='normal')
    text.insert('1.0', """
Кнопка "Загрузить файл" загружает описание топологии из файла.
Поддерживаемые форматы:
- txt: список связей между узлами (каждая строка: u v [вес])
- csv: матрица смежности (первая строка - заголовки узлов)
- json: список узлов и связей, например:
{"nodes": [id1, id2, ...], "edges": 
[[u, v, w], ...], "directed": true/false}
Поле directed в json определяет направленность или ненаправленность 
графа сети.                
""")
    text.config(state='disabled')
    back_btn = Button(info_win, text="Назад", fg = "black", command=lambda: go_back(info_win))
    back_btn.pack()