#!/usr/bin/user_gender
#-*-coding:utf-8-*-
import numpy as np
import os
from numpy import *
import pandas as pd

keywords_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "column_names.txt")
keywords=[]
with open(keywords_path, "r") as fin:
  for line in fin.readlines():
    line=unicode(line.strip(), "utf-8")
    keywords.append(line)
print "There are %d keywords in the dictionary!!!"%len(keywords)

arr=np.load('reduction_mat.npy')
print arr.shape
row_num,col_num=arr.shape

fout_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "config_token_keywords_reduction.csv")
fout=open(fout_path,'w')

for col in range(col_num):
  category='C'+str(col)
  for row in range(row_num):
    keyword=keywords[row]
    value=str(arr[row,col])
    line=keyword+','+category+','+value
    fout.write(line.encode('utf-8')+'\n')
fout.close()