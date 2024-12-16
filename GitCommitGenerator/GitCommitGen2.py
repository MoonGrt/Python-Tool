import requests
import datetime
from collections import defaultdict

def get_user_activity(username, token=None):
    """获取 GitHub 用户的活动数据"""
    url = f'https://api.github.com/users/{username}/events/public'
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    activity = []
    page = 1
    while True:
        response = requests.get(url, headers=headers, params={'page': page, 'per_page': 100})
        if response.status_code != 200:
            print("Failed to fetch data:", response.status_code)
            break
        data = response.json()
        if not data:
            break
        activity.extend(data)
        page += 1
    
    return activity

def parse_commit_dates(activity):
    """解析活动数据并计算每天的提交次数"""
    commit_dates = defaultdict(int)
    
    for event in activity:
        if event['type'] == 'PushEvent':  # 只考虑 PushEvent 作为提交
            date = event['created_at']
            date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").date()  # 转换为日期格式
            commit_dates[date] += 1  # 每次 PushEvent 增加提交数
    
    return commit_dates


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QColor
import datetime

class CommitHeatmap(QWidget):
    def __init__(self, commit_dates):
        super().__init__()

        self.commit_dates = commit_dates  # 提交日期数据

        # 设置窗口
        self.setWindowTitle("GitHub 用户提交热力图")
        self.setGeometry(100, 100, 800, 400)
        
        # 设置网格布局（每年52周，7天）
        layout = QGridLayout()

        # 设置每个方框的大小和间隔
        box_size = 18  # 缩小方框的大小
        margin = 2  # 方框之间的间隔

        # 创建热力图的网格
        for row in range(52):  # 一年有52周
            for col in range(7):  # 一周有7天（从星期一到星期日）
                label = QLabel(self)
                label.setFixedSize(box_size, box_size)
                label.setStyleSheet(f"background-color: {self.get_color_for_commits(row, col)}; border: 1px solid black;")
                layout.addWidget(label, row, col)

        # 设置布局
        self.setLayout(layout)

    def get_color_for_commits(self, row, col):
        """根据提交日期返回相应的颜色。"""
        date = datetime.date(2024, 1, 1) + datetime.timedelta(weeks=row, days=col)  # 计算每个格子对应的日期
        commit_count = self.commit_dates.get(date, 0)  # 获取该日期的提交数量
        if commit_count == 0:
            return QColor(230, 230, 230).name()  # 没有提交时显示浅灰色
        else:
            # 根据提交数量调整颜色强度
            intensity = 255 - (commit_count * 25)  # 提交越多，颜色越深
            return QColor(intensity, 255, intensity).name()

if __name__ == "__main__":
    # 获取 GitHub 用户提交数据并解析
    username = "MoonGrt"  # 替换为您需要查看的 GitHub 用户名
    activity = get_user_activity(username)
    commit_dates = parse_commit_dates(activity)

    # 启动 PyQt 应用
    app = QApplication(sys.argv)
    window = CommitHeatmap(commit_dates)
    window.show()
    sys.exit(app.exec_())
