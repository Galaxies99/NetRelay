import os
import sys
import json
import socket
import struct
import configs


header_buf_size = 4
char_buf_size = 1


def exec_client(dst_addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect_ex(dst_addr)
    id = struct.unpack('i', s.recv(header_buf_size))[0]
    print("Successfully connect to the server, your client ID is", id)
    while True:
        # Read commands from input
        cmd = input("NetRelay > ")
        # Send commands to the server
        s.send(struct.pack('i', len(cmd)))
        s.sendall(cmd.encode('utf-8'))
        # Receive result
        size = struct.unpack('i', s.recv(header_buf_size))[0]
        res = ""
        while len(res) < size:
            res = res + s.recv(char_buf_size).decode('utf-8')
        size = struct.unpack('i', s.recv(header_buf_size))[0]
        err = ""
        while len(err) < size:
            err = err + s.recv(char_buf_size).decode('utf-8')
        print(res, end='')
        if size != 0:
            print("[Err] During executing the commands, an error occured:")
            print(err, end='')
    s.close()


def main(argv):
    exec_client(configs.parse_argv_client(argv))


if __name__ == '__main__':
    main(sys.argv[1:])