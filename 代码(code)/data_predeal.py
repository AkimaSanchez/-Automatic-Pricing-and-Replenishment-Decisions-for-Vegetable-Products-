import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'SimHei'

# 数据导入
data1 = pd.read_excel(r'附件 1.xlsx')
data2 = pd.read_excel(r'附件 2.xlsx')
data3 = pd.read_excel(r'附件 3.xlsx')
data4 = pd.read_excel(r'附件 4.xlsx')# 附件4用excel处理

# 查看各表格是否具有异常值（图一）
plt.figure(figsize = (10, 10))
fig, axs = plt.subplots(1, 3)
axs[0].boxplot(data2['销量(千克)'])
axs[0].set_title('销量(千克)')
axs[0].grid(True)
axs[1].boxplot(data2['销售单价(元/千克)'])
axs[1].set_title('销售单价(元/千克)')
axs[1].grid(True)
axs[2].boxplot(data3['批发价格(元/千克)'])
axs[2].set_title('批发价格(元/千克)')
#axs[3].boxplot(data4['损耗率(%)'])
#axs[3].set_title('损耗率(%)')
axs[2].grid(True)
plt.tight_layout()
plt.show()

# 查看各表格是否存在缺失值（图二）
data1 = pd.read_excel(r'附件 1.xlsx')
data2 = pd.read_excel(r'附件 2.xlsx')
data3 = pd.read_excel(r'附件 3.xlsx')
#data4 = pd.read_excel(r'附件 4.xlsx')

# 查看各表格关键数据
print(data2['销量(千克)'].isnull().sum())
print(data2['销售单价(元/千克)'].isnull().sum())
print(data3['批发价格(元/千克)'].isnull().sum())
#print(data4['损耗率(%)'].isnull().sum())
# 使用 excel 处理异常值与空值与附件 4