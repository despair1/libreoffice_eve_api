'''
Created on 18.12.2011

@author: mayor
'''
from sqlite3 import dbapi2 as sqlite
import config_init

ci=config_init.config_init

class _db():
    def __init__(self):
        self.db=sqlite.connect(ci.get("db_path"))
    
db=_db()


#db=sqlite.connect("db.sql")
