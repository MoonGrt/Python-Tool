from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from ttkbootstrap import Style
import os

def flip_image(input_path, output_path, direction='horizontal'):
    image = Image.open(input_path)

    if direction == 'horizontal':
        flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
    elif direction == 'vertical':
        flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        raise ValueError("Invalid direction. Use 'horizontal' or 'vertical'.")

    flipped_image.save(output_path, format='PNG')

def browse_input():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        input_path_var.set(file_path)
        current_directory = os.getcwd()
        output_path_var.set(os.path.join(current_directory, "output", os.path.basename(file_path)))

def flip_image_entry():
    try:
        flip_image(input_path_var.get(), output_path_var.get(), direction_var.get())
        messagebox.showinfo("Success", "图片已成功翻转并保存到 {}".format(output_path_var.get()))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# 创建主窗口
root = tk.Tk()
root.title("图像翻转")
# 主题修改 可选['cyborg', 'journal', 'darkly', 'flatly' 'solar', 'minty', 'litera', 'united', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero','sandstone']
Style(theme='pulse')

# 变量
input_path_var = tk.StringVar()
output_path_var = tk.StringVar()
direction_var = tk.StringVar(value='horizontal')

# 设置列和行的权重，使得它们能够随窗口大小变化而变化
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)

# 输入路径
tk.Label(root, text="图片路径:").grid(row=0, column=0, sticky='e')
tk.Entry(root, textvariable=input_path_var, width=35).grid(row=0, column=1, sticky='we')
tk.Button(root, text="浏览", command=browse_input).grid(row=0, column=2, sticky='nsew')

# 翻转方向
tk.Label(root, text="翻转方向:").grid(row=2, column=0, sticky='e')
tk.Radiobutton(root, text="水平", variable=direction_var, value='horizontal').grid(row=2, column=1, sticky='w')
tk.Radiobutton(root, text="垂直", variable=direction_var, value='vertical').grid(row=2, column=2, sticky='w')

# 翻转按钮
tk.Button(root, text="翻转图片", command=flip_image_entry).grid(row=3, column=1)

# 启动主循环
root.mainloop()
