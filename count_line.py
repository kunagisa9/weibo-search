import os

def count_csv_rows_simple(directory):
    total = 0
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            path = os.path.join(directory, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = sum(1 for _ in f)
                print(f"{filename}: {lines} 行")
                total += lines
            except Exception as e:
                print(f"读取 {filename} 出错：{e}")
    print(f"\n总行数：{total} 行")

# 替换为你的目录路径
directory_path = "signal_data/"
count_csv_rows_simple(directory_path)