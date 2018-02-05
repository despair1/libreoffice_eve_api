#coding=Cp1251
'''
Created on 24.09.2011

@author: mayor

считывает данные из апи в бд
'''
#elrond aakiwa
userid="7839269"
apikey="C8CBBA900EAF45F090F9D2409414B75B35F8F169F89A4A2A9C7CB2A241C65127"
keyID=415353
vCode="jcHJPMIYIwieOG9yAqlRbygsMebcBuhY9gZcFttfs1qSDgxLjeZW86bOloYVCpso"
characterid="90806628"

#tiomio
#keyID="394742"
#vCode="Whjdo2MIoF8vOSOCgAhNk47VoBcc5i6gX4k90YwstQ0ZPo0nv1f3AJIs8Emhi839"
#characterid="868961038"
#beforeTransID="2277455445"

import urllib,httplib
import xml.parsers.expat
from sqlite3 import dbapi2 as sqlite
from datetime import datetime
#import time1
import config_init
ci=config_init.config_init



#db=sqlite.connect("db.sql")
db=sqlite.connect(ci.get("db_path"))
dc=db.cursor()
dc.execute("""create table if not exists WalletTransactions
 ( transactionDateTime text, transactionID integer primary key, quantity integer,
  typeName text, price real, clientName text, stationName text,
   transactionType text)""")


#import sys

#params = urllib.urlencode({"userID":userid,"apiKey":apikey,"characterID":characterid,"beforeTransID":beforeTransID })
#params = urllib.urlencode({"userID":userid,"apiKey":apikey,"characterID":characterid })
params = urllib.urlencode({"keyID":keyID,"vCode":vCode,"characterID":characterid })
headers = {"Content-type": "application/x-www-form-urlencoded"}


dc.execute("""select max(transactionID),max(transactionDateTime) from WalletTransactions""")
#dc.execute("create temp table tm (transactionID integer primary key, transactionDateTime text)")
#dc.execute("""select max(transactionID),max(transactionDateTime) from tm""")
print dc
#maxID=0
#maxTime="2000-01-01 00:00:00"

for i in dc:
    (maxID,maxTime)=i
print maxID,maxTime, type(maxID)

dc.execute("""create table if not exists last_update 
( uptime text) """)
#i=time1.time2str(datetime.now())
#print "now ",i
#dc.execute("""insert into last_update values (?)""",(i,))
#print "2000-01-01 00:00:00"> None
#sys.exit(0)



conn = httplib.HTTPSConnection("api.eveonline.com")
conn.request("POST", "/char/WalletTransactions.xml.aspx", params, headers)

response = conn.getresponse()
print response.status, response.reason

col=[]
def start_tag(name,atr):
    if name == "row":
        col.append(atr)
p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = start_tag #start_element
p.Parse(response.read(),1)
conn.close()


while(col):
    col.sort(key=lambda x: x["transactionID"],reverse=True)
    print "len col",len(col)
    old="9"
    for i in col:
        if i["transactionDateTime"]>old:
            raise NameError("time and id mismatch "+old+" "+i["transactionDateTime"]+i["transactionID"])
        old = i["transactionDateTime"]
    print col[-1]["transactionID"]
    fl=1
    for i in col:
        #print i["transactionID"]
        #print long(i["transactionID"])>maxID
        if long(i["transactionID"])>maxID:
            if maxTime>i["transactionDateTime"]: 
                raise NameError("""time and id mismatch db: 
                {} {} api: {} {} """.format(maxID,maxTime,i["transactionID"],i["transactionDateTime"]))
            dc.execute("""insert into WalletTransactions values
             ( :transactionDateTime, :transactionID, :quantity,
              :typeName, :price, :clientName, :stationName,
               :transactionType)""",i)
        else :
            print "found base end value maxID: {} , transactionID: {}".format(maxID,i["transactionID"])
            break
    else :
        fl=0
    
    if fl:
        print "terminating cycle by database value"
        break
    beforeTransID=col[-1]["transactionID"]

    params = urllib.urlencode({"userID":userid,"apiKey":apikey,"characterID":characterid,"beforeTransID":beforeTransID })
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn = httplib.HTTPSConnection("api.eveonline.com")
    conn.request("POST", "/char/WalletTransactions.xml.aspx", params, headers)

    response = conn.getresponse()
    print response.status, response.reason
    col=[]
    p = xml.parsers.expat.ParserCreate()
    p.StartElementHandler = start_tag #start_element
    p.Parse(response.read(),1)
    conn.close()
else:
    print "terminating cycle by api end"
db.commit()
db.close()

#import sql_cache
#sql_cache.update_cache()
#sql_cache.check_cache()

