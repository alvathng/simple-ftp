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
	  	self.close_client()
	  except:
	  	print 'Connection to', self.address, ':', self.port, 'failed'
	  	self.close_client()

	def start(self):
		try:
			self.create_connection()
			while True:
				command = raw_input('Enter command: ')
				cmd  = command[:4].strip().upper()
				path = command[4:].strip()

				self.sock.send(command)
				data = self.sock.recv(1024)

				print data
				if (cmd == 'QUIT'):
					self.close_client()
				elif (cmd == 'LIST' or cmd == 'STOR' or cmd == 'RETR'):
					if (data and (data[0:3] == '125')):
						func = getattr(self, cmd)
						func(path)
						data = self.sock.recv(1024)
						print data
		except Exception, e:
			print e
			self.close_client()

	def connect_datasock(self):
		self.datasock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.datasock.connect((self.address, self.data_port))

	def LIST(self, path):
		try:
			self.connect_datasock()

			while True:
				dirlist = self.datasock.recv(1024)
				if not dirlist: break
				sys.stdout.write(dirlist)
				sys.stdout.flush()
		except:
			pass
		finally:
			self.datasock.close()

	def STOR(self, path):
		print 'Storing', path, 'to the server'
		try:
			self.connect_datasock()
		
			f = open(path, 'r')
			upload = f.read(1024)
			while upload:
				self.datasock.send(upload)
				upload = f.read(1024)
		except:
			pass
		finally:
			f.close()
			self.datasock.close()

	def RETR(self, path):
		print 'Retrieving', path, 'from the server'
		try: 
			self.connect_datasock()

			f = open(path,'w')
			while True:
				download = self.datasock.recv(1024)
				if not download: break
				f.write(download)
		finally:
			f.close()
			self.datasock.close()

	# stop FTP client, close the connection and exit the program
	def close_client(self):
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