#!/usr/bin/python
import threading
import sys,os
from os import curdir, sep
from SocketServer import ThreadingMixIn
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

global STATIC_DIR
PORT_NUMBER = 8080

""" html Top and Bottom is used to print out the directory listing
    when on the home page."""
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


""" Get files in current directory i.e active directory
    This uses STATIC_DIR to always keep the main directory known.
    This is useful when changing to different directories. Get_dfiles
    grabs all the files in the current directory ( except .files) and
    puts them in between the htmlTop() and htmlBot()"""
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
        if f.endswith(".py"):
            continue
        files += " <li> " "<a href = " +f + ">" + f + "</a>" "</li>"
        file_list.append(f)
    files +=" </ol>"
    files += htmlBot()
    return files

""" Class to handle threads. The code is the same as my handle class"""
class ThreadHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


    def do_HEAD(self):
        self._set_headers()
        
    def do_GET(self):
        checker = 0
        t = 0
        cgi = 0
        try:
            #Check the file extension required and
            #set the right mime type
            
            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
                checker = 1
            elif  self.path.endswith(".cgi"):
                mimetype = 'text/html'
                cgi = 1
                cgi_file = self.path
                sendReply = True
            else:
                mimetype='text/html'
                files = Get_dFiles(self.path + '/')
                sendReply = True
                t = 1
                checker = 0
            
            if sendReply == True:
                #Open the static file requested and send it
                self._set_headers()
                
                if t == 1:
                    self.wfile.write(files)
                if checker == 1:
                    f = open(curdir + sep + self.path)
                    self.wfile.write(f.read())
                    f.close()
                if cgi == 1:
                    rin,rout = os.popen2('.'+ cgi_file)
                    rin.close()
                    dataout = rout.read()
                    rout.close()
                    self.wfile.write(dataout)
            
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

""" Class to handle Single Threads"""
class myHandler(BaseHTTPRequestHandler):

    """Headers are set to automicatically send a 200 reponse to the client"""
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
   
  
    def do_HEAD(self):
        self._set_headers()
    
    """Gets call from the client
        Only checks for cgi and html files to execute
        List the directory when neither are present"""
    
    def do_GET(self):
        checker = 0
        t = 0
        cgi = 0
        try:
            #Check the file extension required and
            #set the right mime type
            
            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
                checker = 1
            elif  self.path.endswith(".cgi"):
                mimetype = 'text/html'
                cgi = 1
                cgi_file = self.path
                sendReply = True
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
                if cgi == 1:
                    rin,rout = os.popen2('.'+ cgi_file)
                    rin.close()
                    dataout = rout.read()
                    rout.close()
                    self.wfile.write(dataout)
            
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

"""
    Basic if statements to check if the server is single or multi threaded
    If no argument is given. A Single threaded server is defaulted.
    In order to exit out of the Server you need to CTRL-C"""
    
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
        #threads = []
        #for i in range(5):
        server_thread = threading.Thread(target=server.serve_forever)
        threads.append(server_thread)
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)
        while True:
            pass
        server.shutdown()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.server_close()

