import requests
import json
from datetime import datetime

def get_contributions(username, start_date, end_date):
    commits = {}
    page = 1
    while True:
        url = f'https://api.github.com/users/{username}/events/public?per_page=100&page={page}'
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': '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'
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)

        # 获取 Link 头部来判断是否有更多页面
        if 'link' in response.headers:
            links = response.headers['link']
            if 'rel="next"' not in links:
                break  # 没有更多页面，退出循环

        # 如果没有更多数据，结束循环
        if not response.json():
            break

        for event in data:
            try:
                if event['type'] == 'PushEvent':
                    data = event['created_at'].split('T')[0]
                    if data not in commits:
                        commits[data] = 1
                    else:
                        commits[data] += 1
            except:
                pass

        page += 1

    return commits

# 设置时间范围
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

username = 'MoonGrt'
commits = get_contributions(username, start_date, end_date)
print(commits)
