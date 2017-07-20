#!/usr/bin/user_gender
#-*-coding:utf-8-*-
import numpy as np
from numpy import *
import pandas as pd
import pprint
import pickle
from sklearn import preprocessing
import datetime

starttime = datetime.datetime.now()
print 'reading file ...'
B_n1xk1=np.loadtxt('B_n1xk1.txt',delimiter=',',skiprows=0)
B_n2xk2=np.loadtxt('B_n2xk2.txt',delimiter=',',skiprows=0)
B_n3xk3=np.loadtxt('B_n3xk3.txt',delimiter=',',skiprows=0)
print "%s time has beed used for reading file ..." % (datetime.datetime.now() - starttime)
n1,k1=B_n1xk1.shape
n2,k2=B_n2xk2.shape
print B_n1xk1.shape,B_n2xk2.shape,B_n3xk3.shape
#[3000,745],[2934,689],[1434,1083]
arr1=mat(B_n1xk1)*mat(B_n3xk3[:k1,:])
arr2=mat(B_n2xk2)*mat(B_n3xk3[k1:,:])
reduction_mat=np.r_[arr1,arr2]
print reduction_mat.shape
#[5934,1083]
np.savetxt('reduction_mat.txt',reduction_mat,fmt='%.9f',delimiter=',')
np.save('reduction_mat.npy',reduction_mat)
print "end saving results of reduction: %s time has beed used ..." % (datetime.datetime.now() - starttime)
