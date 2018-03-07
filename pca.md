```
#!/usr/bin/python
# -*- coding: utf-8 -*-
# 没有这句的话,有中文注释会报错
import numpy as np
import os
from numpy import *
from sklearn.decomposition import PCA

data_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "data.txt")
arr=np.loadtxt(data_path,delimiter=',')
row,col=arr.shape #(200L, 8L)
X=arr[:,:col-1]  #(200L, 7L)

pca = PCA(n_components=0.85, copy=True, whiten=False)
pca.fit(X)
print pca  #打印模型的输入参数
print "The estimated number of components:",pca.n_components_
print pca.explained_variance_ #(4L,)
#以下两个输出是一样的
print pca.explained_variance_/sum(pca.explained_variance_)
print pca.explained_variance_ratio_
#输出总的贡献率
print sum(pca.explained_variance_ratio_) 

print "="*50
transform_X_1=pca.fit_transform(X) #(200L, 4L)
components=pca.components_ #(4L, 7L)
transform_X_2=mat(X)*components.T
print transform_X_1.shape,transform_X_2.shape
print type(transform_X_1),type(transform_X_2)
print "="*50
print transform_X_1[0,:]
print array(transform_X_2[0])[0,:]
print "-"*50
print transform_X_1[1,:]
print array(transform_X_2[1])[0,:]
print "-"*50
print transform_X_1[2,:]
print array(transform_X_2[2])[0,:]
print "="*50
original_X_1=pca.inverse_transform(transform_X_1)
original_X_2=pca.inverse_transform(transform_X_2)
print original_X_1.shape,original_X_1.shape
print type(original_X_1),type(original_X_2)
print "="*50
print X[0,:]
print original_X_1[0,:]
print array(original_X_2[2])[0,:]
```
###output：
PCA(copy=True, iterated_power='auto', n_components=0.85, random_state=None,
  svd_solver='auto', tol=0.0, whiten=False)
The estimated number of components: 4
[  5.12457453e-05   4.19857453e-05   3.20471371e-05   2.47107956e-05]
[ 0.34166239  0.27992471  0.21366265  0.16475025]
[ 0.32447423  0.26584241  0.20291382  0.15646209]
0.949692541506
==================================================
(200L, 4L) (200L, 4L)
<type 'numpy.ndarray'> <class 'numpy.matrixlib.defmatrix.matrix'>
==================================================
[ 0.00336155  0.00098805 -0.00741123 -0.00084624]
[ 0.00268792  0.00106002 -0.00723514 -0.00110276]
--------------------------------------------------
[-0.00884608  0.00651622  0.00548224 -0.00612608]
[-0.00951971  0.00658819  0.00565833 -0.00638259]
--------------------------------------------------
[ 0.00336197  0.00098824 -0.00741082 -0.00084717]
[ 0.00268835  0.00106021 -0.00723473 -0.00110368]
==================================================
(200L, 7L) (200L, 7L)
<type 'numpy.ndarray'> <class 'numpy.matrixlib.defmatrix.matrix'>
==================================================
[-0.00601349  0.00130851 -0.00513239  0.00418759  0.00437646  0.00239737  0.00168079]
[-0.006065    0.00128792 -0.00511145  0.00433285  0.0043688   0.00242727  0.00168047]
[-0.00608976  0.00128136 -0.00487651  0.00440775  0.00438789  0.0018523   0.00127624]
[Finished in 1.0s]

