import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# 设定中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 导入文件
data1 = pd.read_excel('附件 1.xlsx')
data2 = pd.read_excel('附件 2.xlsx')
data3 = pd.read_excel('附件 3.xlsx')
data4 = pd.read_excel('附件 4.xlsx')

# 获取损耗率
break_rate = data4['损耗率(%)']
# 初始化列表
class_list = [0.0] * 251
profit_list = np.array([class_list] * 1095)
cost_list = np.array([class_list] * 1095)
quantity_list = np.array([class_list] * 1095)
# 设置起始时间
time0 = datetime.datetime.strptime('2020-07-01', "%Y-%m-%d")
# 处理数据
for i in range(len(data2)):
    if i % 10000 == 0:
        print(i)
# 将日期转换为 datetime 格式并计算与起始时间的天数差
time_tmp = datetime.datetime.strptime(data2.iloc[i][0], "%Y-%m-%d")
index_1 = data_timedelta = (time_tmp - time0).days
# 在 data1 中找到对应单品编码的索引
index_2 = data1[data1['单品编码'] == data2.iloc[i][2]].index[0]
# 计算利润、成本和数量
sum_money = (data2.iloc[i, 4] - data3[(data3['单品编码'] == data2.iloc[i, 2]) &(data3['销售日期'] == data2.iloc[i, 0])].iloc[0, 2]) * data2.iloc[i, 3]
cost_money = (data3[(data3['单品编码'] == data2.iloc[i, 2]) & (data3['销售日期'] == data2.iloc[i, 0])].iloc[0, 2]) * data2.iloc[i, 3]
profit_list[index_1][index_2] += sum_money
cost_list[index_1][index_2] += cost_money
quantity_list[index_1][index_2] += data2.iloc[i, 3]

# 读取文件
df_cost_list = pd.read_csv('cost.csv')
df_profit_list = pd.read_csv('profit.csv')
df_quantity_list = pd.read_csv('quantity.csv')
profit_list = df_profit_list.values

# 计算利润和数量的均值
sort_avg_profit_list = pd.DataFrame(sum(profit_list) / 1095)
quantity_list = df_quantity_list.values
sort_avg_quantity_list = pd.DataFrame(sum(quantity_list) / 1095)
# 将均值保存为 CSV 文件
sort_avg_quantity_list.to_csv('mean.csv')

# 绘制直方图（图九）
plt.hist(sort_avg_quantity_list, bins=20)
plt.show()

# 计算单价
unit_price = sum(profit_list) / sum(quantity_list)

# 绘制直方图并设置 x 轴范围（图十）
plt.hist(unit_price, bins=100)
plt.xlim(0, 50)
# 初始化列表
break_rate_list = [0.0] * 251
# 计算损耗率
for i in range(len(break_rate)):
    index_3 = data1[data1['单品名称'] == break_rate.iloc[i, 1]].index[0]
    break_rate_list[index_3] = break_rate.iloc[i, 2]
# 重新设置起始时间
time0 = datetime.datetime.strptime('2020-07-01', "%Y-%m-%d")
# 处理数据
for i in range(len(data2)):
    if i % 10000 == 0:
        print(i)
time_tmp = datetime.datetime.strptime(data2.iloc[i][0], "%Y-%m-%d")
index_1 = data_timedelta = (time_tmp - time0).days
index_2 = data1[data1['单品编码'] == data2.iloc[i][2]].index[0]
sum_money = (data2.iloc[i, 4] - data3[(data3['单品编码'] == data2.iloc[i, 2]) &(data3['销售日期'] == data2.iloc[i, 0])].iloc[0, 2]) * data2.iloc[i, 3]
cost_money = (data3[(data3['单品编码'] == data2.iloc[i, 2]) & (data3['销售日期'] == data2.iloc[i, 0])].iloc[0, 2]) * data2.iloc[i, 3]
profit_list[index_1][index_2] += sum_money
cost_list[index_1][index_2] += cost_money
quantity_list[index_1][index_2] += data2.iloc[i, 3]
# 初始化列表
break_rate_list = [0.0] * 251
# 计算损耗率
for i in range(len(break_rate)):
    index_3 = data1[data1['单品编码'] == break_rate.iloc[i, 1]].index[0]
    break_rate_list[index_3] = break_rate.iloc[i, 2]
# 读取结果文件
dst_data = pd.read_excel('result3.xlsx')

# 绘制直方图并添加参考线（图十一）
plt.hist(dst_data.iloc[:, 6], bins=30)
plt.plot([2.5, 2.5], [0, 150], '--')
# 读取可售文件
onsale_data = pd.read_excel('onsale.xlsx')
# 初始化列表
onsale_list = [0] * 251
# 设置可售标志
for i in range(len(break_rate)):
    index_3 = data1[data1['单品编码'] == onsale_data.iloc[i, 1]].index[0]
    onsale_list[index_3] = 1
# 将可售标志保存为 CSV 文件
pd.DataFrame(onsale_list).to_csv('onsale.csv')

#额外图：
#绘制各菜品销售额饼形图

data1 = pd.read_excel(r'附件 1.xlsx')
data2 = pd.read_excel(r'附件 2.xlsx')

category_codes = [1011010101, 1011010201, 1011010402, 1011010501, 1011010504, 1011010801]
product_codes = data1['单品编码']
category_dict = dict(zip(data1['单品编码'], data1['分类编码']))
# 将附件 2 中的单品编码转化为分类编码，便于聚合不同的菜品
data2['单品编码'] = data2['单品编码'].replace(category_dict)
grouped_data = data2.groupby(data2['单品编码'])['销售金额'].sum()
product_codes = grouped_data.index.tolist() # 获取单品编码列表
vegetables = ['花叶类', '食用菌', '辣椒类', '茄类', '水生根茎类', '花菜类']#对应作图时的各分类编码
plt.figure()
#plt.pie(grouped_data, labels=product_codes, autopct='%1.1f%%')#观察各分类编码位置
plt.pie(grouped_data, labels=vegetables, autopct='%1.1f%%')
plt.title('2020 年至 2023 年各菜品类销售金额（元）')
plt.savefig("test1.png", dpi=600)
plt.show()

#提取销售类型为退货的行并转化为时间段（图十二）
data1 = pd.read_excel(r'附件 1.xlsx')
data2 = pd.read_excel(r'附件 2.xlsx')
#将单品编码转化为分类编码
category_codes = [1011010101, 1011010201, 1011010402, 1011010501, 1011010504, 1011010801]
product_codes = data1['单品编码']
category_dict = dict(zip(data1['单品编码'], data1['分类编码'])) # 通过zip函数打包两个 Series 来创建字典
data2['单品编码'] = data2['单品编码'].replace(category_dict)
# 将时间字符串转换为小时数的函数
def convert_to_hours(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M:%S.%f")
    hours = time_obj.hour + time_obj.minute / 60 + time_obj.second / 3600
    return hours

# 获取退货小时数
df1 = data2[data2['销售类型'] == '退货']
df1['小时数'] = df1['扫码销售时间'].apply(convert_to_hours)
morning = df1[(df1['小时数'] >= 9) & (df1['小时数'] < 12)]
afternoon = df1[(df1['小时数'] >= 12) & (df1['小时数'] < 17)]
night = df1[(df1['小时数'] >= 17) & (df1['小时数'] <= 22)]

#获取退货不同菜品数量
'''花叶类': Flowering Leafy Vegetables
'食用菌': Edible Mushrooms
'辣椒类': Pepper Varieties
'茄类': Eggplant Varieties
'水生根茎类': Aquatic Tubers and Rhizomes
'花菜类': Cauliflower Varieties''' 
FLV = df1[df1['单品编码'] == 1011010101]
EM = df1[df1['单品编码'] == 1011010801]
PV = df1[df1['单品编码'] == 1011010504]
EV = df1[df1['单品编码'] == 1011010501]
ATR = df1[df1['单品编码'] == 1011010402]
CV = df1[df1['单品编码'] == 1011010201]

#作图
plt.figure()
fig, axs = plt.subplots(2, 3)
axs[0, 0].scatter(FLV['小时数'], FLV['销量(千克)'])
axs[0, 0].set_title('花叶类(FLV)')
axs[0, 0].set_xlabel('小时数')
axs[0, 0].set_ylabel('销量(千克)')
axs[0, 1].scatter(EM['小时数'], EM['销量(千克)'])
axs[0, 1].set_title('食用菌(EM)')
axs[0, 1].set_xlabel('小时数')
axs[0, 1].set_ylabel('销量(千克)')
axs[0, 2].scatter(PV['小时数'], PV['销量(千克)'])
axs[0, 2].set_title('辣椒类(PV)')
axs[0, 2].set_xlabel('小时数')
axs[0, 2].set_ylabel('销量(千克)')
axs[1, 0].scatter(EV['小时数'], EV['销量(千克)'])
axs[1, 0].set_title('茄类(EV)')
axs[1, 0].set_xlabel('小时数')
axs[1, 0].set_ylabel('销量(千克)')
axs[1, 1].scatter(ATR['小时数'], ATR['销量(千克)'])
axs[1, 1].set_title('水生根茎类(ATR)')
axs[1, 1].set_xlabel('小时数')
axs[1, 1].set_ylabel('销量(千克)')
axs[1, 2].scatter(CV['小时数'], CV['销量(千克)'])
axs[1, 2].set_title('花菜类(CV)')
axs[1, 2].set_xlabel('小时数')
axs[1, 2].set_ylabel('销量(千克)')

plt.suptitle('不同菜品退货量的时间分布', fontsize=16)
plt.tight_layout()
plt.show()