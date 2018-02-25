#! /usr/bin/env python

#############################################################################
## tunproxy.py --- small demo program for tunneling over UDP with tun/tap  ##
## Copyright (C) 2003  Philippe Biondi <phil@secdev.org>                   ##
#############################################################################

import os, sys
from socket import *
from fcntl import ioctl
from select import select
import getopt, struct
import simT as tcp
import cipher as ciph

TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002

TUNMODE = IFF_TUN
MODE = 0
DEBUG = 0
# came with the barebones tunproxy.py
def usage(status=0):
    print "Usage: sim.py [-s port|-c targetip:port] [-e]"
    sys.exit(status)
	
opts = getopt.getopt(sys.argv[1:],"s:c:ehd")

for opt,optarg in opts[0]:
    if opt == "-h":
        usage()
    elif opt == "-d":
        DEBUG += 1
    elif opt == "-s":
        MODE = 1
        PORT = int(optarg)
    elif opt == "-c":
        MODE = 2
        IP,PORT = optarg.split(":")
        PORT = int(PORT)
        peer = (IP,PORT)
    elif opt == "-e":
        TUNMODE = IFF_TAP
        
if MODE == 0:
    usage(1)


f = os.open("/dev/net/tun", os.O_RDWR)
ifs = ioctl(f, TUNSETIFF, struct.pack("16sH", "toto%d", TUNMODE))
ifname = ifs[:16].strip("\x00")

print "Allocated interface %s. Configure it and use it" % ifname
sec_con = 1
can_write = 1
s = socket(AF_INET, SOCK_DGRAM)
try:
	if MODE == 1:
		s.bind(("", PORT))
		#"Please wait until the client responds to send a message"
		while 1:
                    #connect to TCP to recieve password 
                        if sec_con:
                            key,IV,sec_con = tcp.sTCP(PORT)
                        word,peer = s.recvfrom(1500)
			enc_txt,usr_hmac = word.split(':')
			hmac = ciph.hmac_gen(enc_txt,key)
			if hmac == usr_hmac:
				plaintext = ciph.cbc_dec(enc_txt,key)
				if str.upper(plaintext) == str.upper("Exit"):
                                    print "Connection closed by client."
                                    exit(1)
                                else: 
                                    print "User:{0}".format(plaintext)
			else:
				print "ABORT:TUNNEL IS NO LONGER SECURE"
				sys.exit(1) 
			serv_msg = raw_input("Server:")
			#server send a msg
			ciphertext = ciph.cbc_enc(serv_msg,key,ciph.hexStrToIntList(IV))
			hmac = ciph.hmac_gen(ciphertext,key)
			serv_msg = ciphertext+':'+hmac
			s.sendto(serv_msg,peer)
			serv_msg = ""
	else:
		while 1:
                        if sec_con:
                            key,IV,sec_con = tcp.cTCP(peer,PORT)
			#user send a msg
			usr_msg = raw_input("User:")
			ciphertext = ciph.cbc_enc(usr_msg,key,ciph.hexStrToIntList(IV))
			hmac = ciph.hmac_gen(ciphertext,key)
			usr_msg = ciphertext+':'+hmac
                        s.sendto(usr_msg,peer)
			usr_msg = ""
			#user recieves a msg
			word,peer = s.recvfrom(1500)
			enc_txt,serv_hmac = word.split(':')
			hmac = ciph.hmac_gen(enc_txt,key)
			if hmac == serv_hmac:
				plaintext = ciph.cbc_dec(enc_txt,key)
				if str.upper(plaintext) == str.upper("Exit"):
                                    print "Connection closed by Server."
                                    exit(1)
                                else:
                                    print "Server:{0}".format(plaintext)
			else:
				print "ABORT:TUNNEL IS NO LONGER SECURE"
				sys.exit(1)
			

except KeyboardInterrupt as e:
    print "Stopped by user."
    serv_msg = "Exit"
    ciphertext = ciph.cbc_enc(serv_msg,key,ciph.hexStrToIntList(IV))
    hmac = ciph.hmac_gen(ciphertext,key)
    serv_msg = ciphertext+':'+hmac
    s.sendto(serv_msg,peer)

