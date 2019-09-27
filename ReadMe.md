## 功能介绍

## 实现步骤
1. 获取数据：[query_samples.sql](query_samples.sql)
2. [txt2df.py](txt2df.py)
  * Function: 文本数据转为矩阵
  * Input:
    * [samples_50000.csv](samples_50000.csv): 50000条样本数据
    * [dictionary.txt](dictionary.txt): 5934个特征，即关键词
  * OUtput:
    * [column_names.txt](column_names.txt): DataFrame的列名，即特征与[dictionary.txt](dictionary.txt)一致
    * Amxn.txt: DataFrame保存为txt文件,50000x5934
    * Amxn1.txt: Amxn1=df.ix[:,:n1]，其中n1=3000
    * Amxn2.txt: Amxn2=df.ix[:,n1:]，其中n2=5934-3000=2934


输入$\sqrt{x^{2}}$ 

$$\sqrt 4 = \sqrt[3]{8} = 2$$

\[
\sqrt[n]{\frac{x^2+\sqrt 2}{x+y}}
\]

![](http://latex.codecogs.com/gif.latex?\\sigma=\sqrt{\frac{1}{n}{\sum_{k=1}^n(x_i-\bar{x})^2}})


​​