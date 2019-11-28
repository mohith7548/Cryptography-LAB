import ntplib
import datetime
import time
import socket
import threading
import string
import random
import pyDes
import sys
from datetime import datetime, timezone, timedelta
from threading import Timer

Key_V="ac3Hn57a" # already shared between application server tgs server
Key_C_V="" #session key with client

#================================================================================================================
# function for random key generator
def randomKeyGenerator():
	stringLength=8
	lettersAndDigits = string.ascii_letters + string.digits
	return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


#=================================================================================================================
#Encryption and decrytion for DES 

def des_encrypt(key, plain_text):
	IV="33333333"
	key_handler = pyDes.des(key, pyDes.CBC, IV, pad=None, padmode=pyDes.PAD_PKCS5)
	cipher_text = key_handler.encrypt(plain_text)
	#print("encrpted: {}".format(cipher_text))
	return cipher_text

def des_decrypt(key, cipher_text):
	IV="33333333"
	key_handler = pyDes.des(key, pyDes.CBC, IV, pad=None, padmode=pyDes.PAD_PKCS5)
	plain_text = key_handler.decrypt(cipher_text)
	#print("decrpted: {}".format(plain_text))
	return plain_text


#================================================================================================================

#================================================================================================================

#Class for execution functions periodically in a non-blocking way
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

#global variables used for time server
curr_time_from_GMT=0
GMT_log=0
start_time=0
return_time=0

def initialize_time_variables(): #initializing of variables. Later, Initialization will be implemented after every five minutes
	global curr_time_from_GMT
	global start_time
	global GMT_log
	global return_time
	try:
		c = ntplib.NTPClient()
		# Provide the respective ntp server ip in below function
		response = c.request('0.asia.pool.ntp.org', version=3)
		response.offset 
		curr_time_from_GMT=datetime.fromtimestamp(response.tx_time, timezone.utc)
		start_time=time.time()
		GMT_log=curr_time_from_GMT
		return_time=curr_time_from_GMT
	except Exception as e:
		print("Unable to connect to GMT Server. Will rety in 60 secs.\nTime will be calculated using 'last fetched time' from GMT server.")
		print("------------------------------------------------------------")
initialize_time_variables()		
rt = RepeatedTimer(60, initialize_time_variables) # it auto-starts, no need of rt.start()		

def getGMTtime():
	global curr_time_from_GMT
	global start_time
	global GMT_log
	global return_time
	try:
		c = ntplib.NTPClient()
		# Provide the respective ntp server ip in below function
		response = c.request('0.asia.pool.ntp.org', version=3)
		response.offset 
		curr_time_from_GMT=datetime.fromtimestamp(response.tx_time, timezone.utc);
		start_time=time.time()
		GMT_log=curr_time_from_GMT
		return_time=curr_time_from_GMT
		return return_time
	except Exception as e:
		print("unable to connect to GMT Server online. (Server Down or Connection Issue!)")
		print("Calculating GMT time from last fetched time from GMT Server at {} ".format(GMT_log))
		return_time=curr_time_from_GMT + timedelta(seconds=time.time() - start_time)
		return return_time


################################################################################################################
######################## code for authenticating client and providing gmt time to client #######################
################################################################################################################




class serverThread(threading.Thread):
	def __init__(self, client):
		threading.Thread.__init__(self)
		self.client = client

	def run(self):
		dataRecvd = self.client.recv(256)
		print()
		print("----------------------------------------------------------------")
		print("Request Recieved from client")
		print(dataRecvd)
		values = dataRecvd.split('||'.encode('utf-8'))
		server_ticket_encrypted = values[0]
		authenticator_client_encrypted = values[1]
		print("Components of resquest recieved:	")
		print()
		print("server_ticket: {}".format(server_ticket_encrypted))
		print()
		print("authenticator_client: {}".format(authenticator_client_encrypted))
		print()
		server_ticket_decrypted=des_decrypt(Key_V,server_ticket_encrypted).decode('utf-8')
		print()
		print("======================== Server Ticket ==========================")
		print(server_ticket_decrypted)
		print()
		values=server_ticket_decrypted.split('||')

		Key_C_V=values[0]
		client_id=values[1]
		client_address=values[2]
		server_id=values[3]
		time_stamp4=values[4]
		life_time4=values[5]

		print()
		print("======================== Client Authenticator ===================")
		authenticator_client_decrypted=des_decrypt(Key_C_V,authenticator_client_encrypted).decode('utf-8')
		print(authenticator_client_decrypted)
		print()
		values=authenticator_client_decrypted.split('||')
		client_id_authenticator=values[0]
		client_address_authenticator=values[1]
		time_stamp5=values[2]

		print("----------------------------------------------------------------")
		print("Validating client...")
		if(client_id==client_id_authenticator and client_address==client_address_authenticator):
				print("---------------------------------")
				print("Client Authentication Successful!")
				print("---------------------------------")
		else:
				print("-----------------------------------------")
				print("Client Authentication Failed! Exiting ...")
				print("-----------------------------------------")
				sys.exit()

		#============================= Prepare message for client======================================
		new_time_stamp=str(float(time_stamp5)+1.000000)
		msg = ''
		gmt_time_stamp=str(getGMTtime())
		gmt_time_stamp=gmt_time_stamp
		if len(dataRecvd) != 0:
			msg=new_time_stamp+"||"+gmt_time_stamp
			msg_encrypted = des_encrypt(Key_C_V,msg)
		else:
			msg = 'No data found'
			msg = msg.encode('UTF-8')
		#encrypted_hash = rsa.encrypt(msg, privateKeyServer)
		print("----------------------------------------------------------------")
		print('Message Sent to Client :')
		print(msg_encrypted)
		print("----------------------------------------------------------------")
		
		#print(temp1)
		#self.client.send(pkc)
		self.client.send(msg_encrypted)
		self.client.close()

server_socket = socket.socket()
server_socket.bind(('127.0.0.1', 3335))
server_socket.listen(5)
while True:
	print('Server is Listening... ')
	client,addr = server_socket.accept()
	print('Connected to : {}'.format(addr))
	serverThread(client).start()

server_socket.close()