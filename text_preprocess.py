#!/usr/bin/python
# -+- coding: utf-8 -+-
import re,os
import pickle
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
starttime = datetime.datetime.now()

def split_dict(dict_str):
  keywords=[]
  dict_str=dict_str.strip('{}')
  dict_list=dict_str.split(unicode(';','utf-8'))
  for d in dict_list:
    keyword,value=d.split(unicode(':','utf-8'))
    if keyword.isdigit():
      pass #去掉数字关键词
    else:
      keywords.append(keyword)
  return keywords

input_file_path= os.path.join(os.path.split(os.path.realpath(__file__))[0], "raw_samples_50000_front.csv")
output_file_path= os.path.join(os.path.split(os.path.realpath(__file__))[0], "samples_50000.csv")
dictionary_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "dictionary.txt")

fout=open(output_file_path,'w')

dictionary=set() #所有的词汇
line_no=0
with open(input_file_path, "r") as fin:
  for line in fin.readlines():
    line_no+=1
    line=unicode(line.strip(), "utf-8")
    uid,token_t= line.split(unicode(',','utf-8'))
    if token_t!=u'NULL':
      keywords=split_dict(token_t)
    else:
      keywords=[]
    dictionary=dictionary|set(keywords)
    new_line='|'.join(keywords).encode('utf-8')
    fout.write(new_line+'\n')

dict_fout=open(dictionary_path,'w')
for keyword in dictionary:
  dict_fout.write(keyword.encode('utf-8')+'\n')
dict_fout.close()

print "There are %d keywords in dictionary!!!"%len(dictionary)
print "There are %d lines in output file!!!"%line_no

endtime = datetime.datetime.now()
print "There are %s time used!!!"%(endtime - starttime) #0:00:00.280797
print "Finished!!!!"