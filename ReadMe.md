## 功能介绍
针对维度较高的数据，在做SVD降维时非常耗内存和CPU，一般配置较低的机器可能无法跑出结果。为解决该问题，本项目将高维特征分割成两部分，分别对其进行降维，然后将降维得到的结果拼接起来再做一次降维，得到最终的结果。这样每次做SVD的维度都在可接受的范围内。本项目得到的最终结果是一个降维矩阵，对新的数据直接乘以该降维矩阵进行降维即可，无需再做SVD的运算。
## 实现步骤
1. **获取数据**: [**query_samples.sql**](query_samples.sql)
2. **处理数据**: [**text_preprocess.py**](text_preprocess.py)，将原始Hive表中导出的数据处理成规范的分词数据
  * **Input**:
    * raw_samples_50000_front.csv
  * **Output**:
    * [samples_50000.csv](samples_50000.csv)
    * [dictionary.txt](dictionary.txt)
3. **文本数据转为矩阵**: [**txt2df.py**](txt2df.py)
  * **Input**:
    * [samples_50000.csv](samples_50000.csv): 50000条样本数据
    * [dictionary.txt](dictionary.txt): 5934个特征，即本项目中为一些关键词
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
  * **Output**: reduction_mat.txt，reduction_mat=
$\begin{bmatrix}
\biggl( V_{n_{1} \times k_{1}} \Sigma_{k_{1} \times k_{1}}^{-1}\biggl)\biggl(V_{k_{1} \times k} \Sigma_{k \times k}^{-1}\biggr) \
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
2. 最后得到的降维矩阵，如配置表所示[config_token_keywords_reduction.csv](config_token_keywords_reduction.csv)。在Hive中将矩阵存储为二维表，通过表的连接操作完成矩阵的乘法运算
3. Chrome的插件"GitHub with MathJax"可以在浏览器解析Tex公式，但是没装插件的可能看着还是源码。Chrome官方插件应用商店的地址: <https://chrome.google.com/webstore/category/extensions?hl=zh-CN>

## 附录
* PCA降维的实现代码: [PCA.py](PCA.py)
  * Input: [data4pca.txt](data4pca.txt)
  * Output: 两种实现方式
    * pca.fit_transform(X)
    * mat(X)*pca.components_.T
* 参考资料
  * [SVD and PCA.pdf](SVD_and_PCA.pdf)
  * [svd_pca.pptx](svd_pca.pptx)

-----
欢迎并感谢您提出宝贵的问题或建议: 点击[**【我要提问】**](https://github.com/guoshengkang/SVD-3-times/issues/new)





​​