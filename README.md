# python-ftp-client
An ftp client written in python 2.7 without using libraries

#########################################################
#Compiling instructions: python clientftp.py	        	#
#Running instructions: myftp <server-name>		          #
#########################################################

#########################################################
#		                Instructions:			                  #
#########################################################


##User will get prompted for a username and password.

#########################################################
#		                  COMMANDS: 	(so far)             	#
#########################################################

#RFC-959 Section 4.1 FTP COMMANDS 


#change directory in the remote server

cd <remote-path> 

#download file remotely to your local machine

get <remote-file>

#upload a file to the remote server with the same file name

put <local-file>

#delete a remote file

delete <remote-file>

#quits the ftp client

quit
