import os
import numpy as np


# 指定文件夹路径
folder_path = f"./C20T80/"

# 获取文件夹中所有.npy文件的列表
npy_files = [f for f in os.listdir(folder_path) if f.endswith('.npy')]

# 预期的维度
expected_dimensions = (5, 5, 224)

# 遍历每个.npy文件
for npy_file in npy_files:
    file_path = os.path.join(folder_path, npy_file)

    # 加载.npy文件
    data = np.load(file_path)

    # 获取维度信息
    dimensions = data.shape

    # 判断维度是否不符合预期
    if dimensions != expected_dimensions:
        # 计算值为0的数量
        zero_count = np.sum(data == 0)

        # 打印文件名、维度信息和值为0的数量
        print(f"File: {npy_file}")
        print(f"Dimensions: {dimensions}")
        # print(f"Zero Count: {zero_count}")
        print("-" * 40)
        # 删除文件
        os.remove(file_path)
        print(f"File {npy_file} has been deleted.")
