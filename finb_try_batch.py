import traceback

from transformers import TextClassificationPipeline
from transformers import AutoModelForSequenceClassification, BertTokenizerFast
import pandas as pd
import os
import torch
import time
# ------------------------------
# 1. 加载模型、分词器，并设置 device
# ------------------------------
model_path = "./fin_sentiment_bert_zh/"
device = 0 if torch.cuda.is_available() else -1
# device = -1

new_model = AutoModelForSequenceClassification.from_pretrained(model_path, output_attentions=True)
new_model.to('cuda' if device == 0 else 'cpu')
tokenizer = BertTokenizerFast.from_pretrained(model_path)

# 注意：device 参数在 pipeline 中非常重要
PipelineInterface = TextClassificationPipeline(
    model=new_model,
    tokenizer=tokenizer,
    device=device,
    return_all_scores=True
)


# ------------------------------
# 2. 定义辅助函数
# ------------------------------

def is_valid_text(text):
    """
    判断文本经过 tokenizer 编码后的长度是否小于等于512.
    """
    try:
        tokens = tokenizer(text, add_special_tokens=True, truncation=False)
        return len(tokens['input_ids']) <= 512
    except:
        print(traceback.format_exc())
        print('-----------')
        print(text)
        return False


def extract_score(result, label):
    """
    从 pipeline 返回的结果中提取指定 label 的分数。
    如果 result 为 None 或未找到对应 label，则返回 None。
    """
    if result is None:
        return None
    for item in result:  # 直接遍历 result 列表中的每个字典
        if item['label'] == label:
            return item['score']
    return None


# ------------------------------
# 3. 读取 CSV，并预处理数据
# ------------------------------
# csv_path = "./结果文件3/螺纹钢 期货_2018-01-01_2018-12-31/螺纹钢 期货_2018-01-01_2018-12-31.csv"
# csv_path = "./结果文件/豆一 期货_2014-01-01_2014-12-31/豆一 期货_2014-01-01_2014-12-31.csv"
# csv_path = "./结果文件/PTA 期货_2009-08-01_2023-12-31/PTA 期货_2009-08-01_2023-12-31.csv"
# csv_path = "./结果文件3/螺纹钢 期货_2019-01-01_2023-12-31/螺纹钢 期货_2019-01-01_2023-12-31.csv"
csv_path = "./结果文件3/原油 期货_2018-01-01_2018-05-31/原油 期货_2018-01-01_2018-05-31.csv"


print(f"正在处理文件: {csv_path}")
df = pd.read_csv(csv_path)

# 移除“微博正文”中的 #话题# 部分，并存入新列 'content'
df['content'] = df['微博正文'].str.replace(r'#.*?#', '', regex=True)
df['content'] = df['content'].str.replace(r'@', '')
df['content'] = df['content'].str.replace(r'O网页链接', '')
df['content'] = df['content'].str.replace(r'O微博桌面首页', '')
# 判断每条文本是否有效（token数量不超过512）
df['valid'] = df['content'].apply(is_valid_text)

# 初始化一个新列，用于存放 pipeline 处理结果
df['result'] = None

# ------------------------------
# 4. 对所有合法文本批量调用 pipeline
# ------------------------------
# 取出所有合法文本的索引和文本列表
valid_mask = df['valid']
valid_indices = df.index[valid_mask].tolist()
valid_texts = df.loc[valid_mask, 'content'].tolist()

if valid_texts:  # 如果有合法文本，则批量处理
    # 去重处理
    unique_texts = list(set(valid_texts))  # 去重
    time1 = time.time()
    batch_results = PipelineInterface(unique_texts, batch_size=4)  # 批量处理去重后的文本
    time2 = time.time()
    print(f"处理时间：{time2 - time1:.2f} 秒")

    # 创建一个临时 DataFrame 来存储去重后的结果
    unique_df = pd.DataFrame({'content': unique_texts, 'result': batch_results})

    # 将去重后的结果合并回原始 DataFrame
    df = df.merge(unique_df, on='content', how='left', suffixes=('', '_unique'))
    df['result'] = df['result_unique'].combine_first(df['result'])  # 合并结果列
    df.drop(columns=['result_unique'], inplace=True)  # 删除临时列

    time3 = time.time()
    print(f"填充时间：{time3 - time2:.2f} 秒")

# ------------------------------
# 5. 提取各个情感标签的分数并保存
# ------------------------------
for tag in ['Neutral', 'Positive', 'Negative']:
    df[tag] = df['result'].apply(lambda x: extract_score(x, tag))

df.to_csv(csv_path, index=False, encoding='utf-8-sig')
print(f"文件处理完成并保存: {csv_path}")
