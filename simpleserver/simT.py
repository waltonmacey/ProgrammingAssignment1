'''*** code found at wiki.python.org/moin/TcpCommunication ***'''
#!/usr/bin/env python
import sys
import socket
import cipher as ciph

#mode = sys.argv[]
#print mode
def cTCP(peer,PORT):
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((peer[0],PORT))
    while 1:
        MESSAGE = raw_input('Please enter username:')
        password = raw_input('Please enter password:')
        user_pass = MESSAGE+':'+password        
        s.send(user_pass)
        data = s.recv(BUFFER_SIZE)
        if data == "confirmed":
            while 1:
                #recieve IV from server
                KIV = s.recv(BUFFER_SIZE)
                #Prompt user to check for a yes or no answer if IV is okay
                key,IV = KIV.split(':')
                print "Do you agree to this key,IV pair(yes/no):{0}-{1}?".format(key,IV)
                reply = raw_input()
                if reply == "yes":
                    print "agreed on a key-IV now closing secure connection"
                    s.send(reply)
                    s.close()
                    return key,IV,0
                else:
                    s.send(reply)
                    continue
        elif data == "exit":
            print "Server closed connection."
            s.close()
            exit(1)
        #return data,0

#print "received data:", data

def sTCP(PORT):
    BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",PORT))
    s.listen(1)
    conn, addr = s.accept()
    #print 'Connection address:', addr
    while 1:
        #Wait for the user to send password so we can talk securely 
        data = conn.recv(BUFFER_SIZE)
        #The user sends the correct password
        if data == "user:pass":
            conn.send("confirmed")
            IV = ciph.intListToHexStr(ciph.generateIV())
            key = ciph.randKeyGen()
            KIV = key+':'+IV
            print "Initiating secure Connection ....."
            #Go into while loop so user and server can exchange key and IV
            while 1:
                print "Sending key-IV pair....."       
                conn.send(KIV)
                print "Waiting for key-IV pair confirmation......"
                response = conn.recv(BUFFER_SIZE)
                if response == "yes":
                    conn.close()
                    print "agreed on on key-IV pair. now closing secure connection"
                    return key,IV,0
                else:
                    IV = ciph.intListToHexStr(ciph.generateIV())
                    key = ciph.randKeyGen()
                    KIV = key+':'+IV
            break
        else: 
            print "No user by that name"
            conn.send("exit")
            conn.close()
            exit(1)
    return data,0


