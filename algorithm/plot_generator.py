import pandas as pd
import matplotlib.pyplot as plt
import argparse

# 使用 argparse 获取命令行参数
parser = argparse.ArgumentParser(description='Generate a plot from a CSV file.')
parser.add_argument('file_path', type=str, help='The path to the CSV file')
parser.add_argument('--C_abundance_gt', type=float, default=80, help='The constant value for C_abundance_gt')
parser.add_argument('--T_abundance_gt', type=float, default=20, help='The constant value for T_abundance_gt')
args = parser.parse_args()

# 读取 CSV 文件
file_path = args.file_path
df = pd.read_csv(file_path)

# 获取 CSV 文件名前缀作为图片标题
title = file_path.split('/')[-1].replace('.csv', '')

# 将 C_abundance 和 T_abundance 转换为百分比
df['C_abundance_percentage'] = df['C_abundance'] * 100
df['T_abundance_percentage'] = df['T_abundance'] * 100

# 从命令行参数获取 C_abundance_gt 和 T_abundance_gt 常量
C_abundance_gt = args.C_abundance_gt
T_abundance_gt = args.T_abundance_gt

# 生成折线图
plt.figure(figsize=(10, 6))

# 画 C_abundance 和 T_abundance 折线图
plt.plot(df['file_name'], df['C_abundance_percentage'], label='C Abundance (%)', color='blue', marker='o')
plt.plot(df['file_name'], df['T_abundance_percentage'], label='T Abundance (%)', color='orange', marker='o')

# 画 C_abundance_gt 和 T_abundance_gt 常量线，换颜色并增加线宽
plt.axhline(C_abundance_gt, color='red', linestyle='--', linewidth=2, label='C_abundance_gt')
plt.axhline(T_abundance_gt, color='cyan', linestyle='--', linewidth=2, label='T_abundance_gt')

# 在虚线旁边添加数值标注，移到图片左边
plt.text(len(df) +20, C_abundance_gt + 1, f'{C_abundance_gt}', color='red', va='center', fontsize=10, fontweight='bold')
plt.text(len(df) +20, T_abundance_gt + 1, f'{T_abundance_gt}', color='cyan', va='center', fontsize=10, fontweight='bold')


# 设置标题、标签和图例
plt.title(f'{title}')
plt.xlabel('File Name')
plt.ylabel('Abundance (%)')
plt.xticks(rotation=45)
plt.legend()

# 保存为 JPG 文件
jpg_file_path = f'./gt{title}.jpg'
plt.tight_layout()
plt.savefig(jpg_file_path)

print(f'Saved {jpg_file_path}')
# 显示图表
# plt.show()
