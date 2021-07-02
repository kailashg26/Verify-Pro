import socket
import os  # listdir(), getcwd(), chdir(), mkdir()
from threading import Thread
import subprocess
from predict_nn import *
import predict_nn
import server_dialects
import datetime
from string import digits


# Directory where server files are stored
ServerFolder = os.getcwd() + "/ServerFolder"


class ThreadFunctions(Thread):
    def __init__(self, client_socket, client_ip, client_port):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.client_ip = client_ip
        self.client_port = client_port
        # self.buffer_size = 1024
        print("Server started thread for client {} on port {}".format(
            self.client_ip, self.client_port))

        self.ud = UniDistriModel()
        self.ud.load_model()

    def run(self):
        """
        Inherited method from Thread module.
        This is the main function which look at received data/commands from client and
        decides what to do.
        """
        os.chdir(ServerFolder)
        while True:
            request = self.client_socket.recv(1024).decode().strip()
            if not request:
                print("Disconnecting from client {}:{}".format(
                    self.client_ip, self.client_port))
                self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()
                break
            request = request.split(",")

            cmd = request[0]
            args = request[1:]
            # d = self.ud.predict("get "+ args)
            in_str = cmd + " " + "".join(args).rstrip(digits)
            print(in_str)
            d = self.ud.predict(in_str)
            print("request:%s, dialect:%d" % (request, d))

            if request[0] == "LS":
                self.ls()
            elif request[0] == "PWD":
                self.pwd()
            elif request[0] == "CD":
                self.cd(request[1])
            elif request[0] == "MKDIR":
                self.mkdir(request[1])
            elif request[0] == "RMDIR":
                self.rmdir(request[1])
            elif request[0] == "RM":
                self.rm(request[1])

            elif request[0] == "rget" and len(request[1:]) == 1:
                self.send_file(request[1:], d)

            elif request[0] == "rput" and len(request[1:]) == 2:
                self.receive_file(*request[1:])

    def ls(self):
        packet = subprocess.check_output(
            ["ls", "-l"], universal_newlines=True)
        # print(type(output))
        # packet = ""
        # filelist = os.listdir(os.getcwd())
        # # print(str(filelist))
        # for f in filelist:
        #     packet += f + "   "
        # # print(packet)
        if packet.strip() == "":
            self.client_socket.sendall("EMPTY".encode())
        else:
            # self.client_socket.sendall(packet.encode())
            self.client_socket.sendall(packet.encode())

        # self.client_socket.sendall(response.encode())

    def pwd(self):
        try:
            currDir = os.getcwd()
            self.client_socket.sendall(currDir.encode())
        except:
            self.client_socket.sendall(
                "Server facing issue while getting working directory.")

    def cd(self, dir_path):
        try:
            if (dir_path == '..' and os.getcwd() == ServerFolder):
                self.client_socket.sendall(
                    f"changed directory to '{dir_path}'".encode())
            else:
                os.chdir(dir_path)
                self.client_socket.sendall(
                    f"changed directory to '{dir_path}'".encode())
        except FileNotFoundError:
            self.client_socket.sendall(
                f"directory '{dir_path}' not found".encode())

    def mkdir(self, dir_name):
        try:
            # path = ServerFolder+"/"+dir_name
            os.mkdir(dir_name)
            self.client_socket.sendall(
                f"Directory '{dir_name}' successfully created.".encode())
        except OSError:
            self.client_socket.sendall(
                f"directory named '{dir_name}' already exists.".encode())

    def rmdir(self, dir_name):
        try:
            os.removedirs(dir_name)
            self.client_socket.sendall(
                f"Directory '{dir_name}' successfully removed.".encode())
        except FileNotFoundError:
            self.client_socket.sendall(
                f"directory named '{dir_name}' doesn't exists.".encode())
        except OSError:
            self.client_socket.sendall(f"directory is not empty".encode())

    def rm(self, file_name):
        try:
            os.remove(file_name)
            self.client_socket.sendall(
                f"File '{file_name}' successfully removed.".encode())
        except FileNotFoundError:
            self.client_socket.sendall(
                f"File named '{file_name}' doesn't exists.".encode())
        except IsADirectoryError:
            self.client_socket.sendall(
                f"'{file_name}' is a directory.".encode())
        # except OSError:
        #     self.client_socket.sendall(f"directory is not empty".encode())


    def send_file(self, file_name, dialect):
        """
        Sends requested file to client if it exits on the server.

        Params:
            file_name (str): name of file to find and transfer
        """

        def start_counter():
            return datetime.datetime.now()

        def stop_counter(inp):
            b = datetime.datetime.now()
            s = (b-ini).seconds + ((b-ini).microseconds / 1000000)
            st = '{0:07f} sec'.format(s)
            return st

        #dialect = constraints._d7

        ## added with Decision tree changes: D0 and D1 are structurally 
        ## identical, so using D1 for both
        if dialect == predict_nn._d0:
            dialect = predict_nn._d1

        file_name = file_name[0]
        handler = None
        
        if dialect == predict_nn._d0:
            print("Using dialect D0")
            handler = server_dialects.D0(self.client_socket, self.client_ip, self.client_port)

        elif dialect == predict_nn._d1:
            print("Using dialect D1")
            handler = server_dialects.D1(self.client_socket, self.client_ip, self.client_port)

        elif dialect == predict_nn._d2:
            print("Using dialect D2")
            handler = server_dialects.D2(self.client_socket, self.client_ip, self.client_port)

        elif dialect == predict_nn._d3:
            print("Using dialect D3")
            handler = server_dialects.D3(self.client_socket, self.client_ip, self.client_port)

        elif dialect == predict_nn._d4:
            print("Using dialect D4")
            handler = server_dialects.D4(self.client_socket, self.client_ip, self.client_port)

        elif dialect == predict_nn._d5:
            print("Using dialect D5")
            handler = server_dialects.D5(self.client_socket, self.client_ip, self.client_port)

        elif dialect == predict_nn._d6:
            print("Using dialect D6")
            handler = server_dialects.D6(self.client_socket, self.client_ip, self.client_port)

        elif dialect == predict_nn._d7:
            print("Using dialect D7")
            handler = server_dialects.D7(self.client_socket, self.client_ip, self.client_port)

        elif dialect == predict_nn._d8:
            print("Using dialect D8")
            handler = server_dialects.D8(self.client_socket, self.client_ip, self.client_port)

        elif dialect == predict_nn._d9:
            print("Using dialect D9")
            handler = server_dialects.D9(self.client_socket, self.client_ip, self.client_port)

        elif dialect == predict_nn._d10:
            print("Using dialect D10")
            handler = server_dialects.D10(self.client_socket, self.client_ip, self.client_port)

        elif dialect == predict_nn._d11:
            print("Using dialect D11")
            handler = server_dialects.D11(self.client_socket, self.client_ip, self.client_port)

        elif dialect == predict_nn._d12:
            print("Using dialect D12")
            handler = server_dialects.D12(self.client_socket, self.client_ip, self.client_port)

        elif dialect == predict_nn._d13:
            print("Using dialect D13")
            handler = server_dialects.D13(self.client_socket, self.client_ip, self.client_port)

        elif dialect == predict_nn._d14:
            print("Using dialect D14")
            handler = server_dialects.D14(self.client_socket, self.client_ip, self.client_port)

        elif dialect == predict_nn._d15:
            print("Using dialect D15")
            handler = server_dialects.D15(self.client_socket, self.client_ip, self.client_port)
            
        else:
            print("ERROR: Unknown dialect %d" % dialect)
            # TODO handle this error

        if handler is not None:
            ini = start_counter()
            handler.send_file(file_name)
            total_time = stop_counter(ini)
            print("Time taken: " + total_time)

    def receive_file(self, file_name, length):
        """
        Reads a file that is sent from the client.

        Params:
            file_name (str): name of file to be transfered
            length (str): byte length of the file to be transfered from client
        """
        self.client_socket.sendall("Ready".encode("utf-8"))
        print("Server ready to accept file: {} from client: {}:{}".format(
            file_name, self.client_ip, self.client_port))

        save_file = open("{}".format(file_name), "wb")

        amount_recieved_data = 0
        while amount_recieved_data < int(length):
            recv_data = self.client_socket.recv(1024)
            amount_recieved_data += len(recv_data)
            save_file.write(recv_data)

        save_file.close()

        self.client_socket.sendall("Received,{}".format(
            amount_recieved_data).encode('utf-8'))
        print("Server done receiving from client {}:{}. File Saved.".format(
            self.client_ip, self.client_port))
