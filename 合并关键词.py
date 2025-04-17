import os
import pandas as pd
from collections import defaultdict
from datetime import datetime

base_path = '结果文件2/'

data_dict = defaultdict(list)

# 用于合并相同关键词但不同时间的程序，该程序写得非常糙，时间并没有进行复核，只是单纯找了最远和最近的时间，确保你覆盖了所有的时间且不要出现时间的重复

for folder_name in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder_name)
    if os.path.isdir(folder_path):
        parts = folder_name.split('_')
        if len(parts) == 3:
            keyword, start_time, end_time = parts
            file_name = f"{folder_name}.csv"
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            data_dict[keyword].append({
                'df': df,
                'start_time': start_time,
                'end_time': end_time
            })

output_dir = os.path.join(base_path, '合并结果')
os.makedirs(output_dir, exist_ok=True)

for keyword, data_list in data_dict.items():
    combined_df = pd.concat([item['df'] for item in data_list], ignore_index=True)
    min_start_time = min(item['start_time'] for item in data_list)
    max_end_time = max(item['end_time'] for item in data_list)
    output_file = os.path.join(output_dir, f"{keyword}_{min_start_time}_{max_end_time}.csv")
    combined_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"已保存: {output_file}")