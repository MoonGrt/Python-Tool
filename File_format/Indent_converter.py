import os, chardet
from tkinter import filedialog, messagebox
import tkinter as tk
from ttkbootstrap import Style

def detect_encoding(file_path):
    # 使用chardet检测文件编码
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

def indent_converter():
    """格式化文件夹中的文件"""
    input_folder = folder_path_entry.get()
    output_folder = os.path.join(input_folder, 'output')

    # 获取文件夹中的所有文件
    try:
        files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    except:
        print("系统找不到指定的路径")
        return

    # 创建output文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 遍历每个文件
    for file_name in files:
        input_file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name)

        # 检测文件编码
        encoding = detect_encoding(input_file_path)

        # 读取文件内容
        with open(input_file_path, 'r', encoding=encoding) as input_file:
            # 逐行读取文件内容并转换缩进类型
            lines = []
            for line in input_file:
                # 检测缩进长度
                indent_length = 0
                for char in line:
                    if char == ' ':
                        indent_length += 1
                    else:
                        break
                
                # 将空格缩进转换为制表符缩进
                if indent_length % 4 == 0:
                    line_with_tabs = line.replace(' ' * 4, '\t')
                    lines.append(line_with_tabs)
                elif indent_length % 2 == 0:
                    line_with_tabs = line.replace(' ' * 2, '\t')
                    lines.append(line_with_tabs)
                else:
                    lines.append(line)

            # 将修改后的内容写入output文件夹中的文件
            with open(output_file_path, 'w', encoding=encoding) as output_file:
                output_file.writelines(lines)

    messagebox.showinfo("Success", f"图片已成功格式化并保存到{output_folder}/output")

def browse_folder():
    """浏览文件夹并将路径添加到输入框中"""
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_path)

# 创建主窗口
root = tk.Tk()
root.title("文件格式化工具")
# 主题修改 可选['cyborg', 'journal', 'darkly', 'flatly' 'solar', 'minty', 'litera', 'united', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero','sandstone']
Style(theme='pulse')

# 创建 GUI 组件
folder_label = tk.Label(root, text="输入文件夹:")
folder_path_entry = tk.Entry(root, width=40)
browse_button = tk.Button(root, text="浏览", command=browse_folder)

format_button = tk.Button(root, text="格式化文件", command=indent_converter)

# 安排 GUI 组件
folder_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
folder_path_entry.grid(row=0, column=1, padx=10, pady=5)
browse_button.grid(row=0, column=2, padx=10, pady=5)

format_button.grid(row=1, column=0, columnspan=3, pady=10)

# 运行主循环
root.mainloop()
