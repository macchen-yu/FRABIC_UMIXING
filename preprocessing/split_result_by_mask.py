#cut
import numpy as np
import matplotlib.pyplot as plt

# 加载npy文件
mask = np.load('mask.npy')
result = np.load('result.npy')

number = 7
# 创建一个新的遮罩，只有原始mask为1的地方为1，其余为0
# new_mask = np.where(mask == number, 1, 0)
new_mask = np.where(mask == number, 1, 0)

# 将new_mask扩展到result的形状
expanded_mask = np.expand_dims(new_mask, axis=-1)
expanded_mask = np.repeat(expanded_mask, result.shape[-1], axis=-1)

# 将result和expanded_mask相乘
masked_result = result * expanded_mask

# 找出所有在第一维上存在非零元素的索引
non_zero_rows = np.any(new_mask != 0, axis=1)

# 找出所有在第二维上存在非零元素的索引
non_zero_cols = np.any(new_mask != 0, axis=0)

# 裁剪掉全零的行和列
filtered_result = masked_result[np.ix_(non_zero_rows, non_zero_cols, np.ones(result.shape[2], dtype=bool))]



# 保存结果
np.save(f'{number}.npy', filtered_result)

print("遮罩应用完成，结果已保存为final_result.npy")

# 可视化结果
plt.imshow(np.sum(filtered_result, axis=2))
plt.show()
