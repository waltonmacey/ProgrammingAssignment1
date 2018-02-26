#!/usr/bin/python
from SocketServer import ThreadingMixIn
import threading
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import sys,os
global STATIC_DIR

PORT_NUMBER = 8080



def htmlTop():
    
    top = """<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8"/>
        <meta name= "viewport" content = "width=device-width,intiail-scale=1.0"/>
        <title> Cs560 Project </title>
        </head>
        <body>
        <h2> Directory </h2>"""
    return top

def htmlBot():
    bot ="""
        </body>
        </html>"""
    return bot

""" Get files in current directory i.e active directory"""
def Get_dFiles(h):
    if h == '/':
        os.chdir(STATIC_DIR)
    else:
        os.chdir(STATIC_DIR + h)
    file_list = []
    files = htmlTop() + "<ol>"
    for f in os.listdir(os.getcwd()):
        if f[0] == '.':
            continue
        files += " <li> " "<a href = " +f + ">" + f + "</a>" "</li>"
        file_list.append(f)
    files +=" </ol>"
    files += htmlBot()
    return files


class ThreadHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        checker = 0
        t = 0
        print STATIC_DIR
        try:
            #Check the file extension required and
            #set the right mime type
            
            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
                checker = 1
            else:
                mimetype='text/html'
                files = Get_dFiles(self.path + '/')
                sendReply = True
                t = 1
            
            
            if sendReply == True:
                #Open the static file requested and send it
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                if t == 1:
                    self.wfile.write(files)
                if checker == 1:
                    f = open(curdir + sep + self.path)
                    self.wfile.write(f.read())
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
        print STATIC_DIR
        checker = 0
        t = 0
        try:
            #Check the file extension required and
            #set the right mime type
            
            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
                checker = 1
            else:
                mimetype='text/html'
                files = Get_dFiles(self.path + '/')
                sendReply = True
                t = 1
        
        
            if sendReply == True:
                #Open the static file requested and send it
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                if t == 1:
                    self.wfile.write(files)
                if checker == 1:
                    f = open(curdir + sep + self.path)
                    self.wfile.write(f.read())
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
    
    STATIC_DIR = os.getcwd()
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
