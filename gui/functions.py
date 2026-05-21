from config import root
import tkinter as tk
from tkinter import filedialog
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from logic import load, visualize

def upload_file():
    from buttons import method
    file_path = filedialog.askopenfilename()
    if file_path:
        G = load.load_graph(file_path)          # получаем граф
        positions = load.compute_layout(G, method=method)    # считаем позиции TODO: добавить логику выбора метода
        visualize.visualize_network(G, positions)       # строим интерактивную схему
        

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

def get_info():
    from buttons import back_btn
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
    text.insert('1.0', "Добро пожаловать в систему ОВКС!\nВыберите файл формата *.json, *.txt или *.csv\nЧтобы ознакомиться с допустимой структурой файлов, нажмите \"Справка\"")
    text.config(state='disabled')

    back_btn.pack()

def go_back(current_win):
    current_win.destroy()
    root.deiconify() 