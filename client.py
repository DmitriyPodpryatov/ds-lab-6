import os
import sys
import socket


# HOST = '127.0.0.1'
# PORT = 8800
CHUNK_SIZE = 1024  # Bytes


def send_file(file, host, port):
    # Connect to socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Open file
        f = open(file, "rb")

        # Get file size (in bytes)
        size = os.path.getsize(file)
        print("FILE SIZE:", size, "bytes")

        # Send file name
        # The format is <len(file_name)>.<file_name>
        # For example:
        # 5.a.txt
        # The server then can parse the encoded string and obtain the file name
        file_name = os.path.split(file)[1]
        s.send((str(len(file_name)) + "." + file_name).encode())

        # Send chunks of file (CHUNK_SIZE bytes per chunk)
        chunk = f.read(CHUNK_SIZE)
        i = 1
        while chunk:
            s.send(chunk)

            progress = min(CHUNK_SIZE*i / size, 1) * 100
            print("Sending... ", round(progress, 2), "%")
            i += 1

            chunk = f.read(CHUNK_SIZE)

        s.close()
        print("File is sent")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Invalid number of arguments")
        print("Parameters are: <file> <hostname|ip> <port>")
        exit()

    file = sys.argv[1]

    host = sys.argv[2]

    port = int(sys.argv[3])

    send_file(file, host, port)
