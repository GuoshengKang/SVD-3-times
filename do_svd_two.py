#!/usr/bin/user_gender
#-*-coding:utf-8-*-
import numpy as np
from numpy import *
import pandas as pd
import pprint
import pickle
from sklearn import preprocessing
import datetime

def find_k_dim(arr):
    arr = arr ** 2
    total = sum(arr)
    arr = arr.cumsum()
    threshold = 0.9 * total
    for index, item in enumerate(arr):
        if item >= threshold:
            return index+1

starttime = datetime.datetime.now()
print 'reading file ...'
arr=np.loadtxt('Amxn2.txt',delimiter=',',skiprows=1)
print "%s time has beed used for reading file ..." % (datetime.datetime.now() - starttime)
print arr.shape

print "-- start SVD --"
starttime = datetime.datetime.now()
U,Sigma,VT=np.linalg.svd(arr)
print "-- end SVD --: %s time has beed used..." % (datetime.datetime.now() - starttime)

k=find_k_dim(Sigma)
print 'there are %d columns after reducing dimensions!!!' % k

print "start saving results of SVD"
Sigk=mat(eye(k)*Sigma[:k])
V_nxk=VT[:k,:].T #np.shape(V_nxk)转置
Bnxk=V_nxk*Sigk.I #n*6
np.savetxt('B_n2xk2.txt',Bnxk,fmt='%.9f',delimiter=',')
print Bnxk.shape
print "end saving results of SVD: %s time has beed used ..." % (datetime.datetime.now() - starttime)
