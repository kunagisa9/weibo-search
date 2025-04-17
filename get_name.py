import os
import pandas as pd
from collections import defaultdict
from datetime import datetime

# 用于查看有包含关系的期货关键词

base_path = '结果文件/合并结果/'

data_dict = defaultdict(list)
name_list = []
for folder_name in os.listdir(base_path):

    parts = folder_name.split('_')
    if len(parts) == 3:
        keyword, start_time, end_time = parts
        name_list.append(keyword.split(' ')[0])

for name in name_list:
    for name1 in name_list:
        if name != name1 and name in name1:
            print(name, name1)