# **Simple File Transfer Protocol**

*for Project 1 of Computer Networking<br /> 
University of Indonesia odd AY 2016/2017*

implementation of file transfer protocol using socket<br />
implemented in python, using multiprocessing to handle multi-user connection

### **How to run**
- clone this project
- make sure you have python 2 installed
- run the server by typing `python ftpserver.py` (by default server will use localhost, port 10021 for transfer &amp; 10020 for data transfer)
- In a different terminal session, run the client by typing `python ftpclient.py` (by default it will connect to localhost port 10021 &amp; 10020) 
- start to give command to the server (see some **commands** below)

### **Main Commands**
- [x] LIST
- [ ] STOR
- [ ] RETR 

### **Additional Commands**
- [x] PWD, get current remote directory
- [x] CDUP, change to parent remote directory
- [x] CWD <path>, change current remote directory
- [x] MKD <dir_name>, make a directory in remote server
- [x] RMD <dir_name>, remove a directory in remote server
- [x] DELE <file_name>, delete a file in remote server 
- [ ] other commands... see [list of FTP commands](https://en.wikipedia.org/wiki/List_of_FTP_commands)

### **Milestones**
- [x] Socket
- [x] Multiprocessing
- [x] Read from arguments for server address &amp; ports
- [ ] other...

### **Contributing**
To contribute to this project see [CONTRIBUTING](CONTRIBUTING.md)