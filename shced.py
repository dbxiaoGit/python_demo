#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@author dbxiao
'''

import sched,time

s = sched.scheduler(time.time, time.sleep)
def des(fun):
    def _des(a):
        print "---- in func %s " % fun.__name__
        res=fun(a)
        print "++++ out func %s " % fun.__name__
        return res
    return _des
@des
def print_time(a):
    print a, time.asctime(time.localtime())
@des
def abs_fun(a):
    print a, time.ctime()
def print_some_times():
     print time.asctime(time.localtime())
     s.enter(5, 1, print_time, ("1111",))
     #参数1：延时（单位：秒  ）、参数2：优先级、参数3：调用的函数、参数4：传入的参数
     s.enter(2, 1, print_time, ("2222",))
     t = (2017, 1, 7, 9, 06, 00, 1, 2, 3)
     print 't:', time.ctime(time.mktime(t))
     s.enterabs(time.mktime(t), 1, abs_fun, ("3333",))
     s.run()
     print time.asctime(time.localtime())
print_some_times()