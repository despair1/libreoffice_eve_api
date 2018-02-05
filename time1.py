'''
Created on 24.09.2011

@author: mayor
'''

from datetime import datetime,timedelta

def str2time(string):
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
def str2daytime(string):
    return datetime.strptime(string, "%Y-%m-%d")

def time2str(tm):
    return tm.strftime("%Y-%m-%d %H:%M:%S")
def daytime2str(tm):
    return tm.strftime("%Y-%m-%d")

"""
td=timedelta(days=-1)
tm=str2time("2011-09-23 18:06:08")
print tm
tm=datetime(tm.year,tm.month,tm.day)

print tm
for i in range(30):
    tm=tm+td
    print time2str(tm)
   """ 
    