import socket
import thread
import sys,os

def htmlTop():

    top = """<!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="utf-8"/>
            <meta name= "viewport" content = "width=device-width,intiail-scale=1.0"/>
            <title> Cs560 Project </title>
            </head>
            <body>
            <h2> Jabril Muhammad and Walton </h2>"""
    return top
def htmlBot():
    bot ="""
        <p id="demo" onclick="myFunction()">Click me.</p>
        <script>
        function myFunction() {
        document.getElementById("demo").innerHTML = "YOU CLICKED ME!";
        }
        </script>
        </body>
        </html>"""
    return bot

def Get_dFiles():
    cwd = os.getcwd()
    files = "<ol>"
    file_list = []
    for f in os.listdir(cwd):
        files += " <li> " + f + "</li>"
        file_list.append(f)
    files +=" </ol>"
    return files,file_list

class SingleServer(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.PACKET_SIZE =1024
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))

    def _listen(self):
        self.sock.listen(1)
        print "listening"
        while True:
            client, address = self.sock.accept()
            data = client.recv(self.PACKET_SIZE).decode()
            if not data:
                break
            print data
            req = data.split()[0]
            filename = data.split()[1]
            if req == "GET":
                files,file_list = Get_dFiles()
                if filename == "/" or filename == "/index.html"
                    w_data = htmlTop() + files +htmlBot()
                    client.send('HTTP/1.0 200 OK\r\n')
                    client.send('Content-Type: text/html\r\n')
                    client.send('\r\n')
                    client.send(w_data)
                elif filename in file_list:
#read file and send
                else:
                    raise # not finished just uploading





class ThreadServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.PACKET_SIZE =1024
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))
    
    def _listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            thread.start_new_thread(self.handler,(client,address))

    def handler(self, client, address):
        while True:
            try:
                data = client.recv(self.PACKET_SIZE)
                filename = data.split()[1]
                if len(filename) == 1:
                    filename = "\index.html"
                f = open(filename[1:])
                w_data = f.read()
                f.close()
                client.send('HTTP/1.0 200 OK\r\n\r\n')
                client.sendall(w_data)
            except IOError:
                client.close()




def usage():
    print "USAGE: python server.py m|s "
if __name__ == "__main__":
    port_num = 1234
    if len(sys.argv) == 2:
        if any(x in ['s','m'] for x in sys.argv):
            mode = sys.argv[1]
        else:
            usage()
            exit(1)
    else:
        usage()
        exit(1)

if mode == 'm':
    print "Threaded Server"
    ThreadedServer(socket.gethostname(),port_num)._listen()
else:
    print "single server"
    SingleServer(socket.gethostname(),port_num)._listen()

