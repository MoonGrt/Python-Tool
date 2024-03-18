import os, json
from collections import defaultdict

def aggregate_player_stats(input_dir):
    # 创建输出文件夹
    output_folder = os.path.join(input_dir, 'output')
    os.makedirs(output_folder, exist_ok=True)

    # 初始化玩家数据的总和字典
    aggregated_stats = defaultdict(lambda: defaultdict(int))

    # 遍历输入文件夹中的所有文件
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(input_dir, file_name)
            with open(file_path, 'r') as file:
                player_data = json.load(file)
                stats = player_data.get('stats', {})
                for action_type, action_data in stats.items():
                    for action, count in action_data.items():
                        aggregated_stats[action_type][action] += count

    # 添加DataVersion字段到数据中
    player_stats_with_version = {"stats": aggregated_stats, "DataVersion": 1631}

    # 将总和数据写入输出文件
    output_file_path = os.path.join(output_folder, 'aggregated_stats.json')
    with open(output_file_path, 'w') as output_file:
        json.dump(player_stats_with_version, output_file, indent=4)

    print('数据已成功聚合并写入文件夹:', output_folder)

if __name__ == '__main__':
    input_directory = "F:\Project\Python\Tool\MC_playerdata_integration\stats"
    aggregate_player_stats(input_directory)
