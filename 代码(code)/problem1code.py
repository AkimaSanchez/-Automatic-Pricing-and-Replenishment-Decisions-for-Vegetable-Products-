1.2#绘制各菜品之间关系图
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'SimHei'

# 数据导入
data1 = pd.read_excel(r'附件 1.xlsx')
data2 = pd.read_excel(r'附件 2.xlsx')
# data3 = pd.read_excel(r'食用菌 6 月.xlsx')

category_codes = [1011010101, 1011010201, 1011010402, 1011010501, 1011010504, 1011010801]
product_codes = data1['单品编码']
category_dict = dict(zip(data1['单品编码'], data1['分类编码']))

# 绘制各蔬菜单品的相关性
# 对数据按日期进行分组，并计算销量之和
grouped_data1 = data2.groupby([pd.Grouper(key='销售日期', freq='D'), '菜品编码'])['销量(千克)'].sum()
# 将分组后的数据转换为 DataFrame
grouped_df = grouped_data1.reset_index()

# 绘制按季度的可视化图形（图三）
plt.figure(figsize=(12, 6)) # 设置画布大小
for list2 in category_codes:
    df = grouped_df[grouped_df['菜品编码'] == list2]
    plt.plot(df['销售日期'], df['销量(千克)'], label = list2)
    # 设置标题、坐标轴标签和图例
    plt.xlabel('日期')
    plt.ylabel('销量(千克)')
    plt.legend()
    plt.show()

# 将附件 2 中的单品编码转化为分类编码，便于聚合不同的菜品
data2['单品编码'] = data2['单品编码'].replace(category_dict)
grouped_data = data2.groupby(data2['单品编码'])['销量(千克)'].sum()
#product_codes = grouped_data.index.tolist() # 获取单品编码列表,用于观察各菜品对应编号
vegetables = ['花叶类', '食用菌', '辣椒类', '茄类', '水生根茎类', '花菜类']
plt.figure()
#plt.pie(grouped_data, labels=product_codes, autopct='%1.1f%%')# 观察各菜品对应编号
plt.pie(grouped_data, labels=vegetables, autopct='%1.1f%%')
plt.show()

# 计算各菜品之间的相关性系数
# 绘制各菜品之间的热力关系图（图四）
# 对数据按季度进行分组，并计算销量之和
grouped_data3 = data2.groupby([pd.Grouper(key='销售日期', freq='Q'), '单品编码'])['销量(千克)'].sum()
# 将分组后的数据转换为 DataFrame
grouped_df = grouped_data3.reset_index()
# 使用透视表将单品编码作为列，按季度填充销量值
pivot_table = pd.pivot_table(grouped_df, values='销量(千克)', index='销售日期', columns='单品编码', aggfunc='sum')
# 计算相关性系数
correlation_matrix = abs(pivot_table.corr())
# 绘制热图
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
#设置名称
list2 = ['花叶类', '花菜类', '水生根茎类', '茄类', '辣椒类', '食用菌']
plt.xticks(ticks=range(len(list2)), labels=list2, rotation=45)
plt.yticks(ticks=range(len(list2)), labels=list2, rotation=0)
# 设置标题和坐标轴标签
plt.xlabel('各菜品名称')
plt.ylabel('各菜品名称')
plt.show()

'''# 绘制水生根茎类和食用菌折线图（图五）
data3 = data3.set_index('销售日期')
grouped_data4 = data3.resample('Q').sum().to_period('Q')
plt.figure()
grouped_data4.plot(color = 'r') # 直接使用 values 获取数据值
plt.grid(True)
plt.show()'''