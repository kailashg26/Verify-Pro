import socket
import sys
import os
from cmd import Cmd
from getpass import getpass
import signal
from predict_nn import *
import predict_nn
import client_dialects
import datetime
import pickle
import time




ClientFolder = os.getcwd() + '/' + 'ClientFolder'

os.chdir(ClientFolder)

class Client(Cmd):
    def __init__(self, hostname, port):
        Cmd.__init__(self)
        Cmd.intro = "Starting FTP Client. For help type 'help' or '?'.\n"
        Cmd.prompt = "ftp> "
        self.client_socket = None
        self.server_addr = (socket.gethostbyname(hostname), port)
        self.connected = False
        self.prom = True
        self.Hash = True
        self.ud = UniDistriModel()
        self.ud.load_model("../output/model.h5")
        self.dialect_model = self.load_dt_model("../output/DecisionTrainedModel")

    def load_dt_model(self, path):
        '''
        Given a path of a pickle file which is the decision tree model,
        load it. This is used for dialect authentication. This model is 
        pre trained
        '''
        model = pickle.load(open(path, 'rb'))
        print("*** successfully loaded decision tree model *****")
        return model

    # To handle ctrl + c interrupt. exits without errors
    def sigint_handler(self, signum, frame):
        print('^C')
        sys.exit()

    def authClient(self):
        try:
            self.client_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(self.server_addr)
            try:
                username = input("Username: ")
                # print(username)
                password = getpass()
            except KeyboardInterrupt:
                self.client_socket.close()
                sys.exit()

            packet = "{}:{}".format(username, password)
            self.client_socket.sendall(packet.encode())

            response = self.client_socket.recv(1024).decode()

            if response == "SUCCESS":
                signal.signal(signal.SIGINT, self.sigint_handler)
                self.connected = True
                print("Connected to server {}:{}".format(*self.server_addr))
                return True
            else:
                self.connected = False
                print("Username or Password wrong.")
                return False
        except socket.error:
            print("Check that server is running or mentioned address is right")
            sys.exit()

    def do_hash(self, args):
        """hash      	toggle printing `#' for each buffer transferred"""
        if len(args.split()) != 0:
            if self.Hash == True:
                print("Hash mark printing on(1024 bytes/hash mark).")
            else:
                print("Hash mark printing off.")
        else:
            if self.Hash == True:
                self.Hash = False
                print("Hash mark printing off.")
            else:
                self.Hash = True
                print("Hash mark printing on(1024 bytes/hash mark).")

    def do_prom(self, args):
        """prompt    	force interactive prompting on multiple commands"""
        if self.prom == True:
            self.prom = False
            print("Interactive mode off.")
        else:
            self.prom = True
            print("Interactive mode on.")

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def do_lcd(self, args):
        """lcd       	change local working directory"""
        dir_name = args.split()
        # print(dir_name)
        if len(dir_name) == 1:
            try:
                if (dir_name[0] == '..' and os.getcwd() == ClientFolder):
                    return
                os.chdir(dir_name[0])
                print('Local directory now ' + os.getcwd())
            except FileNotFoundError:
                print(f"directory '{dir_name}' not found")
        else:
            print("CD requires exactly one argument.")

    def do_ls(self, args):
        """ls        	list contents of remote directory"""
        if not self.connected:
            print('Not connected.')
            return
        if len(args) != 0:
            print("No arguments required.")
            return
        self.client_socket.sendall("LS".encode())
        response = self.client_socket.recv(1024).decode()
        if response == "EMPTY":
            return
        else:
            print(response)

    def do_pwd(self, args):
        """pwd       	print working directory on remote machine"""

        if not self.connected:
            print('Not connected.')
            return
        if len(args) != 0:
            print("pwd requires no argument.")
            return
        self.client_socket.sendall("PWD".encode())
        response = self.client_socket.recv(1024).decode()
        if response == "EMPTY":
            return
        else:
            print(response)

    def do_cd(self, args):
        """cd        	change remote working directory"""

        if not self.connected:
            print('Not connected.')
            return
        if len(args) == 0:
            print("cd requires one argument as directory name")
        else:
            dir = args.split(" ")
            if len(dir) != 1:
                print("Only one argument required")
                return
            packet = "CD,{}".format(dir[0])
            self.client_socket.sendall(packet.encode())
            response = self.client_socket.recv(1024).decode()
            print(response)

    def do_mkdir(self, args):
        """mkdir     	make directory on the remote machine"""
        if not self.connected:
            print('Not connected.')
            return
        if len(args) == 0:
            print("mkdir requires one or more arguments as directory name")
        else:
            dirs = args.split(" ")
            for dir in dirs:
                packet = "MKDIR,{}".format(dir)
                self.client_socket.sendall(packet.encode())
                response = self.client_socket.recv(1024).decode()
                print(response)

    def do_rmdir(self, args):
        """rmdir     	remove directory on the remote machine"""
        if not self.connected:
            print('Not connected.')
            return
        if len(args) == 0:
            print("rmdir requires one argument as directory name")
        else:
            dir = args.split(" ")
            # for dir in dirs:
            packet = "RMDIR,{}".format(dir[0])
            self.client_socket.sendall(packet.encode())
            response = self.client_socket.recv(1024).decode()
            print(response)

    def do_delete(self, args):
        """delete    	delete remote file"""
        if not self.connected:
            print('Not connected.')
            return
        if len(args) == 0:
            print("delete requires one argument as directory name")
        else:
            file = args.split(" ")
            # for file in files:
            packet = "RM,{}".format(file[0])
            self.client_socket.sendall(packet.encode())
            response = self.client_socket.recv(1024).decode()
            print(response)

    def do_mdelete(self, args):
        """mdelete   	delete multiple files"""

        if not self.connected:
            print('Not connected.')
            return
        if len(args) == 0:
            print("mdelete requires one or more arguments as filename")
        else:
            files = args.split(" ")
            for file in files:
                if self.prom == True:
                    confirmation = input('mdelete ' + file + '?')
                    if confirmation == 'n' or confirmation == 'no' or confirmation == 'N' or confirmation == 'NO':
                        continue
                    else:
                        self.do_delete(file)
                else:
                    self.do_delete(file)

    def do_get(self, args):
        """get       	receive file"""

        if not self.connected:
            print('Not connected.')
            return
		# dialect = self.ud.predict("get file.txt")
		# dialect = 2
       	# dialect = predict_nn.get_dialect(predict_nn.GETCMD, args)
        # print("request:%s, dialect:%d" % ("get " + args, dialect))
        # dialect =  self.ud.predict(predict_nn.GETCMD, " ".join(args)
        print(args)
        in_str = "rget " + "".join(args)
        print(in_str)
        t1 = time.time()
        dialect = self.ud.predict(in_str)
        t2 = time.time()

        ## added with Decision tree changes: D0 and D1 are structurally 
        ## identical, so using D1 for both
        if dialect == predict_nn._d0:
            dialect = predict_nn._d1
        print("NN Prediction time: %.5f sec" % (t2-t1))
        print("dialect:%d" % (dialect))
        
        def start_counter():
            return datetime.datetime.now()

        def stop_counter(inp):
            b = datetime.datetime.now()
            s = (b-ini).seconds + ((b-ini).microseconds / 1000000)
            st = '{0:07f} sec'.format(s)
            return st

        if dialect is None:
            print('No dialect found')
            return

        #dialect = constraints._d7

        
        handler = None
        if dialect == predict_nn._d0:
            print("Using dialect D0")
            handler = client_dialects.D0(self.client_socket, self.Hash, self.dialect_model)

        elif dialect == predict_nn._d1:
            print("Using dialect D1")
            handler = client_dialects.D1(self.client_socket, self.Hash, self.dialect_model)

        elif dialect == predict_nn._d2:
            print("Using dialect D2")
            handler = client_dialects.D2(self.client_socket, self.Hash, self.dialect_model)

        elif dialect == predict_nn._d3:
            print("Using dialect D3")
            print("Using d3- 2nd time")
            handler = client_dialects.D3(self.client_socket, self.Hash, self.dialect_model)

        elif dialect == predict_nn._d4:
            print("Using dialect D4")
            handler = client_dialects.D4(self.client_socket, self.Hash, self.dialect_model)

        elif dialect == predict_nn._d5:
            print("Using dialect D5")
            handler = client_dialects.D5(self.client_socket, self.Hash, self.dialect_model)

        elif dialect == predict_nn._d6:
            print("Using dialect D6")
            handler = client_dialects.D6(self.client_socket, self.Hash, self.dialect_model)

        elif dialect == predict_nn._d7:
            print("Using dialect D7")
            handler = client_dialects.D7(self.client_socket, self.Hash, self.dialect_model)

        elif dialect == predict_nn._d8:
            print("Using dialect D8")
            handler = client_dialects.D8(self.client_socket, self.Hash, self.dialect_model)

        elif dialect == predict_nn._d9:
            print("Using dialect D9")
            handler = client_dialects.D9(self.client_socket, self.Hash, self.dialect_model)

        elif dialect == predict_nn._d10:
            print("Using dialect D10")
            handler = client_dialects.D10(self.client_socket, self.Hash, self.dialect_model)

        elif dialect == predict_nn._d11:
            print("Using dialect D11")
            handler = client_dialects.D11(self.client_socket, self.Hash, self.dialect_model)

        elif dialect == predict_nn._d12:
            print("Using dialect D12")
            handler = client_dialects.D12(self.client_socket, self.Hash, self.dialect_model)

        elif dialect == predict_nn._d13:
            print("Using dialect D13")
            handler = client_dialects.D13(self.client_socket, self.Hash, self.dialect_model)

        elif dialect == predict_nn._d14:
            print("Using dialect D14")
            handler = client_dialects.D14(self.client_socket, self.Hash, self.dialect_model)

        elif dialect == predict_nn._d15:
            print("Using dialect D15")
            handler = client_dialects.D15(self.client_socket, self.Hash, self.dialect_model)
            

        else:
            print("ERROR: Unknown dialect %d" % dialect)
            # TODO handle this error

        if handler is not None:
            ini = start_counter()
            handler.do_get(args)
            total_time = stop_counter(ini)
            print("Time taken: " + total_time)
        else:
            print("ERROR: Unknown dialect %d" % dialect)
            # TODO handle this error

        # if handler is not None:
        #     handler.do_get(args)



    def do_put(self, args):
        """put       	send one file"""

        if not self.connected:
            print('Not connected.')
            return

        files = args.split()
        if len(files) == 1:
            file_name = files[0]

            try:
                packet = "rput,{},{}".format(
                    file_name, os.path.getsize(file_name))
                self.client_socket.sendall(packet.encode('utf-8'))
                print('200 PORT command successful')
                while True:
                    recv_data = self.client_socket.recv(1024)
                    packet_info = recv_data.decode(
                        'utf-8').strip().split(",")

                    if packet_info[0] == "Ready":
                        # print("Sending file {} to server {}".format(
                        #     file_name, self.client_socket.getpeername()))

                        with open(file_name, mode="rb") as file:
                            self.client_socket.sendfile(file)

                        if self.Hash == True:
                            # printing hash for each 1024 bytes of data transferred
                            for _ in range(os.path.getsize(file_name)//1024):
                                print('#', end="")

                    elif packet_info[0] == "Received":
                        if self.Hash == True:
                            print()
                        if int(packet_info[1]) == os.path.getsize(file_name):
                            print('226 Transfer complete')
                            break
                        else:
                            print("Something went wrong trying to upload to server {}. Try again".format(
                                self.client_socket.getpeername()))
                            break
                    else:
                        print("Something went wrong trying to upload to server {}. Try again.".format(
                            self.client_socket.getpeername()))
                        break
            except IOError:
                print("File doesn't exist on the system!")
        else:
            print("put requires exactly 1 argument.")
            print()

    def do_mget(self, args):
        """mget      	get multiple files"""

        if not self.connected:
            print('Not connected.')
            return
        if len(args) == 0:
            print("atleast one argument required.")
            return
        else:
            filelist = args.split()
            for file in filelist:
                if self.prom == True:
                    confirmation = input('mget ' + file + '?')
                    if confirmation == 'n' or confirmation == 'no' or confirmation == 'N' or confirmation == 'NO':
                        continue
                    else:
                        self.do_get(file)
                else:
                    self.do_get(file)

    def do_mput(self, args):
        """mput      	send multiple files"""

        if not self.connected:
            print('Not connected.')
            return
        if len(args) == 0:
            print("atleast one argument required.")
            return
        else:
            filelist = args.split()
            for file in filelist:
                if self.prom == True:
                    confirmation = input('mput ' + file + '?')
                    if confirmation == 'n' or confirmation == 'no' or confirmation == 'N' or confirmation == 'NO':
                        continue
                    else:
                        self.do_put(file)
                else:
                    self.do_put(file)

    def do_exit(self, args):
        """exit      	terminate ftp session and exit"""
        self.client_socket.send("EXIT".encode())
        self.client_socket.close()
        sys.exit()

    def do_bye(self, args):
        """bye      	terminate ftp session and exit"""
        self.client_socket.send("EXIT".encode())
        self.client_socket.close()
        sys.exit()

    def do_quit(self, args):
        """quit      	terminate ftp session and exit"""
        self.client_socket.send("EXIT".encode())
        self.client_socket.close()
        sys.exit()

    # using '!' before commands, escaping to local command execution
    def do_shell(self, args):
        """Pass command to a system shell when line begins with '!'"""
        os.system(args)

    do_EOF = do_exit        # exiting by ctrl+d

    def do_close(self, args):
        """close     	terminate ftp session"""
        if not self.connected:
            print('Not connected.')
        self.connected = False
        self.client_socket.close()

    def do_open(self, args):
        if not self.connected:
            self.authClient()
        else:
            print('Already connected.')


if __name__ == "__main__":
    if len(sys.argv) == 3:
        hostname = sys.argv[1]
        port = int(sys.argv[2])
    else:
        print("Server IP and PORT NO. required as arguments")
        sys.exit(2)

    client = Client(hostname, port)
    if client.authClient():
        client.cmdloop()
