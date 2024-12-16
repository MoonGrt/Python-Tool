import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

# 获取网页内容
url = "https://github.com/MoonGrt"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 解析贡献热力图的SVG数据
# 贡献热力图通常在SVG元素中，寻找所有的 <rect> 元素
rect_elements = soup.find_all('rect', {'class': 'day'})

# 提取每个 <rect> 元素的 data-count 属性
contributions = []
for rect in rect_elements:
    count = rect.get('data-count')
    if count:
        contributions.append(int(count))

# 假设我们提取了每个贡献数值后，数据是按周（7天）来排列的
# 生成一个矩阵：每列代表一天，每行代表一周
# 假设一共有 52 周，且每周7天
# 这里是一个简化的矩阵处理方式，实际数据会根据页面内容确定

weeks = len(contributions) // 7  # 一共有多少周
contribution_matrix = np.array(contributions).reshape(weeks, 7)

# 生成热力图
plt.imshow(contribution_matrix, cmap='YlGn', interpolation='nearest')
plt.colorbar()  # 显示颜色条
plt.title("GitHub Contributions Heatmap for MoonGrt")
plt.xlabel("Days of the Week")
plt.ylabel("Weeks")
plt.show()
