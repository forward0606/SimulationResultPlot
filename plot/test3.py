import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# 创建一个示例数据框
data = {'Category': ['A', 'A', 'B', 'B', 'C', 'C'], 'Value': [3, 7, 5, 9, 2, 6]}
df = pd.DataFrame(data)

# 绘制箱线图
sns.boxplot(x='Category', y='Value', data=df)
plt.show()
