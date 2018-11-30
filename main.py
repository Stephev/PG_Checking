#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/10/17
# @Author  : Stephev
# @Site    :
# @File    : databaseinfo.py
# @Software: PG_Checking

import infosystem.systeminfo  as  sys_info
import infodatabase.databaseinfo  as  data_info


def system_info():
    sys_info.system_basic()
    sys_info.system_mem()
    sys_info.cpu_info()
    sys_info.disk_info()
    return

def database_info():
    data_info.pg_basic()
    data_info.pg_parameter()
    data_info.pg_database()
    data_info.pg_log()
    return

def main():
    system_info()
    database_info()
    return

if __name__ == '__main__':
    main()
