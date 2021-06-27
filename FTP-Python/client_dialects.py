'''
All client dialects
'''
import socket
import sys
import os
from cmd import Cmd
from getpass import getpass
import signal
import time
import datetime
import dec_tree

'''
## added with Decision tree changes: D0 and D1 are structurally 
## identical, so using D1 for both.
## This deprecates D0
'''
class D0:

    def __init__(self, client_socket, Hash, dialect_model):
        self.client_socket = client_socket
        self.Hash = Hash
        self.dialect_model = dialect_model
        self.dialectNo = 0


    def do_get(self, args):
        """get           receive file"""

        file = args.split()

        if len(file) != 1:
            print("rget requires exactly 1 argument.")
            return

        file_name = file[0]
        try:
            packet = "rget,{}".format(file_name)
            self.client_socket.sendall(packet.encode('utf-8'))

            # Initilize data connection
            dataConnection = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.bind(('', 0))
            dataConnection.listen(1)
            dataPort = dataConnection.getsockname()[1]

            # Send data connection port to server over control connection
            # so server can connect.
            self.client_socket.send(str(dataPort).encode('utf-8'))

            # Wait for server to connect.
            dataConnection, maddr = dataConnection.accept()
            print('[Control] Got connection from', maddr)

            print('200 PORT command successful')

            first_resp = True
            while True:
                recv_data = self.client_socket.recv(1024)

                ## use the decision tree to check if we are in the correct 
                ## dialect
                if first_resp:
                    pkt1 = recv_data.decode('utf-8')
                    inp = 'P1:{}'.format(pkt1)

                    t1 = time.time()
                    predicted_dialect = dec_tree.predict(self.dialect_model, inp)
                    t2 = time.time()

                    print("prediction for :", inp, "was:", predicted_dialect)
                    print("prediction time: %.6f sec" % (t2-t1))
                    if predicted_dialect != self.dialectNo:
                        print("Decision Tree dialect mismatch!")
                        return
                    first_resp = False
                ## end of decision tree usage ##

                packet_info = recv_data.decode('utf-8').split(",")

                if packet_info[0] == "Exists":
                    self.client_socket.sendall("Ready".encode('utf-8'))
                    # print(
                    #     "{} exits on the server, ready to download.".format(file_name))

                    save_file = open(file_name, "wb")

                    amount_recieved_data = 0
                    while amount_recieved_data < int(packet_info[1]):
                        recv_data = dataConnection.recv(1024)
                        amount_recieved_data += len(recv_data)
                        save_file.write(recv_data)

                        # printing hashes for each 1024 bytes of data transfered
                        if self.Hash == True:
                            print('#', end="")

                    # printing new line after printing hashes
                    if self.Hash == True:
                        print()

                    save_file.close()

                    self.client_socket.sendall("Received,{}".format(
                        amount_recieved_data).encode('utf-8'))
                elif packet_info[0] == "Success":
                    print('226 Transfer complete')
                    break
                elif packet_info[0] == "Failed":
                    print(
                        "File {} does not exist on server.".format(file_name))
                    break
                else:
                    print("possible dialect mismatch")
                    print("Something went wrong when downloading '{}' from server. Try again.".format(
                        file_name))
                    break
        except socket.error:
            print("SOCKET_ERROR: Check and ensure that server is running.")


    def do_put(self, args):
        pass
        ...

class D1:

    def __init__(self, client_socket, Hash, dialect_model):
        self.client_socket = client_socket
        self.Hash = Hash
        self.dialect_model = dialect_model
        self.dialectNo = 1


    def do_get(self, args):
        """get           receive file"""

        file = args.split()

        if len(file) != 1:
            print("rget requires exactly 1 argument.")
            return

        file_name = file[0]
        try:
            packet = "rget,{}".format(file_name)
            self.client_socket.sendall(packet.encode('utf-8'))

            # Initilize data connection
            dataConnection = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.bind(('', 0))
            dataConnection.listen(1)
            dataPort = dataConnection.getsockname()[1]

            # Send data connection port to server over control connection
            # so server can connect.
            self.client_socket.send(str(dataPort).encode('utf-8'))

            # Wait for server to connect.
            dataConnection, maddr = dataConnection.accept()
            print('[Control] Got connection from', maddr)

            print('200 PORT command successful')

            first_resp = True
            while True:
                recv_data = self.client_socket.recv(1024)

                ## use the decision tree to check if we are in the correct 
                ## dialect
                if first_resp:
                    pkt1 = recv_data.decode('utf-8')
                    inp = 'P1:{}'.format(pkt1)

                    t1 = time.time()
                    predicted_dialect = dec_tree.predict(self.dialect_model, inp)
                    t2 = time.time()

                    print("prediction for :", inp, "was:", predicted_dialect)
                    print("prediction time: %.6f sec" % (t2-t1))
                    if predicted_dialect != self.dialectNo:
                        print("Decision Tree dialect mismatch!")
                        return
                    first_resp = False
                ## end of decision tree usage ##

                packet_info = recv_data.decode('utf-8').split(",")

                if packet_info[0] == "file exists":
                    self.client_socket.sendall("Ready to recv".encode('utf-8'))
                    # print(
                    #     "{} exits on the server, ready to download.".format(file_name))

                    save_file = open(file_name, "wb")

                    amount_recieved_data = 0
                    while amount_recieved_data < int(packet_info[1]):
                        recv_data = dataConnection.recv(1024)
                        amount_recieved_data += len(recv_data)
                        save_file.write(recv_data)

                        # printing hashes for each 1024 bytes of data transfered
                        if self.Hash == True:
                            print('#', end="")

                    # printing new line after printing hashes
                    if self.Hash == True:
                        print()

                    save_file.close()

                    self.client_socket.sendall("Received,{}".format(
                        amount_recieved_data).encode('utf-8'))
                elif packet_info[0] == "Success":
                    print('226 Transfer complete')
                    break
                elif packet_info[0] == "Failed":
                    print(
                        "File {} does not exist on server.".format(file_name))
                    break
                else:
                    print("possible dialect mismatch")
                    print("Something went wrong when downloading '{}' from server. Try again.".format(
                        file_name))
                    break
        except socket.error:
            print("SOCKET_ERROR: Check and ensure that server is running.")


    def do_put(self, args):
        pass
        ...

# Client: get test.txt
# TODO for Kailash: this description is wrong? (correct in server_dialects)
# TODO need to test this dialect: unable to trigger it
# if (file)
#     server: size(file) / 2
#     server: size(file) / 2
# else
#     server: file not present
#     server: connection closed

# client: Thank you- connection closed

class D2:

    def __init__(self, client_socket, Hash, dialect_model):
        self.client_socket = client_socket
        self.Hash = Hash
        self.dialect_model = dialect_model
        self.dialectNo = 2

    def do_get(self, args):

        file = args.split()

        if len(file) != 1:
            print("rget requires exactly 1 argument.")
            return

        file_name = file[0]
        try:
            packet = "rget,{}".format(file_name)
            self.client_socket.sendall(packet.encode('utf-8'))

            # Initilize data connection
            dataConnection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            dataConnection.bind(('', 0))
            dataConnection.listen(1)
            dataPort = dataConnection.getsockname()[1]

            # Send data connection port to server over control connection
            # so server can connect.
            self.client_socket.send(str(dataPort).encode('utf-8'))

            # Wait for server to connect.
            dataConnection, maddr = dataConnection.accept()
            print('[Control] Got connection from', maddr)
            print('200 PORT command successful')


            recv_data = self.client_socket.recv(1024)
            packet_info = recv_data.decode('utf-8')


            ## use the decision tree to check if we are in the correct 
            ## dialect
            pkt1 = recv_data.decode('utf-8')
            inp = 'P1:{}'.format(pkt1)

            t1 = time.time()
            predicted_dialect = dec_tree.predict(self.dialect_model, inp)
            t2 = time.time()

            print("prediction for :", inp, "was:", predicted_dialect)
            print("prediction time: %.6f sec" % (t2-t1))
            if predicted_dialect != self.dialectNo:
                print("Decision Tree dialect mismatch!")
                return
            
            ## end of decision tree usage ##

            if packet_info != "file not present":

                valid_dialect = False
                file_size = 0
                try:
                    file_size = int(packet_info)
                    if file_size >= 0:
                        valid_dialect = True
                except ValueError as e:
                    pass

                if not valid_dialect:
                    dialect_mismatch("Expected a number (file size)")
                    return

                save_file = open(file_name, "wb")

                amount_recieved_data = 0
                while amount_recieved_data < file_size:
                    recv_data = dataConnection.recv(1024)
                    amount_recieved_data += len(recv_data)
                    save_file.write(recv_data)

                save_file.close()

                t = self.client_socket.recv(1024).decode('utf-8')
                if t != "transfer complete":
                    dialect_mismatch("Expected msg: transfer complete")
                    return

            else:
                print("File {} does not exist on server.".format(file_name))
                t = self.client_socket.recv(1024).decode('utf-8')
                if t != "connection closed":
                    dialect_mismatch("Expected msg: connection closed")
                    return
        
        except socket.error:
            print("SOCKET_ERROR: Check and ensure that server is running.")


    def do_put(self, args):
        pass
        ...


class D3:

    def __init__(self, client_socket, Hash, dialect_model):
        self.client_socket = client_socket
        self.Hash = Hash
        self.dialect_model = dialect_model
        self.dialectNo = 3

    def do_get(self, args):

        file = args.split()

        if len(file) != 1:
            print("rget requires exactly 1 argument.")
            return

        file_name = file[0]
        try:
            packet = "rget,{}".format(file_name)
            self.client_socket.sendall(packet.encode('utf-8'))

            # Initilize data connection
            dataConnection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            dataConnection.bind(('', 0))
            dataConnection.listen(1)
            dataPort = dataConnection.getsockname()[1]

            # Send data connection port to server over control connection
            # so server can connect.
            self.client_socket.send(str(dataPort).encode('utf-8'))

            # Wait for server to connect.
            dataConnection, maddr = dataConnection.accept()
            print('[Control] Got connection from', maddr)
            print('200 PORT command successful')


            recv_data = self.client_socket.recv(1024)
            packet_info = recv_data.decode('utf-8').split(",")


            ## use the decision tree to check if we are in the correct 
            ## dialect
            pkt1 = recv_data.decode('utf-8')
            inp = 'P1:{}'.format(pkt1)

            t1 = time.time()
            predicted_dialect = dec_tree.predict(self.dialect_model, inp)
            t2 = time.time()

            print("prediction for :", inp, "was:", predicted_dialect)
            print("prediction time: %.6f sec" % (t2-t1))
            if predicted_dialect != self.dialectNo:
                print("Decision Tree dialect mismatch!")
                return
            
            ## end of decision tree usage ##

            if packet_info[0] == "file present":

                valid_dialect = False
                file_size = 0
                try:
                    if len(packet_info) == 2:
                        file_size = int(packet_info[1])
                        if file_size >= 0:
                            valid_dialect = True
                except ValueError as e:
                    ...

                if not valid_dialect:
                    dialect_mismatch("Expected a number (file size)")
                    return

                save_file = open(file_name, "wb")

                amount_recieved_data = 0
                while amount_recieved_data < file_size:
                    recv_data = dataConnection.recv(1024)
                    amount_recieved_data += len(recv_data)
                    save_file.write(recv_data)

                save_file.close()

                t = self.client_socket.recv(1024).decode('utf-8')
                if t != "closing the data connection":
                    dialect_mismatch("Expected msg: closing the data connection")
                    return

            else:
                print("possible dialect mismatch")
                print("File {} does not exist on server.".format(file_name))
        
        except socket.error:
            print("SOCKET_ERROR: Check and ensure that server is running.")


    def do_put(self, args):
        pass
        ...



# Client: get test.txt

# if (file)
#     server: size(file) / 2
#     server: size(file) / 2
# else
#     server: file not present
#     server: connection closed

# client: Thank you- connection closed

class D4:

    def __init__(self, client_socket, Hash, dialect_model):
        self.client_socket = client_socket
        self.Hash = Hash
        self.dialect_model = dialect_model
        self.dialectNo = 4

    def do_get(self, args):

        file = args.split()

        if len(file) != 1:
            print("rget requires exactly 1 argument.")
            return

        file_name = file[0]
        try:
            packet = "rget,{}".format(file_name)
            self.client_socket.sendall(packet.encode('utf-8'))

            # Initilize data connection
            dataConnection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            dataConnection.bind(('', 0))
            dataConnection.listen(1)
            dataPort = dataConnection.getsockname()[1]

            # Send data connection port to server over control connection
            # so server can connect.
            self.client_socket.send(str(dataPort).encode('utf-8'))

            # Wait for server to connect.
            dataConnection, maddr = dataConnection.accept()
            print('[Control] Got connection from', maddr)

            print('200 PORT command successful')


            recv_data = self.client_socket.recv(1024)
            recv_data2 = self.client_socket.recv(1024)


            ## use the decision tree to check if we are in the correct 
            ## dialect
            pkt1, pkt2 = recv_data.decode('utf-8'), recv_data2.decode('utf-8')
            inp = 'P1:{}/P2:{}'.format(pkt1, pkt2)

            t1 = time.time()
            predicted_dialect = dec_tree.predict(self.dialect_model, inp)
            t2 = time.time()

            print("prediction for :", inp, "was:", predicted_dialect)
            print("prediction time: %.6f sec" % (t2-t1))
            if predicted_dialect != self.dialectNo:
                print("Decision Tree dialect mismatch!")
                return

            ## end of decision tree usage ##

            packet_info  = recv_data.decode('utf-8').split(",")
            packet_info2 = recv_data2.decode('utf-8').split(",")

            valid_dialect = False
            file_size = 0
            try:
                if len(packet_info) == len(packet_info2) == 1:
                    file_size  = int(packet_info[0])
                    file_size2 = int(packet_info2[0])
                    if file_size >= 0 and file_size == file_size2:
                        valid_dialect = True
                        file_size = 2*file_size
            except ValueError as e:
                ...

            if not valid_dialect:
                dialect_mismatch("Expected a number (file size)")
                return

            if packet_info[0] != "file not present":

                save_file = open(file_name, "wb")

                amount_recieved_data = 0
                while amount_recieved_data < file_size:
                    recv_data = dataConnection.recv(1024)
                    amount_recieved_data += len(recv_data)
                    save_file.write(recv_data)

                save_file.close()

                self.client_socket.sendall("Thank you- connection closed".encode('utf-8'))

            else:
                print("File {} does not exist on server.".format(file_name))
                t = self.client_socket.recv(1024).decode('utf-8')
                if t != "connection closed":
                    dialect_mismatch("Expected msg: connection closed")
                    return
        
        except socket.error:
            print("SOCKET_ERROR: Check and ensure that server is running.")


    def do_put(self, args):
        pass
        ...


class D5:

    def __init__(self, client_socket, Hash, dialect_model):
        self.client_socket = client_socket
        self.Hash = Hash
        self.dialect_model = dialect_model
        self.dialectNo = 5

    def do_get(self, args):

        file = args.split()

        if len(file) != 1:
            print("rget requires exactly 1 argument.")
            return

        file_name = file[0]
        try:
            packet = "rget,{}".format(file_name)
            self.client_socket.sendall(packet.encode('utf-8'))

            # Initilize data connection
            dataConnection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            dataConnection.bind(('', 0))
            dataConnection.listen(1)
            dataPort = dataConnection.getsockname()[1]

            # Send data connection port to server over control connection
            # so server can connect.
            self.client_socket.send(str(dataPort).encode('utf-8'))

            # Wait for server to connect.
            dataConnection, maddr = dataConnection.accept()
            print('[Control] Got connection from', maddr)
            print('200 PORT command successful')


            recv_data = self.client_socket.recv(1024)
            packet_info = recv_data.decode('utf-8')

            ## TODO: in the updated version of this dialect, recv_data
            ## will be int, int, int. That is, 
            ## P1: file exists number, filename len, length
            ## Then the following if condition is accordingly modified/
            ## removed altogether.
            if packet_info == "1":
                recv_data2 = self.client_socket.recv(1024).decode('utf-8')

                ## use the decision tree to check if we are in the correct 
                ## dialect
                pkt1, pkt2 = recv_data.decode('utf-8'), recv_data2.decode('utf-8')
                inp = 'P1:{}/P2:{}'.format(pkt1, pkt2)

                t1 = time.time()
                predicted_dialect = dec_tree.predict(self.dialect_model, inp)
                t2 = time.time()

                print("prediction for :", inp, "was:", predicted_dialect)
                print("prediction time: %.6f sec" % (t2-t1))
                if predicted_dialect != self.dialectNo:
                    print("Decision Tree dialect mismatch!")
                    return

                ## end of decision tree usage ##

                valid_dialect = False
                file_size = 0
                try:
                    file_size = int(recv_data2)
                    if file_size >= 0:
                        valid_dialect = True
                except ValueError as e:
                    ...

                if not valid_dialect:
                    dialect_mismatch("Expected a number (file size)")
                    return

                self.client_socket.send("0".encode("utf-8"))

                save_file = open(file_name, "wb")

                amount_recieved_data = 0
                while amount_recieved_data < file_size:
                    recv_data = dataConnection.recv(1024)
                    amount_recieved_data += len(recv_data)
                    save_file.write(recv_data)

                save_file.close()

                self.client_socket.send("1".encode('utf-8'))

            else:
                # server sent "-1" or wrong dialect
                print("possible dialect mismatch")
                print("File {} does not exist on server.".format(file_name))
        
        except socket.error:
            print("SOCKET_ERROR: Check and ensure that server is running.")


    def do_put(self, args):
        pass
        ...



class D6:

    def __init__(self, client_socket, Hash, dialect_model):
        self.client_socket = client_socket
        self.Hash = Hash
        self.dialect_model = dialect_model
        self.dialectNo = 6

    def do_get(self, args):

        file = args.split()

        if len(file) != 1:
            print("rget requires exactly 1 argument.")
            return

        file_name = file[0]
        try:
            packet = "rget,{}".format(file_name)
            self.client_socket.sendall(packet.encode('utf-8'))

            # Initilize data connection
            dataConnection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            dataConnection.bind(('', 0))
            dataConnection.listen(1)
            dataPort = dataConnection.getsockname()[1]

            # Send data connection port to server over control connection
            # so server can connect.
            self.client_socket.send(str(dataPort).encode('utf-8'))

            # Wait for server to connect.
            dataConnection, maddr = dataConnection.accept()
            print('[Control] Got connection from', maddr)
            print('200 PORT command successful')


            recv_data = self.client_socket.recv(1024)
            packet_info = recv_data.decode('utf-8')

            if packet_info == "file exists":
                recv_data2 = self.client_socket.recv(1024).decode('utf-8')
                recv_data3 = self.client_socket.recv(1024).decode('utf-8')

                #recv_data2 is a,b where a=len of filename and b=4 (len of "rget")
                #recv_data3 is file size

                ## use the decision tree to check if we are in the correct 
                ## dialect
                pkt1 = recv_data.decode('utf-8')
                pkt2 = recv_data2.decode('utf-8')
                pkt3 = recv_data3.decode('utf-8')
                inp = 'P1:{}/P2:{}/P3:{}'.format(pkt1, pkt2, pkt3)

                t1 = time.time()
                predicted_dialect = dec_tree.predict(self.dialect_model, inp)
                t2 = time.time()

                print("prediction for :", inp, "was:", predicted_dialect)
                print("prediction time: %.6f sec" % (t2-t1))
                if predicted_dialect != self.dialectNo:
                    print("Decision Tree dialect mismatch!")
                    return

                ## end of decision tree usage ##

                valid_dialect = False
                file_size = 0
                try:
                    toks = recv_data2.split(",")
                    if len(toks) == 2:
                        a = int(tok[0])
                        b = int(tok[1])
                        file_size = int(recv_data3)
                        if a > 0 and b == 4 and file_size >= 0:
                            valid_dialect = True
                except ValueError as e:
                    ...

                if not valid_dialect:
                    dialect_mismatch("Expected a number (file size)")
                    return

                self.client_socket.send("Details of the request are received".encode("utf-8"))

                save_file = open(file_name, "wb")

                amount_recieved_data = 0
                while amount_recieved_data < file_size:
                    recv_data = dataConnection.recv(1024)
                    amount_recieved_data += len(recv_data)
                    save_file.write(recv_data)

                save_file.close()

                t = self.client_socket.recv(1024).decode('utf-8')
                # t is some float value
                valid_dialect = False
                try:
                    float(t)
                    valid_dialect = True
                except ValueError as e:
                    ...

                if not valid_dialect:
                    dialect_mismatch("Expected a float number")
                    return

                print("TP: " + t)
                self.client_socket.send("success".encode("utf-8"))

            else:
                # server sends "not found"
                print("possible dialect mismatch")
                print("File {} does not exist on server.".format(file_name))
        
        except socket.error:
            print("SOCKET_ERROR: Check and ensure that server is running.")


    def do_put(self, args):
        pass
        ...


# Client: get test.txt

# if (file)
#     Server: "file exists"

# Server: length(filename)
# Server: length(command)
# Server: size(file)

# client: "Details of the request are received"

# Server: send files

# Client: success


class D7:

    def __init__(self, client_socket, Hash, dialect_model):
        self.client_socket = client_socket
        self.Hash = Hash
        self.dialect_model = dialect_model
        self.dialectNo = 7

    def do_get(self, args):

        file = args.split()

        if len(file) != 1:
            print("rget requires exactly 1 argument.")
            return

        file_name = file[0]
        try:
            packet = "rget,{}".format(file_name)
            self.client_socket.sendall(packet.encode('utf-8'))

            # Initilize data connection
            dataConnection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            dataConnection.bind(('', 0))
            dataConnection.listen(1)
            dataPort = dataConnection.getsockname()[1]

            # Send data connection port to server over control connection
            # so server can connect.
            self.client_socket.send(str(dataPort).encode('utf-8'))

            # Wait for server to connect.
            dataConnection, maddr = dataConnection.accept()
            print('[Control] Got connection from', maddr)
            print('200 PORT command successful')


            recv_data = self.client_socket.recv(1024)
            packet_info = recv_data.decode('utf-8')

            if packet_info == "file exists":
                recv_data2 = self.client_socket.recv(1024).decode('utf-8')
                recv_data3 = self.client_socket.recv(1024).decode('utf-8')
                recv_data4 = self.client_socket.recv(1024).decode('utf-8')

                ## use the decision tree to check if we are in the correct 
                ## dialect
                pkt1 = recv_data.decode('utf-8')
                pkt2 = recv_data2.decode('utf-8')
                pkt3 = recv_data3.decode('utf-8')
                pkt4 = recv_data4.decode('utf-8')
                inp = 'P1:{}/P2:{}/P3:{}/P4:{}'.format(pkt1, pkt2, pkt3, pkt4)

                t1 = time.time()
                predicted_dialect = dec_tree.predict(self.dialect_model, inp)
                t2 = time.time()

                print("prediction for :", inp, "was:", predicted_dialect)
                print("prediction time: %.6f sec" % (t2-t1))
                if predicted_dialect != self.dialectNo:
                    print("Decision Tree dialect mismatch!")
                    return

                ## end of decision tree usage ##

                valid_dialect = False
                file_size = 0
                try:
                    a = int(recv_data2)
                    file_size = int(recv_data4)
                    if a > 0 and file_size >= 0 and recv_data3 == "4":
                        valid_dialect = True
                except ValueError as e:
                    ...

                if not valid_dialect:
                    dialect_mismatch("Expected filesize, then 4 (len('rget'), then len file")
                    return


                self.client_socket.send("Details of the request are received".encode('utf-8'))

                save_file = open(file_name, "wb")

                amount_recieved_data = 0
                while amount_recieved_data < file_size:
                    recv_data = dataConnection.recv(1024)
                    amount_recieved_data += len(recv_data)
                    save_file.write(recv_data)

                save_file.close()

                self.client_socket.send("success".encode("utf-8"))

            else:
                print("possible dialect mismatch")
                print("File {} does not exist on server.".format(file_name))
        
        except socket.error:
            print("SOCKET_ERROR: Check and ensure that server is running.")


    def do_put(self, args):
        pass
        ...

class D8:

    def __init__(self, client_socket, Hash, dialect_model):
        self.client_socket = client_socket
        self.Hash = Hash
        self.dialect_model = dialect_model
        self.dialectNo = 8

    def do_get(self, args):

        file = args.split()

        if len(file) != 1:
            print("rget requires exactly 1 argument.")
            return

        file_name = file[0]
        try:
            packet = "rget,{}".format(file_name)
            self.client_socket.sendall(packet.encode('utf-8'))

            # Initilize data connection
            dataConnection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            dataConnection.bind(('', 0))
            dataConnection.listen(1)
            dataPort = dataConnection.getsockname()[1]

            # Send data connection port to server over control connection
            # so server can connect.
            self.client_socket.send(str(dataPort).encode('utf-8'))

            # Wait for server to connect.
            dataConnection, maddr = dataConnection.accept()
            print('[Control] Got connection from', maddr)
            print('200 PORT command successful')


            recv_data = self.client_socket.recv(1024)
            packet_info = recv_data.decode('utf-8').split(',')

            ## use the decision tree to check if we are in the correct 
            ## dialect
            pkt1 = recv_data.decode('utf-8')
            inp = 'P1:{}'.format(pkt1)

            t1 = time.time()
            predicted_dialect = dec_tree.predict(self.dialect_model, inp)
            t2 = time.time()

            print("prediction for :", inp, "was:", predicted_dialect)
            print("prediction time: %.6f sec" % (t2-t1))
            if predicted_dialect != self.dialectNo:
                print("Decision Tree dialect mismatch!")
                return

            ## end of decision tree usage ##

            if len(packet_info) == 4 and packet_info[0] == "file exists":

                valid_dialect = False
                file_size = 0
                try:
                    file_size = int(packet_info[1])
                    if file_size >= 0 and packet_info[3] == "getr":
                        valid_dialect = True
                except ValueError as e:
                    ...

                if not valid_dialect:
                    dialect_mismatch("Expected 'file exists,<file size>,<filename>,getr'")
                    return

                self.client_socket.send("Ready to receive the file".encode('utf-8'))

                save_file = open(file_name, "wb")

                amount_recieved_data = 0
                while amount_recieved_data < file_size:
                    recv_data = dataConnection.recv(1024)
                    amount_recieved_data += len(recv_data)
                    save_file.write(recv_data)

                save_file.close()

                self.client_socket.send("Connection closed, file successfully received".encode('utf-8'))

            else:
                print("possible dialect mismatch")
                print("File {} does not exist on server.".format(file_name))
        
        except socket.error:
            print("SOCKET_ERROR: Check and ensure that server is running.")


    def do_put(self, args):
        pass
        ...

class D9:

    def __init__(self, client_socket, Hash, dialect_model):
        self.client_socket = client_socket
        self.Hash = Hash
        self.dialect_model = dialect_model
        self.dialectNo = 9

    def do_get(self, args):

        file = args.split()

        if len(file) != 1:
            print("rget requires exactly 1 argument.")
            return

        file_name = file[0]
        try:
            packet = "rget,{}".format(file_name)
            self.client_socket.sendall(packet.encode('utf-8'))

            # Initilize data connection
            dataConnection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            dataConnection.bind(('', 0))
            dataConnection.listen(1)
            dataPort = dataConnection.getsockname()[1]

            # Send data connection port to server over control connection
            # so server can connect.
            self.client_socket.send(str(dataPort).encode('utf-8'))

            # Wait for server to connect.
            dataConnection, maddr = dataConnection.accept()
            print('[Control] Got connection from', maddr)
            print('200 PORT command successful')


            recv_data = self.client_socket.recv(1024)
            packet_info = recv_data.decode('utf-8').split(',')

            if len(packet_info) == 2 and packet_info[0] == "file exists":
                file_size = 0
                valid_dialect = False
                try:
                    file_size = int(packet_info[1])
                    if file_size >= 0:
                        valid_dialect = True
                except ValueError as e:
                    ...

                if not valid_dialect:
                    dialect_mismatch("expected filesize as 2nd argument")
                    return

                recv_data2 = self.client_socket.recv(1024)

                ## use the decision tree to check if we are in the correct 
                ## dialect
                pkt1 = recv_data.decode('utf-8')
                pkt2 = recv_data2.decode('utf-8')
                inp = 'P1:{}/P2:{}'.format(pkt1, pkt2)

                t1 = time.time()
                predicted_dialect = dec_tree.predict(self.dialect_model, inp)
                t2 = time.time()

                print("prediction for :", inp, "was:", predicted_dialect)
                print("prediction time: %.6f sec" % (t2-t1))
                if predicted_dialect != self.dialectNo:
                    print("Decision Tree dialect mismatch!")
                    return

                ## end of decision tree usage ##

                packet_info2 = recv_data2.decode('utf-8').split(',')
                if len(packet_info2) != 2 or packet_info2[1] != 'getr':
                    dialect_mismatch("Expected '<filename>,getr'")
                    return

                self.client_socket.send("Ready to receive the file".encode('utf-8'))

                save_file = open(file_name, "wb")

                amount_recieved_data = 0
                while amount_recieved_data < file_size:
                    recv_data = dataConnection.recv(1024)
                    amount_recieved_data += len(recv_data)
                    save_file.write(recv_data)

                save_file.close()

                self.client_socket.send("Connection closed, file successfully received".encode('utf-8'))

            else:
                print("possible dialect mismatch")
                print("File {} does not exist on server.".format(file_name))
        
        except socket.error:
            print("SOCKET_ERROR: Check and ensure that server is running.")


    def do_put(self, args):
        pass
        ...


class D10:

    def __init__(self, client_socket, Hash, dialect_model):
        self.client_socket = client_socket
        self.Hash = Hash
        self.dialect_model = dialect_model
        self.dialectNo = 10

    def do_get(self, args):

        file = args.split()

        if len(file) != 1:
            print("rget requires exactly 1 argument.")
            return

        file_name = file[0]
        try:
            packet = "rget,{}".format(file_name)
            self.client_socket.sendall(packet.encode('utf-8'))

            # Initilize data connection
            dataConnection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            dataConnection.bind(('', 0))
            dataConnection.listen(1)
            dataPort = dataConnection.getsockname()[1]

            # Send data connection port to server over control connection
            # so server can connect.
            self.client_socket.send(str(dataPort).encode('utf-8'))

            # Wait for server to connect.
            dataConnection, maddr = dataConnection.accept()
            print('[Control] Got connection from', maddr)
            print('200 PORT command successful')


            recv_data = self.client_socket.recv(1024)


            expected_recv_data = "file exists"
            if recv_data.decode('utf-8') != expected_recv_data:
                dialect_mismatch("Expected msg: {}".format(expected_recv_data))
                return

            packet_info = recv_data.decode('utf-8')
            

            if packet_info == "file exists":
                recv_data2 = self.client_socket.recv(1024)
                packet_info2 = recv_data2.decode('utf-8').split(',')
                valid_dialect = False

                ## use the decision tree to check if we are in the correct 
                ## dialect
                pkt1, pkt2 = recv_data.decode('utf-8'), recv_data2.decode('utf-8')
                inp = 'P1:{}/P2:{}'.format(pkt1, pkt2)

                t1 = time.time()
                predicted_dialect = dec_tree.predict(self.dialect_model, inp)
                t2 = time.time()

                print("prediction for :", inp, "was:", predicted_dialect)
                print("prediction time: %.6f sec" % (t2-t1))
                if predicted_dialect != self.dialectNo:
                    print("Decision Tree dialect mismatch!")
                    return

                ## end of decision tree usage ##

                if len(packet_info2) == 3:
                    try:
                        size = int(packet_info2[0])
                        if size >= 0 and packet_info2[2] == 'getr':
                            valid_dialect = True
                    except ValueError:
                        ...

                if not valid_dialect:
                    dialect_mismatch("Expected msg: <file_size, file_name, getr>")
                    return

                self.client_socket.send("Ready to receive the file".encode('utf-8'))

                save_file = open(file_name, "wb")

                amount_recieved_data = 0
                while amount_recieved_data < int(packet_info2[0]):
                    recv_data = dataConnection.recv(1024)
                    amount_recieved_data += len(recv_data)
                    save_file.write(recv_data)

                save_file.close()

                self.client_socket.send("Connection closed, file successfully received".encode('utf-8'))

            else:
                print("File {} does not exist on server.".format(file_name))
        
        except socket.error:
            print("SOCKET_ERROR: Check and ensure that server is running.")


    def do_put(self, args):
        pass
        ...

class D11:

    def __init__(self, client_socket, Hash, dialect_model):
        self.client_socket = client_socket
        self.Hash = Hash
        self.dialect_model = dialect_model
        self.dialectNo = 11

    def do_get(self, args):

        file = args.split()

        if len(file) != 1:
            print("rget requires exactly 1 argument.")
            return

        file_name = file[0]
        try:
            packet = "rget,{}".format(file_name)
            self.client_socket.sendall(packet.encode('utf-8'))

            # Initilize data connection
            dataConnection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            dataConnection.bind(('', 0))
            dataConnection.listen(1)
            dataPort = dataConnection.getsockname()[1]

            # Send data connection port to server over control connection
            # so server can connect.
            self.client_socket.send(str(dataPort).encode('utf-8'))

            # Wait for server to connect.
            dataConnection, maddr = dataConnection.accept()
            print('[Control] Got connection from', maddr)
            print('200 PORT command successful')


            recv_data = self.client_socket.recv(1024)
            packet_info = recv_data.decode('utf-8')

            if packet_info == "file exists":
                recv_data2 = self.client_socket.recv(1024).decode('utf-8')
                recv_data3 = self.client_socket.recv(1024).decode('utf-8')
                recv_data4 = self.client_socket.recv(1024).decode('utf-8')


                ## use the decision tree to check if we are in the correct 
                ## dialect
                pkt1 = recv_data.decode('utf-8')
                pkt2 = recv_data2.decode('utf-8')
                pkt3 = recv_data3.decode('utf-8')
                pkt4 = recv_data4.decode('utf-8')
                inp = 'P1:{}/P2:{}/P3:{}/P4:{}'.format(pkt1, pkt2, pkt3, pkt4)

                t1 = time.time()
                predicted_dialect = dec_tree.predict(self.dialect_model, inp)
                t2 = time.time()

                print("prediction for :", inp, "was:", predicted_dialect)
                print("prediction time: %.6f sec" % (t2-t1))
                if predicted_dialect != self.dialectNo:
                    print("Decision Tree dialect mismatch!")
                    return

                ## end of decision tree usage ##

                valid_dialect = False
                file_size = 0
                try:
                    tok2 = recv_data2.split(',')
                    tok3 = recv_data3.split(',')
                    tok4 = recv_data4.split(',')

                    if len(tok2) == 1:
                        file_size = int(tok2[0])
                        if len(tok3) == 2:
                            filename_len = int(tok3[1])
                            if filename_len > 0:
                                if tok4[0] == "rget" and tok4[1] == "4":
                                    valid_dialect = True
                except ValueError as e:
                    ...

                if not valid_dialect:
                    dialect_mismatch("D11: Expected 3 msgs from server. 1 or more are not in the correct format")
                    return

                self.client_socket.send("Ready".encode('utf-8'))
                time.sleep(1)
                self.client_socket.send("to receive the file".encode('utf-8'))

                save_file = open(file_name, "wb")

                amount_recieved_data = 0
                a = datetime.datetime.now()
                while amount_recieved_data < file_size:
                    recv_data = dataConnection.recv(1024)
                    amount_recieved_data += len(recv_data)
                    save_file.write(recv_data)

                save_file.close()
                b = datetime.datetime.now()
                s = (b-a).seconds + ((b-a).microseconds / 1000000)
                t = int(recv_data2) / s

                recv_data5 = self.client_socket.recv(1024).decode('utf-8')
                if recv_data5 != "file transferred":
                    dialect_mismatch("D11: server didn't talk in expected dialect")
                    return

                self.client_socket.sendall("{}".format(t).encode('utf-8'))
                time.sleep(1)
                self.client_socket.sendall("Connection closed, file successfully received ".encode('utf-8'))

            else:
                print("possible dialect mismatch")
                print("File {} does not exist on server.".format(file_name))
        
        except socket.error:
            print("SOCKET_ERROR: Check and ensure that server is running.")


    def do_put(self, args):
        pass
        ...

class D12:

    def __init__(self, client_socket, Hash, dialect_model):
        self.client_socket = client_socket
        self.Hash = Hash
        self.dialect_model = dialect_model
        self.dialectNo = 12

    def do_get(self, args):

        file = args.split()

        if len(file) != 1:
            print("rget requires exactly 1 argument.")
            return

        file_name = file[0]
        try:
            packet = "rget,{}".format(file_name)
            self.client_socket.sendall(packet.encode('utf-8'))

            # Initilize data connection
            dataConnection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            dataConnection.bind(('', 0))
            dataConnection.listen(1)
            dataPort = dataConnection.getsockname()[1]

            # Send data connection port to server over control connection
            # so server can connect.
            self.client_socket.send(str(dataPort).encode('utf-8'))

            # Wait for server to connect.
            dataConnection, maddr = dataConnection.accept()
            print('[Control] Got connection from', maddr)
            print('200 PORT command successful')


            self.client_socket.settimeout(2.0)   # TODO kailash: why this timeout?
            recv_data = self.client_socket.recv(1024)
            packet_info = recv_data.decode('utf-8')


            ## use the decision tree to check if we are in the correct 
            ## dialect
            pkt1 = recv_data.decode('utf-8')
            inp = 'P1:{}'.format(pkt1)

            t1 = time.time()
            predicted_dialect = dec_tree.predict(self.dialect_model, inp)
            t2 = time.time()

            print("prediction for :", inp, "was:", predicted_dialect)
            print("prediction time: %.6f sec" % (t2-t1))
            if predicted_dialect != self.dialectNo:
                print("Decision Tree dialect mismatch!")
                return

            ## end of decision tree usage ##

            file_size = 0
            valid_dialect = False
            try:
                file_size = int(packet_info)
                if file_size >= 0:
                    valid_dialect = True
            except ValueError as e:
                ...

            if not valid_dialect:
                dialect_mismatch("D12: expected a number (file size)")
                return

            save_file = open(file_name, "wb")

            amount_recieved_data = 0
            while amount_recieved_data < file_size:
                recv_data = dataConnection.recv(1024)
                amount_recieved_data += len(recv_data)
                save_file.write(recv_data)

            save_file.close()
        
        except socket.timeout:
            print("File {} does not exist on server.".format(file_name))
        except socket.error:
            print("SOCKET_ERROR: Check and ensure that server is running.")


    def do_put(self, args):
        pass
        ...

class D13:

    def __init__(self, client_socket, Hash, dialect_model):
        self.client_socket = client_socket
        self.Hash = Hash
        self.dialect_model = dialect_model
        self.dialectNo = 13

    def do_get(self, args):

        file = args.split()

        if len(file) != 1:
            print("rget requires exactly 1 argument.")
            return

        file_name = file[0]
        try:
            packet = "rget,{}".format(file_name)
            self.client_socket.sendall(packet.encode('utf-8'))

            # Initilize data connection
            dataConnection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            dataConnection.bind(('', 0))
            dataConnection.listen(1)
            dataPort = dataConnection.getsockname()[1]

            # Send data connection port to server over control connection
            # so server can connect.
            self.client_socket.send(str(dataPort).encode('utf-8'))

            # Wait for server to connect.
            dataConnection, maddr = dataConnection.accept()
            print('[Control] Got connection from', maddr)
            print('200 PORT command successful')


            recv_data = self.client_socket.recv(1024)
            packet_info = recv_data.decode('utf-8')

            ## TODO: in the updated version of this dialect, recv_data
            ## will be str, str, str. That is, 
            ## P1: "file exists", filename, command
            ## Then the following if condition is accordingly modified/
            ## removed altogether.
            if packet_info == "file exists":
                recv_data2 = self.client_socket.recv(1024).decode('utf-8')

                ## use the decision tree to check if we are in the correct 
                ## dialect
                pkt1 = recv_data.decode('utf-8')
                pkt2 = recv_data2.decode('utf-8')
                inp = 'P1:{}/P2:{}'.format(pkt1, pkt2)

                t1 = time.time()
                predicted_dialect = dec_tree.predict(self.dialect_model, inp)
                t2 = time.time()

                print("prediction for :", inp, "was:", predicted_dialect)
                print("prediction time: %.6f sec" % (t2-t1))
                if predicted_dialect != self.dialectNo:
                    print("Decision Tree dialect mismatch!")
                    return

                ## end of decision tree usage ##

                file_size = 0
                valid_dialect = False
                try:
                    file_size = int(recv_data2)
                    if file_size >= 0:
                        valid_dialect = True
                except ValueError as e:
                    ...

                if not valid_dialect:
                    dialect_mismatch("D13: expected file size")
                    return

                self.client_socket.send("Ready".encode('utf-8'))
                time.sleep(1)
                self.client_socket.send("to receive".encode('utf-8'))
                time.sleep(1)
                self.client_socket.send("the file".encode('utf-8'))
                time.sleep(1)

                zp = file_name[:-4] + '.zip'
                save_file = open(zp, "wb")

                amount_recieved_data = 0
                while amount_recieved_data < file_size:
                    recv_data = dataConnection.recv(1024)
                    amount_recieved_data += len(recv_data)
                    save_file.write(recv_data)

                save_file.close()

                self.client_socket.send("success".encode('utf-8'))

            else:
                print("possible dialect mismatch")
                print("File {} does not exist on server.".format(file_name))
        
        except socket.error:
            print("SOCKET_ERROR: Check and ensure that server is running.")


    def do_put(self, args):
        pass
        ...

class D14:

    def __init__(self, client_socket, Hash, dialect_model):
        self.client_socket = client_socket
        self.Hash = Hash
        self.dialect_model = dialect_model
        self.dialectNo = 14

    def do_get(self, args):

        file = args.split()

        if len(file) != 1:
            print("rget requires exactly 1 argument.")
            return

        file_name = file[0]
        try:
            packet = "rget,{}".format(file_name)
            self.client_socket.sendall(packet.encode('utf-8'))

            # Initilize data connection
            dataConnection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            dataConnection.bind(('', 0))
            dataConnection.listen(1)
            dataPort = dataConnection.getsockname()[1]

            # Send data connection port to server over control connection
            # so server can connect.
            self.client_socket.send(str(dataPort).encode('utf-8'))

            # Wait for server to connect.
            dataConnection, maddr = dataConnection.accept()
            print('[Control] Got connection from', maddr)
            print('200 PORT command successful')


            recv_data = self.client_socket.recv(1024)
            packet_info = recv_data.decode('utf-8')

            if packet_info == "file does not exists":
                recv_data2 = self.client_socket.recv(1024)

                ## use the decision tree to check if we are in the correct 
                ## dialect
                pkt1, pkt2 = recv_data.decode('utf-8'), recv_data2.decode('utf-8')
                inp = 'P1:{}/P2:{}'.format(pkt1, pkt2)

                t1 = time.time()
                predicted_dialect = dec_tree.predict(self.dialect_model, inp)
                t2 = time.time()

                print("prediction for :", inp, "was:", predicted_dialect)
                print("prediction time: %.6f sec" % (t2-t1))
                if predicted_dialect != self.dialectNo:
                    print("Decision Tree dialect mismatch!")
                    return

                ## end of decision tree usage ##

                valid_dialect = False
                size = 0
                try:
                    size  = int(recv_data2)
                    if size < 0:
                        valid_dialect = True
                        size = -size
                except ValueError as e:
                    # bad number
                    pass

                if not valid_dialect:
                    # expected a -ve number here.
                    dialect_mismatch("expected a -ve number")
                    #self.client_socket.send("Didn't recv msg in correct dialect!".encode("utf-8"))
                    return

                self.client_socket.send("Not ready, do not send!".encode("utf-8"))

                save_file = open(file_name, "wb")

                amount_recieved_data = 0
                while amount_recieved_data < size:
                    recv_data = dataConnection.recv(1024)
                    amount_recieved_data += len(recv_data)
                    save_file.write(recv_data)

                save_file.close()

                self.client_socket.send("It failed".encode('utf-8'))

            else:
                print("File {} does not exist on server.".format(file_name))
                print("possible dialect mismatch")
        
        except socket.error:
            print("SOCKET_ERROR: Check and ensure that server is running.")


    def do_put(self, args):
        pass
        ...


class D15:

    def __init__(self, client_socket, Hash, dialect_model):
        self.client_socket = client_socket
        self.Hash = Hash
        self.dialect_model = dialect_model
        self.dialectNo = 15

    def do_get(self, args):

        file = args.split()

        if len(file) != 1:
            print("rget requires exactly 1 argument.")
            return

        file_name = file[0]
        try:
            packet = "rget,{}".format(file_name)
            self.client_socket.sendall(packet.encode('utf-8'))

            # Initilize data connection
            dataConnection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            dataConnection.bind(('', 0))
            dataConnection.listen(1)
            dataPort = dataConnection.getsockname()[1]

            # Send data connection port to server over control connection
            # so server can connect.
            self.client_socket.send(str(dataPort).encode('utf-8'))

            # Wait for server to connect.
            dataConnection, maddr = dataConnection.accept()
            print('[Control] Got connection from', maddr)
            print('200 PORT command successful')


            recv_data = self.client_socket.recv(1024)
            packet_info = recv_data.decode('utf-8')

            if packet_info == "file exists":
                recv_data2 = self.client_socket.recv(1024).decode('utf-8')
                recv_data3 = self.client_socket.recv(1024).decode('utf-8')
                recv_data4 = self.client_socket.recv(1024).decode('utf-8')
                recv_data5 = self.client_socket.recv(1024).decode('utf-8')

                ## use the decision tree to check if we are in the correct 
                ## dialect
                pkt1 = recv_data.decode('utf-8')
                pkt2 = recv_data2.decode('utf-8')
                pkt3 = recv_data3.decode('utf-8')
                pkt4 = recv_data4.decode('utf-8')
                pkt5 = recv_data5.decode('utf-8')
                inp = 'P1:{}/P2:{}/P3:{}/P4:{}/P5:{}'.format(pkt1, pkt2, pkt3, pkt4, pkt5)

                t1 = time.time()
                predicted_dialect = dec_tree.predict(self.dialect_model, inp)
                t2 = time.time()

                print("prediction for :", inp, "was:", predicted_dialect)
                print("prediction time: %.6f sec" % (t2-t1))
                if predicted_dialect != self.dialectNo:
                    print("Decision Tree dialect mismatch!")
                    return

                ## end of decision tree usage ##


                valid_dialect = False
                file_size = 0
                try:
                    file_size = int(recv_data2)
                    if file_size >= 0 and recv_data4 == "rget" and recv_data5 == "4":
                        valid_dialect = True
                except ValueError as e:
                    ...

                if not valid_dialect:
                    dialect_mismatch("D15: bad dialect msg")
                    return

                self.client_socket.send("Ready to receive the file".encode('utf-8'))

                save_file = open(file_name, "wb")

                amount_recieved_data = 0
                while amount_recieved_data < file_size:
                    recv_data = dataConnection.recv(1024)
                    amount_recieved_data += len(recv_data)
                    save_file.write(recv_data)

                save_file.close()

                for i in range(1, 10):
                    self.client_socket.send("{}".format(file_size / 10).encode('utf-8'))
                    time.sleep(0.5)

            else:
                print("possible dialect mismatch")
                print("File {} does not exist on server.".format(file_name))
        
        except socket.error:
            print("SOCKET_ERROR: Check and ensure that server is running.")


    def do_put(self, args):
        pass
        ...


def dialect_mismatch(debug_msg=None):
    '''
    Handle if there is a dialect mismatch
    '''
    print("Server didn't communicate in the correct dialect")

    # TODO print the following only if 'debug flag' is on
    if debug_msg:
        print("REASON", debug_msg)