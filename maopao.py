#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@author dbxiao
'''

def mp():
    int_list = [222,333,111,444,555,125,168]
    for i in range(len(int_list)):
        for j in range(i+1,len(int_list)):
            if int_list[i] > int_list[j] :
                print "if_IJ",i,"|",j
                print "if",int_list[i],"|",int_list[j]
                int_list[i] = int_list[i] ^ int_list[j]
                int_list[j] = int_list[i] ^ int_list[j]
                int_list[i] = int_list[i] ^ int_list[j]
                print "if_end", int_list[i], "|", int_list[j]
            print i,"  |   ",j
    print int_list
if __name__ == "__main__":
    mp()