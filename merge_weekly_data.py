import pandas as pd

# 读取 CSV 文件
scores = pd.read_csv("all_average_scores2.csv")
data_w = pd.read_csv("data_w.csv")

# ----------------------------
# 处理 scores 数据，构造周数据
# ----------------------------
# 合成日期（scores 中有 year, month, day 三列）
scores['date'] = pd.to_datetime(scores[['year', 'month', 'day']])
# 利用 dt.to_period('W') 得到周 Period 对象
scores['week_period'] = scores['date'].dt.to_period('W')
# 提取周结束日期，并将其归一化为当天午夜（00:00:00）
scores['week_end'] = scores['week_period'].apply(lambda r: r.end_time.normalize())

# 按 week_end 分组，对 signal 求均值
weekly_scores = scores.groupby(['acro', 'week_end'], as_index=False)['signal'].mean()

# ----------------------------
# 处理 data_w 数据
# ----------------------------
# data_w.csv 中的 date 列本来就是 week_end，转换为 datetime 并归一化为当天午夜
data_w['week_end'] = pd.to_datetime(data_w['date']).dt.normalize()
# 如有需要，可以计算 week_start（假设每周为7天）
data_w['week_start'] = data_w['week_end'] - pd.Timedelta(days=6)

# ----------------------------
# 按 week_end 合并两个数据集
# ----------------------------
merged_df = pd.merge(data_w, weekly_scores,
                     left_on=['week_end','name'],
                     right_on=['week_end','acro'], how='left')

# 保存结果到新文件中，若某周数据不存在，则 signal 列为空
merged_df.to_csv("merged_data_weekly.csv", index=False)

print("合并完成，结果保存在 merged_data_weekly.csv 中。")
