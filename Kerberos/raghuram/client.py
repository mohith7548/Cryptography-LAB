import socket
import sys
import time
import pyDes

client_address = "10.0.0.1"
Key_C="raghuram"
Key_C_TGS=""
server_id="GMT-Time-Server"

client_id= input("Enter your kerberos_id  ID: ")
tgs_id= input("Enter TGS Server ID: ")
kerberos_password=input("Enter your kerberos_password: ")

if(client_id!="user123" or kerberos_password!="pwd123"):
	print("Your username and password didn't match!")
	print("Exiting System...")
	sys.exit()

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


############################################################################
# Make connection with AS server
print("=================================================================")
print("Connecting to Authentication Server ...")
s= socket.socket()
s.connect(('127.0.0.1',3333))
print("Connection Successful!")

print("=================================================================")
print("Request for Ticket-TGS sent ...")
print()
# client_id="client id ***"
# tgs_id="tgs id ***"
time_stamp1=str(time.time())
req_as=client_id+"||"+tgs_id+"||"+time_stamp1
req_as=req_as.encode('utf-8')
s.send(req_as)
reply = s.recv(256)
print(reply)
print()
reply_decrypted= des_decrypt(Key_C,reply)

print("=================================================================")
print("TGS-Ticket + Session Key(Key_C_TGS) recieved from AS Server. (same printed below)")
print()
print(reply)
print()
s.close()
#
#Extract TGS-Ticket and session key from the message
values = reply_decrypted.split('||'.encode('utf-8'))
Key_C_TGS = values[0].decode('utf-8')
tgs_id = values[1].decode('utf-8')
time_stamp2=values[2].decode('utf-8')
lifetime2=values[3].decode('utf-8')
tgs_ticket_encypted=values[4] 

print("Components of message received from AS Server:")
print()
print("Key_C_TGS: {}".format(Key_C_TGS))
print("tgs_id: {}".format(tgs_id))
print("time_stamp2: {}".format(time_stamp2))
print("lifetime2: {}".format(lifetime2))
print("tgs_ticket_encypted: {}".format(tgs_ticket_encypted))
print()
print()
print()
print()



############################################################################
# Make connection with TGS server
print("=================================================================")
print("Connecting to TGS Server ...")
s= socket.socket()
s.connect(('127.0.0.1',3334))
print("Connection Successful!")

print("=================================================================")
print("Request for Ticket-V sent ...")
print()
#makeing authencatior-c
time_stamp3=str(time.time())
authenticator_client = client_id+"||"+client_address+"||"+time_stamp3
#encrypt the authenticator_client using Key_C_TGS
authenticator_client_encrypted=des_encrypt(Key_C_TGS,authenticator_client)

req_as=server_id+"||"
req_as=req_as.encode('utf-8')
req_as=req_as+tgs_ticket_encypted+"||".encode("utf-8")+authenticator_client_encrypted
print(req_as)

s.send(req_as)
reply = s.recv(256)

reply_decrypted= des_decrypt(Key_C_TGS,reply)
print("=================================================================")
print("Server-Ticket + Session Key(Key_C_V) recieved from TGS Server. (same printed below)")
print()
print(reply_decrypted)


s.close()
print()
#Extract Server-Ticket and session key(Key_C_V) from the message
values = reply_decrypted.split('||'.encode('utf-8'))
Key_C_V = values[0].decode('utf-8')
server_id = values[1].decode('utf-8')
time_stamp4=values[2].decode('utf-8')
server_ticket_encrypted=values[3]


print("Components of message received from TGS Server:")
print()
print("Key_C_V:	{}".format(Key_C_V))
print("server_id:	{}".format(server_id))
print("time_stamp4:	{}".format(time_stamp4))
print("server_ticket_encrypted:	{}".format(server_ticket_encrypted))
print()
print()
print()
print()
############################################################################



# ############################################################################
# # Make connection with Application Server

print("=================================================================")
print("Connecting to GMT-Time-Server Server ...")
s= socket.socket()
s.connect(('127.0.0.1',3335))
print("Connection Successful!")

print("=================================================================")
print("Server-Ticket and authenticator_client being sent to Application Server ...")
print()

#makeing authencatior-c
time_stamp5=str(time.time())
authenticator_client = client_id+"||"+client_address+"||"+time_stamp5
#encrypt the authenticator_client using Key_C_TGS
authenticator_client_encrypted=des_encrypt(Key_C_V,authenticator_client)
req_application_server=server_ticket_encrypted+"||".encode('utf-8')+authenticator_client_encrypted
print(req_application_server)

s.send(req_application_server)
reply = s.recv(256)
reply_decrypted= des_decrypt(Key_C_V,reply).decode('utf-8')
print()
print("=================================================================")
print("Reply received from Application(for mutual Authentication)")
print()
print(reply)
print()
print("Verifying Server ......")
values=reply_decrypted.split('||')
time_stamp_recieved=values[0]
gmt_time=values[1]
print("time_stamp5 :  {}".format(float(time_stamp5)))
print("time_stamp_recieved : {}".format(time_stamp_recieved))
print("Server Authentication Successful!")
print()
print("GMT Time recieved from GMT-Time-Server :  {}".format(gmt_time))


s.close()
print()


