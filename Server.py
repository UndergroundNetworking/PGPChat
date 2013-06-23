#! /bin/env python

import os, sys, string, rfc822
import socket 
import time

if __name__ == '__main__':
	users = {}
	messages = {}
	s = socket.socket()         # Create a socket object
	print "Socket Up"
	host = "0.0.0.0" # Get local machine name
	port = 4334            # Reserve a port for your service.
	s.bind((host, port))        # Bind to the port
	s.listen(5)
	while True:
		c, addr = s.accept()     # Establish connection with client.
		print 'Got connection from', addr
		recData =  c.recv(1024)
		print recData.strip()
		if recData.strip() == "AUTH":
			print "AUTHING USER"
			name = c.recv(1024)
			print "Name: ",
			print(name)
			data = ""
			while 1:
				line = ""
				try:
					line = c.recv(1024)
					# print line
				except socket.timeout:
					break
				if "EOF" in line.strip():
					aline = line.replace("EOF", "")
					data += aline
					break
				else:
					data += line
			print "Key Imported: ",
			#print data
			users[name]=data
			print users
			icmd = c.recv(1024)
			if icmd.strip() == "getKey":
				print "key Request"
				c.send("key")
				key = c.recv(1024)
				#print key
				uKey = str(users[key.strip()]).split("\n")
				luk = len(uKey);
				i = 0 
				while i < luk:
					#print str(uKey[i])
					c.send(str(uKey[i]) + "\n")
					i += 1
				#print "EOF"
				time.sleep(1)
				c.send("EOF")
				c.close()
			if icmd.strip() == "encrypt":
				print "encrypt request"
				c.send("encrypt")
				re = c.recv(1024)
				print re
				wh = c.recv(1024)
				print wh
				data = ""
				while 1:
					line = ""
					try:
						line = c.recv(1024)
					except socket.timeout:
						break
					if "EOF" in line.strip():
						aline = line.replace("EOF", "")
						data += aline
						break
					else:
						data += line
				#print data
				messages[re] = {wh:str(data)}
				print messages
			if icmd.strip() == "messages":
				print "message request"
				c.send("messages")
				wh = c.recv(1024)
				print wh
				mes = messages[wh]
				print mes
				lm = len(mes)
				print lm
				c.send(str(mes))
				c.send("EOF")
