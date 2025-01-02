import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import datetime
import random

class GitCommitGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Git Commit Generator")

        # 将主窗口放置在屏幕中央
        self.center_window(self.root, 374, 427)

        # 日历按钮和显示选择的时间
        self.calendar_button = tk.Button(root, text="Calendar", command=self.show_calendar)
        self.calendar_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.time_display = ttk.Entry(root, width=25)
        self.time_display.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        self.time_display.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # 新增提交次数输入框
        self.num_commits_label = tk.Label(root, text="Commit Num:")
        self.num_commits_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.num_commits_entry = ttk.Entry(root, width=5)
        self.num_commits_entry.insert(0, "1")  # 默认值为1
        self.num_commits_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # 生成按钮和显示生成的命令
        self.generate_button = tk.Button(root, text="Gen", command=self.generate_command)
        self.generate_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.output_box = tk.Text(root, height=20, width=50, state='disabled')
        self.output_box.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # 隐藏的日历窗口
        self.calendar_window = None

        # self.root.update_idletasks()
        # actual_width = self.root.winfo_width()
        # actual_height = self.root.winfo_height()

        # 事件处理函数
        self.generate_command()

    def center_window(self, window, width, height):
        """将窗口放置在屏幕中央"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        position_right = int((screen_width / 2) - (width / 2))
        position_down = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{position_right}+{position_down}")

    def show_calendar(self):
        # 如果已有日历窗口，先销毁它
        if self.calendar_window is not None:
            self.calendar_window.destroy()

        self.calendar_window = tk.Toplevel(self.root)
        self.calendar_window.title("Calendar")

        # 将窗口放置在屏幕中央
        self.calendar_window.update_idletasks()  # 更新窗口信息
        screen_width = self.calendar_window.winfo_screenwidth()
        screen_height = self.calendar_window.winfo_screenheight()
        window_width = self.calendar_window.winfo_width()
        window_height = self.calendar_window.winfo_height()
        position_right = int((screen_width / 2) - (window_width / 2))
        position_down = int((screen_height / 2) - (window_height / 2))
        self.calendar_window.geometry(f"+{position_right}+{position_down}")

        # 从 time_display 中获取初始日期
        initial_date = self.time_display.get()

        # 使用初始日期初始化日历小部件，如果日期无效则使用默认日期
        try:
            self.calendar = Calendar(
                self.calendar_window,
                selectmode='day',
                date_pattern='yyyy-mm-dd',
                year=int(initial_date.split('-')[0]),
                month=int(initial_date.split('-')[1]),
                day=int(initial_date.split('-')[2])
            )
        except (ValueError, IndexError):
            # 如果输入的日期无效，回退到默认的今天日期
            self.calendar = Calendar(
                self.calendar_window,
                selectmode='day',
                date_pattern='yyyy-mm-dd'
            )

        self.calendar.pack(padx=10, pady=10)

        # 确认选择日期的按钮
        select_button = tk.Button(self.calendar_window, text="确认", command=self.select_date)
        select_button.pack(padx=10, pady=10)

    def select_date(self):
        selected_date = self.calendar.get_date()
        self.time_display.delete(0, tk.END)
        self.time_display.insert(0, f"{selected_date}")
        self.calendar_window.destroy()
        self.calendar_window = None
        self.generate_command()

    def generate_command(self):
        user_input = self.time_display.get().strip()
        num_commits_input = self.num_commits_entry.get().strip()

        try:
            # 将用户输入解析为 datetime 对象
            base_date = datetime.datetime.strptime(user_input, "%Y-%m-%d").date()

            # 获取提交次数
            num_commits = int(num_commits_input)

            # 清空输出框
            self.output_box.config(state='normal')
            self.output_box.delete(1.0, tk.END)

            # 生成多个 Git 指令
            for i in range(num_commits):
                # 生成随机小时和分钟
                random_hour = random.randint(0, 23)  # 随机小时（0到23）
                random_minute = random.randint(0, 59)  # 随机分钟（0到59）

                # 创建随机时间
                random_time = datetime.datetime.combine(base_date, datetime.time(random_hour, random_minute))

                # 将时间格式化为 ISO 8601 格式
                iso_time = random_time.strftime("%Y-%m-%dT%H:%M:%S+08:00")

                # 生成提交命令
                git_command = f'git commit --allow-empty --date="{iso_time}" -m "Commit"'
                self.output_box.insert(tk.END, git_command + "\n")

            self.output_box.insert(tk.END, 'git push origin master' + "\n")
            self.output_box.config(state='disabled')

        except ValueError:
            # 显示错误提示
            self.output_box.config(state='normal')
            self.output_box.delete(1.0, tk.END)
            self.output_box.insert(tk.END, "输入的时间格式不正确，请重新选择日期和时间。")
            self.output_box.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = GitCommitGenerator(root)
    root.mainloop()
