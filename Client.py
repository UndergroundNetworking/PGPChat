import os, sys, string, rfc822
import socket 
import time

def encrypt(data, userid):
	"Encrypt a string to all keys matching 'userid'."
	pw,pr = os.popen2('echo "' +str(data)+ '"|gpg -e --trust-model always --armor -r "'+userid+'"')
	pw.close()
	ctext = pr.read()
	return ctext

def decrypt(data):
	"Decrypt a string - if you have the right key."
	pw,pr = os.popen2('echo "' +str(data)+ '"|gpg -d --trust-model always')
	pw.close()
	ptext = pr.read()
	return ptext

def md5it(data):
	pw,pr = os.popen2('echo "' +str(data)+ '"|md5')
	pw.close()
	ptext = pr.read()
	return ptext

def getPublicKey(user):
	pw,pr = os.popen2('gpg --export --armor '+ user)
	pw.close()
	ptext = pr.read()
	return ptext
def addKey(key):
	pw,pr = os.popen2('echo "' + key + '"|gpg --import ')
	pw.close()
	ptext = pr.read()
	return ptext

if __name__ == '__main__':
	c = socket.socket()
	clientHost = "127.0.0.1"
	clientPort = 4334
	name = raw_input("Who are you: ")
	key = getPublicKey(name)
	lkey = key.split("\n")
	lkl = len(lkey)
	c.connect((clientHost,clientPort))
	c.send("AUTH")
	time.sleep(1)
	c.send(name)
	time.sleep(1)
	i = 0 
	while i < lkl:
		c.send(str(lkey[i]) + "\n")
		i += 1 
	c.send("EOF")
	print "Sent your Public Key to the server"
	print " You are logged in as " + name
	
	icmd = raw_input("COMMAND: ")
	c.send(icmd)
	resp = c.recv(1024)
	if resp.strip() == "key":
		wKey = raw_input("Which User: ")
		c.send(wKey)
		time.sleep(2)
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
		resk = addKey(data)
		print resk
	if resp.strip() == "encrypt":
		eWho = raw_input("FOR WHO: ")
		eKey = raw_input("DATA: ")
		cText = encrypt(eKey,eWho)
		c.send(eWho)
		c.send(name)
		lText = cText.split("\n")
		ll = len(lText)
		i = 0 
		while i < ll:
			c.send(str(lText[i])+"\n")
			i += 1
		c.send("EOF")
		print "Message sent to " + str(eWho)
	if resp.strip() == "messages":
		# mWho = raw_input("FOR WHO: ")
		mWho = name
		c.send(mWho)
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
		fMes = data
		w = fMes
		m = fMes
		m = m.replace("\\n","\n")
		m = m.replace("\\n","\n")
		tmes = m.split("-----BEGIN PGP MESSAGE-----")
		lmes = tmes[1].replace("'}","")
		emes = "-----BEGIN PGP MESSAGE-----" + lmes
		print "FROM: " + tmes[0].replace("{'","")
		emes = emes.replace("': '","")
		#print emes

		print "----------------------------------------"
		clearMessage = decrypt(emes)
		print clearMessage




	