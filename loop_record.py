#!/usr/bin/env python
# -*-coding: utf-8-*-
'''
@author dbxiao
'''

import os,time
from multiprocessing import Process

def main_fun() :
    while True :
        print 'p1 begin'
        p2= Process(target=rec,args=())
        p2.start()
        time.sleep(180)
def rec():
    print 'begin to record!'
    cmd="adb shell screenrecord  --time-limit 180 /sdcard/Pictures/Screenshots/
    "+time.strftime('%m%d_%H%M%S',time.localtime())+".mp4"
    print cmd
    print os.system(cmd)
if __name__ == "__main__" :
     p1= Process(target=main_fun,args=())
     p1.start()
