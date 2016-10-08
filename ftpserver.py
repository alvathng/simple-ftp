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
import threading

basecwd = os.getcwd()

class FTPThreadServer(threading.Thread):
	def __init__(self, (client, client_address), local_ip, data_port):
		self.client = client
		self.client_address = client_address
		self.cwd = basecwd
		self.data_address = (local_ip, data_port)
		threading.Thread.__init__(self)

	def start_datasock(self):
		# create TCP socket
		self.datasock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.datasock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		try:
			self.client.send('150 Opening data transfer.\r\n')
			print 'Creating data socket on' + str(self.data_address) + '...'
			
			self.datasock.bind(self.data_address)
			self.datasock.listen(1)
			
			print 'Data socket is started. Listening to' + str(self.data_address) + '...'
			self.client.send('125 Data connection already open; transfer starting.\r\n')

			return self.datasock.accept()
		except Exception, e:
			print 'ERROR: ' + str(self.client_address) + ': ' + str(e)
			print 'Closing socket connection...'
			self.close_datasock()
			self.client.send('425 Cannot open data connection.\r\n')
			
	def close_datasock(self):
		self.datasock.close()

	def run(self):
		try :
			print 'client connected: ' + str(self.client_address) + '\n'

			while True:
				cmd = self.client.recv(1024)
				if not cmd: break
				print 'commands from ' + str(self.client_address) + ': ' + cmd
				try:
					func = getattr(self, cmd[:4].strip().upper())
					func(cmd)
				except AttributeError, e:
					print str(e)
					print 'ERROR: ' + str(self.client_address) + ': Invalid Command.'
					self.client.send('550 Invalid Command\r\n')
		except Exception, e:
			print 'ERROR: ' + str(self.client_address) + ': ' + str(e)

			print 'Closing connection from ' + str(self.client_address) + '...'
			self.client.close()
			quit()

	def LIST(self, cmd):
		print 'LIST', self.cwd		
		self.start_datasock()
		try:
			for i in os.listdir(self.cwd):
				print i
				self.datasock.send(i + '\r\n')
			self.close_datasock()
			self.client.send('226 Directory send OK.\r\n')
		except Exception, e:
			print 'ERROR: ' + str(self.client_address) + ': ' + str(e)
			self.close_datasock()
			self.client.send('426 Connection closed; transfer aborted.\r\n')

	def PWD(self, cmd):
		self.client.send('257 \"%s\".\r\n' % self.cwd)

	def CWD(self, cmd):
		dest = os.path.join(self.cwd, cmd[4:].strip())
		if (os.path.isdir(dest)):
			self.cwd = dest
			self.client.send('250 OK \"%s\".\r\n' % self.cwd)
		else:
			print 'ERROR: ' + str(self.client_address) + ': No such file or directory.'
			self.client.send('550 \"' + dest + '\": No such file or directory.\r\n')

	def CDUP(self, cmd):
		dest = os.path.abspath(os.path.join(self.cwd, '..'))
		if (os.path.isdir(dest)):
			self.cwd = dest
			self.client.send('250 OK \"%s\".\r\n' % self.cwd)
		else:
			print 'ERROR: ' + str(self.client_address) + ': No such file or directory.'
			self.client.send('550 \"' + dest + '\": No such file or directory.\r\n')


	def MKD(self, cmd):
		dirname = os.path.join(self.cwd, cmd[4:].strip())
		try:
			if not dirname:
				self.client.send('501 Missing arguments <dirname>.\r\n')
			else:
				os.mkdir(dirname)
				self.client.send('250 Directory created: ' + dirname + '.\r\n')
		except Exception, e:
			print 'ERROR: ' + str(self.client_address) + ': ' + str(e)
			self.client.send('550 Failed to create directory ' + dirname + '.')

	def RMD(self, cmd):
		dirname = os.path.join(self.cwd, cmd[4:].strip())
		try:
			if not dirname:
				self.client.send('501 Missing arguments <dirname>.\r\n')
			else:
				os.rmdir(dirname)
				self.client.send('250 Directory deleted: ' + dirname + '.\r\n')
		except Exception, e:
			print 'ERROR: ' + str(self.client_address) + ': ' + str(e)
			self.client.send('550 Failed to delete directory ' + dirname + '.')

	def DELE(self, cmd):
		filename = os.path.join(self.cwd, cmd[4:].strip())
		try:
			if not filename:
				self.client.send('501 Missing arguments <filename>.\r\n')
			else:
				os.remove(filename)
				self.client.send('250 File deleted: ' + filename + '.\r\n')
		except Exception, e:
			print 'ERROR: ' + str(self.client_address) + ': ' + str(e)
			self.client.send('550 Failed to delete file ' + filename + '.')

	def STOR(self, cmd):
		path = os.path.join(self.cwd, cmd[4:].strip())
		(client_data, client_address) = self.start_datasock()
		
		try:
			file_write = open(path, 'w')
			while True:
				data = client_data.recv(1024)
				if not data:
					break
				file_write.write(data)

			file_write.close()
			self.datasock.close()
			self.client.send('226 Transfer complete.\r\n')
		except Exception, e:
			print 'ERROR: ' + str(self.client_address) + ': ' + str(e)
			self.close_datasock()
			self.client.send('426 Connection closed; transfer aborted.\r\n')

	def RETR(self, cmd):
		path = os.path.join(self.cwd, cmd[4:].strip())
		(client_data, client_address) = self.start_datasock()
		
		try:
			file_read = open(path, "r")
			data = file_read.read(1024)

			while data:
				client_data.send(data)
				data = file_read.read(1024)

			file_read.close()
			self.datasock.close()
			self.client.send('226 Transfer complete.\r\n')
		except Exception, e:
			print 'ERROR: ' + str(self.client_address) + ': ' + str(e)
			self.close_datasock()
			self.client.send('426 Connection closed; transfer aborted.\r\n')


class FTPserver:
	def __init__(self, port, data_port):
		# server address at localhost
		self.address = '127.0.0.1'

		self.port = int(port)
		self.data_port = int(data_port)

	def start_sock(self):
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

	def start(self):
		self.start_sock()

		try:
			while True:
				print 'Waiting for a connection'
				thread = FTPThreadServer(self.sock.accept(), self.address, self.data_port)
				thread.daemon = True
				thread.start()
		except KeyboardInterrupt:
			print 'Closing socket connection'
			self.sock.close()
			quit()


# Main
port = raw_input("Port - if left empty, default port is 10021: ")
if not port:
	port = 10021

data_port = raw_input("Data port - if left empty, default port is 10020: ")
if not data_port:
	data_port = 10020

server = FTPserver(port, data_port)
server.start()