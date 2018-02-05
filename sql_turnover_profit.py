#coding=Cp1251
'''
Created on 17.11.2011

@author: mayor
'''
import time1
from datetime import timedelta

def profit(db,ci,sqt,td=timedelta(days=365)):
    dc=db.cursor()
    dc.execute("""select max(transactionDateTime),min(transactionDateTime) from WalletTransactions""")
    for ii in dc:
        d1,d2=ii
    #print "days pr",d1,d2
    d3=(time1.str2time(d1)-time1.str2time(d2)).days    
    td=timedelta(days=d3)
    _profit(dc,ci,sqt,td)
    i=0
    for ii in sqt.l_profit:
        i+=ii[1]
    print("profit total",format(i,","),format(i/d3,","))
    sqt.summary_profit = i
    sqt.summary_profit_forday = i/d3
    db.commit()
    class a:
        pass
    a1=a()
    _profit(dc,ci,a1,td=timedelta(days=7))
    i=0
    for ii in a1.l_profit:
        #print ii[0],ii[1]
        i+=ii[1]
    print("profit weekly",format(i,","),format(i/7,","))
    sqt.weekly_profit = i
    sqt.weekly_profit_forday = i/7

    sqt.l_profit_week=a1.l_profit
    sqt.d_profit_week=a1.d_profit
    sqt.d_margin_week=a1.d_margin
    a2=a()
    _profit(dc,ci,a2,td=timedelta(days=30))
    i=0
    for ii in a2.l_profit:
        #print ii[0],ii[1]
        i+=ii[1]
    print("profit monthly",format(i,","),format(i/30,","))
    sqt.monthly_profit = i
    sqt.monthly_profit_forday = i/30
    sqt.l_profit_month=a2.l_profit
    sqt.d_profit_month=a2.d_profit
    sqt.d_margin_month=a2.d_margin
    
    
def _profit(dc,ci,sqt,td):
    """считает прибыль
    db линк на открытую субд
    ci config_init
    """
    #dc=db.cursor()
    dc.execute("""select max(transactionDateTime) from WalletTransactions""")
    for ii in dc:
        d1=ii[0]
    tm=time1.str2time(d1)-td
    tm=time1.time2str(tm)
    #print "time2 ",d1,tm
    dc.execute("""create temp table sell_profit (typeName text, volume real, quantity integer)""")
    
    dc.execute("""insert into sell_profit select typeName,sum(price*quantity) as a1,sum(quantity)
    from WalletTransactions where transactionType="sell" and transactionDateTime>? group by typeName having a1>? 
    """,(tm,int(ci.get("profit_sum_limit"))) )
    
    dc.execute("""create temp table buy_profit (typeName text, volume real, quantity integer)""")
    dc.execute("""insert into buy_profit select typeName,sum(price*quantity) as a1, sum(quantity) 
    from WalletTransactions where transactionType="buy" and transactionDateTime>? group by typeName having a1>? 
    order by a1 desc""",(tm,int(ci.get("profit_sum_limit"))) )
    dc.execute("""select b.typeName, s.volume, s.quantity, b.volume, b.quantity 
    from buy_profit b,sell_profit s where b.typeName=s.typeName
    order by s.volume desc""")
    bf=float(ci.get("broker_fee"))
    st=float(ci.get("sales_tax"))
    citadel_fee=float(ci.get("citadel_fee"))
    d_margin={}
    l_margin=[]
    d_profit={}
    l_profit=[]
    for i in dc:
        b=i[3]/i[4]
        s=i[1]/i[2]
        name=i[0]
        sell=s*(1-st)*(1-bf)
        buy=b*(1+citadel_fee)
        
        pft=(sell-buy)*i[2] # i2= sell quantity
        d_profit[name]=pft
        l_profit.append((name,pft))
        
        margin=sell/buy
        d_margin[name]=margin
        l_margin.append((name,margin))
        #print "profit ",name,s,b
    dc.execute("""drop table sell_profit""")
    dc.execute("""drop table buy_profit""")
    #dc.commit()
    l_margin.sort(key = lambda x : x[1],reverse= True)
    l_profit.sort(key = lambda x : x[1],reverse= True)

    sqt.d_margin=d_margin
    sqt.d_profit=d_profit
    sqt.l_profit=l_profit
    sqt.l_margin=l_margin
        
    
