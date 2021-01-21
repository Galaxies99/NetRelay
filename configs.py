import re
import sys
import getopt
from utils import parse_ipv4

def parse_argv_relay(argv):
    src_addr_t = ""
    try:
        opts, _ = getopt.getopt(argv, "hs:", ["help", "src="])
    except getopt.GetoptError:
        print("relay.py -s <sourceAddr> ")
        print("(or)     --src=<sourceAddr>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("relay.py -s <sourceAddr>")
            print("(or)     --src=<sourceAddr>")
            sys.exit()
        elif opt in ("-s", "--src"):
            src_addr_t = arg
    if parse_ipv4(src_addr_t) is False:
        print("[Error] sourceAddr is invalid!")
        sys.exit(2)
    src_ip, src_port = src_addr_t.split(':')
    src_port = int(src_port)
    src_addr = (src_ip, src_port)
    return src_addr


def parse_argv_client(argv):
    dst_addr_t = ""
    try:
        opts, _ = getopt.getopt(argv, "hd:", ["help", "dst="])
    except getopt.GetoptError:
        print("client.py -d <destinationAddr> ")
        print("(or)      --dst=<destinationAddr>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("client.py -d <destinationAddr>")
            print("(or)      --dst=<destinationAddr>")
            sys.exit()
        elif opt in ("-d", "--dst"):
            dst_addr_t = arg
    if parse_ipv4(dst_addr_t) is False:
        print("[Error] destinationAddr is invalid!")
        sys.exit(2)
    dst_ip, dst_port = dst_addr_t.split(':')
    dst_port = int(dst_port)
    dst_addr = (dst_ip, dst_port)
    return dst_addr