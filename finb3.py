from transformers import TextClassificationPipeline
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from transformers import BertTokenizerFast
import pandas as pd
import os
import torch
import time
import traceback
# 加载模型和分词器
model_path = "./fin_sentiment_bert_zh/"
device = 0 if torch.cuda.is_available() else -1

new_model = AutoModelForSequenceClassification.from_pretrained(model_path, output_attentions=True)
new_model.to('cuda' if device == 0 else 'cpu')
tokenizer = BertTokenizerFast.from_pretrained(model_path)
PipelineInterface = TextClassificationPipeline(
    model=new_model,
    tokenizer=tokenizer,
    device=device,
    return_all_scores=True
)
root_path = "./结果文件2"

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

not_file = ['PTA 期货_2009-08-01_2023-12-31.csv',
            '20号胶 期货_2009-08-01_2023-12-31.csv',
            '螺纹钢 期货_2013-01-01_2013-12-31.csv',
            '螺纹钢 期货_2018-01-01_2018-12-31.csv',
            '螺纹钢 期货_2014-01-01_2014-12-31.csv'
            ]
# not_contain = ['豆一','不锈钢','乙二醇','对二甲苯','原油', '尿素', '棉纱', '棉花', '棕榈油', '橡胶', '沥青',
#                '油菜籽', '烧碱', '热轧卷板', '焦炭', '焦煤', '燃料油', '玉米', '玉米淀粉', '玻璃', '生猪',
#                '甲醇', '白糖', '白银', '短纤', '硅铁', '粳米', '红枣', '纯碱', '纸浆', '线材', '聚丙烯',
#                '聚乙烯', '聚氯乙烯', '花生', '苯乙烯', '苹果', '菜籽粕', '螺纹钢', '豆二', '氧化铝', '豆油',
#                '豆粕', '铁矿石', '铅', '铜', '铝', '锌', '锡', '锰硅', '镍', '鸡蛋', '黄金']

not_contain = []

for subdir, _, files in os.walk(root_path):
    for file in files:
        if file.endswith(".csv"):
            if file not in not_file:
                skip_file = False
                for contain in not_contain:
                    if contain in file:
                        print(f"跳过文件: {file}")
                        skip_file = True
                        break
                if skip_file:
                    continue
                csv_path = os.path.join(subdir, file)
                print(f"正在处理文件: {csv_path}")

                # 读取 CSV 文件
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
                valid_mask = df['valid']
                valid_indices = df.index[valid_mask].tolist()
                valid_texts = df.loc[valid_mask, 'content'].tolist()
                if valid_texts:  # 如果有合法文本，则批量处理
                    # 批量处理：一次性传入多个文本，可设置 batch_size 提高 GPU 利用率
                    time1 = time.time()
                    batch_results = PipelineInterface(valid_texts, batch_size=4)
                    time2 = time.time()
                    print(f"处理时间：{time2 - time1:.2f} 秒")
                    # 将批量得到的结果按照原来的索引填回 DataFrame
                    df.loc[valid_indices, 'result'] = pd.Series(batch_results, index=valid_indices)
                    time3 = time.time()
                    print(f"填充时间：{time3 - time2:.2f} 秒")
                # ------------------------------
                # 5. 提取各个情感标签的分数并保存
                # ------------------------------
                for tag in ['Neutral', 'Positive', 'Negative']:
                    df[tag] = df['result'].apply(lambda x: extract_score(x, tag))


                # 保存更新后的 DataFrame 到 CSV 文件
                df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                print(f"文件处理完成并保存: {csv_path}")
            else:
                print(f"跳过文件: {file}")