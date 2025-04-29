import pandas as pd
import os
from glob import glob

# 定义根路径
root_path = '结果文件/去重合并结果'

# 准备收集结果的列表
results = []

# 遍历当前目录下所有CSV文件（不包含子文件夹）
for csv_file in glob(os.path.join(root_path, '*.csv')):
    file_name = os.path.basename(csv_file)

    try:
        df = pd.read_csv(csv_file)
        df = df[df['valid']==True]
        if 'filter_result' not in df.columns:
            print(f"File {csv_file} does not contain 'label' column. Skipping.")
            continue

        label_counts = df['filter_result'].value_counts().to_dict()

        total = len(df)
        count_0 = label_counts.get(0, 0)
        count_1 = label_counts.get(1, 0)
        count_2 = label_counts.get(2, 0)
        count_3 = label_counts.get(3, 0)

        A = (count_0 + count_1 + count_2 + count_3) / total if total else 0
        B_div_A = (count_1 + count_3) / total if total else 0
        C_div_A = count_3 / total if total else 0

        results.append({
            'Filename': file_name,
            'Label 0 Count': count_0,
            'Label 1 Count': count_1,
            'Label 2 Count': count_2,
            'Label 3 Count': count_3,
            'Total Rows': total,
            'A': A,
            'B/A': B_div_A,
            'C/A': C_div_A
        })

    except Exception as e:
        print(f"Error processing file {csv_file}: {e}")
        continue

# 生成汇总表
results_df = pd.DataFrame(results)
summary_file = os.path.join(root_path, 'label_summary.csv')
results_df.to_csv(summary_file, index=False, encoding='utf_8_sig')

print(f"Analysis complete. Summary file saved to: {summary_file}")
print(results_df)
