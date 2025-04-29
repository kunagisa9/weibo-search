import pandas as pd
import os
from glob import glob

# 定义根路径
root_path = '结果文件'  # 替换为你的根路径

# 准备收集结果的列表
results = []

# 遍历根路径下的所有CSV文件
for csv_file in glob(os.path.join(root_path, '*', '*.csv')):
    file_name = os.path.basename(csv_file)
    folder_name = os.path.basename(os.path.dirname(csv_file))
    keywords_part = file_name.split('_')[0]
    keywords = keywords_part.split(' ')

    try:
        df = pd.read_csv(csv_file)

        if '微博正文' not in df.columns:
            print(f"文件 {csv_file} 中没有'微博正文'列，跳过")
            continue

        total_rows = len(df)

        contains_kw1 = df['微博正文'].str.contains(keywords[0], na=False)
        contains_kw2 = df['微博正文'].str.contains(keywords[1], na=False)

        not_both = ~(contains_kw1 & contains_kw2)
        not_any = ~(contains_kw1 | contains_kw2)
        only_kw1 = contains_kw1 & ~contains_kw2
        only_kw2 = contains_kw2 & ~contains_kw1
        not_kw1 = ~contains_kw1
        not_kw2 = ~contains_kw2

        results.append({
            '文件名': file_name,
            '关键词1': keywords[0],
            '关键词2': keywords[1],
            '总行数': total_rows,
            '不同时包含两个关键词的行数': not_both.sum(),
            '不同时包含两个关键词的占比': not_both.sum() / total_rows,
            '不包含任意一个关键词的行数': not_any.sum(),
            '不包含任意一个关键词的占比': not_any.sum() / total_rows,
            '只包含关键词1的行数': only_kw1.sum(),
            '只包含关键词1的占比': only_kw1.sum() / total_rows,
            '只包含关键词2的行数': only_kw2.sum(),
            '只包含关键词2的占比': only_kw2.sum() / total_rows,
            '不包含关键词1的行数': not_kw1.sum(),
            '不包含关键词1的占比': not_kw1.sum() / total_rows,
            '不包含关键词2的行数': not_kw2.sum(),
            '不包含关键词2的占比': not_kw2.sum() / total_rows
        })

    except Exception as e:
        print(f"处理文件 {csv_file} 时出错: {e}")
        continue

results_df = pd.DataFrame(results)
summary_file = os.path.join(root_path, '关键词分析总结2.csv')
results_df.to_csv(summary_file, index=False, encoding='utf_8_sig')

print(f"分析完成，总结文件已保存到: {summary_file}")
print(results_df)
