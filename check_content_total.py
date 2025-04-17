import pandas as pd
import os
from glob import glob

# 定义根路径
root_path = '结果文件'  # 替换为你的根路径

# 准备收集结果的列表
results = []

# 遍历根路径下的所有CSV文件
for csv_file in glob(os.path.join(root_path, '*', '*.csv')):
    # 从路径中提取文件名部分
    file_name = os.path.basename(csv_file)
    folder_name = os.path.basename(os.path.dirname(csv_file))

    # 从文件名中提取关键词（假设文件名格式为"关键词1 关键词2_日期_日期.csv"）
    keywords_part = file_name.split('_')[0]
    keywords = keywords_part.split(' ')

    # 读取CSV文件
    try:
        df = pd.read_csv(csv_file)

        # 确保有'微博正文'列
        if '微博正文' not in df.columns:
            print(f"文件 {csv_file} 中没有'微博正文'列，跳过")
            continue

        total_rows = len(df)

        # 计算不同时包含两个关键词的占比
        not_both = ~(df['微博正文'].str.contains(keywords[0], na=False) &
                     df['微博正文'].str.contains(keywords[1], na=False))
        not_both_count = sum(not_both)
        not_both_percent = (not_both_count / total_rows) * 100

        # 计算不包含任意一个关键词的占比
        not_any = ~(df['微博正文'].str.contains(keywords[0], na=False) |
                    df['微博正文'].str.contains(keywords[1], na=False))
        not_any_count = sum(not_any)
        not_any_percent = (not_any_count / total_rows) * 100

        # 添加到结果列表
        results.append({
            '文件名': file_name,
            '关键词1': keywords[0],
            '关键词2': keywords[1],
            '总行数': total_rows,
            '不同时包含两个关键词的行数': not_both_count,
            '不同时包含两个关键词的占比(%)': not_both_percent,
            '不包含任意一个关键词的行数': not_any_count,
            '不包含任意一个关键词的占比(%)': not_any_percent
        })

    except Exception as e:
        print(f"处理文件 {csv_file} 时出错: {e}")
        continue

# 将结果转换为DataFrame
results_df = pd.DataFrame(results)

# 生成总结文件
summary_file = os.path.join(root_path, '关键词分析总结.csv')
results_df.to_csv(summary_file, index=False, encoding='utf_8_sig')

print(f"分析完成，总结文件已保存到: {summary_file}")
print(results_df)