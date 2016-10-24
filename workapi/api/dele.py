#!/usr/bin/env python
#-*- coding: utf-8 -*- 

import MySQLdb
import time
import string
from DBUtils.PooledDB import PooledDB
import dbconfig


ERROR = {0:"OK", 1:"Parameter Error", 2:"Database Error", 3:u"您已赞", 4:u"你无权开通直播"}
Default_Snapshot = "http://7xvsyw.com2.z0.glb.qiniucdn.com/n.jpg"

class DbManager():
    def __init__(self):
        kwargs = {}
        kwargs['host'] =  dbconfig.DBConfig.getConfig('database', 'dbhost')
        kwargs['port'] =  int(dbconfig.DBConfig.getConfig('database', 'dbport'))
        kwargs['user'] =  dbconfig.DBConfig.getConfig('database', 'dbuser')
        kwargs['passwd'] =  dbconfig.DBConfig.getConfig('database', 'dbpassword')
        kwargs['db'] =  dbconfig.DBConfig.getConfig('database', 'dbname')
        kwargs['charset'] =  dbconfig.DBConfig.getConfig('database', 'dbcharset')
        self._pool = PooledDB(MySQLdb, mincached=1, maxcached=15, maxshared=10, maxusage=10000, **kwargs)

    def getConn(self):
        return self._pool.connection()

_dbManager = DbManager()

def getConn():
    return _dbManager.getConn()

def Delete(snapshot):
    con = getConn()
    cur =  con.cursor()


    sql = "delete from live where snapshot = '{0}' and state = 2".format(snapshot)
    cur.execute(sql)
    con.commit()
#

    sql = 'delete from live where snapshot = "" and state = 2'
    cur.execute(sql)
    con.commit()

    sql = 'delete from live where title like "%测试%" and state = 2'
    cur.execute(sql)
    con.commit()

    sql = 'delete from live where playback_hls_url = "" and state = 2'
    cur.execute(sql)
    con.commit()

    cur.close()
    con.close()


if __name__ ==  '__main__':
    Delete("http://7xvsyw.com2.z0.glb.qiniucdn.com/n.jpg")
