
import pandas as pd
import numpy as np
from future_and_exchange import futures_exchange_dict, futures_english_dict2,future_and_acro
import os







def generate_statistics_table_with_multiindex(data_dict, futures_english_dict2, futures_exchange_dict):
    return_df = pd.read_csv('data_w_c.csv', parse_dates=['date'])
    return_df = return_df[(return_df['date'] >= '2011-01-01') & (return_df['date'] <= '2023-12-31')]

    results = []

    for keyword, df in data_dict.items():
        # 提取期货名称和交易所
        futures_key = keyword.split(' ')[0]
        name = future_and_acro.get(futures_key, 'N/A')
        exchange = futures_exchange_dict.get(futures_key, 'N/A')
        if name in ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9','A10','JR', 'PM', 'RI']:
            continue
        # 获取主代号
        main_code = future_and_acro.get(futures_key)
        if main_code is None:
            matched_codes = []
        else:
            matched_codes = code_groups.get(main_code, [main_code])

        # 筛选 return 数据
        matched_return_df = return_df[return_df['name'].isin(matched_codes)]
        return_mean = matched_return_df['tret'].mean()
        return_std = matched_return_df['tret'].std()

        # 统计原始指标
        count = len(df)
        total_reposts = df['转发数'].sum()
        total_comments = df['评论数'].sum()
        total_likes = df['点赞数'].sum()
        unique_users = df['user_id'].nunique()
        score_mean = df['score'].mean()
        score_std = df['score'].std()

        # 添加到结果
        results.append([
            name,
            exchange,
            count,
            total_reposts,
            total_comments,
            total_likes,
            unique_users,
            score_mean,
            score_std,
            return_mean,
            return_std
        ])

    # 定义列名
    columns = pd.MultiIndex.from_tuples([
        ('', 'english_name'),
        ('', 'exchange'),
        ('Tweets', 'count'),
        ('Retweet', 'total'),
        ('Comments', 'total'),
        ('Likes', 'total'),
        ('Users', 'unique'),
        ('Score', 'mean'),
        ('Score', 'std'),
        ('Return', 'mean'),
        ('Return', 'std')
    ])

    result_df = pd.DataFrame(results, columns=columns)
    return result_df


def load_all_data(directory):
    data_dict = {}
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            keyword = file.split('_')[0]
            file_path = os.path.join(directory, file)
            df = pd.read_csv(file_path)
            data_dict[keyword] = df
    return data_dict

code_groups = {
    'RI': ['RI', 'ER'],
    'ER': ['RI', 'ER'],
    'MA': ['MA', 'ME'],
    'ME': ['MA', 'ME'],
    'OI': ['OI', 'RO'],
    'RO': ['OI', 'RO'],
    'ZC': ['ZC', 'TC'],
    'TC': ['ZC', 'TC'],
    'WH': ['WH', 'WS'],
    'WS': ['WH', 'WS']
}

if __name__ == "__main__":
    directory2 = 'signal_data/'

    data_dict = load_all_data(directory2)

    # 调用函数生成统计表
    result_table = generate_statistics_table_with_multiindex(data_dict, futures_english_dict2, futures_exchange_dict)
    print(result_table)

    result_table.to_excel('statistics_results.xlsx')