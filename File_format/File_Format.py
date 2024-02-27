import os, json, autopep8
from tkinter import filedialog, messagebox
import tkinter as tk
from ttkbootstrap import Style

def format_json_file(input_file_path, output_file_path):
    """格式化 JSON 文件"""
    with open(input_file_path, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {input_file_path}: {e}")
            return

    with open(output_file_path, 'w') as file:
        json.dump(data, file, indent='\t')

def format_python_file(input_file_path, output_file_path):
    """格式化 Python 文件"""
    with open(input_file_path, 'r', encoding='utf-8') as file:
        python_code = file.read()

    formatted_code = autopep8.fix_code(python_code)
    # 用制表符替换空格（假设每个制表符为 4 个空格）
    tab_indented_code = formatted_code.replace(' ' * 4, '\t')

    with open(output_file_path, 'w') as file:
        file.write(tab_indented_code)

def browse_folder():
    """浏览文件夹并将路径添加到输入框中"""
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_path)

def format_folder():
    """格式化文件夹中的文件"""
    folder_path = folder_path_entry.get()

    if not folder_path:
        # 如果用户没有输入路径，显示提示信息
        result_label.config(text="Please select a folder before formatting.")
        return

    output_folder_path = os.path.join(folder_path, "output")
    os.makedirs(output_folder_path, exist_ok=True)

    for filename in os.listdir(folder_path):
        input_file_path = os.path.join(folder_path, filename)
        output_file_path = os.path.join(output_folder_path, filename)

        if filename.endswith(".json"):
            format_json_file(input_file_path, output_file_path)
        elif filename.endswith(".py"):
            format_python_file(input_file_path, output_file_path)

    result_label.config(text="Files formatted successfully!")
    messagebox.showinfo("Success", f"图片已成功格式化并保存到{folder_path}/output")

# 创建主窗口
root = tk.Tk()
root.title("文件格式化工具")
# 主题修改 可选['cyborg', 'journal', 'darkly', 'flatly' 'solar', 'minty', 'litera', 'united', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero','sandstone']
Style(theme='pulse')

# 创建 GUI 组件
folder_label = tk.Label(root, text="输入文件夹:")
folder_path_entry = tk.Entry(root, width=40)
browse_button = tk.Button(root, text="浏览", command=browse_folder)

format_button = tk.Button(root, text="格式化文件", command=format_folder)
result_label = tk.Label(root, text="")

# 安排 GUI 组件
folder_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
folder_path_entry.grid(row=0, column=1, padx=10, pady=5)
browse_button.grid(row=0, column=2, padx=10, pady=5)

format_button.grid(row=1, column=0, columnspan=3, pady=10)
result_label.grid(row=2, column=0, columnspan=3)

# 运行主循环
root.mainloop()
