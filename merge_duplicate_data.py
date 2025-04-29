import os
import pandas as pd
import shutil
from future_and_exchange import duplicate_dict

# 定义路径
base_path = '结果文件/合并结果/'
save_path = '结果文件/去重合并结果/'

# 创建一个集合来记录已经处理过的文件
processed_files = set()

# 遍历duplicate_dict的key
for key in duplicate_dict:
    # 构造文件名
    file1_name = f"{key} 期货_2009-08-01_2023-12-31.csv"
    file2_name = f"{duplicate_dict[key]} 期货_2009-08-01_2023-12-31.csv"

    # 构造文件路径
    file1_path = os.path.join(base_path, file1_name)
    file2_path = os.path.join(base_path, file2_name)

    # 记录已经处理过的文件
    processed_files.add(file1_name)
    processed_files.add(file2_name)

    # 读取文件内容
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)

    # 合并两个DataFrame
    combined_df = pd.concat([df1, df2])

    # 根据'id'列去重
    combined_df = combined_df.drop_duplicates(subset='id')

    # 保存去重后的结果
    output_file_name = f"{key} 期货_2009-08-01_2023-12-31.csv"
    output_file_path = os.path.join(save_path, output_file_name)
    combined_df.to_csv(output_file_path, index=False, encoding='utf_8_sig')

    print(f"已处理并保存: {output_file_name}")

# 获取所有未处理的文件
all_files = set(os.listdir(base_path))
unprocessed_files = all_files - processed_files

# 将未处理的文件复制到save_path
for file_name in unprocessed_files:
    src_path = os.path.join(base_path, file_name)
    dest_path = os.path.join(save_path, file_name)
    shutil.copy(src_path, dest_path)
    print(f"已复制未处理文件: {file_name}")

print("所有文件处理完成。")