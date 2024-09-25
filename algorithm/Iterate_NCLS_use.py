import numpy as np
import pandas as pd
import NCLS
import os
import argparse

# 使用 argparse 处理命令行参数
parser = argparse.ArgumentParser(description='FCLS processing script.')
parser.add_argument('--window_size', type=int, default=5, help='Window size')
parser.add_argument('--start_band', type=int, default=10, help='Start band index')
parser.add_argument('--end_band', type=int, default=210, help='End band index')
parser.add_argument('--folder', type=str, default="C20T80", help='Folder name')

# 解析命令行参数
args = parser.parse_args()

window_size = args.window_size
start_band = args.start_band
end_band = args.end_band
folder = args.folder


# 指定文件夹路径
folder_path = f"./file_patch_{window_size}_{window_size}/"+folder

M = np.load("signature_averge.npy")  # 3 种材料的光谱特征 (光谱库)
M = M[start_band:end_band]

# 获取文件夹中所有文件的列表
files = os.listdir(folder_path)




# 用于存储结果的列表
results = []

# 遍历每个文件
for file_name in files:
    file_path = os.path.join(folder_path, file_name)

    R = np.load(file_path)

    r_mean = np.mean(R, axis=(0, 1))
    r_mean = r_mean[start_band:end_band]
    # 调用 NCLS 函数
    abundance, error_vector = NCLS.NCLS(M, r_mean)
    # 将结果添加到列表中
    results.append({
        "file_name": file_name,
        "C_abundance": abundance[0],
        "T_abundance": abundance[1]
    })
    # 将结果转换为 DataFrame
    df_results = pd.DataFrame(results)

    # 输出 DataFrame
    # print(df_results)

    # 如果需要将 DataFrame 保存为 CSV 文件，可以使用以下代码：
    df_results.to_csv("../band200_result/"+f"{folder}_NCLS_band{end_band - start_band}_{window_size}_{window_size}.csv", index=False)
print(f"{folder}_FCLS_band{end_band-start_band}_{window_size}_{window_size}.csv is done")








