import pandas as pd

# 读取 CSV 文件
scores = pd.read_csv("all_average_scores3.csv")
data_m = pd.read_csv("data_m.csv")

# Change RI
data_m.loc[(data_m['name'] == 'ER') & (data_m['date'] <= '2013-03-31'), 'name'] = 'RI'
# Change MA
data_m.loc[(data_m['name'] == 'ME') & (data_m['date'] <= '2015-03-31'), 'name'] = 'MA'
# Change OI
data_m.loc[(data_m['name'] == 'RO') & (data_m['date'] <= '2013-03-31'), 'name'] = 'OI'
# Change ZC, cut off as 2015-11-27, Friday, for weekly; 2015-11-30, Monday, for monthly
data_m.loc[(data_m['name'] == 'TC') & (data_m['date'] <= '2015-11-27'), 'name'] = 'ZC'
# Change WH
data_m.loc[(data_m['name'] == 'WS') & (data_m['date'] <= '2013-03-31'), 'name'] = 'WH'
# 从 data_m 中提取年份和月份（假设 date 格式为 "YYYY/M/D"）
data_m['year'] = pd.to_datetime(data_m['date']).dt.year
data_m['month'] = pd.to_datetime(data_m['date']).dt.month

groupby_scores = scores.groupby(['year', 'month', 'acro'], as_index=False)['signal'].mean()

# 按照 data_m 的 year, month 以及 name 与 monthly_scores 的 acro 进行左合并
merged_df = pd.merge(data_m, groupby_scores,
                     left_on=['year','month','name'],
                     right_on=['year','month','acro'],
                     how='left')

# 删除多余的辅助列（acro 列以及可选的 year、month 列）
merged_df = merged_df.drop(columns=['acro'])

# 保存合并结果到新文件中，若对应月份数据不存在，signal 列将保持空缺
merged_df.to_csv("merged_data3.csv", index=False)

print("合并完成，结果保存在 merged_data.csv 中。")
