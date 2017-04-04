#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@author dbxiao
'''

import socket;
import struct
import os
import urllib2
import urllib

def postHttp(api_user=None,token=None,name=None,project_id=None,description=None,type_id=None,create_user=None,current_user=None):
    url="http://www.baidu.com"
    #定义要提交的数据
    postdata = dict(api_user=api_user,token=token,name=name,project_id=project_id,
           description=description,type_id=type_id,create_user=create_user,current_user=current_user)
    print postdata
    #url编码
    postdata=urllib.urlencode(postdata)
    #enable cookie
    request = urllib2.Request(url,postdata)
    response = urllib2.urlopen(request)
    print response
    print response.read()
if "__main__" == __name__:
    postHttp('x', 'xx', 'title', 'xxx', 'xxxx', '7', 'xxxxx','xxxxxx')