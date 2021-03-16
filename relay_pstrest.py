import os
import sys
import json
import socket
import struct
import getopt
import pycurl
import threading
import subprocess
from utils import parse_argv_relay
from utils_pstrest import parse_curl

header_buf_size = 4
char_buf_size = 1


first_call = True
call_buf = ""
def callback(data):
    if first_call:
        call_buf = data
        first_call = False


def exec_conn(conn, addr, id):
    conn.send(struct.pack('i', id))
    print('[Log (ID: %d)] Login from' % id, addr)
    while True:
        # Receive command.
        try:
            size = struct.unpack('i', conn.recv(header_buf_size))[0]
        except Exception:
            print('[Log (ID: %d)] Logout' % id)
            break
        cmd = "".encode('utf-8')
        while(len(cmd) < size):
            cmd = cmd + conn.recv(char_buf_size)
        cmd = cmd.decode('utf-8')
        print('[Log (ID: %d)] (1/3) Receive command' % id, cmd)
        # Execute command and get result.
        res = ''
        err = ''
        name, args, cmd_type = parse_curl(cmd)
        if cmd_type == -1 or len(name) != len(args):
            res = 'Not a supported curl command.'
        else:
            c = pycurl.Curl()
            for i in range(len(name)):
                c.setopt(name[i], args[i])
            first_call = True
            c.setopt(pycurl.WRITEFUNCTION, callback)
            c.perform()
            c.close()
            res = call_buf.decode('utf-8')
        
        print('[Log (ID: %d)] (2/3) Finish executing' % id)
        # Send back result.
        conn.send(struct.pack('i', len(res)))
        conn.sendall(res)
        conn.send(struct.pack('i', len(err)))
        conn.sendall(err)
        print('[Log (ID: %d)] (3/3) Finish data sending' % id)


def exec_relay(src_addr):
    if not os.path.exists('netrelay_logs'):
        os.makedirs('netrelay_logs')
    id_cnt = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(src_addr)
    s.listen(5)

    threads = []
    while True:
        conn, addr = s.accept()
        id_cnt = id_cnt + 1
        id = id_cnt
        t = threading.Thread(target=exec_conn, args=(conn, addr, id))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    s.close()


def main(argv):
    exec_relay(parse_argv_relay(argv))


if __name__ == '__main__':
    main(sys.argv[1:])