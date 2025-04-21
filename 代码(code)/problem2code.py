#观察各蔬菜品类的成本加成定价与销售总量的关系
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn import metrics

plt.rcParams['font.family'] = 'SimHei'

# 导入数据
data1 = pd.read_excel(r'附件 1.xlsx')
data2 = pd.read_excel(r'附件 2.xlsx')
data3 = pd.read_excel(r'附件 3.xlsx')

category_codes = [1011010101, 1011010201, 1011010402, 1011010501, 1011010504, 1011010801]
product_codes = data1['单品编码']
category_dict = dict(zip(data1['单品编码'], data1['分类编码']))
# 将附件 2 中的单品编码转化为分类编码，获得各菜品的销售总量
data2['单品编码'] = data2['单品编码'].replace(category_dict)
grouped_data = data2.groupby(data2['单品编码'])['销量(千克)'].sum()
# 成本加成定价 x,成本加成率（利率）w,（平均成本）c，公式：x = c *（1 + w）
data3['单品编码'] = data3['单品编码'].replace(category_dict)
cost_mean = data3.groupby(data3['单品编码'])['批发价格(元/千克)'].mean()#各菜品平均成本
selling_prices = data2.groupby(data2['单品编码'])['销售单价(元/千克)'].sum()#各菜品的总销售单价
cost = data3.groupby(data3['单品编码'])['批发价格(元/千克)'].sum()#各菜品的总批发价格
markup_rate = (selling_prices - cost)/cost#成本加成率
markup_price = cost_mean * (1 + markup_rate)

#成本加成定价作 x 轴，各菜品的销售总量作 y 轴（图六）
plt.figure()
plt.title('各蔬菜品类的销售总量与成本加成定价分析图')
plt.plot(markup_price, grouped_data, 'b', lw = 5)
plt.xlabel('成本加成定价（元）')
plt.ylabel('各菜品销售总量（千克）')
plt.grid(True)
plt.show()

#以花叶菜为例处理成本加成定价与销售总量关系
data1 = pd.read_excel(r'合并后的附件.xlsx')
data2 = pd.read_excel(r'附件 1.xlsx')
#category_name = ['花叶类', '花菜类', '水生根茎类', '茄类', '辣椒类', '食用菌']
# 获取花叶类的单品编码
data4 = data2[data2['分类名称'] == '食用菌']
list1 = data4['单品编码'].to_list()
# 计算成本加成定价
cost_mean = data1[data1['单品编码'].isin(list1)].groupby('单品编码')['批发价格(元/千克)'].mean() # 平均成本
selling_prices = data1[data1['单品编码'].isin(list1)].groupby('单品编码')['销售单价(元/千克)'].sum() # 总销售单价
cost = data1[data1['单品编码'].isin(list1)].groupby('单品编码')['批发价格(元/千克)'].sum() # 总批发价格
markup_rate = (selling_prices - cost) / cost # 成本加成率
markup_price = cost_mean * (1 + markup_rate) # 成本加成定价
# 计算单品的销售总量
grouped_data = data1[data1['单品编码'].isin(list1)].groupby('单品编码')['销量(千克)'].sum()
# 用散点图可视化其关系（图七）
plt.figure(figsize = (5, 5))
plt.scatter(markup_price, grouped_data, c = 'r', marker='o', label = '食用菌')
plt.xlabel('成本加成定价（元）')
plt.ylabel('销售总量（千克）')
plt.legend()
plt.grid(True)
plt.show()

# 使用曲线拟合作出其拟合函数
def exponential_func(x, a, b):
    return a * np.exp(b * x)
popt, pcov = curve_fit(exponential_func, markup_price, grouped_data) # type: ignore
a = popt[0]          
b = popt[1]
print(f"拟合函数：y = {a} * exp({b}x)")
# 敏感性分析
# 定义待分析的参数范围 
grouped_data_range = [100, 200, 300] # 分组数据的范围
markup_price_range = [0.1, 0.2, 0.3] # 加价率的范围
# 定义模拟次数
num_simulations = 1000
# 定义用于记录输出结果的列表
output_results = []
# 进行 Monte Carlo 模拟
for _ in range(num_simulations):
    # 随机选择参数数值
    grouped_data = np.random.choice(grouped_data_range)
    markup_price = np.random.uniform(markup_price_range[0], markup_price_range[1])
    # 执行模型计算，计算总销售额
    profit = grouped_data * markup_price
    # 记录输出结果
    output_results.append(profit)
    # 输出敏感性分析结果
    mean_profit = np.mean(output_results)
    std_profit = np.std(output_results)
    print("平均销售额：", mean_profit)
    print("销售额标准差：", std_profit)

#ARIMA 模型预测未来 7 天销量（以花叶类为例）（图八）
data2 = pd.read_excel(r'花叶类 6 月.xlsx')
# 设置索引列
data2 = data2[['销售日期', '销量(千克)']]
data2 = data2.set_index('销售日期')
# 计算差分并去除缺失值
data2['salesDiff_1'] = data2['销量(千克)'].diff(1)
data2['salesDiff_2'] = data2['salesDiff_1'].diff(1)
data2 = data2.dropna()
# 绘制原始数据和差分数据
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))
data2['销量(千克)'].plot(ax=axes[0])
axes[0].set_ylabel('销量(千克)')
data2['salesDiff_2'].plot(ax=axes[1])
axes[1].set_ylabel('销量差分')
plt.tight_layout()
# 获取差分数据
temp = np.array(data2['salesDiff_2'])
# 创建 ARIMA 模型并拟合数据
model = sm.tsa.ARIMA(temp, order=(2, 0, 0))
results_ARIMA = model.fit()
# 预测未来八天的销量差分值
forecast = results_ARIMA.forecast(steps=8)[0]
# 构建日期索引
idx = pd.date_range(start=data2.index[-1], periods=8, freq='D')
# 将预测结果转换为 DataFrame
forecast_df = pd.DataFrame(forecast, index=idx, columns=['销量差分预测'])
# 计算预测值对应的销量
last_value = data2['销量(千克)'].iloc[-1]
forecast_df['销量预测'] = forecast_df['销量差分预测'].cumsum() + last_value
# 绘制预测结果
plt.figure(figsize=(10, 6))
plt.plot(data2.index, data2['salesDiff_2'], label='销量差分')
plt.plot(data2.index, results_ARIMA.fittedvalues, label='模型拟合')
plt.plot(forecast_df.index, forecast_df['销量差分预测'], label='销量差分预测')
plt.xlabel('日期')
plt.ylabel('销量差分')
plt.legend()
plt.grid(True)
# 打印未来八天的销量预测
print(forecast_df['销量预测'])
# 模型评估
r2 = metrics.r2_score(data2['salesDiff_2'], results_ARIMA.fittedvalues)
print("R-squared:", r2)