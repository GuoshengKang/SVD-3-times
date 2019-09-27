## 功能介绍

## 实现步骤
1. 获取数据: [**query_samples.sql**](query_samples.sql)
2. [**text_preprocess.py**](text_preprocess.py)
  * **Function**: 处理数据，将原始Hive中导出的数据处理成规范的分词数据
  * **Input**:
    * raw_samples_50000_front.csv
  * **Output**:
    * samples_50000.csv
    * [dictionary.txt](dictionary.txt)
3. [**txt2df.py**](txt2df.py)
  * **Function**: 文本数据转为矩阵
  * **Input**:
    * [samples_50000.csv](samples_50000.csv): 50000条样本数据
    * [dictionary.txt](dictionary.txt): 5934个特征，即关键词
  * **Output**:
    * [column_names.txt](column_names.txt): DataFrame的列名，即特征，与[dictionary.txt](dictionary.txt)一致
    * Amxn.txt: DataFrame保存为txt文件,50000x5934
    * Amxn1.txt: Amxn1=df.ix[:,:n1]，其中n1=3000
    * Amxn2.txt: Amxn2=df.ix[:,n1:]，其中n2=5934-3000=2934


**注**：Chrome的插件"GitHub with MathJax"可以在你自己的浏览器解析tex公式，但是没装插件的人看着还是源码。Chrome官方插件应用商店的地址: <https://chrome.google.com/webstore/category/extensions?hl=zh-CN>





​​