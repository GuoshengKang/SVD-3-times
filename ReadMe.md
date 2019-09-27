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
4. **做三次SVD**
  * **第一次**: [do_svd_one.py](do_svd_one.py)
    * **Input**: Amxn1.txt
    * **Output**: B_n1xk1.txt，$B_{n_{1} \times k_{1}}=\biggl( V_{n_{1} \times k_{1}} \Sigma_{k_{1} \times k_{1}}^{-1}\biggl)$
  * **第二次**: [do_svd_two.py](do_svd_two.py)
    * **Input**: Amxn2.txt
    * **Output**: B_n2xk2.txt，$B_{n_{2} \times k_{2}}=\biggl( V_{n_{2} \times k_{2}} \Sigma_{k_{2} \times k_{2}}^{-1}\biggl)$
  * **第三次**: [do_svd_three.py](do_svd_three.py)
    * **Input**: Amxn1.txt，B_n1xk1.txt，Amxn2.txt，B_n2xk2.txt
    * **Output**: B_n3xk3.txt，$B_{n_{3} \times k_{3}}=\biggl( V_{(k_{1}+k_{2}) \times k} \Sigma_{k \times k}^{-1}\biggl)$
5. **结果合并**: [dim_reduction_matrix.py](dim_reduction_matrix.py)
    * **Input**: B_n1xk1.txt，B_n2xk2.txt，B_n3xk3.txt
    * **Output**: reduction_mat.txt，
$reduction\_mat=
\begin{bmatrix}
\biggl( V_{n_{1} \times k_{1}} \Sigma_{k_{1} \times k_{1}}^{-1}\biggl)\biggl(V_{k_{1} \times k} \Sigma_{k \times k}^{-1}\biggr) \\
\biggl(V_{n_{2} \times k_{2}} \Sigma_{k_{2} \times k_{2}}^{-1}\biggr)\biggl(V_{k_{2} \times k} \Sigma_{k \times k}^{-1}\biggr)
\end{bmatrix}_{n \times k}$

## 数学推导
$A_{m \times n} = [A_{m \times n_{1}} \quad A_{m \times n_{2}}]$，其中$n = n_{1} + n_{2}$

SVD分解公式: $A_{m \times n} = U_{m \times m} \Sigma_{m \times n} V_{n \times n}^\mathrm{T} \Rightarrow A_{m \times n} \approx U_{m \times k} \Sigma_{k \times k} V_{k \times n}^\mathrm{T} \Rightarrow A_{m \times n} V_{k \times n} \Sigma_{k \times k}^{-1} \approx U_{m \times k}$

同理: $A_{m \times n_{1}}$和$A_{m \times n_{2}}$分别做SVD
$$A_{m \times n_{1}} = U_{m \times m} \Sigma_{m \times n_{1}} V_{n_{1} \times n_{1}}^\mathrm{T} \Rightarrow A_{m \times n_{1}} \biggl( V_{n_{1} \times k_{1}} \Sigma_{k_{1} \times k_{1}}^{-1}\biggl) \approx U_{m \times k_{1}}$$

$$A_{m \times n_{2}} = U_{m \times m} \Sigma_{m \times n_{2}} V_{n_{2} \times n_{2}}^\mathrm{T} \Rightarrow A_{m \times n_{2}} \biggl(V_{n_{2} \times k_{2}} \Sigma_{k_{2} \times k_{2}}^{-1}\biggr) \approx U_{m \times k_{2}}$$

$A_{m \times n_{1}}$和$A_{m \times n_{2}}$的降维结果$U_{m \times k_{1}}$和$U_{m \times k_{2}}$拼接起来再做一次SVD

$$U_{m \times (k_{1}+k_{2})} =[U_{m \times k_{1}}\quad U_{m \times k_{2}}]= U_{m \times m} \Sigma_{m \times (k_{1}+k_{2})} V_{(k_{1}+k_{2}) \times (k_{1}+k_{2})}^\mathrm{T} \\ \Rightarrow U_{m \times (k_{1}+k_{2})} \biggl(V_{(k_{1}+k_{2}) \times k} \Sigma_{k \times k}^{-1}\biggr) \approx U_{m \times k}$$

因此，$A_{m \times n_{1}}$和$A_{m \times n_{2}}$分别降维，然后拼起来的结果再次降维，有:
$$A_{m \times n} = {[A_{m \times n_{1}}\quad A_{m \times n_{2}}]}_{m \times n}$$

$$\approx \biggl[A_{m \times n_{1}}\biggl( V_{n_{1} \times k_{1}} \Sigma_{k_{1} \times k_{1}}^{-1}\biggl) \quad A_{m \times n_{2}}\biggl(V_{n_{2} \times k_{2}} \Sigma_{k_{2} \times k_{2}}^{-1}\biggr) \biggr]_{m \times n}$$

$$\approx \biggl[A_{m \times n_{1}}\biggl( V_{n_{1} \times k_{1}} \Sigma_{k_{1} \times k_{1}}^{-1}\biggl)\biggl(V_{k_{1} \times k} \Sigma_{k \times k}^{-1}\biggr) + A_{m \times n_{2}}\biggl(V_{n_{2} \times k_{2}} \Sigma_{k_{2} \times k_{2}}^{-1}\biggr)\biggl(V_{k_{2} \times k} \Sigma_{k \times k}^{-1}\biggr) \biggr]_{m \times k}$$

目标降维矩阵为: 
$$\begin{bmatrix}
\biggl( V_{n_{1} \times k_{1}} \Sigma_{k_{1} \times k_{1}}^{-1}\biggl)\biggl(V_{k_{1} \times k} \Sigma_{k \times k}^{-1}\biggr) \\
\biggl(V_{n_{2} \times k_{2}} \Sigma_{k_{2} \times k_{2}}^{-1}\biggr)\biggl(V_{k_{2} \times k} \Sigma_{k \times k}^{-1}\biggr)
\end{bmatrix}_{n \times k}$$


## 注意
1. 最后的目标降维矩阵应为一个列块矩阵，由于Latex换行(即"\\\\")无法兼容显示，所以显示成了行块矩阵
2. Chrome的插件"GitHub with MathJax"可以在浏览器解析Tex公式，但是没装插件的可能看着还是源码。Chrome官方插件应用商店的地址: <https://chrome.google.com/webstore/category/extensions?hl=zh-CN>





​​