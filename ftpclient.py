# simple FTP client
# commands
#		LIST <path>, information of a directory or file,
#					 or information of current remote directory if not specified
#		STOR <file_name>, copy file to current remote directory 
# 	RETR <file_name>, retrieve file from current remote directory
# additional commands
#		PWD, get current remote directory
#		CDUP, change to parent remote directory
#		CWD <path>, change current remote directory
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

	def create_connection(self):
	  print 'Starting connection to', self.address, ':', self.port

	  try:
	  	server_address = (self.address, self.port)
	  	self.sock.connect(server_address)
	  	print 'Connected to', self.address, ':', self.port
	  except KeyboardInterrupt:
	  	self.command_quit()
	  except:
	  	print 'Connection to', self.address, ':', self.port, 'failed'
	  	print 'FTP client terminating...'
	  	quit()


	def start(self):
		try:
			self.create_connection()
			while True:
				raw = raw_input('Enter command: ')
				arguments = raw.split(' ')

				command = arguments[0].upper()
				if (command == 'QUIT'):
					self.command_quit()
				elif (command == 'STOR'):
					self.command_stor(arguments[1])
				elif (command == 'RETR'):
					self.command_retr(arguments[1])
				else:
					self.sock.send(raw)
					# TODO research, what 1024 really means
					data = self.sock.recv(1024)
					print data
		except:
			self.command_quit()

	def command_stor(self, file_name):
		# TODO implement stor, to copy file from client to server
		print 'Storing', file_name, 'to the server'

	def command_retr(self, file_name):
		# TODO implement retr, to retrieve file from server to client
		print 'Retrieving', file_name, 'from the server'

	# stop FTP client, close the connection and exit the program
	def command_quit(self):
		print 'Closing socket connection...'
		self.sock.close()

		print 'FTP client terminating...'
		quit()

address = raw_input("Destination address - if left empty, default address is localhost: ")

if not address:
	address = 'localhost'

port = raw_input("Port - if left empty, default port is 10021: ")

if not port:
	port = 10021

data_port = raw_input("Data port - if left empty, default port is 10020: ")

if not data_port:
	data_port = 10020

ftpClient = FTPclient(address, port, data_port)
ftpClient.start()