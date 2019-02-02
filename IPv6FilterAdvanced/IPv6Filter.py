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

f_send = open('log_send.txt', 'w')
f_delete = open('log_delete.txt', 'w')
f_make = open('log_make.txt', 'w')
f_other = open('log_other.txt', 'w')

first_byte = 34

while 1:
    packet_str = os.read(socket_fd, 2048)

    packet_bytearray = bytearray(packet_str)

    for i in range(6):
	sym_array[i] = chr(packet_bytearray[first_byte+i])

    leng = first_byte + 20
    if len(packet_bytearray) < first_byte + 20:
                leng = len(packet_bytearray)

    if sym_array[0] == 's' and sym_array[1] == 'e' and sym_array[2] == 'n' and sym_array[3] == 'd':
	f_send.write(str(datetime.today()))
	f_send.write('\n')

	for i in range(first_byte, leng):
    		f_send.write(chr(packet_bytearray[i]))
    		f_send.write(' ')
	f_send.write('\n\n')

    elif sym_array[0] == 'd' and sym_array[1] == 'e' and sym_array[2] == 'l' and sym_array[3] == 'e' and sym_array[4] == 't' and sym_array[5] == 'e':
        f_delete.write(str(datetime.today()))
        f_delete.write('\n')

        for i in range(first_byte, leng):
                f_delete.write(chr(packet_bytearray[i]))
                f_de;ete.write(' ')
        f_delete.write('\n\n')

    elif sym_array[0] == 'm' and sym_array[1] == 'a' and sym_array[2] == 'k' and sym_array[3] == 'e':
        f_make.write(str(datetime.today()))
        f_make.write('\n')

        for i in range(first_byte, leng):
                f_make.write(chr(packet_bytearray[i]))
                f_make.write(' ')
        f_make.write('\n\n')

    else:
        f_other.write(str(datetime.today()))
        f_other.write('\n')

        for i in range(first_byte, leng):
                f_other.write(chr(packet_bytearray[i]))
                f_other.write(' ')
        f_other.write('\n\n')

f_send.close()
f_delete.close()
f_make.close()
f_other.close()


