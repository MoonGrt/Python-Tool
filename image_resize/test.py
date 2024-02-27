import tkinter as tk
from tkinter import ttk

def start_progress():
    progress_bar.start()

def stop_progress():
    progress_bar.stop()

root = tk.Tk()
root.title("带背景颜色的进度条示例")

# 创建一个样式
style = ttk.Style()
style.configure("TProgressbar",
                thickness=20,  # 进度条的厚度
                troughcolor="gray",  # 背景颜色
                troughrelief="flat",  # 背景的边框样式
                troughborderwidth=5)  # 背景的边框宽度

# 创建一个进度条，并使用上面定义的样式
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, style="TProgressbar")

# 将进度条放置在窗口中
progress_bar.pack(pady=10)

# 创建开始和停止按钮
start_button = tk.Button(root, text="开始进度条", command=start_progress)
start_button.pack()

stop_button = tk.Button(root, text="停止进度条", command=stop_progress)
stop_button.pack()

root.mainloop()
