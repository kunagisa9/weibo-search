import os
import pandas as pd
from future_and_exchange import future_and_acro

if __name__ == "__main__":
    signal_dict = {
        '1': '',
        '2': '_different_weight',
        '3': '_raw_score',
    }
    choice_signal = signal_dict['2']
    directory = f'signal_data{choice_signal}/'
    all_results = pd.DataFrame()  # 创建一个空的DataFrame来存储所有结果

    # 遍历目录下所有 CSV 文件
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            file_path = os.path.join(directory, file)
            df = pd.read_csv(file_path)  # 读取CSV文件
            keyword = file.split('_')[0].split(' ')[0]  # 提取文件名中的keyword
            df=df[df['valid']==True]
            # df=df[(df['filter_result']==1) | (df['filter_result']==3)]  # 只有期货名+2个都有的
            df = df[df['filter_result']==3]  # 只要两个关键词都有的
            # 按year和month分组，并计算score的平均值
            grouped_df = df.groupby(['year', 'month', 'day']).agg(
                signal=('score', 'mean'),  # 计算score的平均值，列名为signal
                count=('score', 'count')   # 计算记录数，列名为count
            ).reset_index()
            # 添加keyword和文件名作为列，以便区分不同文件的结果
            grouped_df['keyword'] = keyword
            grouped_df['acro'] = future_and_acro.get(keyword, 'NNNNNNN')
            grouped_df.rename(columns={'score': 'signal'}, inplace=True)

            # 将结果追加到all_results中
            all_results = pd.concat([all_results, grouped_df], ignore_index=True)

    # 输出结果到CSV文件
    all_results.to_csv(f'all_average_scores_group_c{choice_signal}.csv', index=False, encoding='utf-8-sig')