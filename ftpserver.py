# simple FTP server
# use multi-threading so it can handle multi FTP request
# commands
#   LIST <path>, information of a directory or file,
#   						 or information of current remote directory if not specified
#   STOR <file_name>, copy file to current remote directory 
#   RETR <file_name>, retrieve file from current remote directory
# additional commands
#		QUIT, quit FTP client
#		PWD, get current remote directory
#   CDUP, change to parent remote directory
#   CWD <path>, change current remote directory
#   MKD, make a directory in remote server
#   RMD <dir_name>, remove a directory in remote server
#   DELE <file_name>, delete a file in remote server 

import socket
import os
import sys
import threading # TODO try to use multi-threading...
import multiprocessing

class FTPserver:
	def __init__(self, port, data_port):
		# server address at localhost
		self.address = '127.0.0.1'

		self.port = int(port)
		self.data_port = int(data_port)

	def open_sock(self):
		# create TCP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_address = (self.address, self.port)

		try:
			print 'Creating data socket on', self.address, ':', self.port, '...'
			self.sock.bind(server_address)
			self.sock.listen(1)
			print 'Server is up. Listening to', self.address, ':', self.port
		except KeyboardInterrupt:
			print 'Closing socket connection...'
			self.sock.close()

			print 'FTP server terminating...'
			quit()
		except Exception, e:
			print 'Failed to create server on', self.address, ':', self.port, 'because', str(e.strerror)
			quit()

	def open_datasock(self):
		# create TCP socket
		self.datasock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.datasock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		data_address = (self.address, self.data_port)

		try:
			print 'Creating data socket on', self.address, ':', self.data_port, '...'
			self.datasock.bind(data_address)
			self.datasock.listen(1)
			print 'Server is up. Listening to', self.address, ':', self.data_port
		except KeyboardInterrupt:
			print 'Closing socket connection...'
			self.datasock.close()

			print 'FTP server terminating...'
			quit()
		except Exception, e:
			print 'Failed to create server on', self.address, ':', self.port, 'because', str(e.strerror)
			quit()

	def run_command(self, command, arguments):
		if (command == 'LIST'):
			ls = os.listdir(self.cwd)
			return '\n'.join(ls)
		elif (command == 'PWD'):
			return self.cwd
		elif (command == 'CWD'):
			if (len(arguments) >= 1):
				try:
					os.chdir(arguments[0])
				except Exception, e:
					return ('Error: ' + str(e.strerror))

				self.cwd = os.getcwd()
				return self.cwd
			else:
				return 'Missing argument: <path>'
			return self.cwd
		elif (command == 'CDUP'):
			os.chdir('..')
			self.cwd = os.getcwd()
			return self.cwd
		elif (command == 'STOR'):
			self.client.send('150 Opening data connection.\r\n')
			self.open_datasock()

			path = os.path.join(self.cwd, arguments[0])
			file_write = open(path, 'wb')
			(client_data, data_addr) = self.datasock.accept()
			print 'Data from', data_addr
			while True:
				data = client_data.recv(1024)
				if not data:
					break
				file_write.write(data)

			file_write.close()
			self.datasock.close()
			return '226 Transfer complete.\r\n'
		else:
		  return 'Invalid command'

	def handle_client(self, client, client_address):
		try:
			print 'client connected: ', client_address
			self.cwd = os.getcwd()
			self.client = client

			while True:
				raw = client.recv(1024)
				if raw:
					print 'commands from', client_address, ':', raw
					split = raw.split(' ')
					command = split[0].upper()
					arguments = split[1:]

					result = self.run_command(command, arguments)
					print result
					self.client.send(result)
				else:
					break
		except Exception, e:
			print str(e)
			print 'Closing connection from', client_address, '...'
			client.close()
			sys.exit(1)

	def start(self):
		self.open_sock()

		try:
			while True:
				print 'Waiting for a connection'
				client, client_address = self.sock.accept()
				
				process = multiprocessing.Process(target = self.handle_client, args = (client, client_address))
				process.daemon = True
				process.start()
		except KeyboardInterrupt:
			print 'Closing socket connection'
			self.sock.close()
			quit()


# TODO change this using command line arguments argv[]
port = 10021
data_port = 10020
server = FTPserver(port, data_port)
server.start()