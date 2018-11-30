#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/10/17
# @Author  : Stephev
# @Site    :
# @File    : systeminfo.py
# @Software: PG_Checking

import commands
import string
import psutil


def system_basic():      #系统主机信息
    print "1、基本信息----"
    hostname_info = commands.getoutput("hostname -s")
    print "该系统的主机名是：",hostname_info
    host_version = commands.getoutput("cat /etc/redhat-release")
    print "该系统的版本为：",host_version
    up_time = commands.getoutput("uptime |cut -d ',' -f1 ")
    print "当前主机运行时间为 ：",up_time
    return

def system_mem():
    print "2、内存信息----"
    mem_size = commands.getoutput("free -mh|grep Mem| tr -s [:space:]|cut -d ' ' -f2")
    print "该主机的内存大小为：",mem_size
    mem_use = psutil.virtual_memory()
    mem_1 = list(mem_use)
    print "内存使用率：", mem_1[2], "%"
    if mem_1[2] > 80:
        print"内存使用率超过80%！"
    swap_size = commands.getoutput("free -mh|grep Swap| tr -s [:space:]|cut -d ' ' -f2")
    print "该主机的swap分区的大小为：", swap_size
    swap_use = commands.getoutput("free -m|grep Swap| tr -s [:space:]|cut -d ' ' -f3")
    swap_int = string.atoi(swap_use)
    if swap_int == 0:
        print "-->好消息是：还未用到swap分区"
    else:
        print "已经用到swap分区，内存已经用尽"
    return


def cpu_info():
    print "3、CPU信息----"
    cpu_times = psutil.cpu_times()
    print "该系统CPU的基本信息为:"
    print cpu_times
    cpu_count = psutil.cpu_count()
    print "该主机的CPU核数为:",cpu_count
    cpu_use=psutil.cpu_percent()

    print "CPU使用率：",cpu_use,"%"
    if cpu_use>80:
        print"有个坏消息：CPU使用率超过80%！尽快查找原因并处理！"
    return

def disk_info():
    print "4、磁盘信息----"
    disk_1 = list(psutil.disk_usage('/'))
    print "根分区使用率：", disk_1[3], "%"
    if disk_1[3] > 80:
        print "警告：根分区使用率超过80%！"
    disk_2 = list(psutil.disk_usage('/boot'))
    print "/boot分区使用率：", disk_2[3], "%"
    if disk_2[3] > 80:
        print " 警告：/boot分区使用率超过80%！"
    df_info = commands.getoutput("df -h |grep /dev/sd")
    print "当前主机的磁盘使用情况"
    print df_info
    lsblk_info = commands.getoutput("lsblk |grep sd")
    print "当前主机的磁盘挂载情况："
    print lsblk_info
    return

def main():
    system_basic()
    system_mem()
    cpu_info()
    disk_info()
    return

if __name__ == '__main__':
    main()
