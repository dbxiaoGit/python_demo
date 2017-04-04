#!/usr/bin/python  
# -*- coding: utf-8 -*-  
'''
@author: dbxiao 
'''  

import socket

def main() :
    server = socket.socket()
    server.bind(('127.0.0.1',80))
    server.listen(5)
    while True :
        con,addr = server.accept()
        buf = con.recv(1024) 
        pwd = buf.split(' ')[1]
        print pwd      
        response="<script type='text/javascript'>window.location.href='http://a.com%s';</script>"%pwd
        con.send(response)
        con.close()
if __name__ == "__main__" :
    main()