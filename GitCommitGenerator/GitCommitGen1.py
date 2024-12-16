import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import datetime
import random

class GitCommitGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Git 回溯提交命令生成器")

        # 日历按钮和显示选择的时间
        self.calendar_button = tk.Button(root, text="日历", command=self.show_calendar)
        self.calendar_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.time_display = ttk.Entry(root, width=25)
        self.time_display.insert(0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.time_display.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # 新增提交次数输入框
        self.num_commits_label = tk.Label(root, text="提交次数:")
        self.num_commits_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.num_commits_entry = ttk.Entry(root, width=5)
        self.num_commits_entry.insert(0, "1")  # 默认值为1
        self.num_commits_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # 生成按钮和显示生成的命令
        self.generate_button = tk.Button(root, text="生成", command=self.generate_command)
        self.generate_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.output_box = tk.Text(root, height=6, width=50, state='disabled')
        self.output_box.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # 隐藏的日历窗口
        self.calendar_window = None

    def show_calendar(self):
        if self.calendar_window is not None:
            self.calendar_window.destroy()

        self.calendar_window = tk.Toplevel(self.root)
        self.calendar_window.title("选择日期")

        self.calendar = Calendar(self.calendar_window, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack(padx=10, pady=10)

        select_button = tk.Button(self.calendar_window, text="确定", command=self.select_date)
        select_button.pack(padx=10, pady=10)

    def select_date(self):
        selected_date = self.calendar.get_date()
        current_time = datetime.datetime.now().strftime("%H:%M")
        self.time_display.delete(0, tk.END)
        self.time_display.insert(0, f"{selected_date} {current_time}")
        self.calendar_window.destroy()
        self.calendar_window = None

    def generate_command(self):
        user_input = self.time_display.get().strip()
        num_commits_input = self.num_commits_entry.get().strip()

        try:
            # 将用户输入解析为 datetime 对象
            base_date = datetime.datetime.strptime(user_input, "%Y-%m-%d %H:%M").date()

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
                git_command = f'git commit --allow-empty --date="{iso_time}" -m "Backdated commit for {random_time.strftime("%Y-%m-%d %H:%M")} China time"'
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
