#!/usr/bin/env python3

'''
# params.txt template:
server: xxx
login: xxx
password: xxx
prg: xxx
mtk: xxx
hh: xxx
timeout: xxx
'''

import sys, yaml, re
from telnetlib import Telnet
from time import time

def print2(s):
    sys.stdout.write('\r%s...      \r' % s)

def tlnt_connect(doc, timeout):
    print2('connecting')
    tn = Telnet(doc['server'])
    print2('sending username')
    s = tn.read_until(b'Username: ', timeout)
    cmd = doc['login'] + '\n\r'
    tn.write(cmd.encode('ascii'))
    print2('sending password')
    s = tn.read_until(b'Password: ', timeout)
    cmd = doc['password'] + '\n\r'
    tn.write(cmd.encode('ascii'))
    t = tn.expect([b'\r\n/', b'\r\nUser authorization failure\r\n'])
    if t[0] in [1, -1]:
        tn.close()
        return
    s = t[2]
    s = s.decode('ascii')
    i1 = s.find('AT')
    i2 = s.find('/')
    dd = s[i1+3:i2]
    hh = s[i2+1:i2+3]
    doc['dd2'] = dd
    doc['hh2'] = hh
    hhh = 24*int(dd) + int(hh)
    hhh -= int(doc['hh'])
    if hhh < 0:
        hhh = 0
    doc['dd1'] = '%d' % (hhh/24)
    doc['hh1'] = '%d' % (hhh%24)
    return tn

def tlnt_cmd(tn, doc, timeout):
    print2('reading data')
    cmd = 'prv/A,%s,ds,%s/%s-%s/%s,%s\n\r' % (doc['prg'], doc['dd1'], doc['hh1'], doc['dd2'], doc['hh2'], doc['mtk'])
    tn.write(cmd.encode('ascii'))
    s = tn.read_until(b'\r\n/', timeout)
    s = s.decode('ascii')
    doc['data'] = s
    return s

def tlnt_logout(tn, doc, timeout):
    print2('logging out')
    cmd = 'logout' + '\n\r'
    s = tn.read_until(b'\r\n/', timeout)
    tn.close()

def save_data(doc):
    with open(doc['result'], 'w') as f:
        f.write(doc['data'])
        f.close()

def print_params(doc):
    print('server\t%s' % doc['server'])
    print('login\t%s' % doc['login'])
    print('result\t%s' % doc['result'])
    print('hours\t%sh' % doc['hh'])
    print('timeout\t%ss' % doc['timeout'])

if __name__ == '__main__':
    fname = 'params.txt'
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    try:
        with open(fname , 'r') as f:
            doc = yaml.load(f)
            f.close()
    except:
        print('ERORR@params')
        sys.exit(5)
    for p in ['server', 'login', 'password', 'prg', 'mtk', 'hh', 'timeout']:
        if p not in doc:
            print('ERORR@%s' % p)
            sys.exit(6)
    doc['result'] = 'Result_%s_%s.txt' % (doc['prg'], doc['mtk'])
    print_params(doc)
    print()
    timeout = int(doc['timeout'])
    t1 = time()
    try:
        tn = tlnt_connect(doc, timeout)
    except:
        print('\n\rERROR@CONNECT')
        sys.exit(1)
    if not tn:
        print('\n\rERROR@LogIn')
        sys.exit(2)
    t1 = time()
    try:
        tlnt_cmd(tn, doc, timeout)
    except:
        t2 = time()
        if (t2 - t1) > timeout:
            print('\n\rERROR@TimeOut')
        else:
            print('\n\rERROR@CONNECT')
        sys.exit(3)
    try:
        tlnt_logout(tn, doc, timeout)
    except:
        print('\n\rERROR@LogOut')
    save_data(doc)
    print('\n\rdone!\r')

