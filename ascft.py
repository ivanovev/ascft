#!/usr/bin/env python3

import sys, yaml
from telnetlib import Telnet

def tlnt_connect(doc):
    tn = Telnet(doc['server'])
    s = tn.read_until(b'Username: ', 10)
    print(s.decode('ascii'))
    cmd = doc['name'] + '\n\r'
    tn.write(cmd.encode('ascii'))
    s = tn.read_until(b'Password: ', 10)
    print(s.decode('ascii'))
    cmd = doc['password'] + '\n\r'
    tn.write(cmd.encode('ascii'))
    s = tn.read_until(b'\r\n/', 10)
    s = s.decode('ascii')
    print(s)
    i1 = s.find('AT')
    i2 = s.find('/')
    dd = s[i1+3:i2]
    hh = s[i2+1:i2+3]
    print(dd, hh)
    doc['dd2'] = dd
    doc['hh2'] = hh
    hhh = 24*int(dd) + int(hh)
    hhh -= int(doc['hh'])
    doc['dd1'] = '%d' % (hhh/24)
    doc['hh1'] = '%d' % (hhh%24)
    return tn

def tlnt_cmd(doc):
    cmd = 'prv/A,%s,ds,%s/%s-%s/%s,%s\n\r' % (doc['prg'], doc['dd1'], doc['hh1'], doc['dd2'], doc['hh2'], doc['mtk'])
    print('cmd', cmd)
    tn.write(cmd.encode('ascii'))
    s = tn.read_until(b'\r\n/', 10)
    s = s.decode('ascii')
    print(s)
    doc['data'] = s

def tlnt_logout(doc):
    print('logout')
    cmd = 'logout' + '\n\r'
    s = tn.read_until(b'\r\n/', 10)
    print(s.decode('ascii'))
    tn.close()

def save_data(doc):
    fname = 'Result_%s_%s.txt' % (doc['prg'], doc['mtk'])
    with open(fname, 'w') as f:
        f.write(doc['data'])
        f.close()

if __name__ == '__main__':
    fname = 'params.txt'
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    print(fname )
    with open(fname , 'r') as f:
        doc = yaml.load(f)
        f.close()
    print(doc)
    tn = tlnt_connect(doc)
    tlnt_cmd(doc)
    tlnt_logout(doc)
    save_data(doc)
    print('done')

