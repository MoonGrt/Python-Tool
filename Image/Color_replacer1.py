import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

def load_image():
    global image
    # 打开文件对话框以选择图片
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    if file_path:
        # 读取图片并显示
        image = Image.open(file_path)
        display_image()
        reset_undo_redo()

def display_image():
    global image, tk_image
    # 将图片转换为Tkinter PhotoImage对象并在画布上显示
    tk_image = ImageTk.PhotoImage(image)
    canvas.config(width=tk_image.width(), height=tk_image.height())
    if(tk_image.width() < 500):
        canvas.create_image(249-int(tk_image.width()/2), 0, anchor="nw", image=tk_image)
    else:
        canvas.create_image(0, 0, anchor="nw", image=tk_image)
    # 设置窗口大小适应图片大小
    geometry_width, geometry_height = max(tk_image.width(), 500), max(tk_image.height()+190, 240)
    root.geometry(f"{geometry_width}x{geometry_height}")

def update_threshold_label(value):
    threshold_label.config(text=f"颜色阈值: {int(value)}")

immediate_replace = False
def toggle_mode():
    global immediate_replace
    immediate_replace = mode_var.get() == 2
    replace_button["state"] = "normal" if not immediate_replace else "disabled"

def on_left_click(event):
    # 获取左键点击位置的像素颜色
    x, y = event.x, event.y
    pixel_color = image.getpixel((x, y))
    target_color_label.config(text=f"目标颜色: {pixel_color}")
    if immediate_replace:
        replace_colors()

def on_right_click(event):
    # 获取右键点击位置的像素颜色
    x, y = event.x, event.y
    pixel_color = image.getpixel((x, y))
    replace_color_label.config(text=f"替换颜色: {pixel_color}")
    if immediate_replace:
        replace_colors()

def replace_colors():
    # 获取目标颜色和替换颜色
    target_color_str = target_color_label.cget("text")
    replace_color_str = replace_color_label.cget("text")
    # 提取RGB值
    try:
        target_color = tuple(map(int, target_color_str.split(":")[1].strip().strip('()').split(',')))
        replace_color = tuple(map(int, replace_color_str.split(":")[1].strip().strip('()').split(',')))
    except:
        print("请输入颜色")
        return
    # 将当前状态存入撤销栈
    undo_stack.append(image.copy())
    # 替换颜色
    threshold = threshold_slider.get()
    replace_color_func(image, target_color, replace_color, threshold)
    # 清空恢复栈
    redo_stack.clear()
    # 重新显示更新后的图片
    display_image()

def replace_color_func(img, target_color, new_color, threshold):
    # 将图像转换为NumPy数组
    img_array = np.array(img)
    # 检查图像通道数
    if img_array.shape[2] == 4:  # 图像具有alpha通道（RGBA）
        # 计算颜色距离并创建掩码（考虑alpha通道）
        color_distances = np.sqrt(np.sum((img_array[:, :, :4] - np.array(target_color))**2, axis=-1))
        mask = color_distances < threshold
        # 将匹配的像素替换为新颜色
        img_array[mask] = new_color
        # 创建新的Image对象
        img.paste(Image.fromarray(img_array, 'RGBA'))
        # new_img = Image.fromarray(img_array, 'RGBA')
    else:  # 图像没有alpha通道（RGB）
        # 计算颜色距离并创建掩码（不考虑alpha通道）
        color_distances = np.sqrt(np.sum((img_array[:, :, :3] - np.array(target_color[:3]))**2, axis=-1))
        mask = color_distances < threshold
        # 将匹配的像素替换为新颜色
        img_array[mask] = new_color
        # 创建新的Image对象
        img.paste(Image.fromarray(img_array, 'RGB'))
        # new_img = Image.fromarray(img_array, 'RGB')

def save_image():
    # 弹出文件对话框以保存图片
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        # 保存图片
        image.save(file_path)

def reset_undo_redo():
    # 重置撤销和恢复栈
    undo_stack.clear()
    redo_stack.clear()

def undo_color():
    if undo_stack:
        # 将当前状态存入恢复栈
        redo_stack.append(image.copy())
        # 恢复到上一状态
        image.paste(undo_stack.pop())
        # 重新显示更新后的图片
        display_image(image)

def redo_color():
    if redo_stack:
        # 将当前状态存入撤销栈
        undo_stack.append(image.copy())
        # 恢复到下一状态
        image.paste(redo_stack.pop())
        # 重新显示更新后的图片
        display_image(image)

root = tk.Tk()
root.title("Image Color Replacer")

load_button = tk.Button(root, text="选择图片", command=load_image)
load_button.grid(row=0, column=0, columnspan=2, sticky="nsew")

mode_var = tk.IntVar()
mode_var.set(1) # 默认为模式1
mode1_radio = tk.Radiobutton(root, text="模式1-点击按钮时替换", variable=mode_var, value=1, command=toggle_mode)
mode1_radio.grid(row=2, column=0, sticky="nsew")
mode2_radio = tk.Radiobutton(root, text="模式2-点击图片时替换", variable=mode_var, value=2, command=toggle_mode)
mode2_radio.grid(row=2, column=1, sticky="nsew")

canvas = tk.Canvas(root, width=496, height=50)
canvas.grid(row=1, column=0, columnspan=2, sticky="nsew")
canvas.bind("<Button-1>", on_left_click)
canvas.bind("<Button-3>", on_right_click)

target_color_label = tk.Label(root, text="目标颜色: (x, x, x)")
target_color_label.grid(row=3, column=0, sticky="nsew")

replace_color_label = tk.Label(root, text="替换颜色: (x, x, x)")
replace_color_label.grid(row=3, column=1, sticky="nsew")

threshold_label = tk.Label(root, text="颜色阈值: 25")
threshold_label.grid(row=4, column=0, columnspan=2, sticky="nsew")

threshold_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", showvalue=0, command=update_threshold_label)
threshold_slider.set(25)
threshold_slider.grid(row=5, column=0, columnspan=2, sticky="nsew")

replace_button = tk.Button(root, text="替换", command=replace_colors)
replace_button.grid(row=6, column=0, sticky="nsew")

save_button = tk.Button(root, text="保存", command=save_image)
save_button.grid(row=6, column=1, sticky="nsew")

undo_button = tk.Button(root, text="撤销", command=undo_color)
undo_button.grid(row=7, column=0, sticky="nsew")

redo_button = tk.Button(root, text="恢复", command=redo_color)
redo_button.grid(row=7, column=1, sticky="nsew")

image = None
tk_image = None
undo_stack = []
redo_stack = []

# 设置列和行的权重
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

# root.update()
# print(f"Tkinter root width: {root.winfo_width()}")
# print(f"Tkinter root height: {root.winfo_height()}")

root.mainloop()
