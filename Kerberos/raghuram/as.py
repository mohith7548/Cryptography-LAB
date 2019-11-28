import socket
import threading
import time
import pyDes
import random
import string

directory = 'my_keys/'
directory2='certificates/'
Key_C="raghuram"#already shared with client
Key_TGS="59ZFTjCt" # already shared with AS and TGS

Key_C_TGS="" #session key for tgs and client

time_stamp2=""
life_time2="3600"
#================================================================================================================
# function for random key generator
def randomKeyGenerator():
	stringLength=8
	lettersAndDigits = string.ascii_letters + string.digits
	return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


#=================================================================================================================
#Encryption and decrytion for DES 
data = "DES Algorithm Implementation"
key = randomKeyGenerator()


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

cipher_text = des_encrypt(key, data)
plain_text=des_decrypt(key,cipher_text)	

#================================================================================================================

#================================================================================================================
# Method to genereate tgs-ticket
def generateTgsTicket(Key_C_TGS, client_id, tgs_id, time_stamp2, Address_C):
		
	
	tgs_ticket = Key_C_TGS+"||"+client_id+"||"+Address_C+"||"+tgs_id+"||"+time_stamp2+"||"+life_time2
	
	#encryt the tgs_ticket with key_tgs(already shared between AS and tgs)

	return tgs_ticket
#=================================================================================================================	


#=================================================================================================================
#Threading class and constructor

class serverThread(threading.Thread):
	def __init__(self, client):
		threading.Thread.__init__(self)
		self.client = client



	

	def run(self):

		dataRecvd = self.client.recv(256).decode('utf-8')
		values = dataRecvd.split('||')
		client_id = values[0]
		tgs_id = values[1]
		time_stamp1=values[2]
		#Netwrok address of Client .. for the assignment purpose, otherwise actual netwrok address of client will be used.
		client_address = "10.0.0.1" 
		

		
	

		if len(dataRecvd ) == 0:
			msg = "error"
		else:
			print("=================================================================")
			print("Following request recieved from client")
			print()
			print(dataRecvd)

			Key_C_TGS=randomKeyGenerator()
			time_stamp2=str(time.time())
			tgs_ticket=generateTgsTicket(Key_C_TGS, client_id, tgs_id, time_stamp2, client_address)
			tgs_ticket_encrypted=des_encrypt(Key_TGS,tgs_ticket)

		
			msg = Key_C_TGS+"||"+tgs_id+"||"+time_stamp2+"||"+life_time2+"||"
			msg = msg.encode('utf-8')
			
			msg = msg+tgs_ticket_encrypted
			# Encrypt the msg with Key_C(already shared key bettwen AS and client)
			msg_encrypted=des_encrypt(Key_C,msg)
			print("=================================================================")
			print("TGS-Ticket + Session Key(Key_C_TGS) being sent to client")
			print()
			print(msg_encrypted)

		
		self.client.send(msg_encrypted)
		self.client.close()

#=================================================================================================================	


#=================================================================================================================
#Creation of threads by Server

server_socket = socket.socket()
server_socket.bind(('127.0.0.1', 3333))
server_socket.listen(5)
while True:
	print('AS  is Listening... ')
	client,addr = server_socket.accept()
	print('Connected to : {}'.format(addr))
	serverThread(client).start()

server_socket.close()
#=================================================================================================================	










