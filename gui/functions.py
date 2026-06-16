from config import root
import tkinter as tk
from tkinter import filedialog, Button
import sys
import webbrowser
from tkinter import messagebox
from json import JSONDecodeError
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from logic import load, visualize
import os 

def upload_file():
    from buttons import method
    
    file_path = filedialog.askopenfilename(filetypes=(
        ("Исходный файл JSON", "*.json"),
        ("Текстовый документ", "*.txt"),
        ("Excel.CSV", "*.csv")
    ))
    if file_path:
        try:
            G = load.load_graph(file_path)          # получаем граф
            print(method.get())
            positions = load.compute_layout(G, method=method.get())    # считаем позиции
            visualize.visualize_network(G, positions, output_path='network_viz.html')       # строим интерактивную схему

        except JSONDecodeError:
            messagebox.showerror("Ошибка", "Ошибка структуры JSON!")
            return

        except ValueError:
            messagebox.showerror("Ошибка", "Ошибка! Не поддерживаемый тип файла!")
            return

        except KeyError as e:
            messagebox.showerror("Ошибка", f"Ошибка структуры файла!\nНе найдено поле {e}")
            return    
           
        if sys.platform.startswith('win'):
            html_path = ''
            current_file_path = os.path.abspath(__file__).split('\\')
            for i in range(len(current_file_path) - 2):
                html_path += f'{current_file_path[i]}\\'
            html_path += 'network_viz.html'    
            webbrowser.open(html_path, new=0, autoraise=True)
        else:    
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
    text.insert('1.0', "Добро пожаловать в систему ССКС!\nВыберите файл формата *.json, *.txt или *.csv\nЧтобы ознакомиться с допустимой структурой файлов, нажмите \"Справка\"")
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
    text.insert('1.0', 
    "СПРАВКА ПО ИСПОЛЬЗОВАНИЮ ПРОГРАММЫ «ССКС»\n\n"
    "1. ЧТО ДЕЛАЕТ ПРОГРАММА?\n"
    "   Программа автоматически строит наглядную схему компьютерной сети по её описанию.\n"
    "   Схема создаётся в виде интерактивной HTML‑страницы, которую можно открыть в браузере, "
    "масштабировать и перемещать.\n\n"
    "2. КАКИЕ ФАЙЛЫ МОЖНО ЗАГРУЖАТЬ?\n"
    "   • JSON (.json) — рекомендуемый формат (см. образец ниже).\n"
    "   • Текстовый список рёбер (.txt) — каждая строка: узел1 узел2 [вес]\n"
    "   • Матрица смежности (.csv или .txt с числами)\n\n"
    "3. СТРУКТУРА JSON‑ФАЙЛА\n"
    '   {\n'
    '     "nodes": [\n'
    '       {"id": "Router1", "type": "router"},\n'
    '       {"id": "PC1", "type": "pc"}\n'
    '     ],\n'
    '     "edges": [\n'
    '       ["Router1", "PC1"]\n'
    '     ],\n'
    '     "directed": false\n'
    '   }\n\n'
    "   Поле \"directed\" необязательно (по умолчанию false).\n"
    "   Поле \"type\" задаёт иконку устройства. Если не указано, используется стандартный значок.\n\n"
    "4. ДОСТУПНЫЕ ТИПЫ УСТРОЙСТВ (для иконок):\n"
    "   • router       — маршрутизатор\n"
    "   • switch       — коммутатор\n"
    "   • hub          — концентратор\n"
    "   • firewall     — межсетевой экран\n"
    "   • pc           — компьютер\n"
    "   • laptop       — ноутбук\n"
    "   • server       — сервер\n"
    "   • printer      — принтер\n"
    "   • ip_phone     — IP‑телефон\n"
    "   • analog_phone — аналоговый телефон\n"
    "   • smartphone   — смартфон\n"
    "   • access_point — точка доступа Wi‑Fi\n"
    "   • repeater     — репитер\n"
    "   • modem        — модем\n"
    "   • cloud        — облачный сервис\n"
    "   • bridge       — мост\n"
    "   • home_gateway — домашний шлюз\n"
    "   • lan_controller — контроллер локальной сети\n"
    "   • multilayer_switch — многоуровневый коммутатор\n"
    "   • cell_tower   — сотовая вышка\n"
    "   • coax_splitter — коаксиальный разветвитель\n"
    "   • co_server    — сервер центрального офиса\n\n"
    "5. КАК РАБОТАТЬ С ПРОГРАММОЙ?\n"
    "   а) Нажмите «Загрузить файл» и выберите файл с описанием сети.\n"
    "   б) Программа сама определит лучший способ отображения (иерархический или радиальный).\n"
    "   в) Откроется окно браузера с оптимизированной визуализацией сети.\n\n"
    "6. ЧТО ДЕЛАТЬ, ЕСЛИ ИКОНКИ НЕ ОТОБРАЖАЮТСЯ?\n"
    "   • Проверьте, что в JSON‑файле имена типов записаны без ошибок.\n\n"
    "7. ЧТО ДЕЛАТЬ, ЕСЛИ СХЕМА ПУСТАЯ?\n"
    "   • Проверьте, что файл не повреждён и содержит узлы и связи.\n"
    "   • Если схема открылась, но ничего не видно, покрутите колёсико мыши для уменьшения масштаба — "
    "возможно, узлы находятся за пределами видимой области.\n"
    "   • Можно также нажать кнопку «Восстановить вид» в браузере или перезагрузить страницу.\n\n"
    "8. ПРИМЕЧАНИЯ\n"
    "   • Программа автоматически минимизирует пересечения линий связи.\n"
    "   • Для очень больших сетей (более 500 узлов) построение может занять несколько секунд.\n"
    "   • Поддерживаются неориентированные и ориентированные графы."
)
    text.config(state='disabled')
    back_btn = Button(info_win, text="Назад", fg = "black", command=lambda: go_back(info_win))
    back_btn.pack()