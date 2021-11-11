import socket
import struct


def is_in_subnet(ip, subnet):
    """
    Return True if the given ip is in the given subnet range (eg: 192.168.0.0/24)
    """
    ip_addr = struct.unpack('<L', socket.inet_aton(ip))[0]
    subnet_ip, bits = subnet.split('/')
    subnet_addr = struct.unpack('<L', socket.inet_aton(subnet_ip))[0]
    subnet_mask = ((1 << int(bits)) - 1)
    return ip_addr & subnet_mask == subnet_addr & subnet_mask
