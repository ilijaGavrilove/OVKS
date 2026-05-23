from tkinter import Button, ttk, StringVar
from config import root
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from functions import upload_file, get_info, go_back

upload_file_btn = Button(root, text = "Загрузить файл" ,
             fg = "black", command=upload_file)

method = StringVar(value='auto')

sugiyama_btn = ttk.Radiobutton(text="Метод Сугиямы", value="sugiyama", variable=method)
radial_btn = ttk.Radiobutton(text="Радиальный метод (для звёздной топологии)", value="radial", variable=method)
auto_btn = ttk.Radiobutton(text="Авто (рекомендуется)", value="auto", variable=method)


info_btn = Button(root, text="Справка", fg = "black", command=get_info)
