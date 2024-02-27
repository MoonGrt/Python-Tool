import os, chardet
import tkinter as tk
from tkinter import filedialog
from ttkbootstrap import Style

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

def replace_in_files(folder_path, search_paragraph, replace_paragraph, backup):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # 备份文件
            if backup:
                backup_path = file_path + '.bak'
                os.replace(file_path, backup_path)

            encoding = detect_encoding(file_path)
            
            with open(file_path, 'r', encoding=encoding) as file:
                file_content = file.read()

            with open(file_path, 'w', encoding=encoding) as file:
                if replace_paragraph:  # Check if replace_paragraph is not empty
                    updated_content = file_content.replace(search_paragraph, replace_paragraph)
                else:
                    updated_content = file_content.replace(search_paragraph, "")
                file.write(updated_content)

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def replace_files():
    folder_path = folder_entry.get()
    search_paragraph = search_entry.get("1.0", tk.END)
    replace_paragraph = replace_entry.get("1.0", tk.END)
    backup = backup_var.get()

    replace_in_files(folder_path, search_paragraph, replace_paragraph, backup)

    result_label.config(text="替换完成。")

# 创建主窗口
root = tk.Tk()
root.title("文件替换工具")
root.geometry("488x320")
Style(theme='pulse')

# 文件夹选择部分
folder_label = tk.Label(root, text="选择文件夹:")
folder_label.place(x=10, y=10)

folder_entry = tk.Entry(root, width=50)
folder_entry.place(x=80, y=10)

browse_button = tk.Button(root, text="浏览", command=browse_folder)
browse_button.place(x=445, y=9)

# 替换字符串部分
search_label = tk.Label(root, text="要替换的段落")
search_label.place(x=80, y=40)

search_entry = tk.Text(root, width=30, height=10)
search_entry.place(x=10+2, y=60)

replace_label = tk.Label(root, text="替换后的段落")
replace_label.place(x=320, y=40)

replace_entry = tk.Text(root, width=30, height=10)
replace_entry.place(x=250+2, y=60)

# 二选一部分
backup_var = tk.BooleanVar()
backup_checkbox = tk.Checkbutton(root, text="备份文件", variable=backup_var)
backup_checkbox.place(x=10, y=244)

# 替换按钮和结果显示
replace_button = tk.Button(root, text="开始替换", command=replace_files)
replace_button.place(x=217, y=260)

result_label = tk.Label(root, text="")
result_label.place(x=10, y=290)

# 启动主循环
root.mainloop()
