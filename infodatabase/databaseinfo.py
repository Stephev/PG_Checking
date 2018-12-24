#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/10/17
# @Author  : Stephev
# @Site    :
# @File    : databaseinfo.py
# @Software: PG_Checking

import psycopg2
import os
import commands
import ConfigParser


db = ConfigParser.ConfigParser()
db.read('database.conf')
host_cus = db.get("db","host")
user_cus = db.get("db","user")
pwd_cus = db.get("db","passwd")
db_cus = db.get("db","database")
port_cus = db.get("db","port")


class PGINFO:

    def __init__(self,host, user, pwd, db, port):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port = port

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise(NameError, "没有设置数据库信息")
        self.conn = psycopg2.connect(database=self.db, user=self.user, password=self.pwd, host=self.host, port=self.port)
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return  cur

    def ExecQuery(self, sql):
        """
        执行查询语句
        """
        if sql == 'close':
            self.conn.close()
        else:
            cur = self.__GetConnect()
            cur.execute(sql)
            # resList = cur.fetchall()
            return cur



def pg_basic():
    pg = PGINFO(host=host_cus, user=user_cus, pwd=pwd_cus, db=db_cus, port=port_cus)
    print "1、数据库基本信息----"
    pg_version = os.popen("psql --version").readlines()
    print ('当前数据库版本是:%s' % (pg_version))
    pg_home = commands.getoutput("which psql")
    print "数据库的安装目录是:", pg_home
    cur = pg.ExecQuery("show data_directory;")
    pgdata = cur.fetchone()
    print "数据文件目录为:", pgdata[0]
    pgdata_size = commands.getoutput("du -h " + pgdata[0] + " |cut -d '/' -f1  |tail -n 1")
    print "目前数据库的数据目录总大小为:", pgdata_size
    cur = pg.ExecQuery("select pg_is_in_recovery();")
    standby = cur.fetchone()
    if standby[0]:
        print "主备状态：当前数据库是备库"
    else:
        print "主备状态：当前数据库是一个主库"
    cur = pg.ExecQuery("select pg_postmaster_start_time();")
    up_time = cur.fetchone()
    print "当前数据库开始运行的时刻为:",up_time[0]
    return

def pg_parameter():     # 数据库的基本参数
    print "2、数据库基本参数-----"
    pg = PGINFO(host=host_cus, user=user_cus, pwd=pwd_cus, db=db_cus, port=port_cus)
    cur = pg.ExecQuery("show shared_buffers;")
    pg_buffe = cur.fetchone()
    print "-->  shared_buffers = ",pg_buffe[0]
    cur = pg.ExecQuery("show work_mem;")
    pg_work_mem = cur.fetchone()
    print "-->  work_mem = ",pg_work_mem[0]
    cur = pg.ExecQuery("show effective_cache_size")
    pg_cache_size = cur.fetchone()
    print "-->  ffective_cache_size = ",pg_cache_size[0]
    cur = pg.ExecQuery("show max_connections;")
    pg_max_con = cur.fetchone()
    print "-->  max_connections = ",pg_max_con[0]
    cur = pg.ExecQuery("show hba_file")
    pg_hba_file = cur.fetchone()
    print "-->  hba_file = ",pg_hba_file[0]
    cur = pg.ExecQuery("show autovacuum")
    pg_auto_vacuum = cur.fetchone()
    print "-->  autovacuum = ",pg_auto_vacuum[0]
    return

def pg_database():
    print "3、数据库中信息----"
    pg = PGINFO(host=host_cus, user=user_cus, pwd=pwd_cus, db=db_cus, port=port_cus)
    cur = pg.ExecQuery("select datname from pg_database;")
    pgs_database = cur.fetchall()
    print("当前pg有以下数据库:")
    for i in pgs_database:
        print "-->  ", i[0]
    cur = pg.ExecQuery("select extname  from pg_extension ;")
    pg_exten = cur.fetchall()
    print("当前数据库安装有以下拓展:")
    for i in pg_exten:
        print "-->  ", i[0]
    cur = pg.ExecQuery("select count(*) from pg_stat_activity;")
    pg_activity = cur.fetchone()
    print "数据库目前的连接数为:", pg_activity[0]
    cur = pg.ExecQuery("select current_database(), \
                            t2.nspname, \
                            t1.relname, \
                            pg_size_pretty(pg_relation_size(t1.oid)), \
                            t3.idx_cnt \
                      from pg_class t1, pg_namespace t2, \
                            (select indrelid,count(*) idx_cnt \
                                      from pg_index group by 1 having count(*)>4) t3 \
                                      where t1.oid=t3.indrelid \
                                      and t1.relnamespace=t2.oid \
                                      and pg_relation_size(t1.oid)/1024/1024.0>1 \
                     order by t3.idx_cnt desc;")
    pg_index_info = cur.fetchall()
    print "索引超过4个，表空间大于10M的表有："
    print "current_database | nspname | relname | pg_size_pretty | idx_cnt"
    for i in pg_index_info:
        print "    ",pg_index_info[0]
    cur = pg.ExecQuery("select current_timestamp - query_start AS runtime,\
                          datname,usename,query \
                          from pg_stat_activity \
                          where state = 'active' and current_timestamp - query_start > '1 min' \
                          order by 1 desc;")
    pg_current_time = cur.fetchall()
    print "该系统中当前查询时间超过一分钟的查询有:"
    print "runtime | datname | usename | query"
    for i in pg_current_time:
        print "    ",pg_current_time[0]
    return

def pg_log():     #日志一些信息
    print "4、日志相关信息----"
    pg = PGINFO(host=host_cus, user=user_cus, pwd=pwd_cus, db=db_cus, port=port_cus)
    cur = pg.ExecQuery("show logging_collector;")
    pg_log_col = cur.fetchone()
    type(pg_log_col)
    if pg_log_col[0]:
        print "数据库已经开启了日志收集 logging_collector = on"
    else:
        print "数据库还未开启日志收集，建议开启。数据库的输出将写在日志中，方便运维。"
    cur = pg.ExecQuery("show wal_level;")
    pg_wal_level = cur.fetchone()
    print "wal日志等级为： ",pg_wal_level[0]
    cur = pg.ExecQuery("show wal_keep_segments;")
    pg_wal_keep = cur.fetchone()
    print "wal日志一共保留的个数为",pg_wal_keep[0]
    return


def main():
    pg_basic()
    pg_parameter()
    pg_database()
    pg_log()
    return


if __name__ == '__main__':
    main()

