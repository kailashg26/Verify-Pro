# Verify-Pro
A Framework for Server Authentication using Communication Protocol Dialects

Abstract: In this paper, we develop a novel system, called Verify-Pro, toprovide server authentication using communication protocol dialects – that uses a client-server architecture based on networkprotocols for customizing the communication transactions. Foreach session, a particular sequence of handshakes will be used as dialects. So, given the context, with the establishment of one time username and password, we use the dialects as an authentication mechanism for each request (e.g.,get filenamein FTP) throughout the session which enforces continuous authentication. Specifically, we leverage a machine learning approach (pre-trained neural network model) on both client and server machines to communicate in a specific dialect dynamically for each request.

Usage of the tool for FTP protocol:
On server side: sudo python3 server.py 21 
On client side: sudo python3 client.py 127.0.0.1 21

127.0.0.1 -> Hostname (can be changed)
21 -> port number (can be changed)

Protocol Customization:
1. clientdialects.py -> all the client dialects for FTP protocol 
2. serverdialects.py -> all the server dialects for FTP protocl 

Note: Please refer the paper for the customized transactions of the communication protocol.

Neural network & decision tree model: check in the output folder

Note: Users who want to try different filenames, can give this input: (get-> command, file.txt is a filename for FTP protocol)\
D1  - get file.txt\
D4  - get karthikeya.txt \
D8  - get gwu.txt \
D9  - get george.txt \
D10 - get dummy.txt 

# 2021 ACSAC Artifact 
# Verify-Pro-A Framework for Server Authentication using Communication Protocol Dialects


In this paper, we develop a novel system, called Verify-Pro, toprovide server authentication using communication protocol dialects – that uses a client-server architecture based on networkprotocols for customizing the communication transactions. Foreach session, a particular sequence of handshakes will be used as dialects. So, given the context, with the establishment of one time username and password, we use the dialects as an authentication mechanism for each request (e.g.,get filenamein FTP) throughout the session which enforces continuous authentication. Specifically, we leverage a machine learning approach (pre-trained neural network model) on both client and server machines to communicate in a specific dialect dynamically for each request.


## Description

An in-depth paragraph about your project and overview of use.

## Getting Started
On server side: sudo python3 server.py 21 
On client side: sudo python3 client.py 127.0.0.1 21

127.0.0.1 -> Hostname (can be changed)
21 -> port number (can be changed)

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* VM image of Verify-Pro tool can be found here: 

### Executing program
```
On server side: sudo python3 server.py 21 
On client side: sudo python3 client.py 127.0.0.1 21

127.0.0.1 -> Hostname (can be changed)
21 -> port number (can be changed)
```

## Note: Users who want to try different filenames, can give this input: (get-> command, file.txt is a filename for FTP protocol)\
```
D1  - get file.txt\
D4  - get karthikeya.txt \
D8  - get gwu.txt \
D9  - get george.txt \
D10 - get dummy.txt 
```

## Programming language Version 

* Python3


## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
