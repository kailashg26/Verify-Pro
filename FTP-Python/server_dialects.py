'''
Include all dialects here.
'''

import socket
import os  # listdir(), getcwd(), chdir(), mkdir()
from threading import Thread
import subprocess
import time
import datetime
import zipfile

class D0:
    '''
    Dialect 0 for server - all cmds
    '''

    def __init__(self, client_socket, client_ip, client_port):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port

    def send_file(self, file_name):
        try:
            dataPort = self.client_socket.recv(1024).decode('utf-8')
            print("[Control] Data port is {}".format(dataPort))

            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((self.client_ip, int(dataPort)))

            # if debug then print
            #print(file_name, type(file_name))
            file_size = os.path.getsize(file_name)
            self.client_socket.sendall(
                "Exists,{}".format(file_size).encode('utf-8'))

            while True:
                recv_data = self.client_socket.recv(1024)
                # client sent "Ready" or "Received,<size>"
                request = recv_data.decode('utf-8').strip().split(",")

                if request[0] == "Ready":
                    print("Sending file {} to client {}".format(
                        file_name, self.client_ip))

                    with open(file_name, "rb") as file:
                        dataConnection.sendfile(file)
                elif request[0] == "Received":
                    if int(request[1]) == file_size:
                        self.client_socket.sendall("Success".encode('utf-8'))
                        print("{} successfully downloaded to client {}".format(
                            file_name, self.client_ip))
                        break
                    else:
                        print("Possible dialect mismatch")
                        print("Something went wrong trying to download to client {}:{}. Try again".format(
                            self.client_ip, self.client_port))
                        break
                else:
                    print("possible dialect mismatch")
                    print("Something went wrong trying to download to client {}:{}. Try again".format(
                        self.client_ip, self.client_port))
                    break
        except IOError:
            print("File {} does not exist on server".format(file_name))
            self.client_socket.sendall("Failed".encode('utf-8'))


    def receive_file(self, file_nam):
        # TODO
        ...


class D1:
    '''
    Dialect 0 for server - all cmds
    '''

    def __init__(self, client_socket, client_ip, client_port):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port

    def send_file(self, file_name):
        try:
            dataPort = self.client_socket.recv(1024).decode('utf-8')
            print("[Control] Data port is {}".format(dataPort))

            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((self.client_ip, int(dataPort)))

            file_size = os.path.getsize(file_name)
            self.client_socket.sendall(
                "file exists,{}".format(file_size).encode('utf-8'))

            while True:
                recv_data = self.client_socket.recv(1024)
                request = recv_data.decode('utf-8').strip().split(",")

                if request[0] == "Ready to recv":
                    print("Sending file {} to client {}".format(
                        file_name, self.client_ip))

                    with open(file_name, "rb") as file:
                        dataConnection.sendfile(file)
                elif request[0] == "Received":
                    if int(request[1]) == file_size:
                        self.client_socket.sendall("Success".encode('utf-8'))
                        print("{} successfully downloaded to client {}".format(
                            file_name, self.client_ip))
                        break
                    else:
                        print("Possible dialect mismatch")
                        print("Something went wrong trying to download to client {}:{}. Try again".format(
                            self.client_ip, self.client_port))
                        break
                else:
                    print("Possible dialect mismatch")
                    print("Something went wrong trying to download to client {}:{}. Try again".format(
                        self.client_ip, self.client_port))
                    break
        except IOError:
            print("File {} does not exist on server".format(file_name))
            self.client_socket.sendall("Failed".encode('utf-8'))


    def receive_file(self, file_nam):
        # TODO
        ...


# Client: get file.txt
# Server: size(file) | "file not present"
# Server: transfer file
# Server: "connection closed"

class D2:

    def __init__(self, client_socket, client_ip, client_port):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port

    def send_file(self, file_name):
        try:
            dataPort = self.client_socket.recv(1024).decode('utf-8')
            print("[Control] Data port is {}".format(dataPort))

            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((self.client_ip, int(dataPort)))

            file = open(file_name, "rb")
            file_size = os.path.getsize(file_name)

            self.client_socket.sendall("{}".format(int(file_size)).encode('utf-8'))
            time.sleep(1)
            
            print("Sending file {} to client {}".format(file_name, self.client_ip)) 
            dataConnection.sendfile(file)
            
            self.client_socket.sendall("transfer complete".encode('utf-8'))

        except IOError:
            print("File {} does not exist on server".format(file_name))
            self.client_socket.sendall("file not present".encode('utf-8'))
            time.sleep(1)
            self.client_socket.sendall("connection closed".encode('utf-8'))


    def receive_file(self, file_nam):
        # TODO
        ...


# Client: get file.txt
# Server: file present + size(file)
# Server: sends file
# Server: closing the data connection

class D3:

    def __init__(self, client_socket, client_ip, client_port):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port

    def send_file(self, file_name):
        try:
            dataPort = self.client_socket.recv(1024).decode('utf-8')
            print("[Control] Data port is {}".format(dataPort))

            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((self.client_ip, int(dataPort)))

            file = open(file_name, "rb")
            file_size = os.path.getsize(file_name)

            self.client_socket.sendall("{},{}".format('file present', int(file_size)).encode('utf-8'))
            time.sleep(1)
            
            print("Sending file {} to client {}".format(file_name, self.client_ip)) 
            dataConnection.sendfile(file)
            
            self.client_socket.sendall("closing the data connection".encode('utf-8'))

        except IOError:
            print("File {} does not exist on server".format(file_name))
            self.client_socket.sendall("not found".encode('utf-8'))


    def receive_file(self, file_nam):
        # TODO
        ...



class D4:
    def __init__(self, client_socket, client_ip, client_port):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port

    def send_file(self, file_name):
        try:
            dataPort = self.client_socket.recv(1024).decode('utf-8')
            print("[Control] Data port is {}".format(dataPort))

            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((self.client_ip, int(dataPort)))

            file = open(file_name, "rb")

            file_size = os.path.getsize(file_name)
            self.client_socket.sendall("{}".format(int(file_size / 2)).encode('utf-8'))
            time.sleep(1)
            self.client_socket.sendall("{}".format(int(file_size / 2)).encode('utf-8'))

            print("Sending file {} to client {}".format(file_name, self.client_ip))
            dataConnection.sendfile(file)

            recv_data = self.client_socket.recv(1024)
            if recv_data.decode('utf-8') != "Thank you- connection closed":
                dialect_mismatch("Expected msg: Thank you- connection closed")
                return

        except IOError:
            print("File {} does not exist on server".format(file_name))
            self.client_socket.sendall("file not present".encode('utf-8'))
            time.sleep(1)
            self.client_socket.sendall("connection closed".encode('utf-8'))


    def receive_file(self, file_nam):
        # TODO
        ...



# Client: file_name
# Server: 1 if has it. -1 otherwise
# Server: size(file)
# Client: 0 (as ready to receive)
# Server: sends the file
# Client 1 if ok, -1 if error  # TODO client never sends -1?

class D5:

    def __init__(self, client_socket, client_ip, client_port):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port

    def send_file(self, file_name):
        try:
            dataPort = self.client_socket.recv(1024).decode('utf-8')
            print("[Control] Data port is {}".format(dataPort))

            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((self.client_ip, int(dataPort)))

            file = open(file_name, "rb")
            file_size = os.path.getsize(file_name)

            self.client_socket.sendall("1".encode('utf-8'))
            time.sleep(1)
            self.client_socket.sendall("{}".format(int(file_size)).encode('utf-8'))

            recv_data = self.client_socket.recv(1024).decode('utf-8')
            if recv_data != "0":
                dialect_mismatch("Expected '0'")
                return
            
            print("Sending file {} to client {}".format(file_name, self.client_ip)) 
            dataConnection.sendfile(file)
            
            recv_data = self.client_socket.recv(1024).decode('utf-8')
            if recv_data != "1":
                dialect_mismatch("Expected '1'")
                return


        except IOError:            
            print("File {} does not exist on server".format(file_name))
            self.client_socket.sendall("-1".encode('utf-8'))


    def receive_file(self, file_nam):
        # TODO
        ...





class D6:

    def __init__(self, client_socket, client_ip, client_port):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port

    def send_file(self, file_name):
        try:
            dataPort = self.client_socket.recv(1024).decode('utf-8')
            print("[Control] Data port is {}".format(dataPort))

            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((self.client_ip, int(dataPort)))

            file = open(file_name, "rb")
            self.client_socket.sendall("file exists".encode('utf-8'))
            time.sleep(1)


            file_size = os.path.getsize(file_name)
            self.client_socket.sendall("{},{}".format(len(file_name), len("rget")).encode('utf-8'))
            time.sleep(1)
            self.client_socket.sendall("{}".format(int(file_size)).encode('utf-8'))
            time.sleep(1)
            recv_data = self.client_socket.recv(1024)

            if recv_data.decode("utf-8") != "Details of the request are received":
                dialect_mismatch("Expected msg was 'Details of the ...'")
                return
            

            print("Sending file {} to client {}".format(file_name, self.client_ip)) 
            a = datetime.datetime.now()
            dataConnection.sendfile(file)
            b = datetime.datetime.now()
            s = (b-a).seconds + ((b-a).microseconds / 1000000)
            t = file_size / s

            print("Throughput: " + str(t))
            self.client_socket.sendall("{}".format(t).encode('utf-8'))
            recv_data = self.client_socket.recv(1024)

            if recv_data.decode("utf-8") != "success":
                dialect_mismatch("Expected msg: success")
                return

        except IOError:
            print("File {} does not exist on server".format(file_name))
            self.client_socket.sendall("not found".encode('utf-8'))


    def receive_file(self, file_nam):
        # TODO
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

    def __init__(self, client_socket, client_ip, client_port):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port

    def send_file(self, file_name):
        try:
            dataPort = self.client_socket.recv(1024).decode('utf-8')
            print("[Control] Data port is {}".format(dataPort))

            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((self.client_ip, int(dataPort)))

            file = open(file_name, "rb")
            self.client_socket.sendall("file exists".encode('utf-8'))
            time.sleep(1)


            file_size = os.path.getsize(file_name)
            self.client_socket.sendall("{}".format(len(file_name)).encode('utf-8'))
            time.sleep(1)
            self.client_socket.sendall("{}".format(len("rget")).encode('utf-8'))
            time.sleep(1)
            self.client_socket.sendall("{}".format(int(file_size)).encode('utf-8'))
            time.sleep(1)
            recv_data = self.client_socket.recv(1024).decode('utf-8')

            if recv_data != "Details of the request are received":
                dialect_mismatch("Got wrong expected messsage from client")
                return

            print("Sending file {} to client {}".format(file_name, self.client_ip))            
            dataConnection.sendfile(file)

            recv_data = self.client_socket.recv(1024).decode('utf-8')
            if recv_data != "success":
                dialect_mismatch("Expected msg: success")
                return

        except IOError:
            print("File {} does not exist on server".format(file_name))
            self.client_socket.sendall("not found".encode('utf-8'))


    def receive_file(self, file_nam):
        # TODO
        ...




# Client: get file.txt
# Server: file exist, packet size, filename, command
# Client: Ready to receive the file
# Server: sends file
# Client: Connection closed, file successfully received

class D8:

    def __init__(self, client_socket, client_ip, client_port):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port

    def send_file(self, file_name):
        try:
            dataPort = self.client_socket.recv(1024).decode('utf-8')
            print("[Control] Data port is {}".format(dataPort))

            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((self.client_ip, int(dataPort)))

            file = open(file_name, "rb")
            file_size = os.path.getsize(file_name)

            self.client_socket.sendall("file exists,{},{},{}".format(file_size, file_name, "getr").encode('utf-8'))
                       
            recv_data = self.client_socket.recv(1024).decode('utf-8')
            if recv_data != "Ready to receive the file":
                dialect_mismatch("Got incorrect expected msg")
                return

            print("Sending file {} to client {}".format(file_name, self.client_ip))            
            dataConnection.sendfile(file)

            recv_data = self.client_socket.recv(1024).decode('utf-8')
            if recv_data != "Connection closed, file successfully received":
                dialect_mismatch("D8: Got incorrect expected msg")
                return


        except IOError:
            print("File {} does not exist on server".format(file_name))
            self.client_socket.sendall("not found".encode('utf-8'))


    def receive_file(self, file_nam):
        # TODO
        ...



# Client: get file.txt
# Server: file exist, packet size
# Server: filename, command
# Client: Ready to receive the file
# Server: sends file
# Client: Connection closed, file successfully received

class D9:

    def __init__(self, client_socket, client_ip, client_port):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port

    def send_file(self, file_name):
        try:
            dataPort = self.client_socket.recv(1024).decode('utf-8')
            print("[Control] Data port is {}".format(dataPort))

            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((self.client_ip, int(dataPort)))

            file = open(file_name, "rb")
            file_size = os.path.getsize(file_name)

            self.client_socket.sendall("file exists,{}".format(file_size).encode('utf-8'))
            time.sleep(1)
            self.client_socket.sendall("{},{}".format(file_name, "getr").encode('utf-8'))
            
            recv_data = self.client_socket.recv(1024).decode('utf-8')
            if recv_data != 'Ready to receive the file':
                dialect_mismatch('D9: got wrong expected msg')
                return

            print("Sending file {} to client {}".format(file_name, self.client_ip))

            dataConnection.sendfile(file)

            recv_data = self.client_socket.recv(1024).decode('utf-8')
            if recv_data != "Connection closed, file successfully received":
                dialect_mismatch('D9: Got incorrect expected msg')
                return

        except IOError:
            print("File {} does not exist on server".format(file_name))
            self.client_socket.sendall("not found".encode('utf-8'))


    def receive_file(self, file_nam):
        # TODO
        ...




# Client: get file.txt
# Server: file exist
# Server: packet size, filename, command
# Client: Ready to receive the file
# Server: sends file
# Client: Connection closed, file successfully received

class D10:

    def __init__(self, client_socket, client_ip, client_port):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port

    def send_file(self, file_name):
        try:
            dataPort = self.client_socket.recv(1024).decode('utf-8')
            print("[Control] Data port is {}".format(dataPort))

            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((self.client_ip, int(dataPort)))

            file = open(file_name, "rb")
            file_size = os.path.getsize(file_name)

            self.client_socket.sendall("file exists".encode('utf-8'))
            time.sleep(1)
            self.client_socket.sendall("{},{},{}".format(file_size, file_name, "getr").encode('utf-8'))
            

            recv_data = self.client_socket.recv(1024)
            expected_recv_data = "Ready to receive the file"
            if recv_data.decode('utf-8') != expected_recv_data:
                dialect_mismatch("Expected msg: {}".format(expected_recv_data))
                return

            print("Sending file {} to client {}".format(file_name, self.client_ip))            
            dataConnection.sendfile(file)

            recv_data = self.client_socket.recv(1024)
            expected_recv_data = "Connection closed, file successfully received"
            if recv_data.decode('utf-8') != expected_recv_data:
                dialect_mismatch("Expected msg: {}".format(expected_recv_data))
                return 


        except IOError:
            print("File {} does not exist on server".format(file_name))
            self.client_socket.sendall("not found".encode('utf-8'))


    def receive_file(self, file_nam):
        # TODO
        ...



class D11:

    def __init__(self, client_socket, client_ip, client_port):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port

    def send_file(self, file_name):
        try:
            dataPort = self.client_socket.recv(1024).decode('utf-8')
            print("[Control] Data port is {}".format(dataPort))

            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((self.client_ip, int(dataPort)))

            file = open(file_name, "rb")
            self.client_socket.sendall("file exists".encode('utf-8'))
            time.sleep(1)


            file_size = os.path.getsize(file_name)
            self.client_socket.sendall("{}".format(int(file_size)).encode('utf-8'))
            time.sleep(1)
            self.client_socket.sendall("{},{}".format(file_name, len(file_name)).encode('utf-8'))
            time.sleep(1)
            self.client_socket.sendall("{},{}".format("rget", len("rget")).encode('utf-8'))
            time.sleep(1)
            recv_data  = self.client_socket.recv(1024).decode('utf-8')
            recv_data2 = self.client_socket.recv(1024).decode('utf-8')

            if recv_data != "Ready" or recv_data2 != "to receive the file":
                dialect_mismatch("D11: Client didn't send expected msg")
                return
            

            print("Sending file {} to client {}".format(file_name, self.client_ip))            
            dataConnection.sendfile(file)

            self.client_socket.sendall("{}".format("file transfered").encode('utf-8'))
            recv_data3 = self.client_socket.recv(1024).decode('utf-8')
            recv_data4 = self.client_socket.recv(1024).decode('utf-8')

            valid_dialect = False
            try:
                float(recv_data3)
                if recv_data4 == 'Connection closed, file successfully received ':
                    valid_dialect = True
            except ValueError as e:
                ...

            if not valid_dialect:
                dialect_mismatch("D11: client didnt talk in the correct dialect")
                return

        except IOError:
            print("File {} does not exist on server".format(file_name))
            self.client_socket.sendall("not found".encode('utf-8'))



    def receive_file(self, file_nam):
        # TODO
        ...


# Client: test.txt
# Server: size(file) // it needs at least this
# Server: sends files

class D12:

    def __init__(self, client_socket, client_ip, client_port):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port

    def send_file(self, file_name):
        try:
            dataPort = self.client_socket.recv(1024).decode('utf-8')
            print("[Control] Data port is {}".format(dataPort))

            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((self.client_ip, int(dataPort)))

            # TODO: what if the file wasn't found?
            # one option: to send a -ve filesize to indicate that in this dialect
            file = open(file_name, "rb")
            file_size = os.path.getsize(file_name)

            self.client_socket.sendall("{}".format(int(file_size)).encode('utf-8'))
            time.sleep(1)
            
            print("Sending file {} to client {}".format(file_name, self.client_ip)) 
            dataConnection.sendfile(file)

        except IOError:
            print("File {} does not exist on server".format(file_name))
            self.client_socket.sendall("not found".encode('utf-8'))


    def receive_file(self, file_nam):
        # TODO
        ...


class D13:

    def __init__(self, client_socket, client_ip, client_port):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port

    def send_file(self, file_name):
        try:
            dataPort = self.client_socket.recv(1024).decode('utf-8')
            print("[Control] Data port is {}".format(dataPort))

            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((self.client_ip, int(dataPort)))

            file = open(file_name, "rb")
            file.close()

            zp = file_name[:-4] + '.zip'
            zipfile.ZipFile(zp, mode='w').write(file_name)
            file = open(zp, "rb")

            self.client_socket.sendall("file exists".encode('utf-8'))
            time.sleep(1)


            file_size = os.path.getsize(zp)
            

            self.client_socket.sendall("{}".format(len(zp)).encode('utf-8'))
            recv_data1 = self.client_socket.recv(1024).decode('utf-8')
            recv_data2 = self.client_socket.recv(1024).decode('utf-8')
            recv_data3 = self.client_socket.recv(1024).decode('utf-8')

            if recv_data1 != "Ready" or recv_data2 != "to receive" or recv_data3 != "the file":
                dialect_mismatch("D13: client didnt talk in expected dialect")
                return
            

            print("Sending file {} to client {}".format(file_name, self.client_ip))            
            dataConnection.sendfile(file)

            recv_data = self.client_socket.recv(1024).decode('utf-8')
            if recv_data != "success":
                dialect_mismatch("D13: Wrong expected msg")
                return

        except IOError:
            print("File {} does not exist on server".format(file_name))
            self.client_socket.sendall("not found".encode('utf-8'))

    def receive_file(self, file_nam):
        # TODO
        ...


# OPPOSITE MESSAGES!

# Client: file_name
# Server: "file does not exists" if has it     | "file exists" otherwise
# Server: NEGATIVE size(file)
# Client: "Not ready, do not send"
# Server: sends the file
# Client: it failed

class D14:

    def __init__(self, client_socket, client_ip, client_port):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port

    def send_file(self, file_name):
        try:
            dataPort = self.client_socket.recv(1024).decode('utf-8')
            print("[Control] Data port is {}".format(dataPort))

            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((self.client_ip, int(dataPort)))

            file = open(file_name, "rb")
            file_size = os.path.getsize(file_name)

            self.client_socket.sendall("file does not exists".encode('utf-8'))
            time.sleep(1)
            self.client_socket.sendall("{}".format(0 - int(file_size)).encode('utf-8'))

            recv_data = self.client_socket.recv(1024)
            expected_recv_data = "Not ready, do not send!"
            if recv_data.decode('utf-8') != expected_recv_data:
                dialect_mismatch(expected_recv_data)
                return
            
            print("Sending file {} to client {}".format(file_name, self.client_ip)) 
            dataConnection.sendfile(file)
            
            recv_data = self.client_socket.recv(1024)
            expected_recv_data = "It failed"
            if recv_data.decode('utf-8') != expected_recv_data:
                dialect_mismatch(expected_recv_data)

        except IOError:            
            print("File {} does not exist on server".format(file_name))
            self.client_socket.sendall("file exists".encode('utf-8'))


    def receive_file(self, file_nam):
        # TODO
        ...

class D15:

    def __init__(self, client_socket, client_ip, client_port):
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port

    def send_file(self, file_name):
        try:
            dataPort = self.client_socket.recv(1024).decode('utf-8')
            print("[Control] Data port is {}".format(dataPort))

            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((self.client_ip, int(dataPort)))

            file = open(file_name, "rb")
            file_size = os.path.getsize(file_name)

            self.client_socket.sendall("file exists".encode('utf-8'))
            time.sleep(1)
            self.client_socket.sendall("{}".format(file_size).encode('utf-8'))
            time.sleep(1)
            self.client_socket.sendall("{}".format(file_name).encode('utf-8'))
            time.sleep(1)
            self.client_socket.sendall("{}".format("rget").encode('utf-8'))
            time.sleep(1)
            self.client_socket.sendall("{}".format(len('rget')).encode('utf-8'))
            time.sleep(1)
            
            
                       
            recv_data = self.client_socket.recv(1024).decode('utf-8')
            if recv_data != "Ready to receive the file":
                dialect_mismatch("D15: client didnt send expected msg")
                return

            print("Sending file {} to client {}".format(file_name, self.client_ip))            
            dataConnection.sendfile(file)

            for i in range(1, 10):
                recv_data = self.client_socket.recv(1024).decode('utf-8')
                try:
                    if abs(float(recv_data) - file_size/10) < 1e-10:
                        # comparing floats by 'close enough' method
                        dialect_mismatch("D15: client didn't send expected msg")
                        return
                except ValueError as e:
                    dialect_mismatch("D15: expected a float from client")
                    return


        except IOError:
            print("File {} does not exist on server".format(file_name))
            self.client_socket.sendall("not found".encode('utf-8'))


    def receive_file(self, file_nam):
        # TODO
        ...



def dialect_mismatch(debug_msg=None):
    '''
    Handle if there is a dialect mismatch
    '''
    print("Client didn't communicate in the correct dialect")

    # TODO print the following only if 'debug flag' is on
    if debug_msg:
        print("REASON", debug_msg)
