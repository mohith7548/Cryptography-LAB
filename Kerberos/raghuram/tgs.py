import socket
import threading
import time
import pyDes
import string
import random

#####################Already Shared Keys######################################
Key_V="ac3Hn57a" # already shared between application server tgs server
Key_TGS="59ZFTjCt" # already shared with AS and TGS

##################### Session Keys Declaration ###############################
Key_C_TGS="" # session Key recieved from AS via client
Key_C_V="" # session key for client and application server

time_stamp4=""
life_time4="4600"

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
# Method to genereate tgs-ticket
def generateApplicationServerTicket(Key_C_V,client_id, server_id, time_stamp4, Address_C, life_time4):
	
		
	server_ticket = Key_C_V+"||"+client_id+"||"+Address_C+"||"+server_id+"||"+time_stamp4+"||"+life_time4
	#encryt the tgs_ticket with key_tgs(already shared between AS and tgs)

	return server_ticket
#=================================================================================================================	


#=================================================================================================================
#Threading class and constructor

class serverThread(threading.Thread):
	def __init__(self, client):
		threading.Thread.__init__(self)
		self.client = client



	

	def run(self):

		dataRecvd = self.client.recv(256)
		
	

		if len(dataRecvd ) == 0:
			msg = "error"
		else:
			#=====================================================================================
			#message received from client
			print("================ Request recieved from client====================")
			print("")
			print()
			print(dataRecvd)
			print()
			#=====================================================================================
			# Reading the message 
			values = dataRecvd.split('||'.encode('utf-8'))
			server_id = values[0].decode('utf-8')
			ticket_tgs_encrypted = values[1]
			authenticator_client_encrypted=values[2]
			print("Components of resquesT recieved:	")
			print()
			print("server_id: {}".format(server_id))
			print()
			print("ticket_tgs_encrypted: {}".format(ticket_tgs_encrypted))
			print()
			print("authenticator_client_encrypted: {}".format(authenticator_client_encrypted))

			#decrypt tgs_ticket with Key_TGS
			tgs_ticket=des_decrypt(Key_TGS,ticket_tgs_encrypted).decode('utf-8')
			print()
			print("======================== Tgs Ticket =============================")
			print(tgs_ticket)
			print()
			values=tgs_ticket.split('||')

			Key_C_TGS=values[0]
			client_id=values[1]
			client_address=values[2]
			tgs_id=values[3]
			time_stamp2=values[4]
			life_time2=values[5]

			print("Key_C_TGS:		{}".format(Key_C_TGS))
			print("client_id:		{}".format(client_id))
			print("client_address:		{}".format(client_address))
			print("tgs_id:			{}".format(tgs_id))
			print("time_stamp2:		{}".format(time_stamp2))
			print("life_time2:		{}".format(life_time2))

			# decrypt authenticator with Key_C_TGS
			authenticator_client = des_decrypt(Key_C_TGS,authenticator_client_encrypted).decode('utf-8') 
			values=authenticator_client.split('||')
			client_id=values[0]
			client_address=values[1]
			time_stamp3=values[2]

			time_stamp4=str(time.time())

			#verify authenticator here.....


			#Netwrok address of Client .. for the assignment purpose, otherwise actual netwrok address of client will be used.
			




			Key_C_V=randomKeyGenerator()
			server_ticket=generateApplicationServerTicket(Key_C_V,client_id, server_id, time_stamp4, client_address, life_time4)
			server_ticket_encrypted=des_encrypt(Key_V,server_ticket)
			print("server_ticket")
			print(server_ticket)
			msg = Key_C_V+"||"+server_id+"||"+time_stamp4+"||"
			msg = msg.encode('utf-8')+server_ticket_encrypted
			msg_encypted=des_encrypt(Key_C_TGS,msg)
			print("=================================================================")
			print("ApplicationServer-Ticket + Session Key(Key_C_V) being sent to client")
			print()
			print(msg_encypted)
			# Encrypt the msg with Key_C(already shared key bettwen AS and client)
		
		
		self.client.send(msg_encypted)
		self.client.close()

#=================================================================================================================	


#=================================================================================================================
#Creation of threads by Server

server_socket = socket.socket()
server_socket.bind(('127.0.0.1', 3334))
server_socket.listen(5)
while True:
	print('TGS  is Listening... ')
	client,addr = server_socket.accept()
	print('Connected to : {}'.format(addr))
	serverThread(client).start()

server_socket.close()
#=================================================================================================================	










