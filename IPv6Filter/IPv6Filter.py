from __future__ import print_function
from bcc import BPF
from sys import argv
from datetime import datetime
import sys
import socket
import os


# args
def usage():
    print("USAGE: %s [-i <if_name>]" % argv[0])
    print("")
    print("Try '%s -h' for more options." % argv[0])
    exit()


# help
def help():
    print("USAGE: %s [-i <if_name>]" % argv[0])
    print("")
    print("optional arguments:")
    print("   -h                       print this help")
    print("   -i if_name               select interface if_name. Default is eth0")
    print("")
    print("examples:")
    print("    IPv6-parse              # bind socket to eth0")
    print("    IPv6-parse -i wlan0     # bind socket to wlan0")
    exit()


interface = "eth0"

if len(argv) == 2:
    if str(argv[1]) == '-h':
        help()
    else:
        usage()

if len(argv) == 3:
    if str(argv[1]) == '-i':
        interface = argv[2]
    else:
        usage()

if len(argv) > 3:
    usage()

print("binding socket to '%s'" % interface)

bpf = BPF(src_file="IPv6Filter.c", debug=0)

function_http_filter = bpf.load_func("ip6_filter", BPF.SOCKET_FILTER)

BPF.attach_raw_socket(function_http_filter, interface)

socket_fd = function_http_filter.sock

sock = socket.fromfd(socket_fd, socket.PF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)

sock.setblocking(True)

f = open('log.txt', 'w')
fb = open('log_bin.txt', 'w')

while 1:
    packet_str = os.read(socket_fd, 2048)    
    packet_bytearray = bytearray(packet_str)
    
    fb.write(str(datetime.today()))
    fb.write('\n')

    f.write(str(datetime.today()))
    f.write('\n')
 
    f.write(str(len(packet_bytearray)))
    f.write('\n')

    leng = 54
    if len(packet_bytearray) < 54:
    	leng = len(packet_bytearray)

    for i in range(34, leng):
    	f.write(chr(packet_bytearray[i]))
    	fb.write(str(packet_bytearray[i]))
    	fb.write(' ')
    f.write('\n\n')
    fb.write('\n\n')
f.close()
fb.close()
