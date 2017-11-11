#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@author dbxiao
'''

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import uuid   
import urllib  
import os, sys  

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        res='{"method":"get","message":"test get","uuid":"%s"}'%uuid.uuid1()
        self.wfile.write(res)
	
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        res='{"method":"post","message":"test post","uuid":"%s"}'%uuid.uuid1()
        self.wfile.write(res)
        
def run():
    try:
        server=HTTPServer(('',80),MyHandler)
        print 'start'
		#server.settimeout(500)
        server.serve_forever()
    except KeyboardInterrupt:
        print 'stop'
        server.socket.close()
if __name__=='__main__':
    run()
