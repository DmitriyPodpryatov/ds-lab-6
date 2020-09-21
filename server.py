import os
import socket
from threading import Thread

clients = []


# Thread to listen one particular client
class ClientListener(Thread):
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name

    # add 'me> ' to sended message
    def _clear_echo(self, data):
        # \033[F – symbol to move the cursor at the beginning of current line (Ctrl+A)
        # \033[K – symbol to clear everything till the end of current line (Ctrl+K)
        self.sock.sendall('\033[F\033[K'.encode())
        data = 'me> '.encode() + data
        # send the message back to user
        self.sock.sendall(data)

    # broadcast the message with name prefix eg: 'u1> '
    def _broadcast(self, data):
        data = (self.name + '> ').encode() + data
        for u in clients:
            # send to everyone except current client
            if u == self.sock:
                continue
            u.sendall(data)

    # clean up
    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')

    def run(self):
        file_name = ""

        while True:
            # try to read 1024 bytes from user
            # this is blocking call, thread will be paused here
            data = self.sock.recv(1024)
            if data:
                # If file name is empty, then it is beginning of the file
                # We need to parse the file name
                if not file_name:
                    # Get length of file name (split by dot - refer to client.py for format)
                    # Since max length of file name is 255, we can search for 3 digits max
                    file_name_len = int(data[:3].decode().partition(".")[0])

                    # Get file name (split after dot and the length of file_name_len)
                    # Offset includes the length of the number, dot, and the length of the file name
                    offset = len(str(file_name_len)) + 1 + file_name_len

                    file_name = data[:offset].decode().partition(".")[2][:file_name_len]

                    # If file already exists, add _copy<number> to the end
                    if os.path.exists(file_name):
                        # Get file name and extension
                        name, ext = os.path.splitext(file_name)

                        # Iterate until file does not exist
                        i = 1
                        while os.path.exists(name + "_copy" + str(i) + ext):
                            i += 1

                        # Open file with new name
                        f = open(name + "_copy" + str(i) + ext, 'wb')
                    else:
                        # Otherwise open file with given name
                        f = open(file_name, 'wb')

                    # Write to file everything that is connected to a file name
                    f.write(data[offset:])
                else:
                    # If file name is defined, then write to file
                    f.write(data)

                print(data)
            else:
                # if we got no data – client has disconnected

                # Close file
                if f:
                    f.close()

                self._close()
                # finish the thread
                return


def main():
    next_name = 1

    # AF_INET – IPv4, SOCK_STREAM – TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # reuse address; in OS address will be reserved after app closed for a while
    # so if we close and immediately start server again – we'll get error
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # listen to all interfaces at 8800 port
    sock.bind(('0.0.0.0', 8800))
    sock.listen()
    while True:
        # blocking call, waiting for new client to connect
        con, addr = sock.accept()
        clients.append(con)
        name = 'U' + str(next_name)
        next_name += 1
        print(str(addr) + ' connected as ' + name)
        # start new thread to deal with client
        ClientListener(name, con).start()


if __name__ == "__main__":
    main()
