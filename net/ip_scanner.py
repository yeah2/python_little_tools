# encoding:utf8

import socket
import time
import sys


# scan network segment ports
# Usage: python ip_scanner.py start_ip end_ip port
# Example: python ip_scanner.py 10.8.123.1 10.8.123.1 21

def do_scan(ip, port):
    server = (ip, port)
    # print('scanning %s:%s...' % server)
    sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_fd.settimeout(0.5)  # timeout depends on the speed of network
    ret = sock_fd.connect_ex(server)  # 返回0则成功
    if not ret:
        sock_fd.close()
        print('%s:%s is open...' % (ip, port))
    else:
        sock_fd.close()
    return ''


def ip2num(ip):
    lp = [int(x) for x in ip.split('.')]
    return lp[0] << 24 | lp[1] << 16 | lp[2] << 8 | lp[3]


def num2ip(num):
    ip = ['', '', '', '']
    ip[3] = (num & 0xff)
    ip[2] = (num & 0xff00) >> 8
    ip[1] = (num & 0xff0000) >> 16
    ip[0] = (num & 0xff000000) >> 24
    return '%s.%s.%s.%s' % (ip[0], ip[1], ip[2], ip[3])


def iprange(ip1, ip2):
    num1 = ip2num(ip1)
    num2 = ip2num(ip2)
    diff = num2 - num1
    if diff < 0:
        return None
    else:
        return num1, num2, diff


if __name__ == '__main__':
    print('start time : %s' % time.ctime(time.time()))
    if len(sys.argv) < 4:
        print('Usage: python ip_scanner.py start_ip end_ip port')
        sys.exit()
    res = ()
    start_ip = sys.argv[1]
    end_ip = sys.argv[2]
    port = int(sys.argv[3])

    res = iprange(start_ip, end_ip)
    if not res:
        print('end_ip must be bigger than start one')
        sys.exit()
    elif res[2] == 0:
        do_scan(start_ip, port)
    else:
        start_ip_num = ip2num(start_ip)
        for x in range(int(res[2]) + 1):
            ip_num = start_ip_num + x
            do_scan(num2ip(ip_num), port)
    print('end time : %s' % time.ctime(time.time()))
