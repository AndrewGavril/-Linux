from __future__ import print_function
from bcc import BPF
from sys import argv

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

while 1:
    packet_str = os.read(socket_fd, 2048)

    packet_bytearray = bytearray(packet_str)
    ETH_HLEN = 14

    # IP HEADER
    # https://tools.ietf.org/html/rfc791
    # 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |Version|  IHL  |Type of Service|          Total Length         |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #
    # IHL : Internet Header Length is the length of the internet header
    # value to multiply * 4 byte
    # e.g. IHL = 5 ; IP Header Length = 5 * 4 byte = 20 byte
    #
    # Total length: This 16-bit field defines the entire packet size,
    # including header and data, in bytes.

    total_length = packet_bytearray[ETH_HLEN + 2]
    total_length = total_length << 8
    total_length = total_length + packet_bytearray[ETH_HLEN + 3]
    
    ip_header_length = packet_bytearray[ETH_HLEN]
    ip_header_length = ip_header_length & 0x0F
    ip_header_length = ip_header_length << 2

    tcp_header_length = packet_bytearray[ETH_HLEN + ip_header_length + 12]
    tcp_header_length = tcp_header_length & 0xF0
    tcp_header_length = tcp_header_length >> 2

    payload_offset = ETH_HLEN + ip_header_length

    leng = 20
    if len(packet_bytearray) < 20:
	leng = len(packet_bytearray)
    for i in range(leng):
	f.write(str(packet_bytearray[i]))
	f.write(' ')    
    f.write('\n\n')

f.close()    
