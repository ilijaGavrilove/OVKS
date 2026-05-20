from tkinter import Button
from tkinter import filedialog
from config import root
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from logic import visualize
from functions import upload_file, get_info, go_back

upload_file_btn = Button(root, text = "Загрузить файл" ,
             fg = "black", command=upload_file)

info_btn = Button(root, text="Справка", fg = "black", command=get_info)
back_btn = Button(root, text="Назад", fg = "black", command=go_back)