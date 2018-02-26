#!/usr/bin/python
from SocketServer import ThreadingMixIn
import threading
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import sys,os
PORT_NUMBER = 8080

""" Get files in current directory i.e active directory"""
def Get_dFiles():
    cwd = os.getcwd()
    file_list = []
    files = "<ol>"
    for f in os.listdir(cwd):
        if f[0] == '.':
            continue
        files += " <li> " + f + "</li>"
        file_list.append(f)
    files +=" </ol>"
    return files


class ThreadHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"
    
        try:
            #Check the file extension required and
            #set the right mime type
            
            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True
            
            if sendReply == True:
                #Open the static file requested and send it
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                self.wfile.write("Directory Files: ")
                files = Get_dFiles()
                self.wfile.write(files)
                f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


class myHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
   
  
    def do_HEAD(self):
        self._set_headers()
    
    #Handler for the GET requests
    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"
        
        try:
            #Check the file extension required and
            #set the right mime type
            
            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True
        
            if sendReply == True:
                #Open the static file requested and send it
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                self.wfile.write("Directory Files: ")
                files = Get_dFiles()
                self.wfile.write(files)
                f.close()
            return
            
        except IOError:
                self.send_error(404,'File Not Found: %s' % self.path)

#Handler for the POST requests
def do_POST(self):
    if self.path=="/send":
        form = cgi.FieldStorage(
                                fp=self.rfile,
                                headers=self.headers,
                                environ={'REQUEST_METHOD':'POST',
                                'CONTENT_TYPE':self.headers['Content-Type'],
                                })
            
        print "Your name is: %s" % form["your_name"].value
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Thanks %s !" % form["your_name"].value)
        return


try:
    #Create a web server and define the handler to manage the
    #incoming request
    if len(sys.argv) == 1 or sys.argv[1] == 's':
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print 'Single Server Started httpserver on port ' , PORT_NUMBER
        #Wait forever for incoming htto requests
        server.serve_forever()
    elif len(sys.argv) == 2 and sys.argv[1] == 'm':
        server = ThreadedHTTPServer(('', PORT_NUMBER), ThreadHandler)
        print 'Multi-Server started on port ' , PORT_NUMBER
        server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
