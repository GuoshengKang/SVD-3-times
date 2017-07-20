#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import os,sys
from pandas import Series,DataFrame
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')
starttime = datetime.datetime.now()    
######################################################        
samples_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "samples_50000.csv")
fin=open(samples_path)
lines=fin.readlines()
row_num=len(lines) #文件的行数
print "There are %d lines in the input file!!!"%row_num

dictionary_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "dictionary.txt")
dictionary=[]
with open(dictionary_path, "r") as fin:
  for line in fin.readlines():
    line=unicode(line.strip(), "utf-8")
    dictionary.append(line)
print "There are %d keywords in the dictionary!!!"%len(dictionary)

col_num=len(dictionary)
df=DataFrame(np.zeros((row_num,col_num)),columns=dictionary)

for row,line in enumerate(lines): #row：0,1,2,3,...
  line=unicode(line.strip(),'utf-8')
  keywords_list=line.split(unicode('|','utf-8'))
  for element in keywords_list:
    if element in dictionary:
      df.ix[row,element]=1 #自动添加列

df.fillna(0,inplace=True) #默认不为NAN,而是为0

columns_path=os.path.join(os.path.split(os.path.realpath(__file__))[0], "column_names.txt")
columns_fout=open(columns_path,'w')
for column_name in df.columns: #将列名写到文件
    columns_fout.write(column_name+'\n')
columns_fout.close()

Amxn_path=type_industry_labels_path=os.path.join(os.path.split(os.path.realpath(__file__))[0], "Amxn.txt")
df.to_csv(Amxn_path,index=False) #将表格写到文件
fin.close()
print df.columns
print df.shape #输出表格的行列数

n1=3000
n2=col_num-n1
Amxn1_path=type_industry_labels_path=os.path.join(os.path.split(os.path.realpath(__file__))[0], "Amxn1.txt")
Amxn1=df.ix[:,:n1]
Amxn1.to_csv(Amxn1_path,index=False)
print Amxn1.shape #输出表格的行列数
Amxn2_path=type_industry_labels_path=os.path.join(os.path.split(os.path.realpath(__file__))[0], "Amxn2.txt")
Amxn2=df.ix[:,n1:]
Amxn2.to_csv(Amxn2_path,index=False)
print Amxn2.shape #输出表格的行列数

#####################################################
endtime = datetime.datetime.now()
print (endtime - starttime),"time used!!!" #0:00:00.280797