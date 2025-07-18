import os
import pandas as pd

def parse_date(s):
    if '-' in s:
        # print(pd.to_datetime(s, format="%Y-%m-%d %H:%M"))
        return pd.to_datetime(s, format="%Y-%m-%d %H:%M")
    else:
        # print(pd.to_datetime(s, format="%Y/%m/%d %H:%M"))
        return pd.to_datetime(s, format="%Y/%m/%d %H:%M")

def produce_signal(file_path,save_directory):
    """ 处理 CSV 文件并保存到 signal_data/ 目录中，如果文件已存在则跳过 """
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    file_name = os.path.basename(file_path)
    save_path = os.path.join(save_directory, file_name)

    # **新增：检查是否已有同名文件，存在则跳过**
    if os.path.exists(save_path):
        print(f"文件已存在，跳过处理: {save_path}")
        return  # 直接返回，不进行后续处理
    print(f"正在处理文件: {file_path}")
    # **读取原始 CSV 数据**
    df = pd.read_csv(file_path, encoding='utf-8-sig')

    # **保留指定列**
    columns = ['id','user_id', '转发数', '评论数', '点赞数', '发布时间', 'valid', 'Neutral', 'Positive', 'Negative', 'score', 'filter_result']
    new_df = df[columns].copy()
    start_date = pd.to_datetime('2011-01-01')
    new_df['发布时间'] = new_df['发布时间'].apply(parse_date)
    new_df = new_df[(new_df['发布时间'] >= start_date)]
    new_df = new_df[new_df['valid'] == True]  # 只保留有效数据
    new_df = new_df[new_df['filter_result'] == 3]  # 只保留两个关键词都有的
    # **处理时间列**

    new_df['year'] = new_df['发布时间'].dt.year
    new_df['month'] = new_df['发布时间'].dt.month
    new_df['day'] = new_df['发布时间'].dt.day

    # **保存 CSV**
    new_df.to_csv(save_path, index=False, encoding='utf-8-sig')
    print(f"文件已保存到: {save_path}")


if __name__ == "__main__":
    signal_dict = {
        '1': '',
        '2': '_different_weight',
        '3': '_raw_score',
    }
    choice_signal = signal_dict['1']
    directory = f'结果文件{choice_signal}/去重合并结果/'

    # **遍历目录下所有 CSV 文件**
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            file_path = os.path.join(directory, file)
            produce_signal(file_path,f'signal_data{choice_signal}/')
