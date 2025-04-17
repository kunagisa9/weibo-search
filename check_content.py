import pandas as pd

# 读取CSV文件
df = pd.read_csv('结果文件\玉米 期货_2009-08-01_2023-12-31\玉米 期货_2009-08-01_2023-12-31.csv')  # 替换为你的文件路径

# 定义要检测的关键词
keywords = ['玉米', '期货']

# 检测不同时包含这两个关键词的行
# ~表示逻辑非，&表示逻辑与
filtered_df = df[~ (df['微博正文'].str.contains(keywords[0], na=False) &
                   df['微博正文'].str.contains(keywords[1], na=False))]

# 打印结果
print("不同时包含'{}'和'{}'的数据:".format(keywords[0], keywords[1]))
print(filtered_df)