#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 将文件夹下的图片居中剪裁为指定比例并缩放到指定大小

import time, sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, UnidentifiedImageError
from pathlib import Path
from ttkbootstrap import Style

resize_algorithm = Image.Resampling.LANCZOS
metrics_list = []
filecount = 0

# 缩放算法映射字典
algorithms = ["NEAREST", "BILINEAR", "BICUBIC", "HAMMING", "BOX", "LANCZOS"]
resampling_options = {
    "NEAREST": Image.Resampling.NEAREST,
    "BILINEAR": Image.Resampling.BILINEAR,
    "BICUBIC": Image.Resampling.BICUBIC,
    "HAMMING": Image.Resampling.HAMMING,
    "BOX": Image.Resampling.BOX,
    "LANCZOS": Image.Resampling.LANCZOS,
}

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Image_Resize')  # 窗口名称
        self.root.geometry("512x256")  # 尺寸位置
        # 主题修改 可选['cyborg', 'journal', 'darkly', 'flatly' 'solar', 'minty', 'litera', 'united', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero','sandstone']
        Style(theme='pulse')  
        self.interface()

    def interface(self):
        # 创建并放置源文件夹标签
        self.src_dir_label = tk.Label(self.root, text="源文件夹", anchor='w') # anchor='w' 左对齐
        self.src_dir_label.place(x=15, y=15, width=80, height=25)
        # 创建并配置源文件夹路径的文本变量和文本输入框
        self.src_dir_var = tk.StringVar()
        self.src_dir_entry = tk.Entry(self.root, textvariable=self.src_dir_var)
        self.src_dir_entry.place(x=80, y=15, width=350, height=25)
        # 创建并配置浏览按钮，调用 browse_src_folder 方法
        self.browse_button = tk.Button(self.root, text="浏览", command=self.browse_src_folder)
        self.browse_button.place(x=440, y=15, width=60, height=25)


        # 创建并放置选择算法标签
        self.algorithm_label = tk.Label(self.root, text="算法选择", anchor='w')
        self.algorithm_label.place(x=15, y=55, width=80, height=25)
        # 创建并配置算法选择下拉框，设置预定义的算法选项
        self.algorithm_var = tk.StringVar()
        self.algorithm_combobox = ttk.Combobox(self.root, textvariable=self.algorithm_var, values=algorithms)
        self.algorithm_combobox.set("LANCZOS")
        self.algorithm_combobox.place(x=80, y=55, width=100, height=25)


        self.length_label = tk.Label(self.root, text="长度")
        self.length_label.place(x=20, y=95, width=40, height=25)
        self.length_var = tk.IntVar(value=256)
        self.length = tk.Entry(self.root, state=tk.NORMAL, textvariable=self.length_var)
        self.length.place(x=440, y=93, width=60, height=30)
        self.length.bind("<KeyRelease>", self.update_scale_from_text)
        self.length_scale_var = tk.IntVar(value=256)
        self.length_scale = tk.Scale(self.root, from_=1, to=2048, orient=tk.HORIZONTAL,variable=self.length_scale_var,
                                      command=lambda value:self.update_text_from_scale(value,self.length))
        self.length_scale.place(x=80, y=100, width=350, height=15)

        self.width_label = tk.Label(self.root, text="宽度")
        self.width_label.place(x=20, y=135, width=40, height=25)
        self.width_var = tk.IntVar(value=256)
        self.width = tk.Entry(self.root, state=tk.NORMAL, textvariable=self.width_var)
        self.width.place(x=440, y=133, width=60, height=30)
        self.width.bind("<KeyRelease>", self.update_scale_from_text)
        self.width_scale_var = tk.IntVar(value=256)
        self.width_scale = tk.Scale(self.root, from_=1, to=2048, orient=tk.HORIZONTAL, variable=self.width_scale_var,
                                      command=lambda value: self.update_text_from_scale(value, self.width))
        self.width_scale.place(x=80, y=140, width=350, height=15)


        # 按钮
        self.resize_button = tk.Button(self.root, text="开始处理", command=self.start_processing)
        self.resize_button.place(x=130, y=185, width=80, height=25)
        self.quit_button = tk.Button(self.root, text="退出程序", command=self.root.destroy)
        self.quit_button.place(x=300, y=185, width=80, height=25)


        # 收发字符监控
        self.count = tk.Label(self.root, text='转换文件数: 0', anchor='w')
        self.count.place(x=25, y=230, width=100, height=20)
        # 时钟实现
        self.timer = tk.Label(self.root, text=' ', anchor='w')
        self.timer.place(x=430, y=230, width=100, height=20)

        # 创建一个进度条
        self.progress_bar = ttk.Progressbar(self.root, variable=tk.DoubleVar(value=100))
        self.progress_bar.place(x=120, y=236, width=300, height=10)

    # -----------------------------------方法---------------------------------- #
    def gettim(self):  # 获取时间 
        timestr = time.strftime("%H:%M:%S")  # 获取当前的时间并转化为字符串
        self.timer.configure(text=timestr)   # 重新设置标签文本
        self.timer.after(1000, self.gettim)  # 每隔1s调用函数 gettime 自身获取时间 GUI自带的定时函数

    def update_text_from_scale(self, value, text_widget):
        self.length_var.set(int(self.length_scale_var.get()))
        self.width_var.set(int(self.width_scale_var.get()))

    def update_scale_from_text(self, event=None):
        self.length_scale_var.set(int(self.length_var.get()))
        self.width_scale_var.set(int(self.width_var.get()))

    def browse_src_folder(self):
        self.src_dir_var.set(filedialog.askdirectory())

    def start_processing(self):
        self.src_dir = self.src_dir_var.get()
        if self.src_dir:
            resampling_options.get(self.algorithm_var.get(), resize_algorithm)
            # 将参数传递给图像处理函数
            while (not Path(self.src_dir).exists()):
                print(f'文件夹{self.src_dir}不存在，请检查输入的文件夹名称是否正确。')
            process_images(self.src_dir, self.algorithm_var.get(), self.length_var.get(), self.width_var.get())
            print("完成", "图像处理完成！")
        else:
            print("错误", "请选择源文件夹！")
            pass

# def calculate_metrics(original, generated):
#     # 计算 SSIM、MSE、PSNR
#     ssim_value, _ = ssim(original, generated, full=True)
#     mse = np.sum((original - generated) ** 2) / float(original.size)
#     psnr = cv2.PSNR(original, generated)
#     return ssim_value, mse, psnr
    
def resize_dir_images(src_path, dst_path, dst_w, dst_h):
    global filecount, metrics_list
    remove_ds_store(src_path)
    total_files = sum(1 for _ in src_path.glob('**/*') if _.is_file())  # 计算总文件数
    progress_step = 100 / total_files  # 计算每个文件的进度步长
    for f in src_path.glob('**/*'):  # 也可以用src_path.rglob('*')
        if f.is_file():
            filecount += 1
            print('正在转换第 %d 个文件:%s       \r'%(filecount,f.name),end='')
            crop_and_resize(f, dst_path, dst_w, dst_h)
            gui.count['text'] = '转换文件数: ' + str(filecount)
            gui.progress_bar.step(progress_step)
            gui.root.update_idletasks()

def remove_ds_store(path):
    # print('检查 %s 内是否存在 .DS_Store 文件'%str(path))
    target = path/'.DS_Store'
    if (target.exists()):
        Path.unlink(target)
        print(f'{target} 文件已自动删除。')
    else:
        # print(f'.DS_Store 文件不存在，继续操作。')
        pass

def crop_and_resize(f, dst_path, dst_w, dst_h):
    ''' 图片按照目标比例裁剪并缩放 '''
    try:
        im = Image.open(str(f))
    except (OSError, UnidentifiedImageError):
        print(f"无法识别的图像文件: {f}")
        return
    src_w,src_h = im.size
    dst_scale = float(dst_h / dst_w) #目标高宽比
    src_scale = float(src_h / src_w) #原高宽比

    if src_scale >= dst_scale:
        #过高
        # print("原图过高")
        width = src_w
        height = int(width*dst_scale)
        x = 0
        y = (src_h - height) / 2
    else:
        #过宽
        # print("原图过宽\n")
        height = src_h
        width = int(height/dst_scale)
        x = (src_w - width) / 2
        y = 0
        
    #裁剪
    box = (x,y,width+x,height+y)
    
    #这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    newIm = im.crop(box)
    im = None
    #压缩
    ratio = float(dst_w) / width
    newWidth = int(width * ratio)
    newHeight = int(height * ratio)
    dst_file = dst_path/f.name  # 保持原文件名
    
    om = newIm.resize((newWidth, newHeight), resize_algorithm)
    om.save(dst_file, quality=100)# 保存生成图像

def process_images(src_dir, algorithm, dst_w, dst_h):
    src_path = Path(src_dir)
    src_path = src_path.expanduser()
    print("输入文件夹: ",src_path)
    
    dst_dir = f'{src_dir}_{algorithm.lower()}_{dst_w}x{dst_h}'
    dst_path = Path(dst_dir)
    print('目标文件夹:',dst_path)

    print("选择的缩放算法:", algorithm)

    if dst_path.exists():
        print(f'目标文件夹: {dst_path} 已经存在...')
        pass
    else:
        dst_path.mkdir(parents=True)

    print(f'目标分辨率:{dst_w}x{dst_h}')

    resize_dir_images(src_path, dst_path, dst_w, dst_h)
    remove_ds_store(dst_path)

    # dst_file_list = dst_path.iterdir() # 
    # 直接遍历目标文件夹下的jpg/jpeg文件(使用*.jp*g来匹配两种后缀名)。
    display_each_line = 10  # 此参数规定了最后文件列表每行显示的文件名数量。
    dst_file_list = dst_path.glob('*.jp*g')
    print(f'\n一共转换了{filecount}个文件\n已转换的文件列表: ',end='')
    line_count = 0
    for f in sorted(dst_file_list, key = lambda f : f.stem):
        cnt += 1
        if cnt%display_each_line == 1:
            line_count += 1
            print('\n%d | %10s'%(line_count,f.name),end='')
        else:
            print('%10s'%f.name,end='')

if __name__ == "__main__":
    gui = GUI()
    gui.gettim()  # 开启时钟
    gui.root.mainloop()
