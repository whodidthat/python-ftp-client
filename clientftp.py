#!usr/bin/python
# -*- coding: utf-8 -*-
"""
Updated on Sun Feb 12 22:15:42 2017

@author: whodidthat
@purpose: To understand how a TCP socket program works by developing
a simplified FTP client that works with any stadard server.
@language: Python 2.7

"""
import socket #so we can connect to a server
#import sys # lets us run system commands
import getpass #promts user for a username and password
import os #lets us access the Operating sysytem and run commands from client to server

global host, ip, s

#creates a socket connection called s
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#define a function that creates a socket to connect to a server
def connect_socket():
    #user inputs myftp followed by target hostname.
    #this format splits user input per each space
    myftp, host = raw_input('>>>').split()
    
    if myftp == 'myftp':
        #gets IP address by host
        ip = socket.gethostbyname(host)
        #defines the port being used to connect
        port = 21
      
        #connects target host to the server socket
        s.connect((ip, port))
    else:
        print 'Invalid command. Try using: "myftp <server-name>'
        connect_socket()

#a function that determines user authentication based on user input
def ftp_login():
        #Prompts user for a username
        USER = raw_input('Login: ')
        #prompts user for a password
        #This format matches username ot password and masks the password field
        PASS = getpass.getpass('Password: ')
        #Sends the server the FTP commands and user input. waits for a response.
        #CRLF lets the server know that its the end of the file
        s.sendall('USER' + USER + 'PASS' + PASS + "\r\n")    
        response = s.recv(1024)
        if response == '220' or '230':
            #displays the servers response and the numner of bytes transferred
            print 'Login successful! You are now logged in.', str(response)
            print len(response), 'bytes  transferred'
        else:
            print 'Invalid username and/or password. Please try again'
            ftp_login()

def commands():  
    msg = raw_input('myftp>')    
    #Now we create an infinite loop so that while it's listening, it can receive instructions.
    #the only way the loop will break is when the server closes it's connection.   
    while True:
        #create a message via user input be adding string ("myftp>") or by string variable(prompt)
        if msg == 'quit':
            try:
                #This command terminates a USER and, if file transfer is not in progress, closes the control connection.
                s.sendall('QUIT')
                response = s.recv(1024)
                print 'Successful. server says: ', str(response)
            except:
                print 'invalid response try again'
                commands()
        #if the firt two characters are cd.                               
        if msg[:2] == 'cd':
            try:
                #read user input starting at the 3rd character       
                cmd = os.chdir(msg[3:])
                #This command is a special case of CWD which allows the transfer of
                # directory trees between operating systems having different syntaxes for naming the parent directory
                s.sendall('CWD' + cmd + "\r\n")
                response = s.recv(1024)
                print'Successful. server says: ', str(response)
                print len(response), 'bytes  transferred'
                commands()
            except:
                print 'The specified directory does not exist.'
                commands()
                
        #downloads a file 
        if msg == 'get':
            try:
                #read user input starting add the fourth character
                cmd = msg[4:] 
                #Sends to server a request to transfer a copy of the remote-file
                s.sendall('RETR'+ cmd + "\r\n")
                response = s.recv(1024)
                print'Download successful. server says: ', str(response)
                print len(response), 'bytes  transferred'
                commands()
            except:
                print 'The specified file does not exist.'
                commands()
       
       #uploads a file
        if msg == 'put': 
            try:
                #read user input starting add the fourth character
                cmd = msg[4:]
                #This command causes the FTP server to accept the data transferred 
                # via the data connection and to store the data as a file at the FTP server
                s.sendall('STOR' + cmd + "\r\n")
                response = s.recv(1024)
                print'Upload successful. server says: ', str(response)
                print len(response), 'bytes  transferred'
                commands()
            except:
                print 'The specified file cannot be found'
                commands()
        
        # delete a file
        if msg == 'delete':
            try:
                #read user input starting add the seventh character
                cmd = msg[7:]
                #This command causes the server to transfer a copy of the file 
                # specified in pathname to the client. 
                s.sendall('DELE' + cmd + "\r\n")
                response = s.recv(1024)
                print'Successful. server says: ', str(response)
                print len(response), 'bytes  transferred'
                commands()
            except:
                print 'File does not exist.'
                commands()
                
        #show current working directory
        if msg == 'cwd':
            try:
                #This command causes the name of the current working directory to be returned in the reply             
                s.sendall('PWD' + "\r\n")
                response = s.recv(1024)
                if str(response) == '530':
                   ftp_login()
                else:
                    print'The current working directory is: ',  str(response)
                    print len(response), 'bytes  transferred'
                    commands()
            except:
                print 'invalid input. Please try again'
                commands()
    s.close()
#main function     
def main():
        
    #runs the following functions.
    connect_socket()
    ftp_login() 
    commands() 
    
#Starts the ftp client
main()       

