from config import root
import tkinter as tk


def upload_file():
    file_path = tk.filedialog.askopenfilename()
    if file_path:
        visualize.visualize_network(file_path)

def main_menu():
    from buttons import upload_file_btn, info_btn
    text = tk.Text(
    root,
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