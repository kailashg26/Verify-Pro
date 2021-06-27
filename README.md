# 2021 ACSAC Artifact for Verify-Pro
# Verify-Pro: A Framework for Server Authentication using Communication Protocol Dialects


In this paper, we develop a novel system, called Verify-Pro, to provide server authentication using communication protocol dialects – that uses a client-server architecture based on network protocols for customizing the communication transactions. For each session, a particular sequence of handshakes will be used as dialects. So, given the context, with the establishment of one time username and password, we use the dialects as an authentication mechanism for each request (e.g.,(get filename) in FTP) throughout the session which enforces continuous authentication. Specifically, we leverage a machine learning approach (pre-trained neural network model) on both client and server machines to communicate in a specific dialect dynamically for each request.

# Background details
* The FTP protocol defines how FTP programs should work together when sharing files. It uses the client/server model in its implementation. 
* File Transfer Protocol is still widely used for fast file sharing. Biggest file sharing companies such as ExaVault, Box.com, BrickFTP, Sharefile and SmartFile are using FTP for their services. 
* FTP was not built to be secure. It is considered to be an insecure protocol because it relies on clear-text usernames and passwords for authentication and does not use encryption. Data sent via FTP is vulnerable to sniffing, spoofing, and brute force attacks, among other basic attack methods.
### Is FTP still a viable option for sending file transfers? 
* While organizations across all industries have started shifting to secure FTP protocols like SFTP and FTPS, a surprising number of businesses still use FTP to transfer sensitive documents across internal and external networks. The search "how to use FTP" comes up with over 163 million results on Google, for example, versus only 29 million for the more secure "how to use secure FTP" search. 
* People are always on the lookout for free or open-source software that will help them do their job quickly and efficiently, and FTP is no exception.

# Objective of this work:
The aim of this work is to utilize protocol dialects (definition below) as an authentication mechanism to verify the identity of server system.
### Note: 
* The objective of this protocol dialect is to add authentication to FTP in addition to the existing authentication performed by TLS. The security mechanisms and protocol dialect provided here is not designed as a replacement to TLS.
### Protocol dialects: 
* A protocol dialect is a variation of an existing protocol at the binary level to incorporate additional security measures, mutating message packets, generate different request-response transactions while maintaining the core functionality of the protocol.
* Examples of dialects:- mutating the message packets, cross-graft numerous implementation of FTP, generating unconventional request-response pairs.

## Verify-Pro
![architecute](https://user-images.githubusercontent.com/68829206/123556724-d2499c00-d75a-11eb-8014-0461d37b67b2.png)![archnew](https://user-images.githubusercontent.com/68829206/123556725-d2499c00-d75a-11eb-9e4d-4c34a673b19d.png)


## Default handshake vs. Verify-Pro handshake
![dialectnew](https://user-images.githubusercontent.com/68829206/123556427-26ec1780-d759-11eb-8ed2-f9d9552532d9.png)

## Getting Started

### Dependencies for system

* Tested on Ubuntu 18.04.5 LTS
* Memory 1.9GiB
* Pocessor- Intel CoreTM i7-4600M CPU @ 2.90GHz
* OS type: 64 bit
* Linux

### Dependencies for Neural network model
```
Python Version: 3.7.10
tensorflow-addons: 0.13.0
Pandas Version: 1.1.5
Numpy Version: 1.19.5
tesnorflow: 2.5.0
tensorflow-probability: 4.4.2

Datatset for the neural network : output/enable2.csv
```
### Libraries for for FTP server
```
import socket
import sys
import os
from cmd import Cmd
from getpass import getpass
import signal
import datetime
import pickle
import time
import csv
from threading import Thread
import subprocess
from string import digits
```

### Installing

* VM image of Verify-Pro tool can be found here: 

### Executing program
```
On server side: sudo python3 server.py 21 
On client side: sudo python3 client.py 127.0.0.1 21

127.0.0.1 -> Hostname (can be changed)
21 -> port number (can be changed)
```
### Demo video:


## Help: 
* FTP server login details can be found in users.txt file
```
FTP server login details can be found in users.txt file 
Users who want to try different filenames, can give this input: (get-> command, file.txt is a filename for FTP protocol)
D1  - get file.txt
D4  - get karthikeya.txt 
D8  - get gwu.txt 
D9  - get george.txt 
D10 - get dummy.txt
```

## Note:
* Please refer the paper for the customized transactions of the communication protocol.
* Neural network & decision tree model: check in the output folder

## Output Screenshot:
![output-dialect](https://user-images.githubusercontent.com/68829206/123555806-0078ad00-d756-11eb-8800-5b58b14edce8.jpeg)

## Requirements

* python3 (version >= 3.6)


## Acknowledgments

Inspiration, code snippets, etc.
* [FTP-python](https://github.com/ShripadMhetre/FTP-Python.git)
