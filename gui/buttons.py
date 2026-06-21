# buttons.py
from tkinter import Button
from config import root
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from functions import start_work, get_info

# Кнопка "Начать работу" (бывшая "Загрузить файл")
start_btn = Button(root, text="Начать работу", fg="black", command=start_work)

# Кнопка "Справка"
info_btn = Button(root, text="Справка", fg="black", command=get_info)