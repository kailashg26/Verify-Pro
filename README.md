# Verify-Pro
A Framework for Server Authentication using Communication Protocol Dialects

Abstract: In this paper, we develop a novel system, calledVerify-Pro, toprovide server authentication using communication protocol dialects – that uses a client-server architecture based on networkprotocols for customizing the communication transactions. Foreach session, a particular sequence of handshakes will be used asdialects. So, given the context, with the establishment of one timeusername and password, we use the dialects as an authenticationmechanism for each request (e.g.,get filenamein FTP) throughoutthe session which enforcescontinuous authentication. Specifi-cally, we leverage a machine learning approach (pre-trained neuralnetwork model) on both client and server machines to communi-cate in a specific dialect dynamically for each request.

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



