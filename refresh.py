#!/usr/bin/env python 
#-*- coding:utf-8 -*-
'''
@author dbxiao
'''

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        res='<meta http-equiv="refresh" content="0,http://a.com%s">'%self.path
        self.wfile.write(res)
def main():
    try:
        server=HTTPServer(('',80),MyHandler)
        print 'start'
        server.serve_forever()
    except KeyboardInterrupt:
        print 'stop'
        server.socket.close()
if __name__=='__main__':
    main()