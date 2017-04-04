#!/usr/bin/env python
# -*-coding: utf-8-*-
'''
@author dbxiao
'''

import os,time

class rec :  
    def __init(self):
        self.vartime=""
        self.cmd=""        
    def enter_time(self):
        self.vartime=raw_input("type in record time :")
        print self.vartime
        print self.vartime==""
        # print int(self.vartime)>180
        try:    
            if self.vartime=="" or int(self.vartime)>180:
                self.vartime=180
        except Exception:
            print "please type correct time !!!"
            self.enter_time()  
    def excute_cmd(self):
        self.cmd="adb shell screenrecord  --time-limit "+str(self.vartime)+
        " /sdcard/Pictures/Screenshots/"+time.strftime('%m%d_%H%M%S',
        time.localtime())+".mp4"
        print self.cmd
        os.system(self.cmd)      
    def start(self):
        self.enter_time()
        self.excute_cmd()       
s=rec()
s.start()    