
import pandas as pd
import numpy as np
from future_and_exchange import futures_exchange_dict, futures_english_dict2,future_and_acro
import os







def generate_statistics_table_with_multiindex(data_dict, futures_english_dict2, futures_exchange_dict):
    # 创建一个空的DataFrame来存储结果
    results = []

    for keyword, df in data_dict.items():
        # 提取期货名称和交易所
        futures_key = keyword.split(' ')[0]
        name = futures_english_dict2.get(futures_key, 'N/A')
        exchange = futures_exchange_dict.get(futures_key, 'N/A')

        # 计算各项统计数据
        count = len(df)
        total_reposts = df['转发数'].sum()
        total_comments = df['评论数'].sum()
        total_likes = df['点赞数'].sum()
        unique_users = df['user_id'].nunique()
        score_mean = df['score'].mean()
        score_std = df['score'].std()

        # 将结果添加到列表中
        results.append([
            name,
            exchange,
            count,
            total_reposts,
            total_comments,
            total_likes,
            unique_users,
            score_mean,
            score_std
        ])

    # 创建多级列名
    columns = pd.MultiIndex.from_tuples([
        ('', 'english_name'),
        ('', 'exchange'),
        ('Tweets', 'count'),
        ('Retweet', 'total'),
        ('Comments', 'total'),
        ('Likes', 'total'),
        ('Users', 'unique'),
        ('Score', 'mean'),
        ('Score', 'std')
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



if __name__ == "__main__":
    directory2 = 'signal_data/'

    data_dict = load_all_data(directory2)

    # 调用函数生成统计表
    result_table = generate_statistics_table_with_multiindex(data_dict, futures_english_dict2, futures_exchange_dict)
    print(result_table)

    result_table.to_excel('statistics_results.xlsx')