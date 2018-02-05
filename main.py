'''
Created on 18.12.2011

@author: mayor
'''
import db
db=db.db
import config_init
ci=config_init.config_init
import sql_turnover_profit


if __name__=="__main__":
    print "hello"
    class a():
        pass
    a1=a()
    sql_turnover_profit.profit(db.db, ci, a1)
    print "\nprofit weekly in detail:\n"
    for i in a1.l_profit_week:
        #print i[0],i[1],a1.d_margin_week[i[0]]
        print format(i[0],"_<50")+format(i[1]/7," >20,.0f")+"\t"+format(a1.d_margin_week[i[0]])
    print "\nprofit monthly in detail:\n"
    for i in a1.l_profit_month:
        #print i[0],i[1],a1.d_margin_week[i[0]] #i[0] name i[1] profit
        #print format(i[0],"_<40")+format(i[1]," >20,.0f")+"\t"+format(a1.d_margin_month[i[0]])
        
        if a1.d_profit_week.has_key(i[0]):
            print format(i[0],"_<50")+format(i[1]/30," >20,.0f")+"\t"+format(a1.d_margin_month[i[0]])+"\t"+format(a1.d_profit_week[i[0]]/7-i[1]/30," <20,.0f")
        else :
            print format(i[0],"_<50")+format(i[1]/30," >20,.0f")+"\t"+format(a1.d_margin_month[i[0]])
    
    
