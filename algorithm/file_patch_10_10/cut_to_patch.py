import numpy as np
import matplotlib.pyplot as plt
import os

# 加载npy文件

orignal_pic = np.load('../file/C80T20.npy')
copy_pic= orignal_pic


height, width, depth = copy_pic.shape

# 创建存储目录，如果不存在则创建
output_dir = f"./C80T20/"
os.makedirs(output_dir, exist_ok=True)

# 定义块的大小
block_size = 10

# 进行切割并保存小方块
counter = 1
for i in range(0, height, block_size):
    for j in range(0, width, block_size):
        # 计算块的结束坐标
        end_i = min(i + block_size, height)
        end_j = min(j + block_size, width)

        # 切割出小方块
        block = copy_pic[i:end_i, j:end_j, :]

        # 判断块中是否包含0
        if np.any(block == 0):
            # 找到所有非零行和列
            non_zero_rows = np.any(block != 0, axis=(1, 2))
            non_zero_cols = np.any(block != 0, axis=(0, 2))

            # 根据非零行和列裁剪块
            block = block[np.ix_(non_zero_rows, non_zero_cols, np.ones(depth, dtype=bool))]

        # 如果裁剪后的块非空，保存它
        if block.size > 0:
            # 构造文件名并保存
            file_path = os.path.join(output_dir, f"{counter}.npy")
            np.save(file_path, block)

            # 更新计数器
            counter += 1