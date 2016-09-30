# simple FTP client
# commands
#		LIST <path>, information of a directory or file,
#					 or information of current remote directory if not specified
#		STOR <file_name>, copy file to current remote directory 
# 	RETR <file_name>, retrieve file from current remote directory
# additional commands
#		QUIT, quit FTP client
#		CWD <path>, change current remote directory
#		CDUP, change to parent remote directory
#		MKD, make a directory in remote server
#		RMD <dir_name>, remove a directory in remote server
#		DELE <file_name>, delete a file in remote server 

import socket
import os
import sys

class FTPclient:
	def __init__(self, address, port, data_port):
		# create TCP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.address = address
		self.port = int(port)
		self.data_port = int(data_port)

	def createConnection(self):
	  print 'Starting connection to', self.address, ':', self.port

	  try:
	  	server_address = (self.address, self.port)
	  	self.sock.connect(server_address)
	  	print 'Connected to', self.address, ':', self.port
	  except KeyboardInterrupt:
	  	self.commandQuit()
	  except:
	  	print 'Connection to', self.address, ':', self.port, 'failed'
	  	print 'FTP client terminating...'
	  	quit()


	def start(self):
		try:
			self.createConnection()
			while True:
				raw = raw_input('Enter command: ')
				arguments = raw.split(' ')

				command = arguments[0].upper()
				if (command == 'QUIT'):
					self.commandQuit()
				elif (command == 'STOR'):
					self.commandStor(arguments[1])
				elif (command == 'RETR'):
					print 'hahaha'
					self.sock.send('lalala')
					self.commandRetr(arguments[1])
				else:
					print 'Command invalid'
		except socket.timeout:
			self.commandQuit()
		except KeyboardInterrupt:
			self.commandQuit()

	def commandStor(self, file_name):
		# TODO implement stor, to copy file from client to server
		print 'Storing', file_name, 'to the server'

	def commandRetr(self, file_name):
		# TODO implement retr, to retrieve file from server to client
		print 'Retrieving', file_name, 'from the server'

	# stop FTP client, close the connection and exit the program
	def commandQuit(self):
		print 'Closing socket connection...'
		self.sock.close()

		print 'FTP client terminating...'
		quit()

# TODO change this using command line arguments argv[]
address = 'localhost'
port = 10022
data_port = 10020
ftpClient = FTPclient(address, port, data_port)
ftpClient.start()